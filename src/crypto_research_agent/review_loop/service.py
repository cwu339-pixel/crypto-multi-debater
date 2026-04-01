from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

from crypto_research_agent.data_layer.openbb_layer import fetch_openbb_data
from crypto_research_agent.schemas import ResearchRequest
from crypto_research_agent.storage.artifacts import refresh_research_card_from_run


def schedule_review(
    *,
    request: ResearchRequest,
    output_root: Path,
) -> Path:
    pending_dir = Path(output_root) / "reviews" / "pending"
    pending_dir.mkdir(parents=True, exist_ok=True)
    task_path = pending_dir / f"{request.run_id}.json"
    due_at_utc = request.as_of_utc + timedelta(days=request.horizon_days)
    task_path.write_text(
        json.dumps(
            {
                "run_id": request.run_id,
                "asset": request.asset,
                "thesis": request.thesis,
                "horizon_days": request.horizon_days,
                "scheduled_at_utc": request.as_of_utc.isoformat(),
                "due_at_utc": due_at_utc.isoformat(),
                "output_root": str(Path(output_root)),
                "run_json_path": str(Path(output_root) / "runs" / request.run_id / "run.json"),
                "status": "pending",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return task_path


def run_pending_reviews(
    *,
    output_root: Path,
    now_utc: datetime | None = None,
    fetch_outcome_fn: Callable[..., dict[str, Any]] | None = None,
) -> dict[str, object]:
    current_time = now_utc or datetime.now(timezone.utc)
    pending_dir = Path(output_root) / "reviews" / "pending"
    completed_dir = Path(output_root) / "reviews" / "completed"
    completed_dir.mkdir(parents=True, exist_ok=True)

    review_results: list[dict[str, object]] = []
    outcome_fetcher = fetch_outcome_fn or _fetch_review_outcome
    if pending_dir.exists():
        for task_path in sorted(pending_dir.glob("*.json")):
            task_payload = json.loads(task_path.read_text(encoding="utf-8"))
            due_at_utc = datetime.fromisoformat(task_payload["due_at_utc"])
            if due_at_utc > current_time:
                continue
            review_path = completed_dir / f"{task_payload['run_id']}.json"
            review_payload = _build_review_payload(
                task_payload=task_payload,
                current_time=current_time,
                outcome_fetcher=outcome_fetcher,
                output_root=Path(output_root),
            )
            review_path.write_text(json.dumps(review_payload, indent=2), encoding="utf-8")
            task_path.unlink()
            resolved_run_json_path = _resolve_run_json_path(task_payload, output_root=output_root)
            if resolved_run_json_path.exists():
                refresh_research_card_from_run(
                    run_json_path=resolved_run_json_path,
                    output_root=Path(output_root),
                )
            review_results.append(
                {
                    "run_id": task_payload["run_id"],
                    "review_path": str(review_path),
                }
            )

    return {
        "command": "run_pending_reviews",
        "status": "completed",
        "processed_reviews": len(review_results),
        "review_results": review_results,
    }


def _build_review_payload(
    *,
    task_payload: dict[str, Any],
    current_time: datetime,
    outcome_fetcher: Callable[..., dict[str, Any]],
    output_root: Path,
) -> dict[str, Any]:
    run_json_path = _resolve_run_json_path(task_payload, output_root=output_root)
    base_payload = {
        "run_id": task_payload["run_id"],
        "asset": task_payload["asset"],
        "due_at_utc": task_payload["due_at_utc"],
        "reviewed_at_utc": current_time.isoformat(),
        "run_json_path": str(run_json_path),
    }

    if not run_json_path.exists():
        return {
            **base_payload,
            "review_status": "failed",
            "failure_reason": "missing_run_json",
            "summary": "Run artifact is missing, so post-horizon outcome comparison could not be completed.",
        }

    run_payload = json.loads(run_json_path.read_text(encoding="utf-8"))
    outcome = outcome_fetcher(
        task_payload=task_payload,
        run_payload=run_payload,
        current_time=current_time,
    )

    if outcome.get("status") != "completed":
        failure_reason = str(outcome.get("failure_reason", "outcome_unavailable"))
        return {
            **base_payload,
            "review_status": "failed",
            "failure_reason": failure_reason,
            "initial_decision": run_payload.get("final_decision"),
            "summary": f"Outcome comparison failed: {failure_reason}.",
        }

    initial_decision = str(run_payload.get("final_decision", "unknown"))
    future_return_pct = float(outcome["future_return_pct"])
    decision_correct = _is_decision_correct(initial_decision, future_return_pct)
    feature_summary = _load_feature_summary(run_payload)

    return {
        **base_payload,
        "review_status": "completed",
        "initial_decision": initial_decision,
        "decision_outcome": {
            "initial_close": feature_summary.get("latest_close"),
            "observed_close": outcome["observed_close"],
            "observed_at_utc": outcome["observed_at_utc"],
            "future_return_pct": future_return_pct,
            "decision_correct": decision_correct,
        },
        "summary": _review_summary(
            decision=initial_decision,
            future_return_pct=future_return_pct,
            decision_correct=decision_correct,
        ),
    }


def _fetch_review_outcome(
    *,
    task_payload: dict[str, Any],
    run_payload: dict[str, Any],
    current_time: datetime,
) -> dict[str, Any]:
    feature_summary = _load_feature_summary(run_payload)
    latest_close = feature_summary.get("latest_close")
    if latest_close in (None, 0):
        return {"status": "failed", "failure_reason": "missing_initial_close"}

    as_of_raw = (
        run_payload.get("request", {}).get("as_of_utc")
        or run_payload.get("request_meta", {}).get("as_of_utc")
        or task_payload.get("scheduled_at_utc")
    )
    if not as_of_raw:
        return {"status": "failed", "failure_reason": "missing_as_of_utc"}

    request = ResearchRequest(
        asset=str(task_payload["asset"]),
        thesis=str(task_payload.get("thesis", run_payload.get("request", {}).get("thesis", ""))),
        horizon_days=int(task_payload["horizon_days"]),
        run_id=str(task_payload["run_id"]),
        as_of_utc=datetime.fromisoformat(as_of_raw),
    )
    outcome = fetch_openbb_data(
        request,
        {"enabled": True, "lookback_days": 400, "quote_currency": "USD"},
    )
    if outcome.status != "fetched":
        return {"status": "failed", "failure_reason": outcome.reason or "openbb_fetch_failed"}

    price_rows = outcome.payloads.get("price_history", [])
    observed = _select_review_price(
        price_rows=price_rows,
        due_at_utc=datetime.fromisoformat(task_payload["due_at_utc"]),
        current_time=current_time,
    )
    if observed is None:
        return {"status": "failed", "failure_reason": "missing_observed_price"}

    observed_close = float(observed["close"])
    initial_close = float(latest_close)
    future_return_pct = ((observed_close - initial_close) / initial_close) * 100
    return {
        "status": "completed",
        "observed_close": observed_close,
        "observed_at_utc": observed["timestamp"],
        "future_return_pct": round(future_return_pct, 6),
    }


def _load_feature_summary(run_payload: dict[str, Any]) -> dict[str, Any]:
    inline_summary = run_payload.get("feature_summary")
    if isinstance(inline_summary, dict):
        return inline_summary

    features_path = run_payload.get("features_path")
    if features_path:
        path = Path(str(features_path))
        if path.exists():
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                return loaded

    return {}


def _resolve_run_json_path(task_payload: dict[str, Any], *, output_root: Path) -> Path:
    run_json_path = task_payload.get("run_json_path")
    if run_json_path:
        path = Path(str(run_json_path))
        if path.is_absolute():
            return path
        return output_root / path
    task_output_root = task_payload.get("output_root")
    if task_output_root:
        return Path(str(task_output_root)) / "runs" / str(task_payload["run_id"]) / "run.json"
    return output_root / "runs" / str(task_payload["run_id"]) / "run.json"


def _select_review_price(
    *,
    price_rows: list[dict[str, Any]],
    due_at_utc: datetime,
    current_time: datetime,
) -> dict[str, Any] | None:
    due_date = due_at_utc.date().isoformat()
    selected: dict[str, Any] | None = None
    for row in price_rows:
        timestamp = _extract_price_timestamp(row)
        close = row.get("close")
        if timestamp is None or close is None:
            continue
        if timestamp > current_time.isoformat():
            continue
        if timestamp[:10] >= due_date:
            selected = {"timestamp": timestamp, "close": close}
            break
        selected = {"timestamp": timestamp, "close": close}
    return selected


def _extract_price_timestamp(row: dict[str, Any]) -> str | None:
    for key in ("date", "datetime", "timestamp"):
        value = row.get(key)
        if value:
            return str(value)
    return None


def _is_decision_correct(decision: str, future_return_pct: float) -> bool | None:
    if decision == "hold":
        return future_return_pct > 0
    if decision == "avoid":
        return future_return_pct <= 0
    return None


def _review_summary(*, decision: str, future_return_pct: float, decision_correct: bool | None) -> str:
    correctness = "correct" if decision_correct else "incorrect"
    if decision_correct is None:
        correctness = "not scoreable"
    return (
        f"Initial decision was {decision}. "
        f"Observed forward return was {future_return_pct:.2f}% over the review horizon, "
        f"so the call was {correctness}."
    )
