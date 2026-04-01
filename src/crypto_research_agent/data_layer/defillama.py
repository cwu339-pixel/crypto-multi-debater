from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Callable

from crypto_research_agent.data_layer.openbb_layer import AdapterOutcome
from crypto_research_agent.schemas import ResearchRequest


def fetch_defillama_data(
    request: ResearchRequest,
    config: dict[str, Any],
    *,
    http_get: Callable[..., Any],
) -> AdapterOutcome:
    if not config.get("enabled", False):
        return AdapterOutcome(
            status="disabled",
            reason="disabled",
            payloads={},
            request_metadata={},
            config_metadata=_sanitize_config(config),
        )

    if request.as_of_utc.date() < datetime.now(timezone.utc).date():
        return AdapterOutcome(
            status="skipped",
            reason="historical_replay_unavailable",
            payloads={},
            request_metadata={"mode": "historical_replay"},
            config_metadata=_sanitize_config(config),
        )

    api_key_env = config.get("api_key_env")
    api_key = os.getenv(api_key_env, "") if api_key_env else ""
    if api_key:
        base_url = config.get("base_url", "https://pro-api.llama.fi").rstrip("/")
        prefix = f"{base_url}/{api_key}"
        payloads = {
            "protocols": http_get(f"{prefix}/api/protocols", headers={}, params={}),
            "yields_pools": http_get(f"{prefix}/yields/pools", headers={}, params={}),
        }
        request_metadata = {
            "mode": "pro",
            "endpoints": ["/api/protocols", "/yields/pools"],
            "base_url": base_url,
        }
    else:
        public_base_url = config.get("public_base_url", "https://api.llama.fi").rstrip("/")
        public_yields_url = config.get("public_yields_url", "https://yields.llama.fi/pools")
        payloads = {
            "protocols": http_get(f"{public_base_url}/protocols", headers={}, params={}),
            "yields_pools": http_get(public_yields_url, headers={}, params={}),
        }
        request_metadata = {
            "mode": "public",
            "endpoints": ["/protocols", public_yields_url],
            "base_url": public_base_url,
        }
    return AdapterOutcome(
        status="fetched",
        reason=None,
        payloads=payloads,
        request_metadata=request_metadata,
        config_metadata=_sanitize_config(config),
    )


def _sanitize_config(config: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in config.items()}
