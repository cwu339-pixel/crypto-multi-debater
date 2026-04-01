import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from crypto_research_agent.data_prep.features import build_feature_bundle
from crypto_research_agent.schemas import FeatureBundle, RawDataBundle, ResearchRequest, SourceResult


def make_request() -> ResearchRequest:
    return ResearchRequest(
        asset="BTC",
        thesis="Assess reversal risk",
        horizon_days=3,
        run_id="r_feature_test",
        as_of_utc=datetime(2026, 3, 25, 9, 30, tzinfo=timezone.utc),
    )


def _write_openbb_snapshot(run_root: Path, rows: list[dict]) -> Path:
    openbb_path = run_root / "raw" / "openbb" / "price_history.json"
    openbb_path.parent.mkdir(parents=True, exist_ok=True)
    openbb_path.write_text(json.dumps(rows), encoding="utf-8")
    return openbb_path


def _write_defillama_snapshots(
    run_root: Path,
    protocols: list[dict] | None = None,
    yields_data: dict | None = None,
) -> list[Path]:
    paths: list[Path] = []
    dl_dir = run_root / "raw" / "defillama"
    dl_dir.mkdir(parents=True, exist_ok=True)

    if protocols is not None:
        p_path = dl_dir / "protocols.json"
        p_path.write_text(json.dumps(protocols), encoding="utf-8")
        paths.append(p_path)

    if yields_data is not None:
        y_path = dl_dir / "yields_pools.json"
        y_path.write_text(json.dumps(yields_data), encoding="utf-8")
        paths.append(y_path)

    return paths


def _write_coinglass_snapshots(
    run_root: Path,
    *,
    open_interest: dict | None = None,
    funding_rate: dict | None = None,
    liquidation: dict | None = None,
) -> list[Path]:
    paths: list[Path] = []
    cg_dir = run_root / "raw" / "coinglass"
    cg_dir.mkdir(parents=True, exist_ok=True)

    payloads = {
        "open_interest_history": open_interest,
        "funding_rate_history": funding_rate,
        "liquidation_history": liquidation,
    }
    for name, payload in payloads.items():
        if payload is None:
            continue
        path = cg_dir / f"{name}.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        paths.append(path)
    return paths


def _make_price_rows(count: int, base_close: float = 100.0, daily_delta: float = 1.0) -> list[dict]:
    rows = []
    start = datetime(2025, 1, 1, tzinfo=timezone.utc)
    for i in range(count):
        close = base_close + i * daily_delta
        row_date = (start + timedelta(days=i)).date().isoformat()
        rows.append({
            "date": row_date,
            "open": close - 0.5,
            "high": close + 2.0,
            "low": close - 2.0,
            "close": close,
            "volume": 1_000_000.0 + i * 100,
        })
    return rows


def test_build_feature_bundle_from_openbb_snapshot(tmp_path: Path) -> None:
    run_root = tmp_path / "runs" / "r_feature_test"
    openbb_path = _write_openbb_snapshot(run_root, [
        {"date": "2026-03-23", "close": 100.0, "volume": 10.0},
        {"date": "2026-03-24", "close": 110.0, "volume": 15.0},
        {"date": "2026-03-25", "close": 121.0, "volume": 20.0},
    ])

    raw_bundle = RawDataBundle(
        run_id="r_feature_test",
        source_results={
            "openbb": SourceResult(
                source="openbb",
                status="fetched",
                reason=None,
                artifact_paths=[openbb_path],
            )
        },
        coverage_gaps=[],
        provenance_path=run_root / "provenance.jsonl",
    )

    bundle = build_feature_bundle(
        request=make_request(),
        raw_data=raw_bundle,
        output_root=tmp_path,
    )

    assert bundle.summary["asset"] == "BTC"
    assert bundle.summary["latest_close"] == 121.0
    assert bundle.summary["return_1d_pct"] == 10.0
    assert bundle.summary["return_total_pct"] == 21.0
    assert bundle.summary["avg_volume"] == 15.0
    assert bundle.features_path.exists()
    assert bundle.notes_path.exists()


def test_build_feature_bundle_respects_as_of_date_for_price_slice(tmp_path: Path) -> None:
    run_root = tmp_path / "runs" / "r_feature_test"
    openbb_path = _write_openbb_snapshot(run_root, [
        {"date": "2025-10-04", "close": 100.0, "volume": 10.0},
        {"date": "2025-10-05", "close": 110.0, "volume": 15.0},
        {"date": "2025-10-06", "close": 220.0, "volume": 20.0},
    ])

    request = ResearchRequest(
        asset="BTC",
        thesis="Assess historical point-in-time state",
        horizon_days=3,
        run_id="r_feature_test",
        as_of_utc=datetime(2025, 10, 5, 0, 0, tzinfo=timezone.utc),
    )

    raw_bundle = RawDataBundle(
        run_id="r_feature_test",
        source_results={
            "openbb": SourceResult(
                source="openbb",
                status="fetched",
                reason=None,
                artifact_paths=[openbb_path],
            )
        },
        coverage_gaps=[],
        provenance_path=run_root / "provenance.jsonl",
    )

    bundle = build_feature_bundle(
        request=request,
        raw_data=raw_bundle,
        output_root=tmp_path,
    )

    assert bundle.summary["latest_close"] == 110.0
    assert bundle.summary["return_1d_pct"] == 10.0
    assert bundle.summary["return_total_pct"] == 10.0


def test_feature_bundle_records_missing_sources_as_gaps(tmp_path: Path) -> None:
    raw_bundle = RawDataBundle(
        run_id="r_feature_test",
        source_results={
            "openbb": SourceResult(
                source="openbb",
                status="skipped",
                reason="openbb_not_installed",
                artifact_paths=[],
            )
        },
        coverage_gaps=["openbb:openbb_not_installed"],
        provenance_path=tmp_path / "runs" / "r_feature_test" / "provenance.jsonl",
    )

    bundle = build_feature_bundle(
        request=make_request(),
        raw_data=raw_bundle,
        output_root=tmp_path,
    )

    assert bundle.summary["asset"] == "BTC"
    assert bundle.summary["feature_status"] == "partial"
    assert "openbb:openbb_not_installed" in bundle.coverage_gaps
    assert bundle.notes_path.read_text(encoding="utf-8")


def test_realized_vol_computed_with_enough_data(tmp_path: Path) -> None:
    rows = _make_price_rows(35)
    run_root = tmp_path / "runs" / "r_feature_test"
    openbb_path = _write_openbb_snapshot(run_root, rows)

    raw_bundle = RawDataBundle(
        run_id="r_feature_test",
        source_results={
            "openbb": SourceResult(source="openbb", status="fetched", reason=None, artifact_paths=[openbb_path])
        },
        coverage_gaps=[],
        provenance_path=run_root / "provenance.jsonl",
    )

    bundle = build_feature_bundle(request=make_request(), raw_data=raw_bundle, output_root=tmp_path)

    assert bundle.summary["realized_vol_7d"] is not None
    assert bundle.summary["realized_vol_30d"] is not None
    assert isinstance(bundle.summary["realized_vol_7d"], float)
    assert bundle.summary["realized_vol_7d"] > 0


def test_rsi_and_sma_computed(tmp_path: Path) -> None:
    rows = _make_price_rows(55, base_close=50000.0, daily_delta=100.0)
    run_root = tmp_path / "runs" / "r_feature_test"
    openbb_path = _write_openbb_snapshot(run_root, rows)

    raw_bundle = RawDataBundle(
        run_id="r_feature_test",
        source_results={
            "openbb": SourceResult(source="openbb", status="fetched", reason=None, artifact_paths=[openbb_path])
        },
        coverage_gaps=[],
        provenance_path=run_root / "provenance.jsonl",
    )

    bundle = build_feature_bundle(request=make_request(), raw_data=raw_bundle, output_root=tmp_path)

    assert bundle.summary["rsi_14"] is not None
    assert 0 <= bundle.summary["rsi_14"] <= 100
    assert bundle.summary["sma_20"] is not None
    assert bundle.summary["sma_50"] is not None
    assert bundle.summary["price_vs_sma20_pct"] is not None
    assert bundle.summary["atr_14"] is not None
    assert bundle.summary["return_7d_pct"] is not None
    assert bundle.summary["return_30d_pct"] is not None


def test_long_term_technical_features_computed(tmp_path: Path) -> None:
    rows = _make_price_rows(220, base_close=50000.0, daily_delta=50.0)
    run_root = tmp_path / "runs" / "r_feature_test"
    openbb_path = _write_openbb_snapshot(run_root, rows)

    raw_bundle = RawDataBundle(
        run_id="r_feature_test",
        source_results={
            "openbb": SourceResult(source="openbb", status="fetched", reason=None, artifact_paths=[openbb_path])
        },
        coverage_gaps=[],
        provenance_path=run_root / "provenance.jsonl",
    )

    bundle = build_feature_bundle(request=make_request(), raw_data=raw_bundle, output_root=tmp_path)

    assert bundle.summary["sma_200"] is not None
    assert bundle.summary["price_vs_sma200_pct"] is not None
    assert bundle.summary["seasonality_month"] is not None
    assert bundle.summary["seasonality_weekday"] is not None
    assert bundle.summary["halving_cycle_day"] is not None


def test_defillama_protocol_features(tmp_path: Path) -> None:
    run_root = tmp_path / "runs" / "r_feature_test"
    protocols = [
        {
            "name": "Aave",
            "chain": "Ethereum",
            "chains": ["Ethereum"],
            "tvl": 10_000_000_000,
            "change_1d": 1.5,
            "change_7d": -2.3,
            "category": "Lending",
        },
        {
            "name": "Uniswap",
            "chain": "Ethereum",
            "chains": ["Ethereum", "Arbitrum"],
            "tvl": 5_000_000_000,
            "change_1d": 0.8,
            "change_7d": 3.1,
            "category": "Dexes",
        },
        {
            "name": "Orca",
            "chain": "Solana",
            "chains": ["Solana"],
            "tvl": 500_000_000,
            "change_1d": -0.5,
            "change_7d": 1.0,
            "category": "Dexes",
        },
    ]
    dl_paths = _write_defillama_snapshots(run_root, protocols=protocols)

    request = ResearchRequest(
        asset="Ethereum",
        thesis="test",
        horizon_days=3,
        run_id="r_feature_test",
        as_of_utc=datetime(2026, 3, 25, 9, 30, tzinfo=timezone.utc),
    )

    raw_bundle = RawDataBundle(
        run_id="r_feature_test",
        source_results={
            "defillama": SourceResult(source="defillama", status="fetched", reason=None, artifact_paths=dl_paths)
        },
        coverage_gaps=[],
        provenance_path=run_root / "provenance.jsonl",
    )

    bundle = build_feature_bundle(request=request, raw_data=raw_bundle, output_root=tmp_path)

    assert bundle.summary["defi_tvl_total"] > 0
    assert bundle.summary["defi_tvl_asset_chain"] == 15_000_000_000
    assert bundle.summary["defi_tvl_asset_share_pct"] is not None
    assert bundle.summary["defi_tvl_change_1d_pct"] is not None
    assert bundle.summary["defi_tvl_change_7d_pct"] is not None
    assert len(bundle.summary["defi_top_protocols"]) == 2


def test_defillama_yield_features(tmp_path: Path) -> None:
    run_root = tmp_path / "runs" / "r_feature_test"
    yields_data = {
        "status": "success",
        "data": [
            {
                "chain": "Ethereum",
                "project": "aave-v3",
                "symbol": "USDC",
                "tvlUsd": 2_000_000_000,
                "apy": 3.5,
                "apyPct7D": 0.2,
                "stablecoin": True,
            },
            {
                "chain": "Ethereum",
                "project": "compound",
                "symbol": "USDT",
                "tvlUsd": 1_000_000_000,
                "apy": 2.8,
                "apyPct7D": -0.1,
                "stablecoin": True,
            },
            {
                "chain": "Ethereum",
                "project": "lido",
                "symbol": "STETH",
                "tvlUsd": 19_000_000_000,
                "apy": 2.4,
                "stablecoin": False,
            },
        ],
    }
    dl_paths = _write_defillama_snapshots(run_root, yields_data=yields_data)

    raw_bundle = RawDataBundle(
        run_id="r_feature_test",
        source_results={
            "defillama": SourceResult(source="defillama", status="fetched", reason=None, artifact_paths=dl_paths)
        },
        coverage_gaps=[],
        provenance_path=run_root / "provenance.jsonl",
    )

    bundle = build_feature_bundle(request=make_request(), raw_data=raw_bundle, output_root=tmp_path)

    assert bundle.summary["defi_stablecoin_median_apy"] is not None
    assert bundle.summary["defi_stablecoin_tvl_weighted_apy"] is not None
    assert bundle.summary["defi_stablecoin_apy_change_7d"] is not None


def test_combined_openbb_and_defillama(tmp_path: Path) -> None:
    run_root = tmp_path / "runs" / "r_feature_test"
    openbb_path = _write_openbb_snapshot(run_root, _make_price_rows(30))
    dl_paths = _write_defillama_snapshots(
        run_root,
        protocols=[
            {"name": "P1", "chain": "Bitcoin", "chains": ["Bitcoin"], "tvl": 1_000_000, "change_1d": 2.0, "change_7d": 5.0, "category": "Bridge"},
        ],
        yields_data={"status": "success", "data": [
            {"chain": "Ethereum", "project": "x", "symbol": "USDC", "tvlUsd": 100, "apy": 4.0, "apyPct7D": 0.1, "stablecoin": True},
        ]},
    )

    raw_bundle = RawDataBundle(
        run_id="r_feature_test",
        source_results={
            "openbb": SourceResult(source="openbb", status="fetched", reason=None, artifact_paths=[openbb_path]),
            "defillama": SourceResult(source="defillama", status="fetched", reason=None, artifact_paths=dl_paths),
        },
        coverage_gaps=[],
        provenance_path=run_root / "provenance.jsonl",
    )

    bundle = build_feature_bundle(request=make_request(), raw_data=raw_bundle, output_root=tmp_path)

    assert bundle.summary["feature_status"] == "complete"
    assert bundle.summary["latest_close"] is not None
    assert bundle.summary["realized_vol_7d"] is not None
    assert bundle.summary["defi_tvl_total"] is not None
    assert bundle.summary["defi_stablecoin_median_apy"] is not None


def test_coinglass_and_defi_derived_features(tmp_path: Path) -> None:
    run_root = tmp_path / "runs" / "r_feature_test"
    openbb_path = _write_openbb_snapshot(run_root, _make_price_rows(40))
    dl_paths = _write_defillama_snapshots(
        run_root,
        protocols=[
            {"name": "P1", "chain": "Bitcoin", "chains": ["Bitcoin"], "tvl": 2_000_000_000, "change_1d": 1.0, "change_7d": 3.0, "category": "Bridge"},
        ],
    )
    cg_paths = _write_coinglass_snapshots(
        run_root,
        open_interest={"data": [{"o": 10_000_000_000, "c": 12_000_000_000}]},
        funding_rate={"data": [{"c": 0.0125}]},
        liquidation={"data": [{"longLiquidationUsd": 1_500_000, "shortLiquidationUsd": 500_000}]},
    )

    raw_bundle = RawDataBundle(
        run_id="r_feature_test",
        source_results={
            "openbb": SourceResult(source="openbb", status="fetched", reason=None, artifact_paths=[openbb_path]),
            "defillama": SourceResult(source="defillama", status="fetched", reason=None, artifact_paths=dl_paths),
            "coinglass": SourceResult(source="coinglass", status="fetched", reason=None, artifact_paths=cg_paths),
        },
        coverage_gaps=[],
        provenance_path=run_root / "provenance.jsonl",
    )

    bundle = build_feature_bundle(request=make_request(), raw_data=raw_bundle, output_root=tmp_path)

    assert bundle.summary["derivatives_open_interest_latest"] == 12_000_000_000
    assert bundle.summary["derivatives_open_interest_change_pct"] == 20.0
    assert bundle.summary["derivatives_funding_rate_latest"] == 0.0125
    assert bundle.summary["derivatives_total_liquidation_usd_24h"] == 2_000_000
    assert bundle.summary["mc_tvl_ratio"] is not None
