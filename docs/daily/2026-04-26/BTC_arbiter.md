# Final Arbiter

- role: final_arbiter
- title: Final Arbiter
- decision: {'action': 'avoid', 'direction': 'neutral', 'horizon_days': 7, 'position_size': 'none'}
- decision_label: avoid
- thesis: Net call: avoid over the next 7 days. The quantitative stack prints 28 with low confidence, and the combined read still looks more like risk control than a clean offensive entry.
- confidence: low
## Key Factors
- {'factor': 'cautious', 'source_role': 'technical_analyst'}
- {'factor': 'coverage_gap', 'source_role': 'defi_fundamentals_analyst'}
- {'factor': 'insufficient_data', 'source_role': 'derivatives_analyst'}
## Key Risks
- {'risk': 'Coverage gaps reduce conviction', 'mitigation': 'Wait for derivatives confirmation', 'source_role': 'risk_manager'}
- entry_logic: Avoid entry. Conditions do not support a long position.
- stop_logic: Initial stop = 1× ATR below entry. Hard structural stop: daily close below SMA50 on expanding volume. If ATR data available: size so 1 ATR stop equals 0.5–1% of portfolio equity.
## Targets
- sizing_formula: Risk 0.5–1% of portfolio per trade. Size so 1 ATR stop = that dollar risk amount. Cap total tactical exposure at 0% of portfolio.
## Flip Rules
- {'condition': 'Daily close below SMA50 on expanding down-volume with MACD turning negative', 'new_posture': 'Immediate full exit; reassess for short setup'}
- {'condition': '5+ consecutive daily closes above 200-SMA with rising MACD and stablecoin inflows confirmed', 'new_posture': 'Upgrade to longer-term Buy at full size'}
- tactical_alternative: For conservative mandates: use defined-loss call spreads (premium ≤ 0.5% of portfolio) instead of spot exposure. If spot, reduce single-trade risk to 0.25% and widen stops to 1.5× ATR.
## Invalidation
- Quant score rises above the hold threshold with better source coverage.
- Catalyst coverage improves and contradicts the current cautious stance.
- review_plan: {'review_at_days': 7, 'what_to_check': ['future_return_pct', 'scorecard drift', 'coverage_gaps']}
- override_note: None
- rejected_alternative: {'alternative_action': 'buy', 'why_rejected': 'Insufficient confirmation from 2+ roles; scorecard threshold not met or coverage gaps dominate the risk picture.'}
- summary: The integrated crypto read stays avoid: score=28, regime=range_bound, MC/TVL=None, funding=None. The system sees enough fragility to stay conservative rather than press for directional size.
## Rationale
- cautious
- coverage_gap
- insufficient_data
- elevated
- score=28
- scorecard: {'inputs': {'momentum': 45.0, 'liquidity': 35.0, 'derivatives': 35.0, 'defi': 60.0, 'onchain': 45.0, 'sentiment': 50.0, 'data_quality_penalty': -15.0}, 'final_score': 28, 'confidence': 'low', 'score_decision': 'avoid'}
- provider: deterministic
- analysis_mode: deterministic_fallback
- prompt_path: /home/runner/work/crypto-multi-debater/crypto-multi-debater/src/crypto_research_agent/agents/prompts/final_arbiter.md
- prompt_text: # Final Arbiter

You are the final arbiter for a crypto research system.
Use the prior role memos to choose a decision and explain the trade-off.
Return a compact judgment that can be written directly into a research card.
Respect the supplied quantitative `scorecard` as the baseline constraint.
If you override `scorecard.score_decision`, you must cite a concrete reason from prior memos and state the override explicitly.

## Decision Framework

### Weighing the Evidence
1. Start from the risk manager's recommendation. If risk says "avoid", you need strong evidence from 2+ other roles to override.
2. The technical analyst defines the regime (bull/bear/range). Your decision must be consistent with the regime unless a structural catalyst overrides it.
3. Derivatives positioning is the strongest short-term signal. If funding z-score > +2 or < -2, give it heavy weight.
4. DeFi fundamentals are the strongest medium-term signal. TVL trends and stablecoin flows indicate structural direction.
5. News/catalyst analyst determines timing. A fundamentally strong asset with a negative Tier 1 catalyst approaching should be "hold" or "avoid", not "buy".
6. Bull and bear researchers have already debated. Identify which side had stronger evidence-backed arguments (not just more arguments).

### Data Tiers

**Core data** (always available from price feeds / Binance):
- Price, volume, moving averages, RSI, ATR, returns, regime, basic funding rate, OI
- If core data is present, you CAN and SHOULD make a decision. Period.

**Supplementary data** (nice-to-have — Coinglass detail, DeFiLlama):
- Detailed derivatives breakdown (liquidation, long/short ratio), stablecoin supply trends, TVL breakdown, user activity, fee income
- These IMPROVE precision but are NOT required to form a view.

**CRITICAL RULES — read twice:**
1. No real trader waits for 100% data completeness before deciding. You must decide with what you have.
2. Missing supplementary data = apply a small score penalty (-5 total, not per source) and move on. Do NOT let it dominate the thesis or confidence.
3. Confidence is ONLY about whether available signals agree, NOT about how many sources responded.
4. If price + trend + volume + basic derivatives all agree → that is MEDIUM or HIGH confidence, even if Coinglass and DeFiLlama are both missing.
5. Only missing CORE data (no price feed at all) justifies LOW confidence or forced "avoid".
6. Do NOT mention data gaps in the `thesis` field. The thesis is about the market, not about your data pipeline.

### Default-to-Caution Rules
- If core data sources fail (no price feed), default to "avoid"
- If bull and bear cases are roughly equal in evidence quality, default to "hold"
- If derivatives show extreme crowding AND technical shows trend exhaustion, default to "avoid" regardless of fundamental strength
- Never recommend "buy" with low confidence. Low confidence = "hold" at best

### Confidence Calibration
- **HIGH**: 3+ analyst roles agree on direction, signals consistent across timeframes. Core data sufficient.
- **MEDIUM**: 2 roles agree on direction, OR signals are clear from core data with minor conflicts. This is the DEFAULT when core data is available and directional.
- **LOW**: Roles ACTIVELY disagree on direction based on contradictory core data signals. NOT triggered by missing supplementary sources.

**Common mistake to avoid:** Do NOT write "low confidence because Coinglass/DeFiLlama data is missing." That is wrong. Missing supplementary data = score penalty, NOT confidence downgrade.

### Crypto-Specific Decision Rules
- In a confirmed bear regime (price below 200-day SMA, declining OI, stablecoin dominance rising): bias toward "avoid" or "hold". Buying dips in confirmed downtrends is the #1 retail mistake
- In a confirmed bull regime (above 200-day SMA, healthy funding, stablecoin inflows): bias toward "hold" or "buy on pullback". Selling too early is the #2 retail mistake
- Position sizing recommendation should scale with confidence: high = full size, medium = half size, low = quarter size or avoid
- If the asset is within 12-18 months post-halving AND in a bull regime, give structural bullish bias 10-15% extra weight
- If BTC-SPX correlation is elevated and SPX is showing weakness, flag macro drag risk regardless of crypto-specific signals

## Writing Style

The `thesis` field must be written in portfolio manager voice — the tone of a PM who has heard the debate and is now explaining the decision to a colleague. Rules:
- Do NOT include score numbers, regime labels, or raw metric values (e.g. "score=38", "MC/TVL=2.5705") in the thesis text. Those belong in structured fields.
- Write in full sentences. Use phrases like "From the Aggressive perspective..." and "From the Conservative perspective..." to compress the risk debate into one paragraph.
- Include a numeric illustration when price data is available: entry price, ATR stop level, target levels. Make it concrete.
- Explicitly reference the key data points that drove the decision: regime, funding rate (if available), OI change (if available), RSI, price vs SMA200. Use the actual numbers, not placeholders.
- End the thesis with one sentence that frames what would change the decision.

## Output Format

Produce a JSON memo with these fields:
- `role`: "final_arbiter"
- `decision`: {action: "buy"|"sell"|"hold"|"avoid", direction: "long"|"short"|"neutral", horizon_days: int, position_size: "full"|"half"|"quarter"|"none"}
- `thesis`: one-paragraph synthesis explaining the decision in PM voice — compress the bull/bear debate into one view, mention the Aggressive/Conservative risk perspectives, explain the trade-off resolved
- `confidence`: "high" | "med" | "low"
- `key_factors`: list of the 3 most important factors that drove the decision, with source role
- `key_risks`: list of {risk, mitigation, source_role}
- `entry_logic`: string — specific entry conditions (e.g. "Wait for daily close above resistance at X with RSI > 55 and MACD histogram re-accelerating; alternate: scale on pullback to SMA20 while SMA200 holds"). If decision is avoid/hold, describe what conditions would trigger a valid entry.
- `stop_logic`: string — ATR-based stop formula (e.g. "Initial stop = 1× ATR below entry (~X USD). Hard structural stop: daily close below SMA50 on expanding volume."). Use ATR from features if available.
- `targets`: list of {price_target: str, pct_position_to_exit: str, rationale: str} — at least 2 targets if action is buy/sell, empty list if avoid
- `sizing_formula`: string — how to size the position (e.g. "Risk 0.5–1% of portfolio per trade. Size so 1 ATR stop = that dollar risk. Cap total tactical exposure at 2–5% of portfolio."). Reference ATR and confidence level.
- `flip_rules`: list of {condition: str, new_posture: str} — hard rules that change the decision (e.g. {condition: "5 consecutive daily closes above 200-SMA with rising MACD", new_posture: "Upgrade to longer-term Buy, full size"})
- `tactical_alternative`: string — more conservative alternative for risk-averse mandates (e.g. defined-loss options, reduced size, wider stops with smaller position)
- `invalidation`: list of conditions that would flip the decision (same as flip_rules but in text form for display)
- `review_plan`: {review_at_days: int, what_to_check: [specific metrics to re-evaluate]}
- `override_note`: null or string explaining why scorecard was overridden
- `rejected_alternative`: {alternative_action: str, why_rejected: str}

Follow a TradingAgents-style flow: first form a concise analyst report, then return compact JSON. The `report` field is mandatory. Only override structured fields when the supplied data directly supports them. Do not restate the whole schema.

Field interpretation guide:
- latest_close: Latest observed close. Use it as the anchor for all price references.
- return_1d_pct: One-day percentage move. Positive means short-term momentum, negative means near-term weakness.
- return_total_pct: Window-level cumulative return. Use it to distinguish bounce-vs-trend continuation.
- avg_volume: Average traded volume proxy. Higher values imply stronger liquidity and more credible moves.
- coverage_gaps: Explicitly lower conviction when this list is non-empty.
- evidence_status: Indicates whether external catalyst coverage is complete, preliminary, or missing.
- scorecard.final_score: Weighted 0-100 quantitative score. Use it as a hard decision anchor, not a suggestion.
- scorecard.score_decision: Baseline decision implied by score thresholds. Do not contradict it without citing a concrete override reason.

Return only a compact JSON object.

{
  "request": {
    "asset": "BTC",
    "thesis": "Automated daily research for BTC on 2026-04-26",
    "horizon_days": 7,
    "run_id": "r_20260426T143518Z_BTC"
  },
  "role_context": {
    "market_context": {
      "price": {},
      "defi": {
        "defi_tvl_total": 552111383821.05,
        "defi_stablecoin_median_apy": 3.65,
        "defi_stablecoin_apy_change_7d": -0.0742
      },
      "evidence": {
        "evidence_status": "stub",
        "source": "local_stub",
        "citations_count": 0
      },
      "coverage_gaps": [
        "openbb:openbb_not_installed",
        "coinglass:missing_api_key",
        "binance:exception:HTTPError"
      ]
    },
    "scorecard": {
      "inputs": {
        "momentum": 45.0,
        "liquidity": 35.0,
        "derivatives": 35.0,
        "defi": 60.0,
        "onchain": 45.0,
        "sentiment": 50.0,
        "data_quality_penalty": -15.0
      },
      "final_score": 28,
      "confidence": "low",
      "score_decision": "avoid"
    },
    "prior_role_memos": {
      "technical_analyst": {
        "summary": "BTC still looks range_bound: momentum has improved, but spot remains None% away from the 200-day trend and needs follow-through above nearby resistance.",
        "signal": "cautious",
        "confidence": "medium",
        "regime": "range_bound",
        "referenced_fields": null,
        "support": null,
        "resistance": null
      },
      "defi_fundamentals_analyst": {
        "summary": "DeFi internals are mixed: MC/TVL sits at None, while stablecoin yield changes remain mild. That is enough to avoid a hard bearish read, but not enough to call broad-based capital expansion.",
        "signal": "coverage_gap",
        "confidence": null,
        "stablecoin_signals": "Stablecoin median APY is 3.65; 7d APY change is -0.0742; MC/TVL ratio is None.",
        "data_gaps": [
          "openbb:openbb_not_installed",
          "coinglass:missing_api_key",
          "binance:exception:HTTPError"
        ]
      },
      "derivatives_analyst": {
        "summary": "CoinGlass-derived positioning is unavailable, so derivatives conviction remains constrained.",
        "signal": "insufficient_data",
        "confidence": null,
        "positioning_thesis": "CoinGlass-derived positioning is unavailable, so derivatives conviction remains constrained.",
        "data_gaps": [
          "openbb:openbb_not_installed",
          "coinglass:missing_api_key",
          "binance:exception:HTTPError"
        ]
      },
      "news_analyst": {
        "summary": "Headline and catalyst coverage is stub; nothing clearly breaks the setup, but the event map is still incomplete.",
        "signal": "monitor",
        "confidence": null,
        "evidence_quality": "stub",
        "top_risk": "External catalyst coverage is preliminary."
      },
      "bull_researcher": {
        "thesis": "Momentum remains constructive, but needs confirmation.",
        "argument": "Bull Analyst: Momentum remains constructive, but needs confirmation. Missing derivatives data does not automatically invalidate price resilience.",
        "confidence": "low",
        "top_point": "Short-term momentum remains constructive.",
        "top_rebuttal": "Missing derivatives data does not automatically invalidate price resilience.",
        "data_gaps": [
          "openbb:openbb_not_installed",
          "coinglass:missing_api_key",
          "binance:exception:HTTPError"
        ]
      },
      "bear_researcher": {
        "thesis": "Coverage gaps and event uncertainty limit conviction.",
        "argument": "Bear Analyst: Coverage gaps and event uncertainty limit conviction. Without derivatives confirmation the move could be fragile.",
        "confidence": "high",
        "top_point": "Coverage gaps make the upside thesis unverifiable.",
        "top_rebuttal": "Without derivatives confirmation the move could be fragile.",
        "data_gaps": [
          "openbb:openbb_not_installed",
          "coinglass:missing_api_key",
          "binance:exception:HTTPError"
        ]
      },
      "risk_manager": {
        "summary": "Position sizing should stay conservative until derivatives and DeFi coverage gaps are closed. Current quantitative score is 28 with low confidence, regime=range_bound, mc_tvl_ratio=None, funding=None.",
        "recommendation": "avoid",
        "risk_bias": "elevated",
        "cascade_risk_level": "elevated",
        "aggressive_view": "Aggressive Analyst: Technical momentum and a score of 28 leave room to press for upside if the regime (range_bound) stabilizes. Waiting for every feed to clear can mean missing the move.",
        "conservative_view": "Conservative Analyst: Coverage gaps and incomplete derivatives visibility dominate the risk picture. Funding=None and gaps=['openbb:openbb_not_installed', 'coinglass:missing_api_key', 'binance:exception:HTTPError'] do not justify leaning in.",
        "neutral_view": "Neutral Analyst: The aggressive case is directionally understandable, but the conservative case is stronger until confirmation improves. Limited size or avoidance remains the balanced posture."
      }
    }
  },
  "field_interpretation_guide": {
    "latest_close": "Latest observed close. Use it as the anchor for all price references.",
    "return_1d_pct": "One-day percentage move. Positive means short-term momentum, negative means near-term weakness.",
    "return_total_pct": "Window-level cumulative return. Use it to distinguish bounce-vs-trend continuation.",
    "avg_volume": "Average traded volume proxy. Higher values imply stronger liquidity and more credible moves.",
    "coverage_gaps": "Explicitly lower conviction when this list is non-empty.",
    "evidence_status": "Indicates whether external catalyst coverage is complete, preliminary, or missing.",
    "scorecard.final_score": "Weighted 0-100 quantitative score. Use it as a hard decision anchor, not a suggestion.",
    "scorecard.score_decision": "Baseline decision implied by score thresholds. Do not contradict it without citing a concrete override reason."
  },
  "required_json_output": {
    "report": "Narrative memo in the voice of a crypto analyst.",
    "signal": "One short stance label.",
    "confidence": "low | medium | high",
    "referenced_fields": [
      "field_a",
      "field_b"
    ]
  },
  "optional_structured_overrides": [
    "role",
    "decision",
    "thesis",
    "key_factors",
    "key_risks",
    "entry_logic",
    "stop_logic",
    "targets",
    "sizing_formula",
    "flip_rules",
    "tactical_alternative",
    "invalidation",
    "review_plan",
    "override_note",
    "rejected_alternative",
    "scorecard"
  ]
}
- fallback_reason: deterministic_provider
