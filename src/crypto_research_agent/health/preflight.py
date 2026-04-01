from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from typing import Any

from crypto_research_agent.agents.provider import DeterministicAnalysisProvider, default_analysis_provider
from crypto_research_agent.research.open_deep_research_client import _resolve_local_project_root


def run_preflight() -> dict[str, Any]:
    provider = default_analysis_provider()
    odr_root = _resolve_local_project_root(None)
    odr_source_root = odr_root / "src"

    checks = {
        "provider": {
            "status": "ok" if not isinstance(provider, DeterministicAnalysisProvider) else "degraded",
            "selected": provider.name,
            "timeout_seconds": getattr(provider, "timeout_seconds", None),
            "max_retries": getattr(provider, "max_retries", None),
            "openai_key_present": bool(os.getenv("OPENAI_API_KEY")),
            "openrouter_key_present": bool(os.getenv("OPENROUTER_API_KEY")),
        },
        "openbb": {
            "status": "ok" if _module_exists("openbb") else "degraded",
            "importable": _module_exists("openbb"),
        },
        "open_deep_research": {
            "status": "ok",
            "project_root": str(odr_root),
            "project_root_exists": odr_root.exists(),
            "langchain_core_importable": _module_exists("langchain_core", extra_path=odr_source_root),
            "open_deep_research_importable": _module_exists("open_deep_research", extra_path=odr_source_root),
            "timeout_seconds": _env_int("ODR_TIMEOUT_SECONDS", 45),
            "http_timeout_seconds": _env_int("ODR_HTTP_TIMEOUT_SECONDS", 30),
            "max_retries": _env_int("ODR_MAX_RETRIES", 1),
            "evidence_timeout_seconds": _env_int("EVIDENCE_TIMEOUT_SECONDS", _env_int("ODR_TIMEOUT_SECONDS", 45) + 5),
        },
        "sources": {
            "defillama_enabled": True,
            "coinglass_key_present": bool(os.getenv("COINGLASS_API_KEY")),
            "binance_enabled": True,
            "data_source_timeout_seconds": _env_int("DATA_SOURCE_TIMEOUT_SECONDS", 20),
        },
    }

    if not checks["open_deep_research"]["project_root_exists"]:
        checks["open_deep_research"]["status"] = "degraded"
    elif not checks["open_deep_research"]["langchain_core_importable"]:
        checks["open_deep_research"]["status"] = "degraded"
    elif not checks["open_deep_research"]["open_deep_research_importable"]:
        checks["open_deep_research"]["status"] = "degraded"

    degraded = [
        name
        for name, payload in checks.items()
        if isinstance(payload, dict) and payload.get("status") == "degraded"
    ]
    return {
        "status": "ready" if not degraded else "degraded",
        "critical_failures": degraded,
        "checks": checks,
    }


def _module_exists(module_name: str, *, extra_path: Path | None = None) -> bool:
    added = False
    if extra_path is not None and extra_path.exists():
        path_string = str(extra_path)
        if path_string not in sys.path:
            sys.path.insert(0, path_string)
            added = True
    try:
        return importlib.util.find_spec(module_name) is not None
    finally:
        if added:
            try:
                sys.path.remove(str(extra_path))
            except ValueError:
                pass


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default
