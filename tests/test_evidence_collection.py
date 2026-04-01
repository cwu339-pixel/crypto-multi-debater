import json
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest

from crypto_research_agent.research.evidence_pack import build_evidence_pack
from crypto_research_agent.research.open_deep_research_client import (
    _default_local_graph_runner,
    fetch_evidence_markdown,
    fetch_evidence_markdown_isolated,
    fetch_evidence_markdown_local,
)
from crypto_research_agent.schemas import EvidencePack, FeatureBundle, RawDataBundle, ResearchRequest, SourceResult


def make_request() -> ResearchRequest:
    return ResearchRequest(
        asset="BTC",
        thesis="Assess reversal risk",
        horizon_days=3,
        run_id="r_evidence_test",
        as_of_utc=datetime(2099, 3, 25, 9, 30, tzinfo=timezone.utc),
    )


def make_raw_data(tmp_path: Path) -> RawDataBundle:
    return RawDataBundle(
        run_id="r_evidence_test",
        source_results={
            "openbb": SourceResult(
                source="openbb",
                status="fetched",
                reason=None,
                artifact_paths=[tmp_path / "runs" / "r_evidence_test" / "raw" / "openbb" / "price_history.json"],
            )
        },
        coverage_gaps=[],
        provenance_path=tmp_path / "runs" / "r_evidence_test" / "provenance.jsonl",
    )


def make_features(tmp_path: Path) -> FeatureBundle:
    return FeatureBundle(
        run_id="r_evidence_test",
        summary={"asset": "BTC", "feature_status": "complete", "latest_close": 100.0},
        coverage_gaps=[],
        features_path=tmp_path / "runs" / "r_evidence_test" / "features" / "summary.json",
        notes_path=tmp_path / "runs" / "r_evidence_test" / "features" / "notes.md",
    )


def test_build_evidence_pack_writes_stub_artifacts(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ODR_BASE_URL", raising=False)
    monkeypatch.delenv("ODR_LOCAL_PROJECT_ROOT", raising=False)
    monkeypatch.setattr(
        "crypto_research_agent.research.evidence_pack._resolve_local_project_root",
        lambda _project_root: tmp_path / "external" / "open_deep_research",
    )
    monkeypatch.setattr(
        "crypto_research_agent.research.evidence_pack.fetch_evidence_markdown_isolated",
        lambda **kwargs: (_ for _ in ()).throw(ModuleNotFoundError("No module named 'langchain'")),
    )
    (tmp_path / "external" / "open_deep_research").mkdir(parents=True, exist_ok=True)
    request = make_request()
    evidence = build_evidence_pack(
        request=request,
        raw_data=make_raw_data(tmp_path),
        features=make_features(tmp_path),
        output_root=tmp_path,
    )

    assert evidence.summary["evidence_status"] == "stub"
    assert evidence.summary["fallback_reason"] == "evidence_collection_error"
    assert evidence.summary["fallback_error_type"] == "ModuleNotFoundError"
    assert "langchain" in evidence.summary["fallback_detail"]
    assert evidence.markdown_path.exists()
    assert evidence.json_path.exists()
    assert "Evidence Stub" in evidence.markdown_path.read_text(encoding="utf-8")


def test_fetch_evidence_markdown_parses_http_response() -> None:
    def fake_http_post(url, payload, headers):
        assert url == "http://127.0.0.1:2024/research"
        assert payload["asset"] == "BTC"
        return {"markdown": "# Claims\n- Example"}

    markdown = fetch_evidence_markdown(
        base_url="http://127.0.0.1:2024",
        request=make_request(),
        http_post=fake_http_post,
    )

    assert markdown == "# Claims\n- Example"


def test_fetch_evidence_markdown_local_uses_graph_runner(tmp_path: Path) -> None:
    def fake_graph_runner(request: ResearchRequest, project_root: Path) -> str:
        assert request.asset == "BTC"
        assert project_root == tmp_path
        return "# Research\n\nBottom line."

    markdown = fetch_evidence_markdown_local(
        request=make_request(),
        project_root=tmp_path,
        graph_runner=fake_graph_runner,
    )

    assert markdown == "# Research\n\nBottom line."


def test_default_local_graph_runner_uses_subprocess_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (tmp_path / "src").mkdir(parents=True, exist_ok=True)

    class Completed:
        returncode = 0
        stdout = json.dumps({"final_report": "# Research\n\nBottom Line\n- ok"})
        stderr = ""

    def fake_run(cmd, input, text, capture_output, timeout, env):
        assert cmd[0]
        payload = json.loads(input)
        assert payload["source_root"] == str(tmp_path / "src")
        assert payload["timeout_seconds"] >= 1
        return Completed()

    monkeypatch.setattr("crypto_research_agent.research.open_deep_research_client.subprocess.run", fake_run)
    monkeypatch.setenv("ODR_TIMEOUT_SECONDS", "5")

    markdown = _default_local_graph_runner(make_request(), tmp_path)

    assert markdown.startswith("# Research")


def test_fetch_evidence_markdown_isolated_uses_subprocess_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Completed:
        returncode = 0
        stdout = json.dumps({"markdown": "# Research\n\nBottom Line\n- ok", "source": "open_deep_research_local"})
        stderr = ""

    def fake_run(cmd, input, text, capture_output, timeout, env):
        payload = json.loads(input)
        assert payload["request"]["asset"] == "BTC"
        return Completed()

    monkeypatch.setattr("crypto_research_agent.research.open_deep_research_client.subprocess.run", fake_run)

    markdown, source = fetch_evidence_markdown_isolated(request=make_request(), project_root="/tmp/fake", timeout_seconds=5)

    assert markdown.startswith("# Research")
    assert source == "open_deep_research_local"


def test_default_local_graph_runner_retries_once_on_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (tmp_path / "src").mkdir(parents=True, exist_ok=True)

    class Failed:
        returncode = 1
        stdout = ""
        stderr = "boom"

    class Succeeded:
        returncode = 0
        stdout = json.dumps({"final_report": "# Research\n\nBottom Line\n- recovered"})
        stderr = ""

    calls = {"count": 0}

    def fake_run(cmd, input, text, capture_output, timeout, env):
        calls["count"] += 1
        if calls["count"] == 1:
            return Failed()
        return Succeeded()

    monkeypatch.setattr("crypto_research_agent.research.open_deep_research_client.subprocess.run", fake_run)
    monkeypatch.setenv("ODR_TIMEOUT_SECONDS", "5")
    monkeypatch.setenv("ODR_MAX_RETRIES", "1")

    markdown = _default_local_graph_runner(make_request(), tmp_path)

    assert calls["count"] == 2
    assert "recovered" in markdown


def test_build_evidence_pack_uses_local_open_deep_research_when_available(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("ODR_BASE_URL", raising=False)
    monkeypatch.delenv("ODR_LOCAL_PROJECT_ROOT", raising=False)
    monkeypatch.setattr(
        "crypto_research_agent.research.evidence_pack._resolve_local_project_root",
        lambda _project_root: tmp_path / "external" / "open_deep_research",
    )
    (tmp_path / "external" / "open_deep_research").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(
        "crypto_research_agent.research.evidence_pack.fetch_evidence_markdown_isolated",
        lambda **kwargs: (
            "# Research\n\n[Source](https://example.com)\n\n## Bottom Line\n- Bullish catalyst",
            "open_deep_research_local",
        ),
    )

    evidence = build_evidence_pack(
        request=make_request(),
        raw_data=make_raw_data(tmp_path),
        features=make_features(tmp_path),
        output_root=tmp_path,
    )

    assert evidence.summary["evidence_status"] == "fetched"
    assert evidence.summary["source"] == "open_deep_research_local"
    assert evidence.summary["citations_count"] == 1
    assert "Bottom Line" in evidence.markdown_path.read_text(encoding="utf-8")


def test_build_evidence_pack_stays_stub_without_explicit_odr_opt_in(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("ODR_BASE_URL", raising=False)
    monkeypatch.delenv("ODR_LOCAL_PROJECT_ROOT", raising=False)
    monkeypatch.setattr(
        "crypto_research_agent.research.evidence_pack._resolve_local_project_root",
        lambda _project_root: tmp_path / "missing" / "open_deep_research",
    )

    called = {"local": 0}

    def fake_local_fetch(**kwargs):
        called["local"] += 1
        return "# Research\n\nShould not be used.", "open_deep_research_local"

    monkeypatch.setattr(
        "crypto_research_agent.research.evidence_pack.fetch_evidence_markdown_isolated",
        fake_local_fetch,
    )

    evidence = build_evidence_pack(
        request=make_request(),
        raw_data=make_raw_data(tmp_path),
        features=make_features(tmp_path),
        output_root=tmp_path,
    )

    assert called["local"] == 0
    assert evidence.summary["evidence_status"] == "stub"
    assert evidence.summary["source"] == "local_stub"
    assert evidence.summary["fallback_reason"] == "evidence_collection_error"
    assert evidence.summary["fallback_error_type"] == "FileNotFoundError"
    assert "open_deep_research checkout not found" in evidence.summary["fallback_detail"]


def test_build_evidence_pack_marks_historical_replay_limitations(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("ODR_BASE_URL", raising=False)
    monkeypatch.delenv("ODR_LOCAL_PROJECT_ROOT", raising=False)

    request = ResearchRequest(
        asset="BTC",
        thesis="Historical replay",
        horizon_days=3,
        run_id="r_evidence_historical_test",
        as_of_utc=datetime(2020, 1, 1, 0, 0, tzinfo=timezone.utc),
    )

    evidence = build_evidence_pack(
        request=request,
        raw_data=make_raw_data(tmp_path),
        features=make_features(tmp_path),
        output_root=tmp_path,
    )

    assert evidence.summary["run_mode"] == "historical_replay"
    assert evidence.summary["historical_replay"] is True
    assert (
        evidence.summary["point_in_time_note"]
        == "Price features are sliced to the requested date. Evidence and non-price inputs are not guaranteed historical snapshots."
    )
    assert "evidence_not_historically_replayed" in evidence.summary["point_in_time_limitations"]
    assert evidence.summary["fallback_reason"] == "historical_replay_unavailable"
    assert evidence.summary["fallback_error_type"] == "HistoricalReplayUnavailableError"


def test_build_evidence_pack_times_out_hung_local_odr(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("EVIDENCE_TIMEOUT_SECONDS", "1")
    monkeypatch.delenv("ODR_BASE_URL", raising=False)
    monkeypatch.delenv("ODR_LOCAL_PROJECT_ROOT", raising=False)
    monkeypatch.setattr(
        "crypto_research_agent.research.evidence_pack._resolve_local_project_root",
        lambda _project_root: tmp_path / "external" / "open_deep_research",
    )
    (tmp_path / "external" / "open_deep_research").mkdir(parents=True, exist_ok=True)

    def slow_local_fetch(**kwargs):
        time.sleep(2)
        return "# Research\n\nToo slow.", "open_deep_research_local"

    monkeypatch.setattr(
        "crypto_research_agent.research.evidence_pack.fetch_evidence_markdown_isolated",
        slow_local_fetch,
    )

    evidence = build_evidence_pack(
        request=make_request(),
        raw_data=make_raw_data(tmp_path),
        features=make_features(tmp_path),
        output_root=tmp_path,
    )

    assert evidence.summary["evidence_status"] == "stub"
    assert evidence.summary["fallback_error_type"] == "TimeoutError"
    assert evidence.summary["fallback_reason"] == "evidence_collection_error"
