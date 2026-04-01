from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from crypto_research_agent.schemas import ResearchRequest


@dataclass(frozen=True)
class AdapterOutcome:
    status: str
    reason: str | None
    payloads: dict[str, Any]
    request_metadata: dict[str, Any]
    config_metadata: dict[str, Any]


def fetch_openbb_data(
    request: ResearchRequest,
    config: dict[str, Any],
    *,
    openbb_client: Any | None = None,
) -> AdapterOutcome:
    if not config.get("enabled", False):
        return AdapterOutcome(
            status="disabled",
            reason="disabled",
            payloads={},
            request_metadata={},
            config_metadata=_sanitize_config(config),
        )

    client = openbb_client or _load_openbb_client()
    if client is None:
        return AdapterOutcome(
            status="skipped",
            reason="openbb_not_installed",
            payloads={},
            request_metadata={},
            config_metadata=_sanitize_config(config),
        )

    lookback_days = int(config.get("lookback_days", 180))
    start_date = (request.as_of_utc - timedelta(days=lookback_days)).date().isoformat()
    symbol = f"{request.asset}{config.get('quote_currency', 'USD')}"
    interval = config.get("interval")

    kwargs = {"symbol": symbol, "start_date": start_date}
    if interval:
        kwargs["interval"] = interval

    response = client.crypto.price.historical(**kwargs)
    payload = _serialize_openbb_response(response)
    return AdapterOutcome(
        status="fetched",
        reason=None,
        payloads={"price_history": payload},
        request_metadata=kwargs,
        config_metadata=_sanitize_config(config),
    )


def _load_openbb_client() -> Any | None:
    try:
        from openbb import obb  # type: ignore
    except ImportError:
        return None
    return obb


def _serialize_openbb_response(response: Any) -> Any:
    rows = getattr(response, "results", response)
    if isinstance(rows, list):
        return [_serialize_openbb_row(row) for row in rows]
    return _serialize_openbb_row(rows)


def _serialize_openbb_row(row: Any) -> Any:
    if hasattr(row, "model_dump"):
        return row.model_dump()
    if hasattr(row, "dict"):
        return row.dict()
    return row


def _sanitize_config(config: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in config.items()}
