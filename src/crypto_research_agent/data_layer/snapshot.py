from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_snapshot(
    payload: Any,
    *,
    run_root: Path,
    source: str,
    artifact_name: str,
) -> Path:
    source_dir = run_root / "raw" / source
    source_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = source_dir / f"{artifact_name}.json"
    artifact_path.write_text(
        json.dumps(payload, indent=2, default=str),
        encoding="utf-8",
    )
    return artifact_path
