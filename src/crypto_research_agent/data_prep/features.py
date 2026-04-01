from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from crypto_research_agent.schemas import FeatureBundle, RawDataBundle, ResearchRequest

BTC_HALVING_DATES = [
    datetime(2012, 11, 28, tzinfo=timezone.utc),
    datetime(2016, 7, 9, tzinfo=timezone.utc),
    datetime(2020, 5, 11, tzinfo=timezone.utc),
    datetime(2024, 4, 19, tzinfo=timezone.utc),
]

MONTH_SEASONALITY = {
    1: "neutral", 2: "neutral", 3: "neutral", 4: "neutral",
    5: "neutral", 6: "neutral", 7: "bullish_lean",
    8: "bearish_lean", 9: "bearish",
    10: "bullish", 11: "bullish_strong", 12: "neutral",
}


def build_feature_bundle(
    *,
    request: ResearchRequest,
    raw_data: RawDataBundle,
    output_root: Path,
) -> FeatureBundle:
    feature_dir = Path(output_root) / "runs" / request.run_id / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    features_path = feature_dir / "summary.json"
    notes_path = feature_dir / "notes.md"

    summary: dict[str, Any] = {
        "asset": request.asset,
        "feature_status": "partial",
    }
    notes: list[str] = []
    coverage_gaps = list(raw_data.coverage_gaps)

    _extract_openbb_features(raw_data, summary, notes, as_of_utc=request.as_of_utc)
    _extract_defillama_features(raw_data, request, summary, notes)
    _extract_coinglass_features(raw_data, summary, notes)
    # Use Binance public API as fallback if CoinGlass derivatives data is missing
    if summary.get("deriv_funding_latest") is None:
        _extract_binance_features(raw_data, summary, notes)
    _derive_cross_domain_features(summary)

    if "coinglass" in raw_data.source_results and raw_data.source_results["coinglass"].status != "fetched":
        notes.append("CoinGlass features pending because source data is unavailable.")

    has_price = summary.get("latest_close") is not None
    has_defi = summary.get("defi_tvl_total") is not None
    if has_price or has_defi:
        summary["feature_status"] = "complete" if (has_price and has_defi) else "partial"

    features_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    notes_path.write_text("\n".join(f"- {note}" for note in notes) + "\n", encoding="utf-8")

    return FeatureBundle(
        run_id=request.run_id,
        summary=summary,
        coverage_gaps=coverage_gaps,
        features_path=features_path,
        notes_path=notes_path,
    )


def _extract_openbb_features(
    raw_data: RawDataBundle,
    summary: dict[str, Any],
    notes: list[str],
    *,
    as_of_utc: datetime | None = None,
) -> None:
    openbb_result = raw_data.source_results.get("openbb")
    if not (openbb_result and openbb_result.status == "fetched" and openbb_result.artifact_paths):
        notes.append("OpenBB price history unavailable; price-derived features were not computed.")
        return

    rows = json.loads(openbb_result.artifact_paths[0].read_text(encoding="utf-8"))
    if not rows:
        notes.append("OpenBB price history empty; price-derived features were not computed.")
        return

    rows = _filter_rows_up_to_as_of(rows, as_of_utc=as_of_utc)
    if not rows:
        notes.append("No OpenBB rows were available at or before the requested as-of date.")
        return

    _summarize_price_rows(rows, summary, as_of_utc=as_of_utc)
    notes.append(f"Built price-derived features from {len(rows)} OpenBB rows.")


def summarize_price_history_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    _summarize_price_rows(rows, summary)
    return summary


def _summarize_price_rows(
    rows: list[dict[str, Any]],
    summary: dict[str, Any],
    *,
    as_of_utc: datetime | None = None,
) -> None:
    if not rows:
        return

    closes = [float(row["close"]) for row in rows if row.get("close") is not None]
    volumes = [float(row["volume"]) for row in rows if row.get("volume") is not None]

    if not closes:
        return

    summary["latest_close"] = round(closes[-1], 6)

    if len(closes) >= 2:
        summary["return_1d_pct"] = round(((closes[-1] / closes[-2]) - 1) * 100, 6)
        summary["return_total_pct"] = round(((closes[-1] / closes[0]) - 1) * 100, 6)

    if volumes:
        summary["avg_volume"] = round(sum(volumes) / len(volumes), 6)

    daily_returns = _daily_returns(closes)
    if len(daily_returns) >= 2:
        summary["realized_vol_30d"] = _realized_vol(daily_returns, window=30)
        summary["realized_vol_7d"] = _realized_vol(daily_returns, window=7)

    if len(closes) >= 7:
        summary["return_7d_pct"] = round(((closes[-1] / closes[-7]) - 1) * 100, 6)
    if len(closes) >= 30:
        summary["return_30d_pct"] = round(((closes[-1] / closes[-30]) - 1) * 100, 6)
    if len(closes) >= 90:
        summary["return_90d_pct"] = round(((closes[-1] / closes[-90]) - 1) * 100, 6)
    if len(closes) >= 180:
        summary["return_180d_pct"] = round(((closes[-1] / closes[-180]) - 1) * 100, 6)

    if len(closes) >= 20:
        summary["sma_20"] = round(sum(closes[-20:]) / 20, 6)
        summary["price_vs_sma20_pct"] = round(((closes[-1] / summary["sma_20"]) - 1) * 100, 6)
    if len(closes) >= 40:
        summary["sma_40"] = round(sum(closes[-40:]) / 40, 6)
    if len(closes) >= 50:
        summary["sma_50"] = round(sum(closes[-50:]) / 50, 6)
        summary["price_vs_sma50_pct"] = round(((closes[-1] / summary["sma_50"]) - 1) * 100, 6)
    if len(closes) >= 200:
        summary["sma_200"] = round(sum(closes[-200:]) / 200, 6)
        summary["price_vs_sma200_pct"] = round(((closes[-1] / summary["sma_200"]) - 1) * 100, 6)
        summary["regime"] = "bull" if closes[-1] > summary["sma_200"] else "bear"

    if len(closes) >= 200:
        sma50 = sum(closes[-50:]) / 50
        sma200 = summary["sma_200"]
        prev_sma50 = sum(closes[-51:-1]) / 50
        prev_sma200 = sum(closes[-201:-1]) / 200
        if prev_sma50 <= prev_sma200 and sma50 > sma200:
            summary["ma_cross"] = "golden_cross"
        elif prev_sma50 >= prev_sma200 and sma50 < sma200:
            summary["ma_cross"] = "death_cross"
        else:
            summary["ma_cross"] = "none"
        summary["sma50_above_sma200"] = sma50 > sma200

    ema_12 = _ema(closes, 12)
    ema_26 = _ema(closes, 26)
    if ema_12 is not None and ema_26 is not None:
        macd_line = ema_12 - ema_26
        summary["macd_line"] = round(macd_line, 6)
        if len(closes) >= 35:
            macd_series = _macd_series(closes)
            if macd_series and len(macd_series) >= 9:
                signal_line = _ema_from_values(macd_series, 9)
                if signal_line is not None:
                    summary["macd_signal"] = round(signal_line, 6)
                    summary["macd_histogram"] = round(macd_series[-1] - signal_line, 6)

    if len(closes) >= 20:
        bb = _bollinger_bands(closes, period=20, num_std=2)
        summary["bb_upper"] = bb["upper"]
        summary["bb_lower"] = bb["lower"]
        summary["bb_pct_b"] = bb["pct_b"]
        summary["bb_bandwidth"] = bb["bandwidth"]

    if len(closes) >= 15:
        summary["rsi_14"] = _rsi(closes, period=14)

    highs = [float(row["high"]) for row in rows if row.get("high") is not None]
    lows = [float(row["low"]) for row in rows if row.get("low") is not None]
    if len(highs) >= 14 and len(lows) >= 14:
        summary["atr_14"] = _atr(highs, lows, closes, period=14)

    if volumes and len(volumes) >= 20:
        avg_vol_20 = sum(volumes[-20:]) / 20
        summary["volume_ratio"] = round(volumes[-1] / avg_vol_20, 4) if avg_vol_20 > 0 else None

    ref_time = as_of_utc or datetime.now(timezone.utc)
    summary["seasonality_month"] = ref_time.month
    summary["seasonality_weekday"] = ref_time.strftime("%A")
    summary["seasonality_bias"] = MONTH_SEASONALITY.get(ref_time.month, "neutral")

    asset_name = summary.get("asset", "")
    if isinstance(asset_name, str) and asset_name.upper() in ("BTC", "BITCOIN"):
        halving_info = _halving_cycle_position(ref_time)
        if halving_info:
            summary.update(halving_info)


def _filter_rows_up_to_as_of(
    rows: list[dict[str, Any]],
    *,
    as_of_utc: datetime | None,
) -> list[dict[str, Any]]:
    if as_of_utc is None:
        return rows
    cutoff = as_of_utc.date().isoformat()
    filtered = [
        row
        for row in rows
        if _row_date(row) is not None and _row_date(row) <= cutoff
    ]
    return filtered


def _row_date(row: dict[str, Any]) -> str | None:
    for key in ("date", "datetime", "timestamp"):
        value = row.get(key)
        if isinstance(value, str) and value:
            return value.split("T", 1)[0]
    return None


def _derive_cross_domain_features(summary: dict[str, Any]) -> None:
    market_cap = _estimated_market_cap(summary)
    tvl_total = _as_float(summary.get("defi_tvl_total"))
    if market_cap is not None:
        summary["estimated_market_cap_usd"] = round(market_cap, 2)
    if market_cap is not None and tvl_total > 0:
        summary["mc_tvl_ratio"] = round(market_cap / tvl_total, 4)


def _extract_defillama_features(
    raw_data: RawDataBundle,
    request: ResearchRequest,
    summary: dict[str, Any],
    notes: list[str],
) -> None:
    dl_result = raw_data.source_results.get("defillama")
    if not (dl_result and dl_result.status == "fetched" and dl_result.artifact_paths):
        if "defillama" in raw_data.source_results:
            notes.append("DefiLlama features pending because source data is unavailable.")
        return

    artifact_map = _build_artifact_map(dl_result.artifact_paths)

    protocols_path = artifact_map.get("protocols")
    if protocols_path and protocols_path.exists():
        _extract_protocol_features(protocols_path, request, summary, notes)

    yields_path = artifact_map.get("yields_pools")
    if yields_path and yields_path.exists():
        _extract_yield_features(yields_path, summary, notes)


def _extract_protocol_features(
    protocols_path: Path,
    request: ResearchRequest,
    summary: dict[str, Any],
    notes: list[str],
) -> None:
    protocols = json.loads(protocols_path.read_text(encoding="utf-8"))
    if not isinstance(protocols, list):
        notes.append("DefiLlama protocols data has unexpected format.")
        return

    asset_lower = request.asset.lower()
    chain_protocols = [
        p for p in protocols
        if _matches_asset(p, asset_lower)
    ]

    total_tvl = sum(float(p.get("tvl", 0) or 0) for p in protocols)
    summary["defi_tvl_total"] = round(total_tvl, 2)

    if chain_protocols:
        chain_tvl = sum(float(p.get("tvl", 0) or 0) for p in chain_protocols)
        summary["defi_tvl_asset_chain"] = round(chain_tvl, 2)
        summary["defi_tvl_asset_share_pct"] = round((chain_tvl / total_tvl) * 100, 4) if total_tvl > 0 else 0

        changes_1d = [float(p["change_1d"]) for p in chain_protocols if p.get("change_1d") is not None]
        changes_7d = [float(p["change_7d"]) for p in chain_protocols if p.get("change_7d") is not None]

        if changes_1d:
            summary["defi_tvl_change_1d_pct"] = round(sum(changes_1d) / len(changes_1d), 4)
        if changes_7d:
            summary["defi_tvl_change_7d_pct"] = round(sum(changes_7d) / len(changes_7d), 4)

        top_protocols = sorted(chain_protocols, key=lambda p: float(p.get("tvl", 0) or 0), reverse=True)[:5]
        summary["defi_top_protocols"] = [
            {
                "name": p.get("name", ""),
                "tvl": round(float(p.get("tvl", 0) or 0), 2),
                "change_1d": p.get("change_1d"),
                "change_7d": p.get("change_7d"),
                "category": p.get("category", ""),
            }
            for p in top_protocols
        ]
        notes.append(f"Extracted DeFi features from {len(chain_protocols)} {request.asset}-chain protocols.")
    else:
        notes.append(f"No DefiLlama protocols found for chain matching '{request.asset}'.")


def _extract_yield_features(
    yields_path: Path,
    summary: dict[str, Any],
    notes: list[str],
) -> None:
    yields_data = json.loads(yields_path.read_text(encoding="utf-8"))
    pools: list[dict[str, Any]] = yields_data.get("data", []) if isinstance(yields_data, dict) else yields_data
    if not isinstance(pools, list) or not pools:
        notes.append("DefiLlama yields data empty or unexpected format.")
        return

    stablecoin_pools = [p for p in pools if p.get("stablecoin") is True and p.get("apy") is not None]

    if stablecoin_pools:
        top_stable = sorted(stablecoin_pools, key=lambda p: float(p.get("tvlUsd", 0) or 0), reverse=True)[:20]
        apys = [float(p["apy"]) for p in top_stable]
        tvl_weighted_apy = sum(
            float(p["apy"]) * float(p.get("tvlUsd", 0) or 0) for p in top_stable
        )
        total_tvl = sum(float(p.get("tvlUsd", 0) or 0) for p in top_stable)

        summary["defi_stablecoin_median_apy"] = round(sorted(apys)[len(apys) // 2], 4)
        summary["defi_stablecoin_tvl_weighted_apy"] = round(tvl_weighted_apy / total_tvl, 4) if total_tvl > 0 else None

        apy_changes_7d = [float(p["apyPct7D"]) for p in top_stable if p.get("apyPct7D") is not None]
        if apy_changes_7d:
            summary["defi_stablecoin_apy_change_7d"] = round(sum(apy_changes_7d) / len(apy_changes_7d), 4)

        notes.append(f"Extracted yield features from {len(stablecoin_pools)} stablecoin pools (top 20 by TVL).")
    else:
        notes.append("No stablecoin pools found in DefiLlama yields data.")


def _matches_asset(protocol: dict[str, Any], asset_lower: str) -> bool:
    chains = protocol.get("chains", [])
    if isinstance(chains, list):
        for chain in chains:
            if isinstance(chain, str) and chain.lower() == asset_lower:
                return True
    chain = protocol.get("chain", "")
    if isinstance(chain, str) and chain.lower() == asset_lower:
        return True
    return False


def _build_artifact_map(artifact_paths: list[Path]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for path in artifact_paths:
        stem = path.stem
        result[stem] = path
    return result


def _last_series_row(payload: Any) -> dict[str, Any] | None:
    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, list) and data:
            last = data[-1]
            if isinstance(last, dict):
                return last
    if isinstance(payload, list) and payload:
        last = payload[-1]
        if isinstance(last, dict):
            return last
    return None


def _extract_series_value(row: dict[str, Any], candidate_keys: list[str]) -> float | None:
    for key in candidate_keys:
        value = row.get(key)
        if isinstance(value, (int, float)):
            return float(value)
    return None


def _daily_returns(closes: list[float]) -> list[float]:
    return [
        (closes[i] / closes[i - 1]) - 1
        for i in range(1, len(closes))
    ]


def _realized_vol(daily_returns: list[float], *, window: int) -> float | None:
    tail = daily_returns[-window:] if len(daily_returns) >= window else daily_returns
    if len(tail) < 2:
        return None
    mean = sum(tail) / len(tail)
    variance = sum((r - mean) ** 2 for r in tail) / (len(tail) - 1)
    annualized = math.sqrt(variance) * math.sqrt(365) * 100
    return round(annualized, 4)


def _rsi(closes: list[float], *, period: int) -> float:
    changes = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    recent = changes[-(period):]
    gains = [c for c in recent if c > 0]
    losses = [-c for c in recent if c < 0]
    avg_gain = sum(gains) / period if gains else 0
    avg_loss = sum(losses) / period if losses else 0
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 4)


def _atr(highs: list[float], lows: list[float], closes: list[float], *, period: int) -> float:
    true_ranges: list[float] = []
    min_len = min(len(highs), len(lows), len(closes))
    for i in range(1, min_len):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        true_ranges.append(tr)
    recent = true_ranges[-period:]
    return round(sum(recent) / len(recent), 6) if recent else 0.0




def _estimated_market_cap(summary: dict[str, Any]) -> float | None:
    latest_close = _as_float(summary.get("latest_close"))
    if latest_close <= 0:
        return None
    asset = str(summary.get("asset", "")).upper()
    circulating_supply = {
        "BTC": 19_800_000,
        "ETH": 120_000_000,
        "SOL": 510_000_000,
    }.get(asset)
    if circulating_supply is None:
        return None
    return latest_close * circulating_supply


def _as_float(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0


def _ema(values: list[float], period: int) -> float | None:
    if len(values) < period:
        return None
    return _ema_from_values(values, period)


def _ema_from_values(values: list[float], period: int) -> float | None:
    if len(values) < period:
        return None
    k = 2 / (period + 1)
    ema = sum(values[:period]) / period
    for v in values[period:]:
        ema = v * k + ema * (1 - k)
    return ema


def _macd_series(closes: list[float]) -> list[float]:
    if len(closes) < 26:
        return []
    result: list[float] = []
    k12 = 2 / 13
    k26 = 2 / 27
    ema12 = sum(closes[:12]) / 12
    ema26 = sum(closes[:26]) / 26
    for i in range(26, len(closes)):
        ema12 = closes[i] * k12 + ema12 * (1 - k12)
        ema26 = closes[i] * k26 + ema26 * (1 - k26)
        result.append(ema12 - ema26)
    return result


def _bollinger_bands(
    closes: list[float], *, period: int, num_std: int,
) -> dict[str, float]:
    window = closes[-period:]
    mean = sum(window) / len(window)
    std = math.sqrt(sum((x - mean) ** 2 for x in window) / len(window))
    upper = round(mean + num_std * std, 6)
    lower = round(mean - num_std * std, 6)
    band_range = upper - lower
    pct_b = round((closes[-1] - lower) / band_range, 4) if band_range > 0 else 0.5
    bandwidth = round(band_range / mean * 100, 4) if mean > 0 else 0.0
    return {"upper": upper, "lower": lower, "pct_b": pct_b, "bandwidth": bandwidth}


def _halving_cycle_position(ref_time: datetime) -> dict[str, Any] | None:
    past_halvings = [h for h in BTC_HALVING_DATES if h <= ref_time]
    if not past_halvings:
        return None
    last_halving = past_halvings[-1]
    days_since = (ref_time - last_halving).days
    cycle_number = len(past_halvings)
    in_bullish_window = 120 <= days_since <= 550
    return {
        "halving_cycle_number": cycle_number,
        "days_since_halving": days_since,
        "halving_cycle_day": days_since,
        "halving_date": last_halving.date().isoformat(),
        "in_post_halving_bullish_window": in_bullish_window,
        "halving_cycle_window": "post_halving_sweet_spot" if in_bullish_window else "other",
    }


def _extract_coinglass_features(
    raw_data: RawDataBundle,
    summary: dict[str, Any],
    notes: list[str],
) -> None:
    cg_result = raw_data.source_results.get("coinglass")
    if not (cg_result and cg_result.status == "fetched" and cg_result.artifact_paths):
        if cg_result and cg_result.status != "disabled":
            notes.append("CoinGlass features pending because source data is unavailable.")
        return

    artifact_map = _build_artifact_map(cg_result.artifact_paths)

    oi_path = artifact_map.get("open_interest_history")
    if oi_path and oi_path.exists():
        _extract_oi_features(oi_path, summary, notes)

    funding_path = artifact_map.get("funding_rate_history")
    if funding_path and funding_path.exists():
        _extract_funding_features(funding_path, summary, notes)

    liq_path = artifact_map.get("liquidation_history")
    if liq_path and liq_path.exists():
        _extract_liquidation_features(liq_path, summary, notes)


def _extract_oi_features(
    oi_path: Path,
    summary: dict[str, Any],
    notes: list[str],
) -> None:
    try:
        raw = json.loads(oi_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        notes.append("Failed to parse CoinGlass OI data.")
        return

    data_list = raw.get("data", []) if isinstance(raw, dict) else raw
    if not isinstance(data_list, list) or not data_list:
        notes.append("CoinGlass OI data empty.")
        return

    oi_values = [float(d["openInterest"]) for d in data_list if d.get("openInterest") is not None]
    if not oi_values:
        oi_values = [
            float(d["c"]) for d in data_list
            if d.get("c") is not None
        ]
    if not oi_values:
        return

    summary["deriv_oi_latest"] = round(oi_values[-1], 2)
    summary["derivatives_open_interest_latest"] = round(oi_values[-1], 2)
    latest_row = data_list[-1] if data_list else {}
    row_open = float(latest_row["o"]) if isinstance(latest_row, dict) and latest_row.get("o") is not None else None
    row_close = float(latest_row["c"]) if isinstance(latest_row, dict) and latest_row.get("c") is not None else None
    if row_open not in (None, 0) and row_close is not None:
        row_change = round(((row_close / row_open) - 1) * 100, 4)
        summary["derivatives_open_interest_change_pct"] = row_change
    if len(oi_values) >= 2:
        summary["deriv_oi_change_1d_pct"] = round(((oi_values[-1] / oi_values[-2]) - 1) * 100, 4)
        summary["derivatives_open_interest_change_pct"] = round(((oi_values[-1] / oi_values[-2]) - 1) * 100, 4)
    if len(oi_values) >= 7:
        summary["deriv_oi_change_7d_pct"] = round(((oi_values[-1] / oi_values[-7]) - 1) * 100, 4)
    if len(oi_values) >= 30:
        summary["deriv_oi_change_30d_pct"] = round(((oi_values[-1] / oi_values[-30]) - 1) * 100, 4)
        summary["deriv_oi_at_30d_high"] = oi_values[-1] >= max(oi_values[-30:]) * 0.98

    notes.append(f"Extracted OI features from {len(oi_values)} CoinGlass data points.")


def _extract_funding_features(
    funding_path: Path,
    summary: dict[str, Any],
    notes: list[str],
) -> None:
    try:
        raw = json.loads(funding_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        notes.append("Failed to parse CoinGlass funding data.")
        return

    data_list = raw.get("data", []) if isinstance(raw, dict) else raw
    if not isinstance(data_list, list) or not data_list:
        notes.append("CoinGlass funding data empty.")
        return

    rates = [float(d["fundingRate"]) for d in data_list if d.get("fundingRate") is not None]
    if not rates:
        rates = [float(d["c"]) for d in data_list if d.get("c") is not None]
    if not rates:
        return

    summary["deriv_funding_latest"] = round(rates[-1], 6)
    summary["derivatives_funding_rate_latest"] = round(rates[-1], 6)

    if len(rates) >= 21:
        ma_7d = sum(rates[-21:]) / 21
        summary["deriv_funding_7d_ma"] = round(ma_7d, 6)

    if len(rates) >= 90:
        window = rates[-90:]
        mean = sum(window) / len(window)
        std = math.sqrt(sum((r - mean) ** 2 for r in window) / (len(window) - 1)) if len(window) > 1 else 0
        z_score = (rates[-1] - mean) / std if std > 0 else 0
        summary["deriv_funding_zscore_30d"] = round(z_score, 4)

        if z_score > 2.0:
            summary["deriv_funding_crowding"] = "extreme_long"
        elif z_score > 1.0:
            summary["deriv_funding_crowding"] = "long_bias"
        elif z_score < -2.0:
            summary["deriv_funding_crowding"] = "extreme_short"
        elif z_score < -1.0:
            summary["deriv_funding_crowding"] = "short_bias"
        else:
            summary["deriv_funding_crowding"] = "neutral"

    notes.append(f"Extracted funding rate features from {len(rates)} CoinGlass data points.")


def _extract_liquidation_features(
    liq_path: Path,
    summary: dict[str, Any],
    notes: list[str],
) -> None:
    try:
        raw = json.loads(liq_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        notes.append("Failed to parse CoinGlass liquidation data.")
        return

    data_list = raw.get("data", []) if isinstance(raw, dict) else raw
    if not isinstance(data_list, list) or not data_list:
        notes.append("CoinGlass liquidation data empty.")
        return

    long_liqs = [float(d.get("longLiquidationUsd", 0) or 0) for d in data_list]
    short_liqs = [float(d.get("shortLiquidationUsd", 0) or 0) for d in data_list]

    if not long_liqs:
        return

    latest_long = long_liqs[-1]
    latest_short = short_liqs[-1] if short_liqs else 0
    total_24h = latest_long + latest_short

    summary["deriv_liq_24h_total"] = round(total_24h, 2)
    summary["deriv_liq_24h_long"] = round(latest_long, 2)
    summary["deriv_liq_24h_short"] = round(latest_short, 2)
    summary["derivatives_long_liquidation_usd_24h"] = round(latest_long, 2)
    summary["derivatives_short_liquidation_usd_24h"] = round(latest_short, 2)
    summary["derivatives_total_liquidation_usd_24h"] = round(total_24h, 2)
    summary["deriv_liq_long_short_ratio"] = round(latest_long / latest_short, 4) if latest_short > 0 else None

    if total_24h < 100_000_000:
        summary["deriv_liq_severity"] = "normal"
    elif total_24h < 300_000_000:
        summary["deriv_liq_severity"] = "elevated"
    elif total_24h < 500_000_000:
        summary["deriv_liq_severity"] = "significant"
    elif total_24h < 1_000_000_000:
        summary["deriv_liq_severity"] = "major"
    else:
        summary["deriv_liq_severity"] = "severe"


def _extract_binance_features(
    raw_data: RawDataBundle,
    summary: dict[str, Any],
    notes: list[str],
) -> None:
    """Extract funding rate and OI from Binance public API data (no key required)."""
    binance_result = raw_data.source_results.get("binance")
    if not (binance_result and binance_result.status == "fetched" and binance_result.artifact_paths):
        return

    artifact_map = _build_artifact_map(binance_result.artifact_paths)

    # Funding rate
    funding_path = artifact_map.get("funding_rate")
    if funding_path and funding_path.exists():
        try:
            data_list = json.loads(funding_path.read_text(encoding="utf-8"))
            if isinstance(data_list, list) and data_list:
                rates = [float(d["fundingRate"]) for d in data_list if d.get("fundingRate") is not None]
                if rates:
                    summary["deriv_funding_latest"] = round(rates[-1], 6)
                    summary["derivatives_funding_rate_latest"] = round(rates[-1], 6)
                    if len(rates) >= 21:  # 7 days * 3 periods/day
                        summary["deriv_funding_7d_ma"] = round(sum(rates[-21:]) / 21, 6)
                    if len(rates) >= 30:
                        mean = sum(rates[-90:]) / len(rates[-90:]) if len(rates) >= 90 else sum(rates) / len(rates)
                        std = (sum((r - mean) ** 2 for r in rates[-90:]) / len(rates[-90:])) ** 0.5 if len(rates) >= 90 else None
                        if std and std > 0:
                            z = (rates[-1] - mean) / std
                            summary["deriv_funding_zscore_30d"] = round(z, 4)
                            if z > 2:
                                summary["deriv_funding_crowding"] = "extreme_long"
                            elif z > 1:
                                summary["deriv_funding_crowding"] = "long_bias"
                            elif z < -2:
                                summary["deriv_funding_crowding"] = "extreme_short"
                            elif z < -1:
                                summary["deriv_funding_crowding"] = "short_bias"
                            else:
                                summary["deriv_funding_crowding"] = "neutral"
                    notes.append(f"Extracted funding rate features from {len(rates)} Binance data points.")
        except (json.JSONDecodeError, KeyError, ValueError, OSError):
            notes.append("Failed to parse Binance funding rate data.")

    # Open interest
    oi_path = artifact_map.get("open_interest_hist")
    if oi_path and oi_path.exists():
        try:
            data_list = json.loads(oi_path.read_text(encoding="utf-8"))
            if isinstance(data_list, list) and data_list:
                oi_values = [float(d["sumOpenInterest"]) for d in data_list if d.get("sumOpenInterest") is not None]
                if oi_values:
                    summary["deriv_oi_latest"] = round(oi_values[-1], 2)
                    summary["derivatives_open_interest_latest"] = round(oi_values[-1], 2)
                    if len(oi_values) >= 2:
                        summary["deriv_oi_change_1d_pct"] = round(((oi_values[-1] / oi_values[-2]) - 1) * 100, 4)
                        summary["derivatives_open_interest_change_pct"] = summary["deriv_oi_change_1d_pct"]
                    if len(oi_values) >= 7:
                        summary["deriv_oi_change_7d_pct"] = round(((oi_values[-1] / oi_values[-7]) - 1) * 100, 4)
                    if len(oi_values) >= 30:
                        summary["deriv_oi_at_30d_high"] = oi_values[-1] >= max(oi_values[-30:]) * 0.98
                    notes.append(f"Extracted OI features from {len(oi_values)} Binance data points.")
        except (json.JSONDecodeError, KeyError, ValueError, OSError):
            notes.append("Failed to parse Binance OI data.")

    notes.append(f"Extracted liquidation features from {len(data_list)} CoinGlass data points.")
