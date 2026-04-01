from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from crypto_research_agent.data_layer.openbb_layer import AdapterOutcome
from crypto_research_agent.schemas import SourceResult


def append_provenance_record(
    *,
    provenance_path: Path,
    source: str,
    outcome: AdapterOutcome,
    result: SourceResult,
) -> None:
    provenance_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "status": result.status,
        "reason": result.reason,
        "request": outcome.request_metadata,
        "config": outcome.config_metadata,
        "artifact_paths": [str(path) for path in result.artifact_paths],
    }
    with provenance_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")
