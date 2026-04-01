import json
import os
from datetime import datetime, timezone

import pytest

from crypto_research_agent.data_layer.service import collect_market_data
from crypto_research_agent.schemas import ResearchRequest


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_OPENBB_INTEGRATION") != "1",
    reason="Set RUN_OPENBB_INTEGRATION=1 to run the real OpenBB integration test.",
)


def test_openbb_real_price_history_fetch_writes_snapshot(tmp_path) -> None:
    request = ResearchRequest(
        asset="BTC",
        thesis="integration test",
        horizon_days=3,
        run_id="r_openbb_integration",
        as_of_utc=datetime.now(timezone.utc),
    )

    bundle = collect_market_data(
        request=request,
        sources_config={
            "sources": {
                "openbb": {
                    "enabled": True,
                    "lookback_days": 30,
                    "quote_currency": "USD",
                },
                "defillama": {"enabled": False},
                "coinglass": {"enabled": False},
            }
        },
        output_root=tmp_path,
    )

    result = bundle.source_results["openbb"]
    assert result.status == "fetched"
    assert len(result.artifact_paths) == 1

    payload = json.loads(result.artifact_paths[0].read_text(encoding="utf-8"))
    assert payload
    assert isinstance(payload, list)
