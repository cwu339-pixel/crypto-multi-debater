import json
from datetime import datetime, timezone

from crypto_research_agent.cli import build_parser, main
from crypto_research_agent.schemas import RawDataBundle, ResearchRequest, SourceResult


def test_run_command_parses_required_arguments() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "run",
            "--asset",
            "BTC",
            "--horizon-days",
            "3",
            "--thesis",
            "Assess reversal risk",
        ]
    )

    assert args.command == "run"
    assert args.asset == "BTC"
    assert args.horizon_days == 3
    assert args.thesis == "Assess reversal risk"


def test_run_pending_reviews_command_is_available() -> None:
    parser = build_parser()

    args = parser.parse_args(["run-pending-reviews"])

    assert args.command == "run_pending_reviews"


def test_preflight_command_is_available() -> None:
    parser = build_parser()

    args = parser.parse_args(["preflight"])

    assert args.command == "preflight"


def test_run_command_accepts_as_of_date() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "run",
            "--asset",
            "BTC",
            "--horizon-days",
            "3",
            "--thesis",
            "Assess reversal risk",
            "--as-of-date",
            "2025-10-05",
        ]
    )

    assert args.as_of_date == "2025-10-05"


def test_run_pending_reviews_command_executes_review_runner(
    monkeypatch, tmp_path, capsys
) -> None:
    def fake_run_pending_reviews(*, output_root):
        assert output_root == tmp_path
        return {
            "command": "run_pending_reviews",
            "status": "completed",
            "processed_reviews": 1,
            "review_results": [
                {
                    "run_id": "r_test",
                    "review_path": str(tmp_path / "reviews" / "completed" / "r_test.json"),
                }
            ],
        }

    monkeypatch.setattr("crypto_research_agent.cli.run_pending_reviews", fake_run_pending_reviews)

    exit_code = main(
        [
            "run-pending-reviews",
            "--output-dir",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "completed"
    assert payload["processed_reviews"] == 1


def test_run_command_prints_data_layer_summary(
    monkeypatch, tmp_path, capsys
) -> None:
    def fake_load_yaml_config(_path):
        return {"sources": {"openbb": {"enabled": True}}}

    def fake_run_workflow(request, sources_config, output_root):
        assert isinstance(request, ResearchRequest)
        assert request.asset == "BTC"
        assert request.as_of_utc == datetime(2025, 10, 5, tzinfo=timezone.utc)
        assert output_root == tmp_path
        assert sources_config["sources"]["openbb"]["enabled"] is True
        return {
            "status": "framework_ready",
            "run_id": request.run_id,
            "sources": {
                "openbb": SourceResult(
                    source="openbb",
                    status="fetched",
                    reason=None,
                    artifact_paths=[],
                ).to_dict(),
                "coinglass": SourceResult(
                    source="coinglass",
                    status="skipped",
                    reason="missing_api_key",
                    artifact_paths=[],
                ).to_dict(),
            },
            "coverage_gaps": ["coinglass:missing_api_key"],
            "artifacts": {
                "run_json": str(tmp_path / "runs" / request.run_id / "run.json"),
                "research_card": str(tmp_path / "research_cards" / "2026-03-25" / f"BTC_{request.run_id}.md"),
            },
        }

    monkeypatch.setattr("crypto_research_agent.cli.load_yaml_config", fake_load_yaml_config)
    monkeypatch.setattr("crypto_research_agent.cli.run_workflow", fake_run_workflow)

    exit_code = main(
        [
            "run",
            "--asset",
            "BTC",
            "--horizon-days",
            "3",
            "--thesis",
            "Assess reversal risk",
            "--as-of-date",
            "2025-10-05",
            "--sources-config",
            str(tmp_path / "sources.yaml"),
            "--output-dir",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "framework_ready"
    assert payload["coverage_gaps"] == ["coinglass:missing_api_key"]
    assert payload["sources"]["openbb"]["status"] == "fetched"
    assert payload["artifacts"]["run_json"].endswith("run.json")


def test_preflight_command_prints_environment_summary(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        "crypto_research_agent.cli.run_preflight",
        lambda: {
            "status": "degraded",
            "critical_failures": ["provider"],
            "checks": {"provider": {"status": "degraded", "selected": "deterministic"}},
        },
    )

    exit_code = main(["preflight"])

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "degraded"
    assert payload["critical_failures"] == ["provider"]
