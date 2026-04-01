from __future__ import annotations

from pathlib import Path

from crypto_research_agent.orchestration.state import RunArtifacts, RunState
from crypto_research_agent.storage.artifacts import write_run_artifacts


def persist_run_state(state: RunState, *, output_root: Path) -> RunArtifacts:
    return write_run_artifacts(state, output_root=output_root)
