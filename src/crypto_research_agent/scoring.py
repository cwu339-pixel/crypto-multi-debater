from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoreInputs:
    momentum: float
    liquidity: float
    derivatives: float
    defi: float
    onchain: float
    sentiment: float
    data_quality_penalty: float = 0.0


@dataclass(frozen=True)
class ScoreResult:
    final_score: int
    confidence: str


WEIGHTS = {
    "momentum": 0.20,
    "liquidity": 0.10,
    "derivatives": 0.20,
    "defi": 0.20,
    "onchain": 0.15,
    "sentiment": 0.10,
}


def compute_weighted_score(inputs: ScoreInputs) -> ScoreResult:
    weighted_sum = (
        WEIGHTS["momentum"] * inputs.momentum
        + WEIGHTS["liquidity"] * inputs.liquidity
        + WEIGHTS["derivatives"] * inputs.derivatives
        + WEIGHTS["defi"] * inputs.defi
        + WEIGHTS["onchain"] * inputs.onchain
        + WEIGHTS["sentiment"] * inputs.sentiment
    )
    final_score = round(max(0.0, min(100.0, weighted_sum + inputs.data_quality_penalty)))
    confidence = _confidence_from_score(final_score)
    return ScoreResult(final_score=final_score, confidence=confidence)


def build_scorecard(
    *,
    feature_summary: dict[str, object],
    coverage_gaps: list[str],
    evidence_summary: dict[str, object],
) -> dict[str, object]:
    core_gaps, supplementary_gaps = _classify_gaps(coverage_gaps)
    inputs = ScoreInputs(
        momentum=_score_momentum(feature_summary),
        liquidity=_score_liquidity(feature_summary),
        derivatives=_score_derivatives(coverage_gaps, feature_summary),
        defi=_score_defi(coverage_gaps, feature_summary),
        onchain=_score_onchain(feature_summary),
        sentiment=_score_sentiment(evidence_summary),
        data_quality_penalty=_score_data_quality_penalty(coverage_gaps, evidence_summary),
    )
    result = compute_weighted_score(inputs)
    confidence = _confidence_from_market_context(feature_summary=feature_summary, core_gaps=core_gaps)
    return {
        "inputs": {
            "momentum": round(inputs.momentum, 2),
            "liquidity": round(inputs.liquidity, 2),
            "derivatives": round(inputs.derivatives, 2),
            "defi": round(inputs.defi, 2),
            "onchain": round(inputs.onchain, 2),
            "sentiment": round(inputs.sentiment, 2),
            "data_quality_penalty": round(inputs.data_quality_penalty, 2),
        },
        "action_score": result.final_score,
        "final_score": result.final_score,
        "confidence": confidence,
        "score_decision": _decision_from_score(result.final_score),
        "data_quality": {
            "core_complete": not core_gaps,
            "supplementary_complete": not supplementary_gaps,
            "core_gaps": core_gaps,
            "supplementary_gaps": supplementary_gaps,
            "penalty": round(inputs.data_quality_penalty, 2),
        },
    }


def _confidence_from_score(score: int) -> str:
    if score >= 70:
        return "high"
    if score >= 50:
        return "medium"
    return "low"


def _decision_from_score(score: int) -> str:
    if score >= 55:
        return "hold"
    return "avoid"


def _score_momentum(feature_summary: dict[str, object]) -> float:
    total_return = _as_float(feature_summary.get("return_total_pct"))
    one_day_return = _as_float(feature_summary.get("return_1d_pct"))
    return_30d = _as_float(feature_summary.get("return_30d_pct"))
    price_vs_sma200 = _as_float(feature_summary.get("price_vs_sma200_pct"))
    rsi_14 = _as_float(feature_summary.get("rsi_14"))
    score = 50.0 + (0.5 * total_return) + (1.5 * one_day_return) + (0.4 * return_30d) + (0.3 * price_vs_sma200)
    if 45 <= rsi_14 <= 70:
        score += 5.0
    elif rsi_14 > 80 or rsi_14 < 25:
        score -= 5.0
    halving_window = str(feature_summary.get("halving_cycle_window", ""))
    if halving_window == "post_halving_sweet_spot":
        score += 5.0
    return _clamp(score)


def _score_liquidity(feature_summary: dict[str, object]) -> float:
    avg_volume = _as_float(feature_summary.get("avg_volume"))
    if avg_volume >= 1000:
        return 80.0
    if avg_volume > 0:
        return 65.0
    return 35.0


def _score_derivatives(coverage_gaps: list[str], feature_summary: dict[str, object]) -> float:
    funding_rate = _as_float(feature_summary.get("derivatives_funding_rate_latest"))
    oi_change = _as_float(feature_summary.get("derivatives_open_interest_change_pct"))
    liquidation_total = _as_float(feature_summary.get("derivatives_total_liquidation_usd_24h"))
    has_basic_derivatives = any(
        value != 0.0 for value in (funding_rate, oi_change, liquidation_total)
    )
    if not has_basic_derivatives:
        return 50.0 if any(_is_effective_gap(gap, "coinglass:") for gap in coverage_gaps) else 60.0
    score = 60.0
    if 0 < funding_rate <= 0.01:
        score += 8.0
    elif -0.01 <= funding_rate < 0:
        score -= 4.0
    elif funding_rate > 0.03:
        score -= 8.0
    if 0 < oi_change <= 5.0:
        score += 4.0
    elif oi_change < 0:
        score -= 4.0
    elif oi_change > 10.0:
        score -= 6.0
    if liquidation_total >= 300_000_000:
        score -= 6.0
    elif 0 < liquidation_total < 100_000_000:
        score += 2.0
    return _clamp(score)


def _score_defi(coverage_gaps: list[str], feature_summary: dict[str, object]) -> float:
    tvl_change_7d = _as_float(feature_summary.get("defi_tvl_change_7d_pct"))
    mc_tvl_ratio = _as_float(feature_summary.get("mc_tvl_ratio"))
    stablecoin_apy_change_7d = _as_float(feature_summary.get("defi_stablecoin_apy_change_7d"))
    has_defi_inputs = any(value != 0.0 for value in (tvl_change_7d, mc_tvl_ratio, stablecoin_apy_change_7d))
    if not has_defi_inputs:
        return 50.0 if any(_is_effective_gap(gap, "defillama:") for gap in coverage_gaps) else 60.0
    score = 60.0
    score += min(max(tvl_change_7d, -10.0), 10.0)
    if 0 < mc_tvl_ratio <= 1.0:
        score += 8.0
    elif mc_tvl_ratio > 2.5:
        score -= 8.0
    if stablecoin_apy_change_7d > 0:
        score += 4.0
    return _clamp(score)


def _score_onchain(feature_summary: dict[str, object]) -> float:
    feature_status = str(feature_summary.get("feature_status", "")).lower()
    if feature_status != "complete":
        return 45.0
    score = 55.0
    regime = str(feature_summary.get("regime", ""))
    price_vs_sma200 = _as_float(feature_summary.get("price_vs_sma200_pct"))
    if regime == "bull":
        score += 8.0
    elif regime == "bear":
        score -= 6.0
    score += max(min(price_vs_sma200 / 2.0, 8.0), -8.0)
    return _clamp(score)


def _score_sentiment(evidence_summary: dict[str, object]) -> float:
    evidence_status = str(evidence_summary.get("evidence_status", "")).lower()
    if evidence_status == "complete":
        return 65.0
    if evidence_status == "stub":
        return 50.0
    return 45.0


def _score_data_quality_penalty(coverage_gaps: list[str], evidence_summary: dict[str, object]) -> float:
    core_gaps, supplementary_gaps = _classify_gaps(coverage_gaps)
    penalty = -10.0 * len(core_gaps)
    if supplementary_gaps:
        penalty -= 5.0
    if str(evidence_summary.get("evidence_status", "")).lower() == "stub":
        penalty -= 0.0
    return penalty


def _confidence_from_market_context(
    *,
    feature_summary: dict[str, object],
    core_gaps: list[str],
) -> str:
    if core_gaps or not _core_data_complete(feature_summary):
        return "low"

    signals = [
        _trend_signal(feature_summary),
        _momentum_signal(feature_summary),
        _derivatives_signal(feature_summary),
    ]
    bullish = sum(1 for signal in signals if signal == "bull")
    bearish = sum(1 for signal in signals if signal == "bear")

    if bullish and bearish:
        return "low" if abs(bullish - bearish) <= 1 else "medium"
    if not bullish and not bearish:
        return "medium"
    if max(bullish, bearish) >= 3:
        return "high"
    return "medium"


def _core_data_complete(feature_summary: dict[str, object]) -> bool:
    if str(feature_summary.get("feature_status", "")).lower() != "complete":
        return False
    return _as_float(feature_summary.get("latest_close")) > 0 and _as_float(feature_summary.get("avg_volume")) > 0


def _trend_signal(feature_summary: dict[str, object]) -> str | None:
    regime = str(feature_summary.get("regime", "")).lower()
    price_vs_sma200 = _as_float(feature_summary.get("price_vs_sma200_pct"))
    if regime == "bear" or price_vs_sma200 <= -10.0:
        return "bear"
    if regime == "bull" or price_vs_sma200 >= 10.0:
        return "bull"
    return None


def _momentum_signal(feature_summary: dict[str, object]) -> str | None:
    total_return = _as_float(feature_summary.get("return_total_pct"))
    one_day_return = _as_float(feature_summary.get("return_1d_pct"))
    rsi_14 = _as_float(feature_summary.get("rsi_14"))
    if total_return <= -10.0 or one_day_return <= -2.0 or (0 < rsi_14 < 45):
        return "bear"
    if total_return >= 10.0 or one_day_return >= 2.0 or rsi_14 >= 55.0:
        return "bull"
    return None


def _derivatives_signal(feature_summary: dict[str, object]) -> str | None:
    funding_rate = _as_float(feature_summary.get("derivatives_funding_rate_latest"))
    oi_change = _as_float(feature_summary.get("derivatives_open_interest_change_pct"))
    if funding_rate == 0.0 and oi_change == 0.0:
        return None
    if funding_rate < 0 or oi_change < 0:
        return "bear"
    if 0 < funding_rate <= 0.01 and 0 < oi_change <= 5.0:
        return "bull"
    return None


def _classify_gaps(coverage_gaps: list[str]) -> tuple[list[str], list[str]]:
    core_prefixes = ("openbb", "binance")
    core_keywords = ("price", "ohlcv", "candle", "volume")
    core: list[str] = []
    supplementary: list[str] = []
    for gap in coverage_gaps:
        if not _is_effective_gap(gap):
            continue
        label = gap.split(":")[0].lower()
        if label.startswith(core_prefixes) or any(keyword in label for keyword in core_keywords):
            core.append(gap)
        else:
            supplementary.append(gap)
    return core, supplementary


def _is_effective_gap(gap: str, prefix: str | None = None) -> bool:
    if prefix is not None and not gap.startswith(prefix):
        return False
    return not gap.endswith(":historical_unavailable")


def _clamp(value: float) -> float:
    return max(0.0, min(100.0, value))


def _as_float(value: object) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0
