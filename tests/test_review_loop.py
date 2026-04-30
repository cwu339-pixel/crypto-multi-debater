import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from crypto_research_agent.review_loop.service import run_pending_reviews, schedule_review
from crypto_research_agent.schemas import ResearchRequest


def make_request() -> ResearchRequest:
    return ResearchRequest(
        asset="BTC",
        thesis="Assess reversal risk",
        horizon_days=3,
        run_id="r_review_test",
        as_of_utc=datetime(2026, 3, 25, 9, 30, tzinfo=timezone.utc),
    )


def test_schedule_review_writes_pending_task(tmp_path: Path) -> None:
    task_path = schedule_review(
        request=make_request(),
        output_root=tmp_path,
    )

    assert task_path.exists()
    payload = json.loads(task_path.read_text(encoding="utf-8"))
    assert payload["run_id"] == "r_review_test"
    assert payload["status"] == "pending"
    assert payload["due_at_utc"] == "2026-03-28T09:30:00+00:00"
    assert payload["run_json_path"].endswith("/runs/r_review_test/run.json")


def test_run_pending_reviews_processes_due_tasks(tmp_path: Path) -> None:
    task_path = schedule_review(
        request=make_request(),
        output_root=tmp_path,
    )
    payload = json.loads(task_path.read_text(encoding="utf-8"))
    payload["due_at_utc"] = "2026-03-25T09:00:00+00:00"
    task_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    run_json_path = tmp_path / "runs" / "r_review_test" / "run.json"
    run_json_path.parent.mkdir(parents=True, exist_ok=True)
    run_json_path.write_text(
        json.dumps(
            {
                "request": {"asset": "BTC", "horizon_days": 3, "thesis": "Assess reversal risk"},
                "request_meta": {"as_of_utc": "2026-03-25T09:30:00+00:00"},
                "feature_summary": {"latest_close": 100.0},
                "final_decision": "avoid",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_pending_reviews(
        output_root=tmp_path,
        now_utc=datetime(2026, 3, 25, 10, 0, tzinfo=timezone.utc),
        fetch_outcome_fn=lambda **kwargs: {
            "status": "completed",
            "observed_close": 95.0,
            "observed_at_utc": "2026-03-25T10:00:00+00:00",
            "future_return_pct": -5.0,
        },
    )

    assert result["status"] == "completed"
    assert result["processed_reviews"] == 1
    review_path = Path(result["review_results"][0]["review_path"])
    assert review_path.exists()
    review_payload = json.loads(review_path.read_text(encoding="utf-8"))
    assert review_payload["run_id"] == "r_review_test"
    assert review_payload["review_status"] == "completed"
    assert review_payload["decision_outcome"]["future_return_pct"] == -5.0
    assert review_payload["decision_outcome"]["decision_correct"] is True
    assert not task_path.exists()


def test_run_pending_reviews_skips_future_tasks(tmp_path: Path) -> None:
    schedule_review(
        request=make_request(),
        output_root=tmp_path,
    )

    result = run_pending_reviews(
        output_root=tmp_path,
        now_utc=datetime(2026, 3, 25, 10, 0, tzinfo=timezone.utc),
    )

    assert result["status"] == "completed"
    assert result["processed_reviews"] == 0


def test_run_pending_reviews_marks_missing_run_json(tmp_path: Path) -> None:
    task_path = schedule_review(
        request=make_request(),
        output_root=tmp_path,
    )
    payload = json.loads(task_path.read_text(encoding="utf-8"))
    payload["due_at_utc"] = "2026-03-25T09:00:00+00:00"
    task_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = run_pending_reviews(
        output_root=tmp_path,
        now_utc=datetime(2026, 3, 25, 10, 0, tzinfo=timezone.utc),
    )

    review_payload = json.loads(Path(result["review_results"][0]["review_path"]).read_text(encoding="utf-8"))
    assert review_payload["review_status"] == "failed"
    assert review_payload["failure_reason"] == "missing_run_json"


def test_run_pending_reviews_handles_positive_hold_outcome(tmp_path: Path) -> None:
    task_path = schedule_review(
        request=make_request(),
        output_root=tmp_path,
    )
    payload = json.loads(task_path.read_text(encoding="utf-8"))
    payload["due_at_utc"] = "2026-03-25T09:00:00+00:00"
    task_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    run_json_path = tmp_path / "runs" / "r_review_test" / "run.json"
    run_json_path.parent.mkdir(parents=True, exist_ok=True)
    run_json_path.write_text(
        json.dumps(
            {
                "request": {"asset": "BTC", "horizon_days": 3, "thesis": "Assess reversal risk"},
                "request_meta": {"as_of_utc": "2026-03-25T09:30:00+00:00"},
                "feature_summary": {"latest_close": 100.0},
                "final_decision": "hold",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_pending_reviews(
        output_root=tmp_path,
        now_utc=datetime(2026, 3, 25, 10, 0, tzinfo=timezone.utc),
        fetch_outcome_fn=lambda **kwargs: {
            "status": "completed",
            "observed_close": 103.0,
            "observed_at_utc": "2026-03-25T10:00:00+00:00",
            "future_return_pct": 3.0,
        },
    )

    review_payload = json.loads(Path(result["review_results"][0]["review_path"]).read_text(encoding="utf-8"))
    assert review_payload["decision_outcome"]["decision_correct"] is True
    assert review_payload["decision_outcome"]["future_return_pct"] == 3.0


def test_run_pending_reviews_resolves_relative_run_json_path_from_old_task(tmp_path: Path) -> None:
    task_path = schedule_review(
        request=make_request(),
        output_root=tmp_path,
    )
    payload = json.loads(task_path.read_text(encoding="utf-8"))
    payload["due_at_utc"] = "2026-03-25T09:00:00+00:00"
    payload["run_json_path"] = "runs/r_review_test/run.json"
    payload.pop("output_root", None)
    task_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    run_json_path = tmp_path / "runs" / "r_review_test" / "run.json"
    run_json_path.parent.mkdir(parents=True, exist_ok=True)
    run_json_path.write_text(
        json.dumps(
            {
                "request": {"asset": "BTC", "horizon_days": 3, "thesis": "Assess reversal risk"},
                "request_meta": {"as_of_utc": "2026-03-25T09:30:00+00:00"},
                "feature_summary": {"latest_close": 100.0},
                "final_decision": "avoid",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_pending_reviews(
        output_root=tmp_path,
        now_utc=datetime(2026, 3, 25, 10, 0, tzinfo=timezone.utc),
        fetch_outcome_fn=lambda **kwargs: {
            "status": "completed",
            "observed_close": 99.0,
            "observed_at_utc": "2026-03-25T10:00:00+00:00",
            "future_return_pct": -1.0,
        },
    )

    review_payload = json.loads(Path(result["review_results"][0]["review_path"]).read_text(encoding="utf-8"))
    assert review_payload["review_status"] == "completed"
    assert review_payload["decision_outcome"]["decision_correct"] is True


def test_run_pending_reviews_backwrites_research_card(tmp_path: Path) -> None:
    task_path = schedule_review(
        request=make_request(),
        output_root=tmp_path,
    )
    payload = json.loads(task_path.read_text(encoding="utf-8"))
    payload["due_at_utc"] = "2026-03-25T09:00:00+00:00"
    task_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    run_root = tmp_path / "runs" / "r_review_test"
    run_root.mkdir(parents=True, exist_ok=True)
    features_path = run_root / "features" / "summary.json"
    features_path.parent.mkdir(parents=True, exist_ok=True)
    features_path.write_text(
        json.dumps(
            {
                "asset": "BTC",
                "latest_close": 100.0,
                "return_1d_pct": 1.2,
                "return_total_pct": 4.0,
                "avg_volume": 123456,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    evidence_path = run_root / "evidence" / "evidence.json"
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text(
        json.dumps({"evidence_status": "fetched", "source": "open_deep_research_local"}, indent=2),
        encoding="utf-8",
    )

    agents_dir = run_root / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    (agents_dir / "call_log.jsonl").write_text(
        '{"role":"final_arbiter","provider":"deterministic","analysis_mode":"deterministic_fallback","duration_ms":0}\n',
        encoding="utf-8",
    )
    final_arbiter_path = agents_dir / "final_arbiter.json"
    final_arbiter_path.write_text(
        json.dumps(
            {
                "summary": "Decision is avoid for the 3-day horizon.",
                "decision_label": "avoid",
                "scorecard": {"final_score": 41, "confidence": "low", "score_decision": "avoid"},
                "rationale": ["cautious", "coverage_gap"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    risk_manager_path = agents_dir / "risk_manager.json"
    risk_manager_path.write_text(
        json.dumps({"summary": "Keep size small.", "risk_bias": "elevated"}, indent=2),
        encoding="utf-8",
    )
    for role_name in (
        "technical_analyst",
        "defi_fundamentals_analyst",
        "derivatives_analyst",
        "news_analyst",
        "bull_researcher",
        "bear_researcher",
    ):
        (agents_dir / f"{role_name}.json").write_text(
            json.dumps({"summary": f"{role_name} summary"}, indent=2),
            encoding="utf-8",
        )

    roles_index = {
        "roles": {
            role_name: {"json_path": str(agents_dir / f"{role_name}.json")}
            for role_name in (
                "technical_analyst",
                "defi_fundamentals_analyst",
                "derivatives_analyst",
                "news_analyst",
                "bull_researcher",
                "bear_researcher",
                "risk_manager",
                "final_arbiter",
            )
        }
    }
    (agents_dir / "index.json").write_text(json.dumps(roles_index, indent=2), encoding="utf-8")

    run_json_path = run_root / "run.json"
    run_json_path.write_text(
        json.dumps(
            {
                "request": {
                    "asset": "BTC",
                    "horizon_days": 3,
                    "thesis": "Assess reversal risk",
                    "as_of_utc": "2026-03-25T09:30:00+00:00",
                },
                "coverage_gaps": ["coinglass:missing_api_key"],
                "stages": {
                    "data_collection": "completed",
                    "feature_engineering": "completed",
                    "evidence_collection": "completed",
                    "multi_role_analysis": "completed",
                    "decisioning": "completed",
                    "review_loop": "scheduled",
                },
                "features_path": str(features_path),
                "evidence_path": str(evidence_path),
                "roles_index_path": str(agents_dir / "index.json"),
                "final_decision": "avoid",
                "scorecard": {"final_score": 41, "confidence": "low", "score_decision": "avoid"},
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = run_pending_reviews(
        output_root=tmp_path,
        now_utc=datetime(2026, 3, 25, 10, 0, tzinfo=timezone.utc),
        fetch_outcome_fn=lambda **kwargs: {
            "status": "completed",
            "observed_close": 95.0,
            "observed_at_utc": "2026-03-25T10:00:00+00:00",
            "future_return_pct": -5.0,
        },
    )

    assert result["processed_reviews"] == 1
    research_card_path = tmp_path / "research_cards" / "2026-03-25" / "BTC_r_review_test.md"
    assert research_card_path.exists()
    card_text = research_card_path.read_text(encoding="utf-8")
    assert "8. Appeal Conditions" in card_text
    assert "Latest review: completed" in card_text
