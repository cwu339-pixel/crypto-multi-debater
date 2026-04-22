import json
import subprocess
import time
from datetime import datetime, timezone

from crypto_research_agent.data_layer.service import collect_market_data
from crypto_research_agent.schemas import ResearchRequest


def make_request() -> ResearchRequest:
    return ResearchRequest(
        asset="BTC",
        thesis="Assess reversal risk",
        horizon_days=3,
        run_id="r_test_data_layer",
        as_of_utc=datetime(2099, 3, 25, 9, 30, tzinfo=timezone.utc),
    )


def test_collect_market_data_skips_coinglass_without_key(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.delenv("COINGLASS_API_KEY", raising=False)

    bundle = collect_market_data(
        request=make_request(),
        sources_config={
            "sources": {
                "openbb": {"enabled": False},
                "defillama": {"enabled": False},
                "binance": {"enabled": False},
                "coinglass": {
                    "enabled": True,
                    "base_url": "https://open-api-v4.coinglass.com",
                    "api_key_env": "COINGLASS_API_KEY",
                },
            }
        },
        output_root=tmp_path,
    )

    result = bundle.source_results["coinglass"]
    assert result.status == "skipped"
    assert result.reason == "missing_api_key"
    assert bundle.coverage_gaps == ["coinglass:missing_api_key"]
    assert bundle.provenance_path.exists()

    provenance_rows = [
        json.loads(line)
        for line in bundle.provenance_path.read_text(encoding="utf-8").splitlines()
    ]
    coinglass_row = next(row for row in provenance_rows if row["source"] == "coinglass")
    assert coinglass_row["status"] == "skipped"
    assert coinglass_row["reason"] == "missing_api_key"
    assert coinglass_row["artifact_paths"] == []


def test_collect_market_data_writes_coinglass_snapshots(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("COINGLASS_API_KEY", "test-key")

    def fake_http_get(url, headers=None, params=None):
        assert headers["CG-API-KEY"] == "test-key"
        assert params["symbol"] == "BTCUSDT"
        if url.endswith("/api/futures/open-interest/history"):
            return {"data": [{"t": 1, "o": 10, "h": 11, "l": 9, "c": 10.5}]}
        if url.endswith("/api/futures/funding-rate/history"):
            return {"data": [{"t": 1, "o": 0.01, "h": 0.02, "l": 0.005, "c": 0.015}]}
        if url.endswith("/api/futures/liquidation/history"):
            return {"data": [{"longLiquidationUsd": 1000000, "shortLiquidationUsd": 250000}]}
        raise AssertionError(url)

    bundle = collect_market_data(
        request=make_request(),
        sources_config={
            "sources": {
                "openbb": {"enabled": False},
                "defillama": {"enabled": False},
                "coinglass": {
                    "enabled": True,
                    "base_url": "https://open-api-v4.coinglass.com",
                    "api_key_env": "COINGLASS_API_KEY",
                    "api_key_header": "CG-API-KEY",
                },
            }
        },
        output_root=tmp_path,
        http_get=fake_http_get,
    )

    result = bundle.source_results["coinglass"]
    assert result.status == "fetched"
    assert len(result.artifact_paths) == 3

    artifact_names = {path.stem for path in result.artifact_paths}
    assert artifact_names == {"open_interest_history", "funding_rate_history", "liquidation_history"}


def test_collect_market_data_writes_defillama_snapshots(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.setenv("DEFILLAMA_API_KEY", "test-key")

    def fake_http_get(url, headers=None, params=None):
        assert headers == {}
        assert params == {}
        if url.endswith("/api/protocols"):
            return [{"name": "Aave", "tvl": 100}]
        if url.endswith("/yields/pools"):
            return {"status": "success", "data": [{"pool": "aave-v3-usdc"}]}
        raise AssertionError(url)

    bundle = collect_market_data(
        request=make_request(),
        sources_config={
            "sources": {
                "openbb": {"enabled": False},
                "coinglass": {"enabled": False},
                "defillama": {
                    "enabled": True,
                    "base_url": "https://pro-api.llama.fi",
                    "api_key_env": "DEFILLAMA_API_KEY",
                },
            }
        },
        output_root=tmp_path,
        http_get=fake_http_get,
    )

    result = bundle.source_results["defillama"]
    assert result.status == "fetched"
    assert len(result.artifact_paths) == 2
    for artifact_path in result.artifact_paths:
        assert artifact_path.exists()
    protocols_payload = json.loads(result.artifact_paths[0].read_text(encoding="utf-8"))
    assert protocols_payload[0]["name"] == "Aave"

    provenance_rows = [
        json.loads(line)
        for line in bundle.provenance_path.read_text(encoding="utf-8").splitlines()
    ]
    defillama_row = next(row for row in provenance_rows if row["source"] == "defillama")
    assert defillama_row["status"] == "fetched"
    assert len(defillama_row["artifact_paths"]) == 2
    assert defillama_row["config"]["base_url"] == "https://pro-api.llama.fi"


def test_collect_market_data_falls_back_to_public_defillama_without_key(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.delenv("DEFILLAMA_API_KEY", raising=False)

    def fake_http_get(url, headers=None, params=None):
        assert headers == {}
        assert params == {}
        if url == "https://api.llama.fi/protocols":
            return [{"name": "Aave", "slug": "aave"}]
        if url == "https://yields.llama.fi/pools":
            return {"status": "success", "data": [{"project": "aave-v3"}]}
        raise AssertionError(url)

    bundle = collect_market_data(
        request=make_request(),
        sources_config={
            "sources": {
                "openbb": {"enabled": False},
                "coinglass": {"enabled": False},
                "binance": {"enabled": False},
                "defillama": {
                    "enabled": True,
                    "api_key_env": "DEFILLAMA_API_KEY",
                    "base_url": "https://pro-api.llama.fi",
                    "public_base_url": "https://api.llama.fi",
                    "public_yields_url": "https://yields.llama.fi/pools",
                },
            }
        },
        output_root=tmp_path,
        http_get=fake_http_get,
    )

    result = bundle.source_results["defillama"]
    assert result.status == "fetched"
    assert result.reason is None
    assert bundle.coverage_gaps == []

    provenance_rows = [
        json.loads(line)
        for line in bundle.provenance_path.read_text(encoding="utf-8").splitlines()
    ]
    defillama_row = next(row for row in provenance_rows if row["source"] == "defillama")
    assert defillama_row["status"] == "fetched"
    assert defillama_row["request"]["mode"] == "public"


def test_collect_market_data_skips_defillama_for_historical_replay(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.delenv("DEFILLAMA_API_KEY", raising=False)

    request = ResearchRequest(
        asset="BTC",
        thesis="Historical replay",
        horizon_days=3,
        run_id="r_test_historical_defillama",
        as_of_utc=datetime(2020, 1, 1, 0, 0, tzinfo=timezone.utc),
    )

    called = {"http": 0}

    def fake_http_get(url, headers=None, params=None):
        called["http"] += 1
        raise AssertionError("historical replay should not call DefiLlama")

    bundle = collect_market_data(
        request=request,
        sources_config={
            "sources": {
                "openbb": {"enabled": False},
                "coinglass": {"enabled": False},
                "binance": {"enabled": False},
                "defillama": {
                    "enabled": True,
                    "api_key_env": "DEFILLAMA_API_KEY",
                    "base_url": "https://pro-api.llama.fi",
                    "public_base_url": "https://api.llama.fi",
                    "public_yields_url": "https://yields.llama.fi/pools",
                },
            }
        },
        output_root=tmp_path,
        http_get=fake_http_get,
    )

    result = bundle.source_results["defillama"]
    assert called["http"] == 0
    assert result.status == "skipped"
    assert result.reason == "historical_replay_unavailable"
    assert "defillama:historical_replay_unavailable" in bundle.coverage_gaps


def test_collect_market_data_writes_openbb_snapshot(tmp_path) -> None:
    class DummyHistoricalResult:
        def __init__(self, rows):
            self.results = rows

    class DummyPrice:
        def __init__(self):
            self.calls = []

        def historical(self, **kwargs):
            self.calls.append(kwargs)
            return DummyHistoricalResult([{"open": 1, "close": 2}])

    class DummyCrypto:
        def __init__(self):
            self.price = DummyPrice()

    class DummyOpenBB:
        def __init__(self):
            self.crypto = DummyCrypto()

    openbb_client = DummyOpenBB()

    bundle = collect_market_data(
        request=make_request(),
        sources_config={
            "sources": {
                "openbb": {"enabled": True},
                "coinglass": {"enabled": False},
                "defillama": {"enabled": False},
            }
        },
        output_root=tmp_path,
        openbb_client=openbb_client,
    )

    result = bundle.source_results["openbb"]
    assert result.status == "fetched"
    assert len(result.artifact_paths) == 1
    payload = json.loads(result.artifact_paths[0].read_text(encoding="utf-8"))
    assert payload[0]["close"] == 2
    assert openbb_client.crypto.price.calls[0]["symbol"] == "BTCUSD"

    provenance_rows = [
        json.loads(line)
        for line in bundle.provenance_path.read_text(encoding="utf-8").splitlines()
    ]
    openbb_row = next(row for row in provenance_rows if row["source"] == "openbb")
    assert openbb_row["status"] == "fetched"
    assert openbb_row["request"]["symbol"] == "BTCUSD"
    assert openbb_row["artifact_paths"][0].endswith("price_history.json")


def test_collect_market_data_does_not_crash_on_defillama_http_error(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.delenv("DEFILLAMA_API_KEY", raising=False)

    def failing_http_get(url, headers=None, params=None):
        raise RuntimeError("network_flake")

    bundle = collect_market_data(
        request=make_request(),
        sources_config={
            "sources": {
                "openbb": {"enabled": False},
                "coinglass": {"enabled": False},
                "defillama": {
                    "enabled": True,
                    "api_key_env": "DEFILLAMA_API_KEY",
                    "public_base_url": "https://api.llama.fi",
                    "public_yields_url": "https://yields.llama.fi/pools",
                },
            }
        },
        output_root=tmp_path,
        http_get=failing_http_get,
    )

    result = bundle.source_results["defillama"]
    assert result.status == "error"
    assert result.reason == "exception:RuntimeError"
    assert "defillama:exception:RuntimeError" in bundle.coverage_gaps


def test_collect_market_data_times_out_hung_adapter(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("ADAPTER_TIMEOUT_SECONDS", "1")

    class DummyHistoricalResult:
        def __init__(self, rows):
            self.results = rows

    class SlowPrice:
        def historical(self, **kwargs):
            time.sleep(2)
            return DummyHistoricalResult([{"open": 1, "close": 2}])

    class DummyCrypto:
        def __init__(self):
            self.price = SlowPrice()

    class DummyOpenBB:
        def __init__(self):
            self.crypto = DummyCrypto()

    bundle = collect_market_data(
        request=make_request(),
        sources_config={
            "sources": {
                "openbb": {"enabled": True},
                "coinglass": {"enabled": False},
                "defillama": {"enabled": False},
                "binance": {"enabled": False},
            }
        },
        output_root=tmp_path,
        openbb_client=DummyOpenBB(),
    )

    result = bundle.source_results["openbb"]
    assert result.status == "error"
    assert result.reason == "exception:TimeoutError"
    assert "openbb:exception:TimeoutError" in bundle.coverage_gaps


def test_collect_market_data_uses_isolated_adapter_execution_when_not_injected(
    monkeypatch, tmp_path
) -> None:
    calls = {"count": 0}

    class Completed:
        returncode = 0
        stdout = json.dumps(
            {
                "status": "fetched",
                "reason": None,
                "payloads": {
                    "protocols": [{"name": "Aave"}],
                    "yields_pools": {"status": "success", "data": []},
                },
                "request_metadata": {"mode": "public"},
                "config_metadata": {"enabled": True},
            }
        )
        stderr = ""

    def fake_run(cmd, input, text, capture_output, timeout, env):
        calls["count"] += 1
        payload = json.loads(input)
        if payload["source"] == "defillama":
            return Completed()
        return type(
            "CompletedDisabled",
            (),
            {
                "returncode": 0,
                "stdout": json.dumps(
                    {
                        "status": "disabled",
                        "reason": "disabled",
                        "payloads": {},
                        "request_metadata": {},
                        "config_metadata": {},
                    }
                ),
                "stderr": "",
            },
        )()

    monkeypatch.setattr("crypto_research_agent.data_layer.service.subprocess.run", fake_run)

    bundle = collect_market_data(
        request=make_request(),
        sources_config={
            "sources": {
                "openbb": {"enabled": False},
                "coinglass": {"enabled": False},
                "binance": {"enabled": False},
                "defillama": {"enabled": True},
            }
        },
        output_root=tmp_path,
    )

    assert calls["count"] == 4
    assert bundle.source_results["defillama"].status == "fetched"


def test_collect_market_data_marks_isolated_adapter_timeout(
    monkeypatch, tmp_path
) -> None:
    def fake_run(cmd, input, text, capture_output, timeout, env):
        payload = json.loads(input)
        if payload["source"] == "defillama":
            raise subprocess.TimeoutExpired(cmd=cmd, timeout=timeout)
        return type(
            "CompletedDisabled",
            (),
            {
                "returncode": 0,
                "stdout": json.dumps(
                    {
                        "status": "disabled",
                        "reason": "disabled",
                        "payloads": {},
                        "request_metadata": {},
                        "config_metadata": {},
                    }
                ),
                "stderr": "",
            },
        )()

    monkeypatch.setattr("crypto_research_agent.data_layer.service.subprocess.run", fake_run)

    bundle = collect_market_data(
        request=make_request(),
        sources_config={
            "sources": {
                "openbb": {"enabled": False},
                "coinglass": {"enabled": False},
                "binance": {"enabled": False},
                "defillama": {"enabled": True},
            }
        },
        output_root=tmp_path,
    )

    assert bundle.source_results["defillama"].status == "error"
    assert bundle.source_results["defillama"].reason == "exception:TimeoutError"
    assert "defillama:exception:TimeoutError" in bundle.coverage_gaps
