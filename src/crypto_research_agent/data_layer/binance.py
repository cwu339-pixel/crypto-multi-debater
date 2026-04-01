from __future__ import annotations

from typing import Any, Callable

from crypto_research_agent.data_layer.openbb_layer import AdapterOutcome
from crypto_research_agent.schemas import ResearchRequest

_FAPI_BASE = "https://fapi.binance.com"


def fetch_binance_data(
    request: ResearchRequest,
    config: dict[str, Any],
    *,
    http_get: Callable[..., Any],
) -> AdapterOutcome:
    if not config.get("enabled", True):
        return AdapterOutcome(
            status="disabled",
            reason="disabled",
            payloads={},
            request_metadata={},
            config_metadata=config,
        )

    symbol = f"{request.asset}USDT"

    try:
        funding_payload = http_get(
            f"{_FAPI_BASE}/fapi/v1/fundingRate",
            headers={"accept": "application/json"},
            params={"symbol": symbol, "limit": 100},
        )
    except Exception as exc:  # noqa: BLE001
        return AdapterOutcome(
            status="error",
            reason=f"exception:{type(exc).__name__}",
            payloads={},
            request_metadata={"symbol": symbol},
            config_metadata=config,
        )

    try:
        oi_payload = http_get(
            f"{_FAPI_BASE}/futures/data/openInterestHist",
            headers={"accept": "application/json"},
            params={"symbol": symbol, "period": "1d", "limit": 30},
        )
    except Exception as exc:  # noqa: BLE001
        oi_payload = []

    return AdapterOutcome(
        status="fetched",
        reason=None,
        payloads={
            "funding_rate": funding_payload,
            "open_interest_hist": oi_payload,
        },
        request_metadata={"symbol": symbol},
        config_metadata=config,
    )
