from __future__ import annotations

from pathlib import Path

from crypto_research_agent.agents.provider import DeterministicAnalysisProvider
from crypto_research_agent.health.preflight import run_preflight


def test_run_preflight_reports_runtime_paths_and_output_contract(monkeypatch, tmp_path) -> None:
    project_root = tmp_path / "repo"
    project_root.mkdir()
    (project_root / ".env").write_text("OPENAI_API_KEY=test")
    (project_root / ".venv" / "bin").mkdir(parents=True)
    repo_python = project_root / ".venv" / "bin" / "python"
    repo_python.write_text("")
    odr_root = project_root / "external" / "open_deep_research"
    (odr_root / "src").mkdir(parents=True)
    (project_root / "tmp_showcase").mkdir()

    monkeypatch.setattr(
        "crypto_research_agent.health.preflight.default_analysis_provider",
        lambda: DeterministicAnalysisProvider(),
    )
    monkeypatch.setattr(
        "crypto_research_agent.health.preflight._resolve_local_project_root",
        lambda _root: odr_root,
    )
    monkeypatch.setattr(
        "crypto_research_agent.health.preflight._module_exists",
        lambda module_name, extra_path=None: module_name in {"langchain_core", "open_deep_research", "openbb"},
    )
    monkeypatch.setattr(
        "crypto_research_agent.health.preflight.Path.cwd",
        lambda: project_root,
    )
    monkeypatch.setattr(
        "crypto_research_agent.health.preflight.Path.resolve",
        lambda self: self,
        raising=False,
    )
    monkeypatch.setattr(
        "crypto_research_agent.health.preflight.__file__",
        str(project_root / "src" / "crypto_research_agent" / "health" / "preflight.py"),
    )

    result = run_preflight()

    assert result["status"] == "degraded"
    assert "provider" in result["critical_failures"]
    assert result["checks"]["paths"]["project_root"] == str(project_root)
    assert result["checks"]["runtime"]["repo_venv_python"] == str(repo_python)
    assert result["checks"]["output_contract"]["showcase_dir_exists"] is True
    assert result["checks"]["output_contract"]["tmp_dir_writable"] is True
    assert result["remediation"][0].startswith("Set OPENAI_API_KEY or OPENROUTER_API_KEY")


def test_run_preflight_degrades_when_not_using_repo_venv_or_project_cwd(monkeypatch, tmp_path) -> None:
    project_root = tmp_path / "repo"
    project_root.mkdir()
    (project_root / ".env").write_text("OPENAI_API_KEY=test")
    (project_root / ".venv" / "bin").mkdir(parents=True)
    repo_python = project_root / ".venv" / "bin" / "python"
    repo_python.write_text("")
    odr_root = project_root / "external" / "open_deep_research"
    (odr_root / "src").mkdir(parents=True)

    monkeypatch.setattr(
        "crypto_research_agent.health.preflight.default_analysis_provider",
        lambda: DeterministicAnalysisProvider(),
    )
    monkeypatch.setattr(
        "crypto_research_agent.health.preflight._resolve_local_project_root",
        lambda _root: odr_root,
    )
    monkeypatch.setattr(
        "crypto_research_agent.health.preflight._module_exists",
        lambda module_name, extra_path=None: module_name in {"langchain_core", "open_deep_research", "openbb"},
    )
    monkeypatch.setattr(
        "crypto_research_agent.health.preflight.Path.cwd",
        lambda: tmp_path,
    )
    monkeypatch.setattr(
        "crypto_research_agent.health.preflight.sys.executable",
        str(tmp_path / "global-python"),
    )
    monkeypatch.setattr(
        "crypto_research_agent.health.preflight.Path.resolve",
        lambda self: self,
        raising=False,
    )
    monkeypatch.setattr(
        "crypto_research_agent.health.preflight.__file__",
        str(project_root / "src" / "crypto_research_agent" / "health" / "preflight.py"),
    )

    result = run_preflight()

    assert result["status"] == "degraded"
    assert "paths" in result["critical_failures"]
    assert "runtime" in result["critical_failures"]
    assert any(".venv/bin/crypto-multi-debater preflight" in line for line in result["remediation"])


def test_run_preflight_adds_odr_remediation_when_dependencies_missing(monkeypatch, tmp_path) -> None:
    project_root = tmp_path / "repo"
    project_root.mkdir()
    odr_root = project_root / "external" / "open_deep_research"

    monkeypatch.setattr(
        "crypto_research_agent.health.preflight.default_analysis_provider",
        lambda: DeterministicAnalysisProvider(),
    )
    monkeypatch.setattr(
        "crypto_research_agent.health.preflight._resolve_local_project_root",
        lambda _root: odr_root,
    )
    monkeypatch.setattr(
        "crypto_research_agent.health.preflight._module_exists",
        lambda module_name, extra_path=None: False,
    )
    monkeypatch.setattr(
        "crypto_research_agent.health.preflight.Path.cwd",
        lambda: project_root,
    )
    monkeypatch.setattr(
        "crypto_research_agent.health.preflight.Path.resolve",
        lambda self: self,
        raising=False,
    )
    monkeypatch.setattr(
        "crypto_research_agent.health.preflight.__file__",
        str(project_root / "src" / "crypto_research_agent" / "health" / "preflight.py"),
    )

    result = run_preflight()

    assert result["status"] == "degraded"
    assert "open_deep_research" in result["critical_failures"]
    assert any("external/open_deep_research" in line for line in result["remediation"])
