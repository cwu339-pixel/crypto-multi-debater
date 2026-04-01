from __future__ import annotations

import json
import os
import re
import signal
import threading
from datetime import datetime, timezone
from contextlib import contextmanager
from pathlib import Path

from crypto_research_agent.research.open_deep_research_client import (
    _resolve_local_project_root,
    fetch_evidence_markdown_isolated,
)
from crypto_research_agent.schemas import EvidencePack, FeatureBundle, RawDataBundle, ResearchRequest


def build_evidence_pack(
    *,
    request: ResearchRequest,
    raw_data: RawDataBundle,
    features: FeatureBundle,
    output_root: Path,
) -> EvidencePack:
    evidence_dir = Path(output_root) / "runs" / request.run_id / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    markdown_path = evidence_dir / "evidence.md"
    json_path = evidence_dir / "evidence.json"

    odr_base_url = os.getenv("ODR_BASE_URL")
    odr_local_project_root = os.getenv("ODR_LOCAL_PROJECT_ROOT")
    replay_metadata = _build_replay_metadata(request=request)
    evidence_timeout_seconds = _env_int("EVIDENCE_TIMEOUT_SECONDS", _env_int("ODR_TIMEOUT_SECONDS", 45) + 5)
    try:
        with _timeout_guard(evidence_timeout_seconds):
            if replay_metadata.get("historical_replay") is True:
                raise HistoricalReplayUnavailableError("historical_replay_unavailable")
            local_project_root = (
                None
                if odr_base_url
                else (Path(odr_local_project_root) if odr_local_project_root else _resolve_local_project_root(None))
            )
            if local_project_root is not None and not local_project_root.exists():
                raise FileNotFoundError(f"open_deep_research checkout not found: {local_project_root}")
            markdown, evidence_source = fetch_evidence_markdown_isolated(
                request=request,
                base_url=odr_base_url,
                project_root=local_project_root,
                timeout_seconds=evidence_timeout_seconds,
            )
            summary = _build_evidence_summary(
                markdown,
                source=evidence_source,
                status="fetched",
                replay_metadata=replay_metadata,
            )
    except Exception as exc:
        fallback_reason = (
            "historical_replay_unavailable"
            if isinstance(exc, HistoricalReplayUnavailableError)
            else "evidence_collection_error"
        )
        markdown = _render_stub_markdown(
            request,
            raw_data,
            features,
            fallback_reason=fallback_reason,
            fallback_detail=_format_fallback_detail(exc),
        )
        summary = {
            "evidence_status": "stub",
            "source": "local_stub",
            "fallback_reason": fallback_reason,
            "fallback_error_type": type(exc).__name__,
            "fallback_detail": _format_fallback_detail(exc),
            "coverage_gaps": raw_data.coverage_gaps,
            "citations_count": 0,
        }
        summary.update(replay_metadata)

    markdown_path.write_text(markdown, encoding="utf-8")
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    return EvidencePack(
        run_id=request.run_id,
        summary=summary,
        markdown_path=markdown_path,
        json_path=json_path,
    )


def _render_stub_markdown(
    request: ResearchRequest,
    raw_data: RawDataBundle,
    features: FeatureBundle,
    fallback_reason: str | None = None,
    fallback_detail: str | None = None,
) -> str:
    fallback_line = f"- Fallback reason: {fallback_reason}\n" if fallback_reason else ""
    fallback_detail_line = f"- Fallback detail: {fallback_detail}\n" if fallback_detail else ""
    return (
        "# Evidence Stub\n\n"
        "## Request\n"
        f"- Asset: {request.asset}\n"
        f"- Thesis: {request.thesis}\n\n"
        "## Available Inputs\n"
        f"- Feature status: {features.summary.get('feature_status')}\n"
        f"- Coverage gaps: {', '.join(raw_data.coverage_gaps) if raw_data.coverage_gaps else 'none'}\n\n"
        "## Status\n"
        f"{fallback_line}{fallback_detail_line}\n"
        "## Claims\n"
        "- Evidence collection fell back to the local stub for this run.\n"
    )


def _build_evidence_summary(
    markdown: str,
    *,
    source: str,
    status: str,
    replay_metadata: dict[str, object],
) -> dict[str, object]:
    summary = {
        "evidence_status": status,
        "source": source,
        "citations_count": len(re.findall(r"\[[^\]]+\]\([^)]+\)", markdown)),
    }
    summary.update(replay_metadata)
    return summary


def _build_replay_metadata(*, request: ResearchRequest) -> dict[str, object]:
    today_utc = datetime.now(timezone.utc).date()
    if request.as_of_utc.date() >= today_utc:
        return {
            "run_mode": "live_or_current",
            "historical_replay": False,
            "point_in_time_limitations": [],
        }
    return {
        "run_mode": "historical_replay",
        "historical_replay": True,
        "point_in_time_note": (
            "Price features are sliced to the requested date. Evidence and non-price inputs are not guaranteed historical snapshots."
        ),
        "point_in_time_limitations": [
            "evidence_not_historically_replayed",
            "non_price_inputs_not_point_in_time_verified",
        ],
    }


class HistoricalReplayUnavailableError(RuntimeError):
    pass


def _format_fallback_detail(exc: Exception) -> str:
    message = str(exc).strip()
    if not message:
        return type(exc).__name__
    return f"{type(exc).__name__}: {message}"


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


@contextmanager
def _timeout_guard(seconds: int):
    if seconds <= 0 or threading.current_thread() is not threading.main_thread() or not hasattr(signal, "SIGALRM"):
        yield
        return

    def _handle_timeout(signum, frame):  # noqa: ARG001
        raise TimeoutError(f"evidence timed out after {seconds}s")

    previous_handler = signal.getsignal(signal.SIGALRM)
    signal.signal(signal.SIGALRM, _handle_timeout)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)
