from __future__ import annotations

import json
import time
from dataclasses import is_dataclass, replace
from pathlib import Path

from crypto_research_agent.agents.provider import AnalysisProvider, DeterministicAnalysisProvider
from crypto_research_agent.scoring import build_scorecard
from crypto_research_agent.schemas import EvidencePack, FeatureBundle, ResearchRequest, RoleAnalysisBundle


ROLE_ORDER = [
    "technical_analyst",
    "defi_fundamentals_analyst",
    "derivatives_analyst",
    "news_analyst",
    "bull_researcher",
    "bear_researcher",
    "risk_manager",
    "final_arbiter",
]
FIRST_ORDER_ROLES = [
    "technical_analyst",
    "defi_fundamentals_analyst",
    "derivatives_analyst",
    "news_analyst",
]
SECOND_ORDER_ROLES = [
    "bull_researcher",
    "bear_researcher",
    "risk_manager",
    "final_arbiter",
]
NARRATIVE_FIRST_ROLES = set(FIRST_ORDER_ROLES + ["bull_researcher", "bear_researcher", "risk_manager", "final_arbiter"])
MAX_INVEST_DEBATE_ROUNDS = 1
RISK_DEBATE_ORDER = ("aggressive", "conservative", "neutral")
ROLE_TIMEOUT_OVERRIDES = {
    "derivatives_analyst": 45,
    "news_analyst": 45,
    "bull_researcher": 45,
    "bear_researcher": 45,
    "risk_manager": 60,
    "final_arbiter": 60,
    "aggressive_risk_analyst": 30,
    "conservative_risk_analyst": 30,
    "neutral_risk_analyst": 30,
}
ROLE_RETRY_OVERRIDES = {
    "bull_researcher": 1,
    "bear_researcher": 1,
    "news_analyst": 1,
    "risk_manager": 1,
    "final_arbiter": 1,
}

ROLE_TITLES = {
    "technical_analyst": "Technical Analyst",
    "defi_fundamentals_analyst": "DeFi Fundamentals Analyst",
    "derivatives_analyst": "Derivatives Analyst",
    "news_analyst": "News Analyst",
    "bull_researcher": "Bull Researcher",
    "bear_researcher": "Bear Researcher",
    "risk_manager": "Risk Manager",
    "final_arbiter": "Final Arbiter",
}

SYSTEM_FIELDS = {
    "title",
    "summary",
    "provider",
    "analysis_mode",
    "prompt_path",
    "prompt_text",
    "validation_error",
    "decision_label",
    "risk_bias",
    "rationale",
    "signal",
    "confidence",
}


def run_multi_role_analysis(
    *,
    request: ResearchRequest,
    features: FeatureBundle,
    evidence: EvidencePack,
    output_root: Path,
    provider: AnalysisProvider | None = None,
) -> RoleAnalysisBundle:
    agents_dir = Path(output_root) / "runs" / request.run_id / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    call_log_path = agents_dir / "call_log.jsonl"
    call_log_path.unlink(missing_ok=True)

    role_memos = _build_role_memos(
        request=request,
        features=features,
        evidence=evidence,
        provider=provider or DeterministicAnalysisProvider(),
        call_log_path=call_log_path,
    )
    markdown_paths: dict[str, Path] = {}
    json_paths: dict[str, Path] = {}

    for role in ROLE_ORDER:
        markdown_path = agents_dir / f"{role}.md"
        json_path = agents_dir / f"{role}.json"
        markdown_path.write_text(_render_role_markdown(role, role_memos[role]), encoding="utf-8")
        json_path.write_text(json.dumps(role_memos[role], indent=2), encoding="utf-8")
        markdown_paths[role] = markdown_path
        json_paths[role] = json_path

    index_path = agents_dir / "index.json"
    index_path.write_text(
        json.dumps(
            {
                "run_id": request.run_id,
                "asset": request.asset,
                "roles": {
                    role: {
                        "title": ROLE_TITLES[role],
                        "markdown_path": str(markdown_paths[role]),
                        "json_path": str(json_paths[role]),
                    }
                    for role in ROLE_ORDER
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    return RoleAnalysisBundle(
        run_id=request.run_id,
        role_memos=role_memos,
        markdown_paths=markdown_paths,
        json_paths=json_paths,
        index_path=index_path,
    )


def _build_role_memos(
    *,
    request: ResearchRequest,
    features: FeatureBundle,
    evidence: EvidencePack,
    provider: AnalysisProvider,
    call_log_path: Path,
) -> dict[str, dict[str, object]]:
    latest_close = features.summary.get("latest_close")
    one_day_return = _as_float(features.summary.get("return_1d_pct"))
    total_return = _as_float(features.summary.get("return_total_pct"))
    avg_volume = features.summary.get("avg_volume")
    evidence_status = evidence.summary.get("evidence_status", "unknown")
    evidence_source = evidence.summary.get("source", "unknown")
    coverage_gaps = list(features.coverage_gaps)
    scorecard = build_scorecard(
        feature_summary=features.summary,
        coverage_gaps=coverage_gaps,
        evidence_summary=evidence.summary,
    )

    technical_signal = "bullish" if total_return > 0 else "cautious"
    technical_confidence = "medium" if one_day_return >= 0 else "low"
    derivatives_signal = "insufficient_data" if coverage_gaps else "neutral"
    fundamentals_signal = "coverage_gap" if coverage_gaps else "stable"
    news_signal = "monitor" if evidence_status == "stub" else "contextualized"
    bull_thesis = "Momentum remains constructive, but needs confirmation."
    bear_thesis = "Coverage gaps and event uncertainty limit conviction."
    risk_bias = "elevated" if coverage_gaps or scorecard["final_score"] < 50 or one_day_return >= 4.0 else "moderate"
    final_decision = str(scorecard["score_decision"])
    regime = _technical_regime(features.summary)
    price_vs_sma200 = features.summary.get("price_vs_sma200_pct")
    mc_tvl_ratio = features.summary.get("mc_tvl_ratio")
    funding_rate = features.summary.get("derivatives_funding_rate_latest")
    oi_change = features.summary.get("derivatives_open_interest_change_pct")
    total_liquidation = features.summary.get("derivatives_total_liquidation_usd_24h")

    prompts_dir = Path(__file__).resolve().parent / "prompts"
    base_memos = {
        "technical_analyst": {
            "role": "technical_analyst",
            "title": ROLE_TITLES["technical_analyst"],
            "regime": _technical_regime(features.summary),
            "signals": [
                {
                    "name": "rsi_14",
                    "value": features.summary.get("rsi_14"),
                    "interpretation": "Momentum is constructive." if one_day_return >= 0 else "Momentum remains weak.",
                    "bull_bear": "bull" if one_day_return >= 0 else "bear",
                    "confidence": technical_confidence,
                },
                {
                    "name": "price_vs_sma20_pct",
                    "value": features.summary.get("price_vs_sma20_pct"),
                    "interpretation": "Price is above short-term trend." if _as_float(features.summary.get("price_vs_sma20_pct")) >= 0 else "Price is below short-term trend.",
                    "bull_bear": "bull" if _as_float(features.summary.get("price_vs_sma20_pct")) >= 0 else "bear",
                    "confidence": technical_confidence,
                },
            ],
            "levels": {
                "support": [latest_close * 0.97] if isinstance(latest_close, (int, float)) else [],
                "resistance": [latest_close * 1.03] if isinstance(latest_close, (int, float)) else [],
                "invalidations": [
                    "Loss of short-term momentum below the recent support zone.",
                ],
            },
            "setup": {
                "thesis": (
                    f"{request.asset} screens as {regime}: spot is trading at {latest_close}, "
                    f"roughly {price_vs_sma200}% vs the 200-day trend, with RSI {features.summary.get('rsi_14')} "
                    f"and a {one_day_return:.2f}% 1-day move. The tape looks tradable, but this is still a "
                    "fragile short-horizon setup rather than a clean trend-confirmation regime."
                ),
                "what_would_change_my_mind": [
                    "A decisive break below support with expanding realized volatility.",
                    "Volume fading while price fails to hold above the 20-day trend.",
                ],
            },
            "risks": [
                {
                    "risk": "Coverage gaps reduce regime confidence.",
                    "mitigation": "Treat technical read as provisional until derivatives context is available.",
                }
            ],
            "uncertainties": coverage_gaps or ["Higher-timeframe trend context is incomplete."],
            "signal": technical_signal,
            "confidence": technical_confidence,
            "summary": (
                f"{request.asset} still looks {regime}: momentum has improved, but spot remains "
                f"{price_vs_sma200}% away from the 200-day trend and needs follow-through above nearby resistance."
            ),
        },
        "defi_fundamentals_analyst": {
            "role": "defi_fundamentals_analyst",
            "title": ROLE_TITLES["defi_fundamentals_analyst"],
            "data_coverage": {
                "available": _available_feature_keys(
                    features.summary,
                    [
                        "defi_tvl_total",
                        "defi_tvl_asset_chain",
                        "defi_tvl_change_1d_pct",
                        "defi_tvl_change_7d_pct",
                        "defi_stablecoin_median_apy",
                        "defi_stablecoin_tvl_weighted_apy",
                        "defi_stablecoin_apy_change_7d",
                    ],
                ),
                "missing": _missing_feature_keys(
                    features.summary,
                    [
                        "mc_tvl_ratio",
                        "stablecoin_supply_ratio",
                        "lending_utilization",
                        "cross_chain_net_flows",
                    ],
                ) + coverage_gaps,
            },
            "protocol_metrics": _defi_protocol_metrics(features.summary),
            "stablecoin_signals": (
                f"Stablecoin median APY is {features.summary.get('defi_stablecoin_median_apy')}; "
                f"7d APY change is {features.summary.get('defi_stablecoin_apy_change_7d')}; "
                f"MC/TVL ratio is {mc_tvl_ratio}."
            ),
            "fundamental_thesis": (
                "The DeFi read is driven by capital efficiency rather than price alone. "
                f"MC/TVL is {mc_tvl_ratio}, and stablecoin yield structure is still relatively contained, "
                "which argues against an obvious stress unwind but does not yet confirm fresh crypto-native demand."
            ),
            "risks": [
                {
                    "risk": "Protocol and cross-chain capital flow coverage is incomplete.",
                    "why_it_matters": "TVL changes can be price-led rather than capital-led.",
                    "severity": "high" if coverage_gaps else "med",
                }
            ],
            "what_would_change_my_mind": [
                "Sustained improvement in TVL trend with stablecoin inflows.",
                "Broader protocol-level fee and utilization data confirming healthy demand.",
            ],
            "uncertainties": coverage_gaps or ["MC/TVL and SSR are not currently available."],
            "signal": fundamentals_signal,
            "summary": (
                f"DeFi internals are mixed: MC/TVL sits at {mc_tvl_ratio}, while stablecoin yield changes "
                "remain mild. That is enough to avoid a hard bearish read, but not enough to call broad-based capital expansion."
            ),
        },
        "derivatives_analyst": {
            "role": "derivatives_analyst",
            "title": ROLE_TITLES["derivatives_analyst"],
            "data_coverage": {
                "available": [],
                "missing": coverage_gaps or ["coinglass:missing_metrics"],
            },
            "observations": [
                {
                    "metric": "spot_momentum_proxy",
                    "value": funding_rate if funding_rate is not None else features.summary.get("return_1d_pct"),
                    "interpretation": (
                        f"Funding={funding_rate}, oi_change={oi_change}, total_liquidation={total_liquidation}."
                        if funding_rate is not None else
                        "Only weak proxy because derivatives data is absent."
                    ),
                    "bull_bear": "bull" if _as_float(funding_rate) > 0 else "neutral",
                    "confidence": "med" if funding_rate is not None else "low",
                }
            ],
            "stress_signals": [
                {
                    "signal": "derivatives_coverage_gap",
                    "threshold": "coinglass data available",
                    "current": "missing",
                    "risk_level": "high",
                }
            ],
            "positioning_thesis": (
                (
                    f"Funding={funding_rate}, oi_change={oi_change}, total_liquidation={total_liquidation} "
                    "suggest current derivatives positioning."
                    if funding_rate is not None else
                    "CoinGlass-derived positioning is unavailable, so derivatives conviction remains constrained."
                )
            ),
            "what_would_change_my_mind": [
                "Funding, OI, and liquidation data showing crowding or squeeze conditions.",
            ],
            "uncertainties": coverage_gaps or ["Funding, OI, ELR, basis, and CVD are unavailable."],
            "signal": derivatives_signal,
            "summary": (
                (
                    f"Derivatives read uses funding={funding_rate}, oi_change={oi_change}, "
                    f"liquidation_24h={total_liquidation}."
                    if funding_rate is not None else
                    "CoinGlass-derived positioning is unavailable, so derivatives conviction remains constrained."
                )
            ),
        },
        "news_analyst": {
            "role": "news_analyst",
            "title": ROLE_TITLES["news_analyst"],
            "evidence_quality": "stub" if evidence_status == "stub" else "preliminary",
            "top_catalysts": [],
            "top_risks": [
                {
                    "risk": "External catalyst coverage is preliminary.",
                    "tier": 2,
                    "time_window": f"{request.horizon_days}d",
                    "impact_estimate": "unknown",
                    "confidence": "low",
                }
            ],
            "btrstn_assessment": "insufficient_evidence",
            "macro_context": "Macro catalyst coverage is not yet populated in the evidence pack.",
            "narrative": (
                f"External catalyst coverage comes from {evidence_source} and is currently {evidence_status}. "
                "The tape is not trading against a confirmed headline shock, but catalyst confidence is still below the standard needed for a high-conviction short-horizon call."
            ),
            "missing_evidence": [
                "Token unlock schedule",
                "Macro calendar context",
                "Regulatory catalyst screening",
            ],
            "signal": news_signal,
            "summary": (
                f"Headline and catalyst coverage is {evidence_status}; nothing clearly breaks the setup, "
                "but the event map is still incomplete."
            ),
        },
        "bull_researcher": {
            "role": "bull_researcher",
            "title": ROLE_TITLES["bull_researcher"],
            "thesis": bull_thesis,
            "key_points": [
                {"point": "Short-term momentum remains constructive.", "evidence_source": "technical_analyst", "confidence": "med"},
                {"point": "No confirmed negative catalyst in evidence pack.", "evidence_source": "news_analyst", "confidence": "low"},
            ],
            "rebuttals_to_bear": [
                {"bear_point": "Coverage gaps lower conviction", "rebuttal": "Missing derivatives data does not automatically invalidate price resilience.", "evidence_source": "technical_analyst"},
            ],
            "invalidation": ["Momentum fails and price loses support with expanding volatility."],
            "confidence": "med" if scorecard["score_decision"] == "hold" else "low",
            "data_gaps": coverage_gaps,
            "summary": bull_thesis,
            "provider": "deterministic",
            "analysis_mode": "deterministic_fallback",
        },
        "bear_researcher": {
            "role": "bear_researcher",
            "title": ROLE_TITLES["bear_researcher"],
            "thesis": bear_thesis,
            "key_points": [
                {"point": "Coverage gaps make the upside thesis unverifiable.", "evidence_source": "derivatives_analyst", "confidence": "high"},
                {"point": "DeFi signals remain incomplete.", "evidence_source": "defi_fundamentals_analyst", "confidence": "med"},
            ],
            "rebuttals_to_bull": [
                {"bull_point": "Momentum remains constructive", "rebuttal": "Without derivatives confirmation the move could be fragile.", "evidence_source": "derivatives_analyst"},
            ],
            "invalidation": ["Derivatives and DeFi data both confirm constructive participation."],
            "confidence": "high" if scorecard["score_decision"] == "avoid" else "med",
            "data_gaps": coverage_gaps,
            "summary": bear_thesis,
            "provider": "deterministic",
            "analysis_mode": "deterministic_fallback",
        },
        "risk_manager": {
            "role": "risk_manager",
            "title": ROLE_TITLES["risk_manager"],
            "risk_summary": [
                {
                    "risk": "Data coverage gap",
                    "severity": "high" if coverage_gaps else "med",
                    "source_role": "derivatives_analyst",
                    "mitigation": "Reduce size until derivatives context is available.",
                }
            ],
            "guardrails": {
                "max_position_pct": "quarter" if scorecard["confidence"] == "low" else "half",
                "stop_logic": ["Use volatility-adjusted stops based on ATR."],
                "sizing_recommendation": "quarter" if scorecard["score_decision"] == "avoid" else "half",
            },
            "cascade_risk_level": "elevated" if coverage_gaps else "moderate",
            "operational_risks": ["Evidence and derivatives feeds are incomplete."],
            "data_quality_flags": coverage_gaps or ["none"],
            "recommendation": "avoid" if scorecard["score_decision"] == "avoid" else "reduce_size",
            "risk_bias": risk_bias,
            "summary": (
                "Position sizing should stay conservative until derivatives and DeFi "
                f"coverage gaps are closed. Current quantitative score is {scorecard['final_score']} "
                f"with {scorecard['confidence']} confidence, regime={regime}, mc_tvl_ratio={mc_tvl_ratio}, "
                f"funding={funding_rate}."
            ),
            "provider": "deterministic",
            "analysis_mode": "deterministic_fallback",
        },
        "final_arbiter": {
            "role": "final_arbiter",
            "title": ROLE_TITLES["final_arbiter"],
            "decision": {
                "action": final_decision,
                "direction": "neutral",
                "horizon_days": request.horizon_days,
                "position_size": "none" if final_decision == "avoid" else "half",
            },
            "decision_label": final_decision,
            "thesis": (
                f"Net call: {final_decision} over the next {request.horizon_days} days. "
                f"The quantitative stack prints {scorecard['final_score']} with {scorecard['confidence']} confidence, "
                "and the combined read still looks more like risk control than a clean offensive entry."
            ),
            "confidence": _map_confidence(scorecard["confidence"]),
            "key_factors": [
                {"factor": technical_signal, "source_role": "technical_analyst"},
                {"factor": fundamentals_signal, "source_role": "defi_fundamentals_analyst"},
                {"factor": derivatives_signal, "source_role": "derivatives_analyst"},
            ],
            "key_risks": [
                {"risk": "Coverage gaps reduce conviction", "mitigation": "Wait for derivatives confirmation", "source_role": "risk_manager"},
            ],
            "entry_logic": (
                f"No clean entry until coverage gaps close. Watch for daily close above resistance "
                f"({_fmt(latest_close * 1.03 if isinstance(latest_close, (int, float)) else None)}) "
                f"with RSI > 55 and MACD histogram re-accelerating. "
                f"Alternate: scale on pullback to SMA20 while SMA200 holds."
                if final_decision in {"hold", "buy"}
                else "Avoid entry. Conditions do not support a long position."
            ),
            "stop_logic": (
                f"Initial stop = 1× ATR below entry. "
                f"Hard structural stop: daily close below SMA50 on expanding volume. "
                f"If ATR data available: size so 1 ATR stop equals 0.5–1% of portfolio equity."
            ),
            "targets": (
                [
                    {"price_target": _fmt(latest_close * 1.06 if isinstance(latest_close, (int, float)) else None), "pct_position_to_exit": "30–40%", "rationale": "First resistance zone"},
                    {"price_target": _fmt(latest_close * 1.12 if isinstance(latest_close, (int, float)) else None), "pct_position_to_exit": "40–50%", "rationale": "Second resistance zone / prior swing high"},
                ]
                if final_decision == "buy"
                else []
            ),
            "sizing_formula": (
                "Risk 0.5–1% of portfolio per trade. "
                "Size so 1 ATR stop = that dollar risk amount. "
                f"Cap total tactical exposure at {'2–5%' if final_decision == 'buy' else '0%'} of portfolio."
            ),
            "flip_rules": [
                {
                    "condition": "Daily close below SMA50 on expanding down-volume with MACD turning negative",
                    "new_posture": "Immediate full exit; reassess for short setup",
                },
                {
                    "condition": "5+ consecutive daily closes above 200-SMA with rising MACD and stablecoin inflows confirmed",
                    "new_posture": "Upgrade to longer-term Buy at full size",
                },
            ],
            "tactical_alternative": (
                "For conservative mandates: use defined-loss call spreads (premium ≤ 0.5% of portfolio) "
                "instead of spot exposure. If spot, reduce single-trade risk to 0.25% and widen stops to 1.5× ATR."
            ),
            "invalidation": [
                "Quant score rises above the hold threshold with better source coverage.",
                "Catalyst coverage improves and contradicts the current cautious stance.",
            ],
            "review_plan": {
                "review_at_days": request.horizon_days,
                "what_to_check": ["future_return_pct", "scorecard drift", "coverage_gaps"],
            },
            "override_note": None,
            "rejected_alternative": {
                "alternative_action": (
                    "buy" if final_decision == "avoid"
                    else ("avoid" if final_decision == "buy" else "hold")
                ),
                "why_rejected": (
                    "Insufficient confirmation from 2+ roles; scorecard threshold not met "
                    "or coverage gaps dominate the risk picture."
                ),
            },
            "summary": (
                f"The integrated crypto read stays {final_decision}: score={scorecard['final_score']}, "
                f"regime={regime}, MC/TVL={mc_tvl_ratio}, funding={funding_rate}. "
                "The system sees enough fragility to stay conservative rather than press for directional size."
            ),
            "rationale": [
                technical_signal,
                fundamentals_signal,
                derivatives_signal,
                risk_bias,
                f"score={scorecard['final_score']}",
            ],
            "scorecard": scorecard,
            "provider": "deterministic",
            "analysis_mode": "deterministic_fallback",
        },
    }
    role_memos: dict[str, dict[str, object]] = {}

    for role in FIRST_ORDER_ROLES:
        role_memos[role] = _generate_role_memo(
            role=role,
            fallback_memo=base_memos[role],
            prompts_dir=prompts_dir,
            request=request,
            features=features,
            evidence=evidence,
            provider=provider,
            prior_memos={},
            use_provider=True,
            call_log_path=call_log_path,
        )

    debate_state = {
        "history": "",
        "bull_history": "",
        "bear_history": "",
        "current_response": "",
        "count": 0,
    }
    for _round in range(MAX_INVEST_DEBATE_ROUNDS):
        bull_memo, debate_state = _generate_debate_role_memo(
            role="bull_researcher",
            fallback_memo=base_memos["bull_researcher"],
            debate_state=debate_state,
            prompts_dir=prompts_dir,
            request=request,
            features=features,
            evidence=evidence,
            provider=provider,
            prior_memos=role_memos,
            call_log_path=call_log_path,
            use_provider=True,
        )
        role_memos["bull_researcher"] = bull_memo
        bear_memo, debate_state = _generate_debate_role_memo(
            role="bear_researcher",
            fallback_memo=base_memos["bear_researcher"],
            debate_state=debate_state,
            prompts_dir=prompts_dir,
            request=request,
            features=features,
            evidence=evidence,
            provider=provider,
            prior_memos=role_memos,
            call_log_path=call_log_path,
            use_provider=True,
        )
        role_memos["bear_researcher"] = bear_memo

    risk_debate_envelope = _build_risk_debate_envelope(
        base_risk_memo=base_memos["risk_manager"],
        scorecard=scorecard,
        regime=regime,
        funding_rate=funding_rate,
        coverage_gaps=coverage_gaps,
        request=request,
        features=features,
        evidence=evidence,
        provider=provider,
        prior_memos=role_memos,
    )

    role_memos["risk_manager"] = _generate_role_memo(
        role="risk_manager",
        fallback_memo=risk_debate_envelope,
        prompts_dir=prompts_dir,
        request=request,
        features=features,
        evidence=evidence,
        provider=provider,
        prior_memos=role_memos,
        use_provider=True,
        call_log_path=call_log_path,
    )

    role_memos["final_arbiter"] = _generate_role_memo(
        role="final_arbiter",
        fallback_memo=base_memos["final_arbiter"],
        prompts_dir=prompts_dir,
        request=request,
        features=features,
        evidence=evidence,
        provider=provider,
        prior_memos=role_memos,
        use_provider=True,
        call_log_path=call_log_path,
    )

    return role_memos


def _generate_debate_role_memo(
    *,
    role: str,
    fallback_memo: dict[str, object],
    debate_state: dict[str, object],
    prompts_dir: Path,
    request: ResearchRequest,
    features: FeatureBundle,
    evidence: EvidencePack,
    provider: AnalysisProvider,
    prior_memos: dict[str, dict[str, object]],
    call_log_path: Path,
    use_provider: bool,
) -> tuple[dict[str, object], dict[str, object]]:
    prepared_fallback = _prepare_investment_debate_turn(
        role=role,
        fallback_memo=fallback_memo,
        debate_state=debate_state,
    )
    debate_prior_memos = {
        **prior_memos,
        "investment_debate_state": {
            "history": debate_state.get("history", ""),
            "current_response": debate_state.get("current_response", ""),
            "count": debate_state.get("count", 0),
        },
    }
    memo = _generate_role_memo(
        role=role,
        fallback_memo=prepared_fallback,
        prompts_dir=prompts_dir,
        request=request,
        features=features,
        evidence=evidence,
        provider=provider,
        prior_memos=debate_prior_memos,
        use_provider=use_provider,
        call_log_path=call_log_path,
    )
    final_argument = _debate_argument_from_memo(
        role=role,
        memo=memo,
        fallback_argument=str(prepared_fallback["argument"]),
    )
    new_state = _append_investment_debate_state(
        role=role,
        debate_state=debate_state,
        argument=final_argument,
    )
    memo["speaker"] = prepared_fallback["speaker"]
    memo["argument"] = final_argument
    memo["counterparty_response"] = prepared_fallback["counterparty_response"]
    memo["debate_state"] = new_state
    return memo, new_state


def _prepare_investment_debate_turn(
    *,
    role: str,
    fallback_memo: dict[str, object],
    debate_state: dict[str, object],
) -> dict[str, object]:
    speaker = "Bull Analyst" if role == "bull_researcher" else "Bear Analyst"
    prior_response = str(debate_state.get("current_response", ""))
    argument = _compose_debate_argument(
        role=role,
        fallback_memo=fallback_memo,
        counterparty_response=prior_response,
    )
    return {
        **fallback_memo,
        "speaker": speaker,
        "argument": argument,
        "counterparty_response": prior_response,
    }


def _append_investment_debate_state(
    *,
    role: str,
    debate_state: dict[str, object],
    argument: str,
) -> dict[str, object]:
    history = str(debate_state.get("history", "")).strip()
    new_history = f"{history}\n{argument}".strip() if history else argument
    return {
        "history": new_history,
        "bull_history": (
            f"{str(debate_state.get('bull_history', '')).strip()}\n{argument}".strip()
            if role == "bull_researcher"
            else str(debate_state.get("bull_history", ""))
        ),
        "bear_history": (
            f"{str(debate_state.get('bear_history', '')).strip()}\n{argument}".strip()
            if role == "bear_researcher"
            else str(debate_state.get("bear_history", ""))
        ),
        "current_response": argument,
        "count": int(debate_state.get("count", 0)) + 1,
    }


def _compose_debate_argument(
    *,
    role: str,
    fallback_memo: dict[str, object],
    counterparty_response: str,
) -> str:
    thesis = str(fallback_memo.get("thesis") or fallback_memo.get("summary") or "")
    if role == "bull_researcher":
        lead = "Bull Analyst"
        rebuttal = (
            "The technical stack still argues for upside persistence."
            if not counterparty_response
            else "The bear case leans too heavily on missing coverage and does not invalidate the current tape."
        )
    else:
        lead = "Bear Analyst"
        rebuttal = (
            "The bullish case overstates momentum without enough confirmation."
            if counterparty_response
            else "The upside case is incomplete without cross-checking leverage and participation."
        )
    return f"{lead}: {thesis} {rebuttal}".strip()


def _debate_argument_from_memo(
    *,
    role: str,
    memo: dict[str, object],
    fallback_argument: str,
) -> str:
    lead = "Bull Analyst" if role == "bull_researcher" else "Bear Analyst"
    thesis = role_summary_text(memo)
    rebuttal_key = "rebuttals_to_bear" if role == "bull_researcher" else "rebuttals_to_bull"
    rebuttal = _extract_rebuttal_snippet(memo.get(rebuttal_key))
    body = thesis if isinstance(thesis, str) and thesis.strip() else fallback_argument
    if rebuttal:
        body = f"{body} {rebuttal}".strip()
    if body.startswith(f"{lead}:"):
        return body
    return f"{lead}: {body}".strip()


def _build_risk_debate_envelope(
    *,
    base_risk_memo: dict[str, object],
    scorecard: dict[str, object],
    regime: str,
    funding_rate: object,
    coverage_gaps: list[str],
    request: ResearchRequest,
    features: FeatureBundle,
    evidence: EvidencePack,
    provider: AnalysisProvider,
    prior_memos: dict[str, dict[str, object]],
) -> dict[str, object]:
    state = {
        "history": "",
        "aggressive_history": "",
        "conservative_history": "",
        "neutral_history": "",
        "latest_speaker": "",
        "current_aggressive_response": "",
        "current_conservative_response": "",
        "current_neutral_response": "",
        "count": 0,
    }
    views: dict[str, str] = {}
    for stance in RISK_DEBATE_ORDER:
        argument, state = _run_risk_debate_turn(
            stance=stance,
            state=state,
            scorecard=scorecard,
            regime=regime,
            funding_rate=funding_rate,
            coverage_gaps=coverage_gaps,
            request=request,
            features=features,
            evidence=evidence,
            provider=provider,
            prior_memos=prior_memos,
        )
        views[stance] = argument
    return {
        **base_risk_memo,
        "risk_views": views,
        "risk_debate_state": state,
    }


def _run_risk_debate_turn(
    *,
    stance: str,
    state: dict[str, object],
    scorecard: dict[str, object],
    regime: str,
    funding_rate: object,
    coverage_gaps: list[str],
    request: ResearchRequest,
    features: FeatureBundle,
    evidence: EvidencePack,
    provider: AnalysisProvider,
    prior_memos: dict[str, dict[str, object]],
) -> tuple[str, dict[str, object]]:
    fallback_argument = _compose_risk_debate_argument(
        stance=stance,
        state=state,
        scorecard=scorecard,
        regime=regime,
        funding_rate=funding_rate,
        coverage_gaps=coverage_gaps,
    )
    prompt = _build_risk_debate_prompt(
        stance=stance,
        state=state,
        scorecard=scorecard,
        regime=regime,
        funding_rate=funding_rate,
        coverage_gaps=coverage_gaps,
        request=request,
        features=features,
        evidence=evidence,
        prior_memos=prior_memos,
    )
    debate_role = f"{stance}_risk_analyst"
    role_provider = _provider_for_role(provider, debate_role)
    generated = role_provider.generate(
        role=debate_role,
        prompt=prompt,
        fallback_memo={"report": fallback_argument, "confidence": "medium"},
    )
    argument = _normalize_risk_debate_argument(
        stance=stance,
        text=_narrative_text(generated) or fallback_argument,
    )
    history = str(state.get("history", "")).strip()
    new_history = f"{history}\n{argument}".strip() if history else argument
    new_state = dict(state)
    new_state["history"] = new_history
    new_state["count"] = int(state.get("count", 0)) + 1
    if stance == "aggressive":
        new_state["aggressive_history"] = f"{str(state.get('aggressive_history', '')).strip()}\n{argument}".strip()
        new_state["current_aggressive_response"] = argument
        new_state["latest_speaker"] = "Aggressive"
    elif stance == "conservative":
        new_state["conservative_history"] = f"{str(state.get('conservative_history', '')).strip()}\n{argument}".strip()
        new_state["current_conservative_response"] = argument
        new_state["latest_speaker"] = "Conservative"
    else:
        new_state["neutral_history"] = f"{str(state.get('neutral_history', '')).strip()}\n{argument}".strip()
        new_state["current_neutral_response"] = argument
        new_state["latest_speaker"] = "Neutral"
    return argument, new_state


def _compose_risk_debate_argument(
    *,
    stance: str,
    state: dict[str, object],
    scorecard: dict[str, object],
    regime: str,
    funding_rate: object,
    coverage_gaps: list[str],
) -> str:
    if stance == "aggressive":
        return (
            "Aggressive Analyst: Technical momentum and a score of "
            f"{scorecard['final_score']} leave room to press for upside if the regime ({regime}) stabilizes. "
            "Waiting for every feed to clear can mean missing the move."
        )
    if stance == "conservative":
        return (
            "Conservative Analyst: Coverage gaps and incomplete derivatives visibility dominate the risk picture. "
            f"Funding={funding_rate} and gaps={coverage_gaps or ['none']} do not justify leaning in."
        )
    return (
        "Neutral Analyst: The aggressive case is directionally understandable, but the conservative case is stronger "
        "until confirmation improves. Limited size or avoidance remains the balanced posture."
    )


def _build_risk_debate_prompt(
    *,
    stance: str,
    state: dict[str, object],
    scorecard: dict[str, object],
    regime: str,
    funding_rate: object,
    coverage_gaps: list[str],
    request: ResearchRequest,
    features: FeatureBundle,
    evidence: EvidencePack,
    prior_memos: dict[str, dict[str, object]],
) -> str:
    stance_titles = {
        "aggressive": "Aggressive Analyst",
        "conservative": "Conservative Analyst",
        "neutral": "Neutral Analyst",
    }
    instructions = {
        "aggressive": "Argue for pressing risk when the setup justifies it. Challenge excessive caution and explain what limited confirmation is still enough to proceed.",
        "conservative": "Argue for capital preservation. Emphasize why missing data, leverage risk, or fragile structure should cap or avoid exposure.",
        "neutral": "Act as the balancing voice. Weigh both sides and recommend the most disciplined posture for this horizon.",
    }
    context = {
        "request": {
            "asset": request.asset,
            "thesis": request.thesis,
            "horizon_days": request.horizon_days,
        },
        "scorecard": scorecard,
        "regime": regime,
        "funding_rate": funding_rate,
        "coverage_gaps": coverage_gaps,
        "feature_context": {
            key: features.summary.get(key)
            for key in (
                "latest_close",
                "return_1d_pct",
                "return_30d_pct",
                "realized_vol_30d",
                "price_vs_sma200_pct",
                "mc_tvl_ratio",
            )
        },
        "evidence_context": {
            key: evidence.summary.get(key)
            for key in ("evidence_status", "source", "citations_count")
        },
        "prior_role_memos": _compact_role_memos(prior_memos),
        "risk_debate_state": state,
    }
    return (
        f"You are the {stance_titles[stance]} in a crypto risk debate.\n"
        f"{instructions[stance]}\n"
        "Return only compact JSON with at least `report` and optional `confidence`.\n\n"
        f"{json.dumps(context, indent=2)}"
    )


def _normalize_risk_debate_argument(*, stance: str, text: str) -> str:
    labels = {
        "aggressive": "Aggressive Analyst",
        "conservative": "Conservative Analyst",
        "neutral": "Neutral Analyst",
    }
    label = labels[stance]
    stripped = text.strip()
    if stripped.startswith(f"{label}:"):
        return stripped
    return f"{label}: {stripped}".strip()


def _extract_rebuttal_snippet(value: object) -> str | None:
    if not isinstance(value, list) or not value:
        return None
    first = value[0]
    if not isinstance(first, dict):
        return None
    rebuttal = first.get("rebuttal")
    if isinstance(rebuttal, str) and rebuttal.strip():
        return rebuttal.strip()
    return None


def _generate_role_memo(
    *,
    role: str,
    fallback_memo: dict[str, object],
    prompts_dir: Path,
    request: ResearchRequest,
    features: FeatureBundle,
    evidence: EvidencePack,
    provider: AnalysisProvider,
    prior_memos: dict[str, dict[str, object]],
    use_provider: bool,
    call_log_path: Path,
) -> dict[str, object]:
    prompt_path = prompts_dir / f"{role}.md"
    prompt_text = _build_role_prompt(
        role=role,
        prompt_path=prompt_path,
        request=request,
        features=features,
        evidence=evidence,
        fallback_memo=fallback_memo,
        prior_memos=prior_memos,
    )
    role_provider = _provider_for_role(provider, role) if use_provider else provider
    start = time.perf_counter()
    timeout_seconds = getattr(role_provider, "timeout_seconds", None) if use_provider else None
    generated = (
        role_provider.generate(role=role, prompt=prompt_text, fallback_memo=fallback_memo)
        if use_provider
        else {}
    )
    duration_ms = int((time.perf_counter() - start) * 1000)
    provider_meta = getattr(role_provider, "last_meta", {}) if use_provider else {}
    if not generated and use_provider:
        generated = _salvage_narrative_generated(role=role, provider_meta=provider_meta)
    validation_error = _validate_generated_memo(
        role=role,
        fallback_memo=fallback_memo,
        generated=generated,
    ) if use_provider else None
    if validation_error is not None:
        import sys
        missing = [k for k in _required_output_fields(fallback_memo) if k not in generated]
        print(f"[validation] {role}: {validation_error}, missing={missing}, got={sorted(generated.keys())}", file=sys.stderr)
    if generated and validation_error is None:
        memo = {
            **_normalize_generated_memo(
                role=role,
                fallback_memo=fallback_memo,
                generated=generated,
            ),
            "provider": role_provider.name,
            "analysis_mode": "prompt_driven",
            "prompt_path": str(prompt_path),
            "prompt_text": prompt_text,
        }
        memo = _polish_generated_memo(
            role=role,
            memo=memo,
            fallback_memo=fallback_memo,
            features=features,
            evidence=evidence,
        )
        citation_warning = _check_citation_coverage(role, memo)
        if citation_warning is not None:
            memo["citation_warning"] = citation_warning
        _append_call_log(
            call_log_path=call_log_path,
            role=role,
            provider=role_provider.name,
            analysis_mode="prompt_driven",
            timeout_seconds=timeout_seconds,
            duration_ms=duration_ms,
            validation_error=None,
            fallback_reason=None,
            fallback_detail=None,
            provider_error_type=None,
        )
        return memo
    fallback_reason = validation_error or str(provider_meta.get("reason") or "provider_empty_response")
    fallback_detail = provider_meta.get("detail")
    provider_error_type = provider_meta.get("error_type")
    memo = {
        **fallback_memo,
        "provider": "deterministic",
        "analysis_mode": "deterministic_fallback",
        "prompt_path": str(prompt_path),
        "prompt_text": prompt_text,
        "fallback_reason": fallback_reason,
    }
    if validation_error is not None:
        memo["validation_error"] = validation_error
    if isinstance(fallback_detail, str) and fallback_detail.strip():
        memo["fallback_detail"] = fallback_detail
    if isinstance(provider_error_type, str) and provider_error_type.strip():
        memo["provider_error_type"] = provider_error_type
    _append_call_log(
        call_log_path=call_log_path,
        role=role,
        provider="deterministic",
        analysis_mode="deterministic_fallback",
        timeout_seconds=timeout_seconds,
        duration_ms=duration_ms,
        validation_error=validation_error,
        fallback_reason=fallback_reason,
        fallback_detail=fallback_detail if isinstance(fallback_detail, str) else None,
        provider_error_type=provider_error_type if isinstance(provider_error_type, str) else None,
    )
    return memo


def _build_role_prompt(
    *,
    role: str,
    prompt_path: Path,
    request: ResearchRequest,
    features: FeatureBundle,
    evidence: EvidencePack,
    fallback_memo: dict[str, object],
    prior_memos: dict[str, dict[str, object]],
) -> str:
    prompt_template = prompt_path.read_text(encoding="utf-8").strip()
    if role in NARRATIVE_FIRST_ROLES:
        compact_context = {
            "request": {
                "asset": request.asset,
                "thesis": request.thesis,
                "horizon_days": request.horizon_days,
                "run_id": request.run_id,
            },
            "role_context": (
                _provider_context_for_role(role, features.summary, evidence.summary, features.coverage_gaps)
                if role in FIRST_ORDER_ROLES
                else _strategic_role_context(
                    role=role,
                    feature_summary=features.summary,
                    evidence_summary=evidence.summary,
                    coverage_gaps=features.coverage_gaps,
                    scorecard=build_scorecard(
                        feature_summary=features.summary,
                        coverage_gaps=features.coverage_gaps,
                        evidence_summary=evidence.summary,
                    ),
                    prior_memos=prior_memos,
                )
            ),
            "field_interpretation_guide": _field_interpretation_guide(role),
            "required_json_output": {
                "report": "Narrative memo in the voice of a crypto analyst.",
                "signal": "One short stance label.",
                "confidence": "low | medium | high",
                "referenced_fields": ["field_a", "field_b"],
            },
            "optional_structured_overrides": _required_output_fields(fallback_memo),
        }
        # Inject actual evidence content for news_analyst when available
        if role == "news_analyst" and evidence.summary.get("evidence_status") == "fetched":
            try:
                evidence_text = evidence.markdown_path.read_text(encoding="utf-8").strip()
                if evidence_text:
                    compact_context["evidence_content"] = evidence_text
            except (OSError, AttributeError):
                pass
        return (
            f"{prompt_template}\n\n"
            "Follow a TradingAgents-style flow: first form a concise analyst report, then return compact JSON. "
            "The `report` field is mandatory. Only override structured fields when the supplied data directly supports them. "
            "Do not restate the whole schema.\n\n"
            "Field interpretation guide:\n"
            f"{_render_field_guide_lines(role)}\n\n"
            "Return only a compact JSON object.\n\n"
            f"{json.dumps(compact_context, indent=2)}"
        )
    context = {
        "request": {
            "asset": request.asset,
            "thesis": request.thesis,
            "horizon_days": request.horizon_days,
            "run_id": request.run_id,
        },
        "market_context": _strategic_market_context(
            feature_summary=features.summary,
            evidence_summary=evidence.summary,
            coverage_gaps=features.coverage_gaps,
        ),
        "field_interpretation_guide": _field_interpretation_guide(role),
        "scorecard": build_scorecard(
            feature_summary=features.summary,
            coverage_gaps=features.coverage_gaps,
            evidence_summary=evidence.summary,
        ),
        "prior_role_memos": _compact_role_memos(prior_memos, strategic_only=True),
        "decision_baseline": _compact_fallback_memo(fallback_memo),
        "output_contract": {
            "role": role,
            "required_fields": _required_output_fields(fallback_memo),
        },
    }
    return (
        f"{prompt_template}\n\n"
        "Field interpretation guide:\n"
        f"{_render_field_guide_lines(role)}\n\n"
        "Use the field names exactly as provided below. Ground every claim in these fields, "
        "and state when the available data is insufficient.\n\n"
        "Return only a compact JSON object for this role.\n\n"
        f"{json.dumps(context, indent=2)}"
    )


def _render_role_markdown(role: str, memo: dict[str, object]) -> str:
    title = ROLE_TITLES[role]
    lines = [f"# {title}", ""]
    for key, value in memo.items():
        if isinstance(value, list):
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.extend(f"- {item}" for item in value)
        else:
            lines.append(f"- {key}: {value}")
    lines.append("")
    return "\n".join(lines)


def _as_float(value: object) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0


def _fmt(value: object) -> str:
    """Format a numeric price value to a display string, or return 'n/a'."""
    if isinstance(value, (int, float)):
        return f"{value:,.2f}"
    return "n/a"


def _compact_role_memos(
    role_memos: dict[str, dict[str, object]],
    *,
    strategic_only: bool = False,
) -> dict[str, dict[str, object]]:
    compacted: dict[str, dict[str, object]] = {}
    if strategic_only:
        for role, memo in role_memos.items():
            compacted[role] = _strategic_memo_view(role, memo)
        return compacted
    excluded_fields = {"prompt_text", "prompt_path"}
    for role, memo in role_memos.items():
        compacted[role] = {
            key: value
            for key, value in memo.items()
            if key not in excluded_fields
        }
    return compacted


def _strategic_memo_view(role: str, memo: dict[str, object]) -> dict[str, object]:
    if role == "investment_debate_state":
        return {
            key: memo.get(key)
            for key in ("history", "current_response", "count")
        }
    common = {
        "summary": role_summary_text(memo),
        "signal": memo.get("signal"),
        "confidence": memo.get("confidence"),
    }
    if role == "technical_analyst":
        return {
            **common,
            "regime": memo.get("regime"),
            "referenced_fields": memo.get("referenced_fields"),
            "support": _first_level(memo, "support"),
            "resistance": _first_level(memo, "resistance"),
        }
    if role == "defi_fundamentals_analyst":
        return {
            **common,
            "stablecoin_signals": memo.get("stablecoin_signals"),
            "data_gaps": memo.get("uncertainties"),
        }
    if role == "derivatives_analyst":
        return {
            **common,
            "positioning_thesis": memo.get("positioning_thesis"),
            "data_gaps": memo.get("uncertainties"),
        }
    if role == "news_analyst":
        return {
            **common,
            "evidence_quality": memo.get("evidence_quality"),
            "top_risk": _first_risk(memo.get("top_risks")),
        }
    if role in {"bull_researcher", "bear_researcher"}:
        return {
            "thesis": memo.get("thesis") or memo.get("summary"),
            "argument": memo.get("argument"),
            "confidence": memo.get("confidence"),
            "top_point": _first_point(memo.get("key_points")),
            "top_rebuttal": _first_rebuttal(memo),
            "data_gaps": memo.get("data_gaps"),
        }
    if role == "risk_manager":
        risk_views = memo.get("risk_views") if isinstance(memo.get("risk_views"), dict) else {}
        return {
            "summary": role_summary_text(memo),
            "recommendation": memo.get("recommendation"),
            "risk_bias": memo.get("risk_bias"),
            "cascade_risk_level": memo.get("cascade_risk_level"),
            "aggressive_view": risk_views.get("aggressive"),
            "conservative_view": risk_views.get("conservative"),
            "neutral_view": risk_views.get("neutral"),
        }
    if role == "final_arbiter":
        return {
            "decision": memo.get("decision"),
            "summary": role_summary_text(memo),
            "confidence": memo.get("confidence"),
            "key_factors": memo.get("key_factors"),
            "rejected_alternative": memo.get("rejected_alternative"),
        }
    return common


def _strategic_market_context(
    *,
    feature_summary: dict[str, object],
    evidence_summary: dict[str, object],
    coverage_gaps: list[str],
) -> dict[str, object]:
    return {
        "price": {
            key: feature_summary.get(key)
            for key in (
                "latest_close",
                "return_1d_pct",
                "return_7d_pct",
                "return_30d_pct",
                "price_vs_sma20_pct",
                "price_vs_sma200_pct",
                "rsi_14",
                "realized_vol_30d",
                "volume_ratio",
                "regime",
                "halving_cycle_day",
            )
            if feature_summary.get(key) is not None
        },
        "defi": {
            key: feature_summary.get(key)
            for key in (
                "defi_tvl_total",
                "defi_stablecoin_median_apy",
                "defi_stablecoin_apy_change_7d",
                "mc_tvl_ratio",
            )
            if feature_summary.get(key) is not None
        },
        "evidence": {
            key: evidence_summary.get(key)
            for key in ("evidence_status", "source", "citations_count")
            if evidence_summary.get(key) is not None
        },
        "coverage_gaps": coverage_gaps,
    }


def _compact_fallback_memo(fallback_memo: dict[str, object]) -> dict[str, object]:
    compact = {
        "role": fallback_memo.get("role"),
        "summary": fallback_memo.get("summary") or fallback_memo.get("thesis"),
    }
    if "decision" in fallback_memo:
        compact["decision"] = fallback_memo.get("decision")
    if "recommendation" in fallback_memo:
        compact["recommendation"] = fallback_memo.get("recommendation")
    if "scorecard" in fallback_memo:
        compact["scorecard"] = fallback_memo.get("scorecard")
    return compact


def _strategic_role_context(
    *,
    role: str,
    feature_summary: dict[str, object],
    evidence_summary: dict[str, object],
    coverage_gaps: list[str],
    scorecard: dict[str, object],
    prior_memos: dict[str, dict[str, object]],
) -> dict[str, object]:
    context = {
        "market_context": _strategic_market_context(
            feature_summary=feature_summary,
            evidence_summary=evidence_summary,
            coverage_gaps=coverage_gaps,
        ),
        "scorecard": scorecard,
        "prior_role_memos": _compact_role_memos(prior_memos, strategic_only=True),
    }
    if role in {"bull_researcher", "bear_researcher"}:
        context["debate_state"] = _strategic_memo_view(
            "investment_debate_state",
            prior_memos.get("investment_debate_state", {}),
        )
    if role == "bear_researcher" and "bull_researcher" in prior_memos:
        bull_memo = prior_memos["bull_researcher"]
        context["bull_key_points_to_rebut"] = bull_memo.get("key_points", [])
    return context


def _first_level(memo: dict[str, object], level_key: str) -> object:
    levels = memo.get("levels")
    if not isinstance(levels, dict):
        return None
    values = levels.get(level_key)
    if isinstance(values, list) and values:
        return values[0]
    return None


def _first_risk(value: object) -> object:
    if not isinstance(value, list) or not value:
        return None
    first = value[0]
    if isinstance(first, dict):
        return first.get("risk")
    return None


def _first_point(value: object) -> object:
    if not isinstance(value, list) or not value:
        return None
    first = value[0]
    if isinstance(first, dict):
        return first.get("point")
    return None


def _first_rebuttal(memo: dict[str, object]) -> object:
    for key in ("rebuttals_to_bear", "rebuttals_to_bull"):
        value = memo.get(key)
        if not isinstance(value, list) or not value:
            continue
        first = value[0]
        if isinstance(first, dict):
            return first.get("rebuttal")
    return None


def _field_interpretation_guide(role: str) -> dict[str, str]:
    base_guide = {
        "latest_close": "Latest observed close. Use it as the anchor for all price references.",
        "return_1d_pct": "One-day percentage move. Positive means short-term momentum, negative means near-term weakness.",
        "return_total_pct": "Window-level cumulative return. Use it to distinguish bounce-vs-trend continuation.",
        "avg_volume": "Average traded volume proxy. Higher values imply stronger liquidity and more credible moves.",
        "coverage_gaps": "Explicitly lower conviction when this list is non-empty.",
        "evidence_status": "Indicates whether external catalyst coverage is complete, preliminary, or missing.",
    }
    if role == "derivatives_analyst":
        base_guide["coverage_gaps"] = "If coinglass coverage is missing, say derivatives conviction is constrained."
    if role == "defi_fundamentals_analyst":
        base_guide["coverage_gaps"] = "If defillama or protocol coverage is missing, say DeFi evidence is incomplete."
    if role == "news_analyst":
        base_guide["evidence_status"] = "Treat stub or preliminary evidence as non-actionable catalyst coverage."
    if role == "final_arbiter":
        base_guide["scorecard.final_score"] = "Weighted 0-100 quantitative score. Use it as a hard decision anchor, not a suggestion."
        base_guide["scorecard.score_decision"] = "Baseline decision implied by score thresholds. Do not contradict it without citing a concrete override reason."
    return base_guide


def _render_field_guide_lines(role: str) -> str:
    guide = _field_interpretation_guide(role)
    return "\n".join(f"- {field}: {meaning}" for field, meaning in guide.items())


def _required_output_fields(fallback_memo: dict[str, object]) -> list[str]:
    return [key for key in fallback_memo.keys() if key not in SYSTEM_FIELDS]


def _polish_generated_memo(
    *,
    role: str,
    memo: dict[str, object],
    fallback_memo: dict[str, object],
    features: FeatureBundle,
    evidence: EvidencePack,
) -> dict[str, object]:
    polished = dict(memo)
    if not isinstance(polished.get("referenced_fields"), list) or not polished.get("referenced_fields"):
        polished["referenced_fields"] = _referenced_fields_for_role(role, features.summary, evidence.summary)
    report = _narrative_text(polished)
    if isinstance(report, str):
        polished["report"] = report
    if isinstance(report, str) and len(report.strip()) >= 80:
        polished["summary"] = report.strip()
    summary = polished.get("summary")
    fallback_summary = fallback_memo.get("summary")
    if not isinstance(summary, str) or len(summary.strip()) < 80 or summary == fallback_summary:
        polished["summary"] = _synthesized_summary(
            role=role,
            memo=polished,
            feature_summary=features.summary,
            evidence_summary=evidence.summary,
        )
    return polished


def _referenced_fields_for_role(
    role: str,
    feature_summary: dict[str, object],
    evidence_summary: dict[str, object],
) -> list[str]:
    field_map = {
        "technical_analyst": [
            "latest_close",
            "return_1d_pct",
            "return_30d_pct",
            "rsi_14",
            "price_vs_sma20_pct",
            "price_vs_sma200_pct",
            "realized_vol_30d",
            "volume_ratio",
            "regime",
        ],
        "defi_fundamentals_analyst": [
            "defi_tvl_total",
            "defi_tvl_change_7d_pct",
            "defi_stablecoin_median_apy",
            "defi_stablecoin_apy_change_7d",
            "mc_tvl_ratio",
        ],
        "derivatives_analyst": [
            "derivatives_funding_rate_latest",
            "derivatives_open_interest_change_pct",
            "derivatives_total_liquidation_usd_24h",
            "coverage_gaps",
        ],
        "news_analyst": [
            "evidence_status",
            "source",
            "citations_count",
            "coverage_gaps",
        ],
    }
    referenced = []
    for field in field_map.get(role, []):
        if field in {"evidence_status", "source", "citations_count"}:
            if evidence_summary.get(field) is not None:
                referenced.append(field)
        elif field == "coverage_gaps":
            referenced.append(field)
        elif feature_summary.get(field) is not None:
            referenced.append(field)
    return referenced


def _provider_context_for_role(
    role: str,
    feature_summary: dict[str, object],
    evidence_summary: dict[str, object],
    coverage_gaps: list[str],
) -> dict[str, object]:
    field_map = {
        "technical_analyst": [
            "latest_close",
            "return_1d_pct",
            "return_30d_pct",
            "rsi_14",
            "price_vs_sma20_pct",
            "price_vs_sma200_pct",
            "realized_vol_30d",
            "volume_ratio",
            "regime",
            "halving_cycle_day",
            "seasonality_weekday",
        ],
        "defi_fundamentals_analyst": [
            "defi_tvl_total",
            "defi_tvl_change_1d_pct",
            "defi_tvl_change_7d_pct",
            "defi_stablecoin_median_apy",
            "defi_stablecoin_tvl_weighted_apy",
            "defi_stablecoin_apy_change_7d",
            "mc_tvl_ratio",
        ],
        "derivatives_analyst": [
            "derivatives_funding_rate_latest",
            "derivatives_open_interest_latest",
            "derivatives_open_interest_change_pct",
            "derivatives_long_liquidation_usd_24h",
            "derivatives_short_liquidation_usd_24h",
            "derivatives_total_liquidation_usd_24h",
        ],
        "news_analyst": [
            "latest_close",
            "return_1d_pct",
            "price_vs_sma200_pct",
            "regime",
        ],
    }
    payload = {
        "fields": {
            field: feature_summary.get(field)
            for field in field_map.get(role, [])
            if feature_summary.get(field) is not None
        },
        "coverage_gaps": coverage_gaps,
    }
    if role == "news_analyst":
        payload["evidence"] = evidence_summary
    elif evidence_summary:
        payload["evidence"] = {
            key: evidence_summary.get(key)
            for key in ("evidence_status", "source", "citations_count")
            if evidence_summary.get(key) is not None
        }
    return payload


def _synthesized_summary(
    *,
    role: str,
    memo: dict[str, object],
    feature_summary: dict[str, object],
    evidence_summary: dict[str, object],
) -> str:
    if role == "technical_analyst":
        regime = memo.get("regime") or _technical_regime(feature_summary)
        rsi = feature_summary.get("rsi_14")
        price_vs_sma200 = feature_summary.get("price_vs_sma200_pct")
        levels = memo.get("levels", {})
        support = levels.get("support", []) if isinstance(levels, dict) else []
        resistance = levels.get("resistance", []) if isinstance(levels, dict) else []
        clauses = [
            f"BTC technical setup remains {regime}.",
            f"RSI is {rsi} and price is {price_vs_sma200}% vs the 200-day trend.",
        ]
        if support or resistance:
            level_parts = []
            if support:
                level_parts.append(f"support near {support[0]:.2f}")
            if resistance:
                level_parts.append(f"resistance near {resistance[0]:.2f}")
            clauses.append("Key levels are " + " and ".join(level_parts) + ".")
        clauses.append("Base case is tactical rather than cycle-confirming unless spot holds above resistance.")
        return " ".join(clauses)

    if role == "defi_fundamentals_analyst":
        mc_tvl_ratio = feature_summary.get("mc_tvl_ratio")
        stablecoin_apy_change = feature_summary.get("defi_stablecoin_apy_change_7d")
        tvl_change = feature_summary.get("defi_tvl_change_7d_pct")
        return (
            f"DeFi fundamentals are mixed: MC/TVL is {mc_tvl_ratio}, 7d TVL change is {tvl_change}, "
            f"and stablecoin APY change is {stablecoin_apy_change}. The read does not show obvious capital stress, "
            "but it still falls short of a clean capital-expansion signal."
        )

    if role == "derivatives_analyst":
        funding = feature_summary.get("derivatives_funding_rate_latest")
        oi_change = feature_summary.get("derivatives_open_interest_change_pct")
        liq = feature_summary.get("derivatives_total_liquidation_usd_24h")
        if funding is None and oi_change is None and liq is None:
            return (
                "Derivatives conviction remains constrained because funding, open interest, and liquidation metrics "
                "are unavailable. That keeps this role in risk-control mode rather than directional confirmation."
            )
        return (
            f"Derivatives positioning shows funding={funding}, OI change={oi_change}, and liquidation flow={liq}. "
            "Use that mix to judge whether the move is being built by fresh leverage, short covering, or a fragile unwind."
        )

    if role == "news_analyst":
        evidence_status = evidence_summary.get("evidence_status")
        citations = evidence_summary.get("citations_count", 0)
        top_risks = memo.get("top_risks")
        risk_text = ""
        if isinstance(top_risks, list) and top_risks:
            first = top_risks[0]
            if isinstance(first, dict) and first.get("risk"):
                risk_text = f" Top flagged risk is {first['risk']}."
        return (
            f"Catalyst coverage is {evidence_status} with {citations} captured citations."
            f"{risk_text} The event map is useful for context, but it should only raise conviction when it clearly changes near-term flow or positioning."
        )

    return role_summary_text(memo)


def _append_call_log(
    *,
    call_log_path: Path,
    role: str,
    provider: str,
    analysis_mode: str,
    timeout_seconds: int | None,
    duration_ms: int,
    validation_error: str | None,
    fallback_reason: str | None,
    fallback_detail: str | None,
    provider_error_type: str | None,
) -> None:
    payload = {
        "role": role,
        "provider": provider,
        "analysis_mode": analysis_mode,
        "timeout_seconds": timeout_seconds,
        "duration_ms": duration_ms,
        "validation_error": validation_error,
        "fallback_reason": fallback_reason,
        "fallback_detail": fallback_detail,
        "provider_error_type": provider_error_type,
    }
    with call_log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def _salvage_narrative_generated(*, role: str, provider_meta: dict[str, object]) -> dict[str, object]:
    if role not in NARRATIVE_FIRST_ROLES:
        return {}
    raw_text = provider_meta.get("raw_text")
    if not isinstance(raw_text, str) or len(raw_text.strip()) < 40:
        return {}
    return {
        "report": raw_text.strip(),
        "confidence": "medium",
    }


def _provider_for_role(provider: AnalysisProvider, role: str) -> AnalysisProvider:
    timeout_override = ROLE_TIMEOUT_OVERRIDES.get(role)
    retry_override = ROLE_RETRY_OVERRIDES.get(role)
    if timeout_override is None and retry_override is None:
        return provider
    if not is_dataclass(provider):
        return provider
    updates: dict[str, object] = {}
    current_timeout = getattr(provider, "timeout_seconds", None)
    current_retries = getattr(provider, "max_retries", None)
    if timeout_override is not None and isinstance(current_timeout, int) and timeout_override > current_timeout:
        updates["timeout_seconds"] = timeout_override
    if retry_override is not None and isinstance(current_retries, int) and retry_override > current_retries:
        updates["max_retries"] = retry_override
    if not updates:
        return provider
    return replace(provider, **updates)


def _validate_generated_memo(
    *,
    role: str,
    fallback_memo: dict[str, object],
    generated: dict[str, object],
) -> str | None:
    if not generated:
        return None
    if role in NARRATIVE_FIRST_ROLES and (
        isinstance(_narrative_text(generated), str)
        or _has_narrative_first_metadata(generated, fallback_memo)
    ):
        if "signal" in generated and not isinstance(generated.get("signal"), str):
            return "invalid_field_type"
        if "confidence" in generated and not isinstance(generated.get("confidence"), str):
            return "invalid_field_type"
        if "referenced_fields" in generated and not isinstance(generated.get("referenced_fields"), list):
            return "invalid_field_type"
        return None
    missing_required_fields = [
        key for key in _required_output_fields(fallback_memo)
        if key not in generated
    ]
    if missing_required_fields:
        return "missing_required_fields"
    for key, fallback_value in fallback_memo.items():
        if key in SYSTEM_FIELDS or key not in generated:
            continue
        generated_value = generated[key]
        if not _matches_expected_type(fallback_value, generated_value):
            return "invalid_field_type"
    return None


def _check_citation_coverage(role: str, memo: dict[str, object]) -> str | None:
    """Returns a warning tag if key_points items are missing evidence_source, else None."""
    if role not in {"bull_researcher", "bear_researcher"}:
        return None
    key_points = memo.get("key_points")
    if not isinstance(key_points, list) or not key_points:
        return None
    missing = sum(
        1
        for point in key_points
        if isinstance(point, dict) and not point.get("evidence_source")
    )
    if missing > 0:
        return f"{missing}_of_{len(key_points)}_key_points_missing_evidence_source"
    return None


def _matches_expected_type(expected: object, actual: object) -> bool:
    if isinstance(expected, list):
        return isinstance(actual, list)
    if isinstance(expected, str):
        return isinstance(actual, str)
    if isinstance(expected, (int, float)):
        return isinstance(actual, (int, float))
    if isinstance(expected, dict):
        return isinstance(actual, dict)
    return True


def _normalize_generated_memo(
    *,
    role: str,
    fallback_memo: dict[str, object],
    generated: dict[str, object],
) -> dict[str, object]:
    report = _narrative_text(generated)
    if role in NARRATIVE_FIRST_ROLES and (
        isinstance(report, str)
        or _has_narrative_first_metadata(generated, fallback_memo)
    ):
        normalized = dict(fallback_memo)
        if isinstance(report, str):
            normalized["report"] = report
        for key, value in generated.items():
            if key in {"report", "summary", "narrative", "signal", "confidence", "referenced_fields"}:
                normalized[key] = value
                continue
            if key in fallback_memo and _matches_expected_type(fallback_memo[key], value):
                normalized[key] = value
        return normalized
    return {
        **fallback_memo,
        **generated,
    }


def final_decision_label(memo: dict[str, object]) -> str:
    decision = memo.get("decision")
    if isinstance(decision, dict):
        action = decision.get("action")
        if isinstance(action, str):
            return action
    label = memo.get("decision_label")
    if isinstance(label, str):
        return label
    if isinstance(decision, str):
        return decision
    return "unknown"


def role_summary_text(memo: dict[str, object]) -> str:
    for key in ("summary", "thesis", "fundamental_thesis", "positioning_thesis", "narrative"):
        value = memo.get(key)
        if isinstance(value, str):
            return value
    setup = memo.get("setup")
    if isinstance(setup, dict):
        thesis = setup.get("thesis")
        if isinstance(thesis, str):
            return thesis
    recommendation = memo.get("recommendation")
    if isinstance(recommendation, str):
        return recommendation
    return "Unavailable."


def risk_bias_label(memo: dict[str, object]) -> str:
    value = memo.get("risk_bias")
    if isinstance(value, str):
        return value
    cascade = memo.get("cascade_risk_level")
    if isinstance(cascade, str):
        return cascade
    return "unknown"


def _technical_regime(feature_summary: dict[str, object]) -> str:
    price_vs_sma20 = _as_float(feature_summary.get("price_vs_sma20_pct"))
    rsi_14 = _as_float(feature_summary.get("rsi_14"))
    if price_vs_sma20 > 0 and rsi_14 >= 55:
        return "bull_trend"
    if price_vs_sma20 < 0 and rsi_14 <= 45:
        return "bear_trend"
    return "range_bound"


def _available_feature_keys(summary: dict[str, object], keys: list[str]) -> list[str]:
    return [key for key in keys if summary.get(key) is not None]


def _missing_feature_keys(summary: dict[str, object], keys: list[str]) -> list[str]:
    return [key for key in keys if summary.get(key) is None]


def _defi_protocol_metrics(summary: dict[str, object]) -> list[dict[str, object]]:
    metrics: list[dict[str, object]] = []
    if summary.get("defi_tvl_total") is not None:
        metrics.append(
            {
                "name": "defi_tvl_total",
                "metric": "tvl_usd",
                "value": summary.get("defi_tvl_total"),
                "interpretation": "Aggregate protocol TVL snapshot.",
                "confidence": "med",
            }
        )
    if summary.get("defi_tvl_change_7d_pct") is not None:
        metrics.append(
            {
                "name": "defi_tvl_change_7d_pct",
                "metric": "tvl_change_7d_pct",
                "value": summary.get("defi_tvl_change_7d_pct"),
                "interpretation": "Short-term TVL trend across matched protocols.",
                "confidence": "med",
            }
        )
    return metrics


def _map_confidence(value: object) -> str:
    if value == "high":
        return "high"
    if value == "medium":
        return "med"
    return "low"


def _narrative_text(payload: dict[str, object]) -> str | None:
    for key in ("report", "summary", "narrative"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _has_narrative_first_metadata(
    generated: dict[str, object],
    fallback_memo: dict[str, object],
) -> bool:
    preferred = {"signal", "confidence", "referenced_fields"}
    if any(key in generated for key in preferred):
        return True
    allowed_structured = {
        key
        for key in fallback_memo
        if key not in SYSTEM_FIELDS
    }
    return any(key in generated for key in allowed_structured)
