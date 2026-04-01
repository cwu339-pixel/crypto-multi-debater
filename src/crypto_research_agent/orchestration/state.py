from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from crypto_research_agent.schemas import (
    EvidencePack,
    FeatureBundle,
    RawDataBundle,
    ResearchRequest,
    RoleAnalysisBundle,
)


@dataclass(frozen=True)
class RunArtifacts:
    run_json: Path
    artifact_index: Path
    research_card: Path


@dataclass(frozen=True)
class RunState:
    request: ResearchRequest
    raw_data: RawDataBundle
    features: FeatureBundle
    evidence: EvidencePack
    role_analysis: RoleAnalysisBundle
    artifacts: RunArtifacts
    stages: dict[str, str]
