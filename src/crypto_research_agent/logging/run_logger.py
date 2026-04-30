from __future__ import annotations

from pathlib import Path

from crypto_research_agent.orchestration.state import RunArtifacts, RunState
from crypto_research_agent.storage.artifacts import write_partial_run_artifacts, write_run_artifacts


def persist_run_state(state: RunState, *, output_root: Path) -> RunArtifacts:
    return write_run_artifacts(state, output_root=output_root)


def persist_partial_run_state(
    *,
    request,
    output_root: Path,
    stages: dict[str, str],
    raw_data=None,
    features=None,
    evidence=None,
    role_analysis=None,
    status: str = "running",
    failed_stage: str | None = None,
    error_type: str | None = None,
    error_detail: str | None = None,
) -> RunArtifacts:
    return write_partial_run_artifacts(
        request=request,
        output_root=output_root,
        stages=stages,
        raw_data=raw_data,
        features=features,
        evidence=evidence,
        role_analysis=role_analysis,
        status=status,
        failed_stage=failed_stage,
        error_type=error_type,
        error_detail=error_detail,
    )
