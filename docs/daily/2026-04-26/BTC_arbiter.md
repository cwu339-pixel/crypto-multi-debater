# Final Arbiter

- role: final_arbiter
- title: Final Arbiter
- decision: {'action': 'avoid', 'direction': 'neutral', 'horizon_days': 7, 'position_size': 'none'}
- decision_label: avoid
- thesis: After weighing all inputs, the prudent stance is to avoid new BTC exposure at this time given significant data gaps across core technical, derivatives, and on-chain signals. The risk manager’s elevated caution and recommendation to reduce size underscores the structural uncertainty and potential latent tail risks posed by missing funding rate and open interest data. From the Aggressive perspective, while the 12-18 month post-halving window and stable DeFi TVL suggest structural support, the lack of volume and RSI blocks tactical confirmation or breakout validation. The Conservative view rightly prioritizes capital preservation amid unknown leverage and liquidity risks, favoring restraint until more complete data emerges. The neutral stance aligns with this balance, maintaining optionality but no commitment. Entry is only justified once BTC sustains closes above the 200-day SMA on strong volume coupled with restored positive derivatives funding and open interest trends, and evidence of stablecoin capital inflows, which would increase confidence materially. Until then, avoid new longs and manage existing risk tightly.
- confidence: medium
## Key Factors
- Elevated risk and structural uncertainty due to missing derivatives data (risk_manager)
- Insufficient technical confirmation from price, volume, RSI, and moving averages (technical_analyst)
- Mature but subdued DeFi environment with stagnant stablecoin APYs and lack of clear capital inflows (defi_fundamentals_analyst)
## Key Risks
- {'risk': 'Unexpected liquidation cascades or leverage deleveraging hidden by missing derivatives data', 'mitigation': 'Strict risk sizing and abstaining from new exposure until data returns', 'source_role': 'risk_manager'}
- {'risk': 'False breakout or failed trend confirmation due to absent volume and RSI signals', 'mitigation': 'Wait for strong volume and RSI confirmation above key moving averages', 'source_role': 'technical_analyst'}
- {'risk': 'Sudden DeFi capital outflows reducing ecosystem leverage and price support', 'mitigation': 'Monitor on-chain stablecoin supply and lending utilization on data restoration', 'source_role': 'defi_fundamentals_analyst'}
- entry_logic: Enter longs only after BTC closes above 200-day SMA on expanding volume (above 1.5x average) with RSI rising above 50 and positive confirmed derivatives funding rates sustained for 3+ days alongside increasing open interest indicating trend participation. Additionally, stablecoin supply metrics should confirm capital inflows to DeFi.
- stop_logic: Initial stop = 1× ATR below entry price to limit risk to one day’s volatility (~X USD). Hard stop if BTC closes below 200-day SMA on volume > average, signaling regime break.
## Targets
- sizing_formula: No new allocation until confirmed signals. Upon entry, risk 0.5–1% of portfolio per trade with position scaled by confidence: full size if strong confirmation, quarter size if marginal. Caps on total crypto exposure due to data uncertainty.
## Flip Rules
- {'condition': 'BTC sustains 5 consecutive daily closes above 200-day SMA on rising volume and RSI above 60, with positive funding rates > +0.01% sustained', 'new_posture': 'Upgrade to medium-term buy, half to full size'}
- {'condition': 'BTC closes below 200-day SMA on heavy volume (>1.5x avg) and derivatives show negative funding or surge in liquidations', 'new_posture': 'Downgrade to sell, close positions'}
- tactical_alternative: For less risk-averse mandates, consider defined-loss option structures or size exposure to quarter position with wider stops to hedge data risk while maintaining optionality.
## Invalidation
- Sustained daily closes above 200-day SMA on expanding volume
- Restoration of positive derivatives funding rate signals and open interest growth
- Stablecoin supply growth confirming capital inflows
- review_plan: {'review_at_days': 7, 'what_to_check': ['BTC price relation to 200-day SMA and volume', 'Derivatives funding rate and open interest metrics', 'DeFi stablecoin supply and lending APY trends']}
- override_note: Scorecard baseline 'avoid' decision retained due to critical data gaps and risk manager’s elevated caution overriding bullish bias from macro post-halving window and nominal DeFi fundamentals.
- rejected_alternative: {'alternative_action': 'buy', 'why_rejected': 'Lack of technical and derivatives confirmation, alongside risk management warnings and data gaps, precludes justified bullish entry at this time.'}
- summary: The integrated crypto read stays avoid: score=28, regime=range_bound, MC/TVL=None, funding=None. The system sees enough fragility to stay conservative rather than press for directional size.
## Rationale
- cautious
- coverage_gap
- insufficient_data
- elevated
- score=28
- scorecard: {'inputs': {'momentum': 45.0, 'liquidity': 35.0, 'derivatives': 35.0, 'defi': 60.0, 'onchain': 45.0, 'sentiment': 50.0, 'data_quality_penalty': -15.0}, 'final_score': 28, 'confidence': 'low', 'score_decision': 'avoid'}
- provider: openai
- analysis_mode: prompt_driven
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
    "run_id": "r_20260426T143618Z_BTC"
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
        "summary": "Current technical conditions lack sufficient direct data inputs due to significant coverage gaps (lack of volume, price action, RSI, and moving average values). Without these key metrics, regime classification is uncertain, and conviction is low. Critical indicators like RSI and SMA crossovers cannot be confirmed, and volume data required to validate breakout or breakdowns are absent. Given crypto-specific thresholds for RSI and moving averages, without price vs 200-day SMA or 50-day/40-day SMA data, trend bias cannot be established. The absence of volatility measures like ATR or BB/Keltner squeezes further obscures volatility regime assessment. Thus, no actionable internal technical signal can be reliably offered. The base case is a cautious wait for data confirmation, watching for a golden cross with strong volume (>1.5x avg) for a bullish setup or volume spikes on key support break for bearish confirmation. Monitoring macro factors\u2014DXY direction, S&P sell-offs, halving cycle phase\u2014is recommended to supplement technical framework. Invalidation of a bullish bias would occur if price closes sustainably below the 200-day SMA or if bearish RSI readings dip below 20 with volume confirming breakdowns. Coverage gaps necessitate low conviction until input data improves.",
        "signal": "cautious",
        "confidence": "medium",
        "regime": "uncertain",
        "referenced_fields": [],
        "support": null,
        "resistance": null
      },
      "defi_fundamentals_analyst": {
        "summary": "DeFi TVL stands at $552B nationally, reflecting scale but with stablecoin lending APYs subdued around 3.7%, indicative of a low leverage, risk-off environment. The slight decline in APY over the last 7 days (-0.07%) and lack of data on protocol-level fees, lending utilization, unique wallet growth, or stablecoin supply growth limits confidence in bullish DeFi narratives. Without user growth data, there is risk TVL stability masks capital concentration or passive holdings. Coverage gaps from major data providers further restrict granularity. Overall, evidence suggests a mature, low-volatility DeFi market with insufficient inflows or leverage demand, consistent with a sideways to cautious near-term stance.",
        "signal": "neutral",
        "confidence": "low",
        "stablecoin_signals": "No stablecoin supply growth data provided; unable to confirm capital inflow or outflow trends. Stability of APYs and lack of yield spikes suggests neutral to mildly bearish capital positioning.",
        "data_gaps": [
          "Lack of comprehensive user activity data preventing judgment on capital concentration and TVL quality",
          "Absence of stablecoin supply and dominance metrics restricting macro capital flow assessment",
          "Missing lending protocol utilization and big-wallet activity data limiting stress and risk insights"
        ]
      },
      "derivatives_analyst": {
        "summary": "Derivatives-based conviction for BTC on 2026-04-26 is limited due to missing data across most key metrics, including funding rates, open interest, and liquidations. Without coinglass or exchange data, key crowding and leverage signals cannot be assessed, nor can market fragility or risk of liquidation cascades be evaluated. This results in a neutral baseline stance, with only spot momentum as a very weak proxy, insufficient for directional inference. Practitioners are advised to treat current positioning as uncertain and wait for restoration of reliable derivatives feeds before committing. Key triggers that would upgrade conviction include sustained high funding, rising OI confirming genuine long trends, or large liquidation events signaling stress. Until then, derivatives-related risk management should remain cautious and rely on spot and other market signals.",
        "signal": "neutral",
        "confidence": "low",
        "positioning_thesis": "Derivatives data coverage for BTC is absent, including funding rates, open interest, liquidations, basis, and leverage metrics, constraining any confident derivative-based positioning. Without coinglass or exchange-level data, no funding or crowding signals are available. Consequently, derivatives conviction is low. The current signal is neutral by default, relying only on weak spot momentum proxy. This leads to a cautious stance with no strong lean on either long or short. Traders should rely on other data sources or wait for restored derivatives signals to better assess risk and positioning.",
        "data_gaps": [
          "Current funding rate levels and trends are unknown due to missing coinglass data",
          "Open interest size, flow, and composition are unavailable, preventing assessment of new longs vs. shorts, or fatigue",
          "Liquidations volume and long/short imbalance data are absent, hiding potential deleveraging events",
          "Futures basis and premium status cannot be evaluated to gauge institutional sentiment or euphoric greed",
          "No CVD data to confirm authenticity of price moves vs. derivative positioning"
        ]
      },
      "news_analyst": {
        "summary": "Due to a lack of current and reliable evidence, no actionable catalysts or risks for BTC can be identified within the next week. The coverage gaps and evidence status marked as a stub indicate that the analysis cannot incorporate meaningful market-moving or sector-specific events. Without additional data on regulatory developments, protocol upgrades, or macroeconomic surprises, no near-term catalyst call is warranted.",
        "signal": "monitor",
        "confidence": null,
        "evidence_quality": "stub",
        "top_risk": null
      },
      "bull_researcher": {
        "thesis": "Despite significant data gaps, the BTC macro cycle and stable DeFi conditions support a constructive outlook. The ongoing post-halving 12-18 month window has historically been the highest-probability bullish period. DeFi TVL at $552B signals strong ecosystem scale and capital presence. Stablecoin lending APYs near 3.7% reflect a healthy, low leverage environment consistent with early-stage leverage demand rather than overheating. The absence of extreme derivatives crowding or liquidations (due to data gaps) does not negate potential sustained positive funding regimes, which historically provide a bullish backdrop. Thus, while short-term signals remain uncertain due to coverage gaps, the fundamental framework supports positioned accumulation ahead of a potential mid-cycle uptrend.",
        "argument": "Bull Analyst: While the current BTC technical and derivatives data coverage is insufficient for immediate high conviction signals, the prevailing structural dynamics support a cautious bullish stance. The coin remains in the crucial 12-18 month post-halving window historically linked to upward price trends. The DeFi ecosystem\u2019s substantial TVL near $552B along with stable stablecoin lending APYs implies sound and measured leverage demand rather than exuberant overheating. Absence of extreme derivatives crowding and funding rate data is a gap, but partial evidence suggests the market is not in a clear bearish liquidating phase, aligning with a possible positive funding regime. Key near-term risk factors like price falling below 200-day SMA or capital outflows in stablecoins would undermine this view. However, barring these, the structural content favors disciplined accumulation in anticipation of a mid-cycle bullish run. Restoring derivatives and stablecoin inflow data remains critical to upgrading conviction. Absence of extreme funding rate crowding signals may actually imply a healthy, sustainable regime as per Glassnode patterns; lack of data is a limitation but does not indicate bearish positioning.",
        "confidence": "med",
        "top_point": "BTC is in the historically high-probability 12-18 month post-halving bullish window, a robust macro positive.",
        "top_rebuttal": "Absence of extreme funding rate crowding signals may actually imply a healthy, sustainable regime as per Glassnode patterns; lack of data is a limitation but does not indicate bearish positioning.",
        "data_gaps": [
          "Derivatives funding rates, open interest flow, and liquidation data",
          "Stablecoin supply growth and dominance metrics",
          "User growth and capital concentration data for DeFi protocols",
          "Technical indicators such as RSI, moving averages, volume"
        ]
      },
      "bear_researcher": {
        "thesis": "BTC\u2019s current setup is characterized by significant data gaps, notably in critical derivatives metrics such as funding rates, open interest, and liquidations, which precludes reliable assessment of market crowding or sustained bullish regimes. The large DeFi TVL figure is nominal and measured only in USD, failing to account for token price fluctuations or true capital at risk, while stablecoin lending APYs are low and declining, suggesting muted leverage and limited proto-bullish demand. The absence of volume and technical confirmation prevents validation of any sustainable breakout, and historical post-halving returns continue to diminish, cautioning against extrapolating past cycle gains. Additionally, the lack of macro and on-chain data limits safe haven or risk-on narratives. These factors, combined with unresolved coverage gaps, favor a defensive stance given elevated risk of a late-cycle fade or protracted sideways trading.",
        "argument": "Bear Analyst: BTC currently suffers from substantial data blackouts, undermining any confident bullish stance. Key derivatives metrics are missing, preventing robust assessment of funding regimes or crowding that historically precede corrections. While the DeFi ecosystem's nominal TVL suggests scale, its USD measurement and absent user growth mask underlying capital flows and potential weakness in leverage demand, further evidenced by stablecoin APYs declining slightly. Technical data gaps, notably volume and momentum indicators, obscure breakout validation; given crypto's frequent failed breakouts, this is a critical omission. The post-halving historical context, often cited as a macro bullish anchor, is weakened by the shrinking magnitude of vanilla returns over successive cycles. Thus, the current evidence tilts toward caution with elevated risk of a late-cycle fade or rangebound conditions. Only restoration of reliable derivatives data, confirmatory volume spikes on price breakouts, and real capital inflow signals would overturn this bearish base case. While the 12-18 month post-halving window is historically bullish, recent cycles show sharply diminishing returns and no guarantee of repeat magnitude; without confirming technical or derivatives signals, this macro pattern alone is insufficient to justify bullish conviction.",
        "confidence": "med",
        "top_point": "Derivatives data absence on funding rates and open interest means any bullish interpretation is unverifiable and market crowding could be hidden.",
        "top_rebuttal": "While the 12-18 month post-halving window is historically bullish, recent cycles show sharply diminishing returns and no guarantee of repeat magnitude; without confirming technical or derivatives signals, this macro pattern alone is insufficient to justify bullish conviction.",
        "data_gaps": [
          "Derivatives market data including funding rates, open interest flows, and liquidations.",
          "On-chain metrics about user growth, stablecoin supply and dominance, and capital concentration in DeFi.",
          "Comprehensive volume and technical indicators (RSI, moving averages, volume) for breakout validation.",
          "Macro correlation trends and fundamental revenue analyses of BTC protocols."
        ]
      },
      "risk_manager": {
        "summary": "BTC risk assessment for 2026-04-26 reveals high uncertainty driven by large coverage gaps in critical derivatives data (funding rates, open interest, liquidations) and incomplete technical signals (volume, RSI, moving averages). This severely limits confidence in detecting leverage-induced crowding or liquidation cascade risk, essential in crypto given historical drawdowns and rapid deleveraging risk. DeFi fundamentals show a mature, low-volatility environment but lack user activity and capital flow data to clarify leverage shifts or fragility. Correlation risk remains elevated as altcoins heavily track BTC and macro cross-asset shocks (SPX) remain a tail risk. Single-position risk should strictly adhere to existing sizing rules with volatility scaling due to absent volatility regime indicators. Portfolio drawdown rules mandate review and size reduction if interim losses approach typical -5% and -10% thresholds. Operational risks include inability to verify exchange or protocol-level anomalies due to missing analytics. Cascade risk is elevated given unknown leverage and open interest conditions, plus no data refutation of alignment of multiple negative catalysts. Recommendation is to reduce position size and leverage exposure until derivatives and technical data restore visibility. Key to upgrading outlook are restoration of derivatives metrics showing moderate funding dynamics and open interest without excessive leverage, more granular DeFi user and stablecoin supply data, and confirmation of sustainable volume-backed technical price action. Invalidating the cautious stance would be emergence of large, sustained funding rate spikes or significant derivative liquidations suggesting imminent deleveraging.",
        "recommendation": "reduce_size",
        "risk_bias": "elevated",
        "cascade_risk_level": "elevated",
        "aggressive_view": "Aggressive Analyst: Despite significant data gaps\u2014missing critical technical indicators (RSI, volume, SMA), derivatives data (funding rates, open interest), and insufficient on-chain signals\u2014the BTC setup warrants pressing risk moderately now rather than excessive caution. The absence of extreme derivatives crowding or liquidation signals arguably reduces immediate systemic risk, while the ongoing 12-18 month post-halving window historically favors accumulation. Waiting for full volume and RSI confirmation risks missed entry points since crypto\u2019s volatility and price asymmetry favor early positioning with measured sizing. Limited confirmation such as stable DeFi TVL near $552B with stablecoin lending APYs around 3.7%, and historical macro cycle context, provide enough foundation to tactically increase exposure while managing risk via tight stops and scaling. Excessive hesitation driven by data absence is a self-imposed latency that can forfeit outsized mid-cycle gains. What would change this aggressive stance is visible sustained price closure below the 200-day SMA on strong volume, restoration of derivatives data showing persistent negative funding or large liquidation cascades, or clear on-chain capital outflows. Until such invalidations emerge, layering risk incrementally on this constructive but data-imperfect setup aligns with alpha-seeking behavior.",
        "conservative_view": "Conservative Analyst: Given BTC's current data blackout\u2014lacking critical derivatives metrics (funding rates, open interest, liquidations), technical confirmations (volume, RSI, SMA), and comprehensive on-chain user or stablecoin supply data\u2014risk management must prioritize capital preservation. The nominal $552B DeFi TVL in USD terms does not reveal real capital quality or inflows and paired with declining stablecoin lending APYs suggests subdued leverage demand and limited bullish conviction. Absent derivatives data obscures crowding, leverage, and liquidation risk, making unknown systemic fragility a material threat. Technical indicators vital to confirming breakouts and regime shifts are missing; given crypto\u2019s high failure rate of breakouts without volume confirmation, this raises the likelihood of false signals. Furthermore, post-halving diminishing returns caution against over-reliance on historical bullish cycles without confirming present data. The fragile structure and severe coverage gaps amplify tail risk of sharp drawdowns or prolonged sideways movement. The prudent stance is to limit or avoid fresh BTC exposure until derivative metrics and technical confirmations return. A strict stop-loss regime keyed to 200-day SMA breaches on strong volume is essential. This conservative posture maximizes capital preservation amid structural uncertainty and incomplete data. Conviction would improve only with restored derivatives signals showing stable positive funding and open interest indicating genuine trend participation, volume-backed technical breakouts, and evidence of stablecoin capital inflows supporting leverage expansion. Until such data is available, restraint is warranted.",
        "neutral_view": "Neutral Analyst: Given the pronounced data gaps across critical BTC technical indicators (RSI, volume, SMA), derivatives metrics (funding rates, open interest, liquidations), and on-chain capital flows, a balanced stance favors disciplined caution over aggressive positioning in the coming week. The bull case leans on the historically supportive 12-18 month post-halving window, stable DeFi TVL (~$552B), and moderate stablecoin lending APYs (~3.7%) implying subdued but steady ecosystem engagement. However, the bear case rightly highlights that missing derivatives data obscures leverage, crowding, and liquidation risk, while absent volume and price trend confirmations limit breakout reliability. Without firm confirmation, reliance on nominal DeFi TVL and macro cycle alone risks overextension. The prudent approach is to maintain low exposure, apply strict risk controls keyed to strong volume-confirmed price support levels (notably the 200-day SMA), and await restoration of derivatives and technical data to reassess trend conviction. Key invalidation triggers include sustained BTC closes below 200-day SMA on heavy volumes, negative derivatives funding signals if restored, and meaningful DeFi capital outflows. This neutral posture manages latent risk under uncertainty while preserving optionality for a mid-cycle bullish acceleration should data improve. Confidence remains low due to data gaps."
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
## Referenced Fields
- report: The integrated crypto read stays avoid: score=28, regime=range_bound, MC/TVL=None, funding=None. The system sees enough fragility to stay conservative rather than press for directional size.
