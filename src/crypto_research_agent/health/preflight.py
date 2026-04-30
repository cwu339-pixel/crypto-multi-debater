from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from typing import Any

from crypto_research_agent.agents.provider import DeterministicAnalysisProvider, default_analysis_provider
from crypto_research_agent.research.open_deep_research_client import _resolve_local_project_root


def run_preflight() -> dict[str, Any]:
    project_root = Path(__file__).resolve().parents[3]
    env_file = project_root / ".env"
    repo_venv_python = project_root / ".venv" / "bin" / "python"
    preferred_python = Path("/opt/miniconda3/bin/python3")
    provider = default_analysis_provider()
    odr_root = _resolve_local_project_root(None)
    odr_source_root = odr_root / "src"
    output_root = project_root / "tmp"

    checks = {
        "paths": {
            "status": "ok",
            "project_root": str(project_root),
            "project_root_exists": project_root.exists(),
            "env_file_present": env_file.exists(),
            "cwd": os.getcwd(),
            "cwd_inside_project": _is_relative_to(Path.cwd(), project_root),
        },
        "runtime": {
            "status": "ok",
            "python_executable": sys.executable,
            "python_version": sys.version.split()[0],
            "preferred_python": str(preferred_python),
            "preferred_python_exists": preferred_python.exists(),
            "repo_venv_python": str(repo_venv_python),
            "repo_venv_python_exists": repo_venv_python.exists(),
            "using_repo_venv": Path(sys.executable).resolve() == repo_venv_python.resolve() if repo_venv_python.exists() else False,
        },
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
        "output_contract": {
            "status": "ok",
            "default_output_root": str(project_root),
            "tmp_dir": str(output_root),
            "tmp_dir_exists": output_root.exists(),
            "tmp_dir_writable": _dir_writable(output_root),
            "showcase_dir": str(project_root / "tmp_showcase"),
            "showcase_dir_exists": (project_root / "tmp_showcase").exists(),
        },
    }

    if not checks["paths"]["project_root_exists"] or not checks["paths"]["cwd_inside_project"]:
        checks["paths"]["status"] = "degraded"

    if not checks["runtime"]["repo_venv_python_exists"] or not checks["runtime"]["using_repo_venv"]:
        checks["runtime"]["status"] = "degraded"

    if not checks["open_deep_research"]["project_root_exists"]:
        checks["open_deep_research"]["status"] = "degraded"
    elif not checks["open_deep_research"]["langchain_core_importable"]:
        checks["open_deep_research"]["status"] = "degraded"
    elif not checks["open_deep_research"]["open_deep_research_importable"]:
        checks["open_deep_research"]["status"] = "degraded"

    if not checks["output_contract"]["tmp_dir_writable"]:
        checks["output_contract"]["status"] = "degraded"

    degraded = [
        name
        for name, payload in checks.items()
        if isinstance(payload, dict) and payload.get("status") == "degraded"
    ]
    return {
        "status": "ready" if not degraded else "degraded",
        "critical_failures": degraded,
        "remediation": _build_remediation(project_root, checks),
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


def _dir_writable(path: Path) -> bool:
    candidate = path if path.exists() else path.parent
    try:
        candidate.mkdir(parents=True, exist_ok=True)
        probe = candidate / ".preflight_write_test"
        probe.write_text("ok")
        probe.unlink()
        return True
    except OSError:
        return False


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _build_remediation(project_root: Path, checks: dict[str, dict[str, Any]]) -> list[str]:
    fixes: list[str] = []
    if checks["provider"]["status"] == "degraded":
        fixes.append("Set OPENAI_API_KEY or OPENROUTER_API_KEY before running live debate jobs.")
    if checks["paths"]["status"] == "degraded" or checks["runtime"]["status"] == "degraded":
        fixes.append(
            f"Run from the repo environment: cd {project_root} && .venv/bin/crypto-multi-debater preflight"
        )
    if checks["runtime"]["status"] == "degraded":
        fixes.append(f"Create the repo virtualenv with: cd {project_root} && uv venv .venv && uv pip install --python .venv/bin/python -e '.[dev]'")
    if checks["openbb"]["status"] == "degraded":
        fixes.append(f"Install OpenBB in the repo environment: cd {project_root} && uv pip install --python .venv/bin/python openbb && .venv/bin/openbb-build")
    if checks["open_deep_research"]["status"] == "degraded":
        fixes.append(f"Install ODR dependencies in the repo environment: cd {project_root} && uv pip install --python .venv/bin/python -e external/open_deep_research")
    if checks["output_contract"]["status"] == "degraded":
        fixes.append(f"Ensure {project_root}/tmp is writable for run artifacts.")
    return fixes
