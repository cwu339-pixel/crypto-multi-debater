from pathlib import Path

from crypto_research_agent.config import load_yaml_config


def test_load_yaml_config_reads_nested_source_settings(tmp_path: Path) -> None:
    config_path = tmp_path / "sources.yaml"
    config_path.write_text(
        "sources:\n"
        "  openbb:\n"
        "    enabled: true\n"
        "  coinglass:\n"
        "    enabled: false\n",
        encoding="utf-8",
    )

    config = load_yaml_config(config_path)

    assert config["sources"]["openbb"]["enabled"] is True
    assert config["sources"]["coinglass"]["enabled"] is False
