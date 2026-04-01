from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class ResearchRequest:
    asset: str
    thesis: str
    horizon_days: int
    run_id: str
    as_of_utc: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class SourceResult:
    source: str
    status: str
    reason: str | None
    artifact_paths: list[Path]

    def to_dict(self) -> dict[str, object]:
        return {
            "source": self.source,
            "status": self.status,
            "reason": self.reason,
            "artifact_paths": [str(path) for path in self.artifact_paths],
        }


@dataclass(frozen=True)
class RawDataBundle:
    run_id: str
    source_results: dict[str, SourceResult]
    coverage_gaps: list[str]
    provenance_path: Path

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "sources": {
                source: result.to_dict()
                for source, result in self.source_results.items()
            },
            "coverage_gaps": self.coverage_gaps,
            "provenance_path": str(self.provenance_path),
        }


@dataclass(frozen=True)
class FeatureBundle:
    run_id: str
    summary: dict[str, object]
    coverage_gaps: list[str]
    features_path: Path
    notes_path: Path

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "summary": self.summary,
            "coverage_gaps": self.coverage_gaps,
            "features_path": str(self.features_path),
            "notes_path": str(self.notes_path),
        }


@dataclass(frozen=True)
class EvidencePack:
    run_id: str
    summary: dict[str, object]
    markdown_path: Path
    json_path: Path

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "summary": self.summary,
            "markdown_path": str(self.markdown_path),
            "json_path": str(self.json_path),
        }


@dataclass(frozen=True)
class RoleAnalysisBundle:
    run_id: str
    role_memos: dict[str, dict[str, object]]
    markdown_paths: dict[str, Path]
    json_paths: dict[str, Path]
    index_path: Path

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "role_memos": self.role_memos,
            "markdown_paths": {
                role: str(path) for role, path in self.markdown_paths.items()
            },
            "json_paths": {
                role: str(path) for role, path in self.json_paths.items()
            },
            "index_path": str(self.index_path),
        }
