from __future__ import annotations

import os
from typing import Any, Callable

from crypto_research_agent.data_layer.openbb_layer import AdapterOutcome
from crypto_research_agent.schemas import ResearchRequest


def fetch_coinglass_data(
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

    api_key_env = config.get("api_key_env")
    api_key = os.getenv(api_key_env, "") if api_key_env else ""
    if not api_key:
        return AdapterOutcome(
            status="skipped",
            reason="missing_api_key",
            payloads={},
            request_metadata={},
            config_metadata=_sanitize_config(config),
        )

    base_url = config.get("base_url", "https://open-api-v4.coinglass.com").rstrip("/")
    params = {
        "exchange": config.get("exchange", "Binance"),
        "symbol": f"{request.asset}{config.get('symbol_suffix', 'USDT')}",
        "interval": config.get("interval", "1d"),
    }
    payload = http_get(
        f"{base_url}/api/futures/open-interest/history",
        headers={
            "accept": "application/json",
            config.get("api_key_header", "CG-API-KEY"): api_key,
        },
        params=params,
    )
    funding_payload = http_get(
        f"{base_url}/api/futures/funding-rate/history",
        headers={
            "accept": "application/json",
            config.get("api_key_header", "CG-API-KEY"): api_key,
        },
        params=params,
    )
    liquidation_payload = http_get(
        f"{base_url}/api/futures/liquidation/history",
        headers={
            "accept": "application/json",
            config.get("api_key_header", "CG-API-KEY"): api_key,
        },
        params=params,
    )
    return AdapterOutcome(
        status="fetched",
        reason=None,
        payloads={
            "open_interest_history": payload,
            "funding_rate_history": funding_payload,
            "liquidation_history": liquidation_payload,
        },
        request_metadata=params,
        config_metadata=_sanitize_config(config),
    )


def _sanitize_config(config: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in config.items()}
