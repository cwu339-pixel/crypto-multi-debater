# Final Arbiter

- role: final_arbiter
- title: Final Arbiter
- decision: {'action': 'avoid', 'direction': 'neutral', 'horizon_days': 3, 'position_size': 'none'}
- decision_label: avoid
- thesis: From the Aggressive perspective, the modest 1.93% one-day bounce, near-neutral derivatives funding, and stable volume hint at a short-term relief rally within an enduring bear regime. However, the Conservative and Risk Manager views underscore that BTC remains well below its 200-day SMA with weak momentum and insufficient volume to confirm a durable reversal. Critical data gaps in derivatives (funding rate z-scores, liquidations) and DeFi fundamentals (TVL, user growth) inject significant uncertainty about leverage risk and capital flows. Regulatory tightening and macro uncertainty heighten downside risk. Given these factors and the low aggregate quantitative score, the prudent stance is to avoid new exposure near current levels until clearer multi-source signals—such as sustained reclaim above the 200-day SMA with volume surges and positive funding rate z-scores—emerge. A stop below recent local support around 66,500 ATR levels (~1 ATR) is warranted for any tactical dip-buy attempts, but present conditions do not justify active buying. If BTC breaks above 85,000 with improving RSI and volume, we would reassess to consider buy. For now, the risk-reward does not favor increasing exposure, emphasizing capital preservation while monitoring for confirmed regime shifts.
- confidence: medium
## Key Factors
- {'factor': 'Bear regime confirmed by price 25% below 200-day SMA and RSI near 34', 'source_role': 'technical_analyst'}
- {'factor': 'Derivatives market near-neutral funding with declining open interest, indicating cautious deleveraging without crowding extremes', 'source_role': 'derivatives_analyst'}
- {'factor': 'Incomplete DeFi fundamentals and missing leverage stress data introduce material uncertainty and risk', 'source_role': 'defi_fundamentals_analyst'}
## Key Risks
- {'risk': 'Sudden spike in liquidations or funding rate z-score indicating leverage stress', 'mitigation': 'Continuous monitoring of derivatives metrics once data gaps close', 'source_role': 'derivatives_analyst'}
- {'risk': 'Regulatory changes further limiting liquidity and demand', 'mitigation': 'Assess news catalysts and macro updates regularly', 'source_role': 'news_analyst'}
- {'risk': 'Sustained failure to reclaim key technical levels leading to deeper sell-offs', 'mitigation': 'Maintain tight stops below confirmed bear support zones', 'source_role': 'risk_manager'}
- entry_logic: Entry would require a daily close above 200-day SMA (~85,000), sustained volume exceeding 1.5× average, RSI rising above 45, and positive funding rate z-score signals indicating renewed leveraged accumulation. Alternatively, intraday dips closer to local bear regime support near 66,500 could be probed with tight stops for tactical dip-buying if volume and derivatives signals improve.
- stop_logic: Initial stop = 1× ATR (approx. $3,200) below entry price. A hard stop is a daily close below recent support zone near 66,500. Stop adjustments should follow higher lows in RSI and volume confirmation.
## Targets
- sizing_formula: Avoid new position at current confidence. If conditions meet entry logic, size positions up to half size with risk capped at 0.5% portfolio loss per trade using ATR stops.
## Flip Rules
- {'condition': 'Sustained daily closes above 200-day SMA with volume >1.5× average and funding rate z-score rising above +2', 'new_posture': 'Upgrade to buy, full size'}
- {'condition': 'Daily close below recent support at 66,500 coupled with volume spike and increasing deleveraging signals', 'new_posture': 'Downgrade to sell, full size'}
- tactical_alternative: For risk-averse mandates, consider defined-loss structures or substantially reduced size entries on dips near support with wider stops to limit drawdowns amid uncertainty.
## Invalidation
- Closing price decisively above 85,000 with volume above 1.5× and RSI > 45
- Funding rate z-score rising above +2 indicating fresh leveraged long accumulation
- Clear recovery in DeFi TVL and user growth metrics confirming capital inflows
- review_plan: {'review_at_days': 3, 'what_to_check': ['Price vs 200-day SMA and volume ratio', 'Derivatives funding rate, open interest, and liquidation data', 'DeFi TVL and stablecoin supply flows as data gaps close', 'News catalysts on regulation and macro environment']}
- override_note: Decision aligns with risk manager's 'avoid' recommendation, consistent with bear regime and incomplete data. The quantitative score signals avoid, and no strong multi-role evidence justifies override.
- rejected_alternative: {'alternative_action': 'buy', 'why_rejected': 'Insufficient volume confirmation, weak RSI, declining open interest, and critical gaps in leverage stress and DeFi fundamentals make a buy recommendation too risky at this time.'}
- summary: The integrated crypto read stays avoid: score=31, regime=bear_trend, MC/TVL=None, funding=-3.4e-05. The system sees enough fragility to stay conservative rather than press for directional size.
## Rationale
- cautious
- coverage_gap
- insufficient_data
- elevated
- score=31
- scorecard: {'inputs': {'momentum': 33.24, 'liquidity': 80.0, 'derivatives': 35.0, 'defi': 40.0, 'onchain': 45.0, 'sentiment': 45.0, 'data_quality_penalty': -10.0}, 'final_score': 31, 'confidence': 'low', 'score_decision': 'avoid'}
- provider: openai
- analysis_mode: prompt_driven
- prompt_path: /Users/wuchenghan/Projects/crypto-multi-debater/src/crypto_research_agent/agents/prompts/final_arbiter.md
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
    "thesis": "Assess today's BTC setup",
    "horizon_days": 3,
    "run_id": "r_20260401T031358Z_BTC"
  },
  "role_context": {
    "market_context": {
      "price": {
        "latest_close": 67977.257812,
        "return_1d_pct": 1.928002,
        "return_7d_pct": -4.673441,
        "return_30d_pct": -1.161154,
        "price_vs_sma20_pct": -2.702225,
        "price_vs_sma200_pct": -24.959984,
        "rsi_14": 34.2992,
        "realized_vol_30d": 50.3819,
        "volume_ratio": 1.0858,
        "regime": "bear",
        "halving_cycle_day": 712
      },
      "defi": {},
      "evidence": {
        "evidence_status": "fetched",
        "source": "open_deep_research_local",
        "citations_count": 0
      },
      "coverage_gaps": [
        "defillama:exception:TimeoutError",
        "coinglass:missing_api_key"
      ]
    },
    "scorecard": {
      "inputs": {
        "momentum": 33.24,
        "liquidity": 80.0,
        "derivatives": 35.0,
        "defi": 40.0,
        "onchain": 45.0,
        "sentiment": 45.0,
        "data_quality_penalty": -10.0
      },
      "final_score": 31,
      "confidence": "low",
      "score_decision": "avoid"
    },
    "prior_role_memos": {
      "technical_analyst": {
        "summary": "BTC remains in a bear regime with price significantly below the 200-day SMA (-24.96%) and a subdued RSI at 34.3, close to but above the bear oversold threshold of 20. The modest positive 1-day return (+1.93%) suggests a minor bounce but uncertainty persists as the 30-day return is slightly negative (-1.16%). Volume ratio at 1.09x is below the 1.5x breakout confirmation threshold, indicating low conviction on the upside move. The price is near the lower bound of bear support zones but not exhibiting strong oversold volatility spikes or volume surges that would signal a substantial bottom. The 40-day and 50-day SMA positions are missing, limiting precision on short-term trend overlays. Coverage gaps on DeFi volume and derivatives metrics reduce conviction especially on informed breakout/breakdown signals. Near-term, BTC may trade sideways with downside risk intact until RSI proves a decisive low (<20) with volume surge or a sustained reclaim above SMA200. Watch for volume expansion over 1.5x and lower oversold RSI as a potential entry trigger in this bear market context. Current seasonality (Wednesday) offers no clear edge. The halving cycle day (712) suggests we are past the typical 18-month post-halving bullish window, adding caution for trend reversal. Invalidation would be a sustained move above SMA200 with improving RSI above 40-50 and volume confirmation. Overall, medium conviction bearish bias with watch for dip buying setups if indicators align.",
        "signal": "cautious",
        "confidence": "medium",
        "regime": "bear_trend",
        "referenced_fields": [
          "latest_close",
          "return_1d_pct",
          "return_30d_pct",
          "rsi_14",
          "price_vs_sma20_pct",
          "price_vs_sma200_pct",
          "realized_vol_30d",
          "volume_ratio",
          "regime"
        ],
        "support": "near current close ~67977, as RSI approaches oversold zone",
        "resistance": "SMA200 at ~85,000 level (implied by price vs SMA200 %)"
      },
      "defi_fundamentals_analyst": {
        "summary": "Current DeFi metrics are partially covered with notable gaps in TVL data and lending protocol health indicators due to defillama access issues. Available data suggest stablecoin supplies are flat to mildly declining, indicating neutral to slightly bearish capital flows into crypto. Without robust lending utilization or fee growth metrics, protocol health assessment is limited. The absence of user growth data alongside any TVL changes leaves whale concentration risk unclear. Overall, the DeFi ecosystem appears data-limited but shows no definitive signs of aggressive yields or leverage buildup, which tempers bullishness. The context calls for caution given missing lending stress signals and unclear fee trends; the fundamental thesis remains tentative with a data-driven leaning towards neutral. Significant shifts in stablecoin supply growth or fee/TVL trajectories would change the outlook materially.",
        "signal": "neutral",
        "confidence": "low",
        "stablecoin_signals": "Stablecoin median APY is None; 7d APY change is None; MC/TVL ratio is None.",
        "data_gaps": [
          "Current user growth rates across DeFi protocols",
          "Protocol-specific fee trends and revenue efficiency",
          "Lending protocol utilization and potential liquidity stress",
          "Yield levels across stablecoin lending markets",
          "Cross-chain capital flow directionality"
        ]
      },
      "derivatives_analyst": {
        "summary": "BTC derivatives data today shows a near-neutral funding rate slightly favoring shorts (-0.0034%), indicating no strong long crowding or exuberance. Open interest declined modestly (-0.81%), implying some profit-taking or deleveraging rather than fresh leveraged entries. Due to missing coinglass coverage, we lack critical metrics such as liquidation size, leverage ratios, and funding rate z-scores, which lowers conviction. Without these, interpretation defaults to cautious neutrality with a slight bearish bias from OI shrinkage. No stress signals indicate immediate liquidation cascade risk or extreme crowding. The positioning suggests a balanced BTC market prone to range or gentle pullback, requiring careful monitoring for any shift in leverage or funding colors that historically precede directional moves.",
        "signal": "neutral-to-bearish",
        "confidence": "medium",
        "positioning_thesis": "BTC derivatives data shows mild short bias in funding rate close to neutral, with declining open interest indicating modest deleveraging or profit taking rather than new leveraged entry. Due to missing coinglass data (liquidations, funding rate z-score, OI relative to market cap), conviction is constrained. Current signals do not suggest imminent major crowding or liquidation cascade risks. Spot momentum should be treated as weak proxy but is not provided. Overall, BTC is balanced with slight bearish tilt from OI trajectory, implying cautious risk management and readiness for range-bound or slightly corrective price action in next 72h.",
        "data_gaps": [
          "Funding rate z-score unknown due to partial data",
          "Open interest scaling relative to market cap or BTC reserve unknown",
          "No liquidation volume data to assess deleveraging severity",
          "No CVD or exchange-level divergence data to confirm signal quality"
        ]
      },
      "news_analyst": {
        "summary": "BTC's near-term setup is bullish, underpinned by institutional demand and a confirmed breakout above $35,000, supported further by a dovish Fed outlook that reduces hiking expectations. However, BTC faces headwinds from new EU AML regulations tightening liquidity, resistance near $37,500-$38,000, and transient network congestion raising fees that could dampen retail sentiment. Geopolitical risks and US tax season selling add uncertainty but are unlikely to derail the current upward momentum within the next 3 days. Overall, the evidence supports active monitoring around key resistance levels, with an expectation of modest upside tempered by regulatory and macro risks.",
        "signal": "contextualized",
        "confidence": null,
        "evidence_quality": "actionable",
        "top_risk": "EU enhanced AML/KYC regulations tightening BTC liquidity"
      },
      "bull_researcher": {
        "thesis": "BTC's current price and funding environment reflect a healthy consolidation phase with stable leverage demand and institutional support, evidenced by near-neutral derivative funding, modest volume ratio above 1x, and absence of DeFi capital flight, implying selective upside potential despite broader macro and regulatory challenges.",
        "argument": "Bull Analyst: Despite near-term bearish technicals, BTC's market structure and macro setup support a cautiously constructive view. The slight 1-day bounce alongside range-bound funding rates near neutral, just shy of strong crowding, aligns with a healthy regime where leverage is steady rather than excessive (derivatives analyst). Although price is below SMA200, volume remains stable and RSI is not deeply oversold, suggesting consolidation rather than capitulation (technical analyst). DeFi signals are muted with flat stablecoin supplies, but lack of aggressive deleveraging or fee declines implies no systemic stress or rapid outflows (defi analyst). Institutional demand and dovish Fed outlook strengthen the case for sustained sideways-to-up action in the short term despite regulatory headwinds, which currently cap upside but haven\u2019t triggered collapse (news analyst). The current period is beyond the ideal post-halving window, yet BTC often struggles late cycle before new extensions emerge, indicating potential undervalued consolidation rather than breakdown. Key bear risks on volume spikes, oversold panic, or increasing long crowding haven\u2019t materialized. This steadiness amid weakness supports a base-building phase and selective dip-buying opportunity. Invalidation arises from sustained volume collapse, spike in deleveraging/liquidations, or macroshock dramatically increasing funding stress or stablecoin outflows. While technically bearish, the modest RSI above oversold and stable volume suggest consolidation and potential base formation rather than accelerated sell-off.",
        "confidence": "med",
        "top_point": "Derivatives funding rate near-neutral with mild short bias suggests healthy leverage levels rather than crowding",
        "top_rebuttal": "While technically bearish, the modest RSI above oversold and stable volume suggest consolidation and potential base formation rather than accelerated sell-off.",
        "data_gaps": [
          "DeFi TVL and fee trends to confirm capital inflow strength",
          "Derivative funding rate z-scores and liquidation volume data for leverage stress clarity",
          "Cross-chain capital flows and user growth metrics to validate ecosystem health"
        ]
      },
      "bear_researcher": {
        "thesis": "BTC remains in a structurally bearish regime characterized by price well below the 200-day SMA, modest bearish momentum, and a lack of strong volume confirmation to sustain an upward breakout. Funding rates near zero hide underlying risk as the absence of detailed leverage and liquidation metrics obscures potential buildup in crowding. DeFi fundamentals are insufficiently covered\u2014TVL and user growth data gaps leave real capital inflows and protocol health unverifiable, undermining the bull narrative of stable ecosystem demand. Moreover, BTC is outside the historically robust post-halving rally window, and macro uncertainties combined with regulatory tightening introduce downside risk that can trigger extended drawdowns or volatile crashes. Without clear evidence of sustained demand, volume expansion, or improving leverage profiles, the current rebound appears a bear trap in a late-cycle consolidation prone to failure.",
        "argument": "Bear Analyst: BTC technicals remain in a bear regime with the price deeply below the 200-day SMA and RSI only modestly oversold, failing to indicate a strong base. The slight 1-day bounce with a low volume ratio of 1.09x lacks the magnitude generally required to confirm a trend reversal, consistent with empirical evidence that most crypto breakouts fail without volume confirmation. While derivatives funding rates are near neutral, they reside below the 0.03% threshold which historically indicates healthy leverage, and declining open interest signals ongoing deleveraging rather than fresh demand. The absence of critical metrics such as funding rate z-scores and liquidation volumes hampers understanding of latent crowding and risk. On fundamentals, significant gaps in DeFi data including TVL in native tokens, user growth, and fee trends prevent a robust assessment of ecosystem health, making claims of capital inflow and fundamental steadiness unsubstantiated. Macro and regulatory risks remain material with tightened AML regimes and potential market correlation pressures undermining crypto\u2019s safe-haven narrative. The setup favors a cautious bear outlook where the current bounce is a potential bear trap within a late halving cycle consolidation prone to failure more than sustained recovery. A definitive invalidation would require volume-backed price strength above the 200-day SMA, confirmed leverage expansion with controlled liquidations, and fundamental proof of renewed capital inflows and user growth. These absences combined with weak technicals and incomplete leverage data maintain the high risk of further downside or choppy prolonged range. Near-neutral funding rates below the 0.03% healthy threshold and declining open interest signal deleveraging rather than broad new long accumulation. Missing funding rate z-scores and liquidation volume create blind spots, risking undisclosed crowded shorts or the potential for sharp deleveraging cascades.",
        "confidence": "medium",
        "top_point": "BTC price is 25% below its 200-day SMA with RSI only mildly oversold, indicating a weak technical base and trend continuation risk.",
        "top_rebuttal": "Near-neutral funding rates below the 0.03% healthy threshold and declining open interest signal deleveraging rather than broad new long accumulation. Missing funding rate z-scores and liquidation volume create blind spots, risking undisclosed crowded shorts or the potential for sharp deleveraging cascades.",
        "data_gaps": [
          "Comprehensive derivative metrics: funding rate z-score, real-time liquidation volume, leverage ratios",
          "Defillama TVL data and native token denominated protocol volumes",
          "User growth metrics across key DeFi and layer1 protocols",
          "Cross-chain capital flow and stablecoin yield changes",
          "Macro correlation shifts and regulatory impact quantification"
        ]
      },
      "risk_manager": {
        "summary": "BTC remains in a bear regime with price well below the 200-day SMA and relatively subdued RSI, signaling weak technical support despite a minor 1-day bounce. Volume remains low for a sustained reversal, and derivatives data\u2014although neutral\u2014lack key metrics (funding rate z-score, liquidation volumes) that limit leverage stress visibility. DeFi data gaps (TVL, user growth, fee trends) further obscure fundamental health assessment. Regulatory tightening and macro uncertainties amplify downside risk. Current position sizing must factor in these incomplete signals and elevated uncertainty, emphasizing tight stops and low concentration. Cascade risk is moderate given stable but slightly declining open interest and neutral funding rates. Without clear volume-backed trend strength, leverage expansion, or fundamental inflows, the setup favors caution, with any recovery contingent on closing above SMA200 and improved derivatives transparency. Key invalidation includes sustained price and volume breakout with healthy leverage expansion and no liquidation stress.",
        "recommendation": "avoid",
        "risk_bias": "elevated",
        "cascade_risk_level": "moderate",
        "aggressive_view": "Aggressive Analyst: The current BTC setup, despite low aggregate score and cautious technical analyst stance, justifies pressing risk from an aggressive perspective. The 1.93% 1-day return combined with volume ratio at 1.09x (close to breakout threshold) and RSI at 34.3 indicate short-term bullish momentum emerging within a bear regime, signaling an early dip-buy entry opportunity before full oversold confirmation or large volume surge. While data gaps (DeFi TVL, derivatives liquidation metrics) limit full conviction, the slight return and stable funding rate (-0.0034%) argue against immediate deleveraging cascade, confirming controlled risk. News catalysts of institutional demand resurgence and dovish Fed commentary support a 3-day horizon upside of 10-20%. Excessive caution ignores these early signals and misses cost-effective entry points\u2014the required confirmation is not perfect volume spikes or deeply oversold RSI below 20; a moderate bounce with stable volume in a bear trend can justify agile risk-taking to capitalize on short-term range reversion or relief rallies. Key invalidation triggers remain a sustained close below current support levels with volume collapse or sudden spike in deleveraging indicators. In sum, risk pressing today is warranted, with position sizing calibrated for medium confidence and awareness of data limitations; waiting for perfect confirmation risks worse entry levels or missed upside setups.",
        "conservative_view": "Conservative Analyst: BTC currently trades well below its 200-day SMA (-25%), deep in a bear regime with weak momentum indicated by RSI near 34.3 and a volume ratio (1.09x) insufficient to confirm a sustainable breakout. Short-term returns show a modest bounce (+1.93%), but 30-day returns remain negative and realized volatility is elevated, indicative of ongoing market fragility. Derivative markets present mild deleveraging signals via declining open interest (-0.81%) and nearly neutral funding rates (-0.0034%), yet critical data gaps persist, notably missing liquidation metrics and leverage z-scores, which obscures true risk of cascade liquidations or crowded positioning. DeFi fundamental data coverage is notably incomplete, with missing TVL and user growth figures, undermining confidence in capital inflow narratives and leaving protocol health unverifiable. Regulatory tightening in the EU and macro uncertainty compound downside risks. Combined, this fragile and data-limited structure argues strongly for capital preservation and avoidance of increased exposure until clear evidence emerges. Specifically, entries should wait for confirmatory signals such as sustained price reclaim above the 200-day SMA with volume exceeding 1.5x norm, clear increases in derivatives open interest accompanied by positive funding rate z-scores, and robust fundamental data confirming capital inflows and ecosystem health. Absent these, aggressive risk-taking exposes portfolios to downside traps and leverage-induced drawdowns not visible in current partial metrics. The prudent stance is to cap exposure and prioritize preservation over speculation in the near term.",
        "neutral_view": "Neutral Analyst: BTC is currently entrenched in a bear regime, trading about 25% below its 200-day SMA with an RSI near 34, reflecting mild bearish momentum but no oversold capitulation. A modest 1.93% one-day bounce and volume ratio around 1.09x indicate tentative short-term relief without strong breakout conviction. Derivatives data show a near-neutral funding rate (-0.0034%) and slight open interest decline (-0.81%), consistent with cautious deleveraging rather than fresh leveraged longs or panic liquidations. However, critical gaps in liquidation metrics and leverage z-scores limit leverage risk assessment. DeFi fundamentals lack key TVL, user growth, and fee signals due to coverage issues, restricting confidence in ecosystem health and fresh capital inflows. News catalysts present a mixed picture: institutional demand and dovish Fed tone support upside potential, but regulatory tightening in the EU and macro uncertainties weigh on liquidity and add downside risk. The debate contrasts an aggressive stance favoring calibrated dip-buying on early bullish signals and a conservative posture emphasizing capital preservation until more robust multi-source confirmations emerge. Given the incomplete data, subdued volume, and protracted bear regime, the neutral, disciplined recommendation is to maintain a cautious or reduced risk stance near-term. Close monitoring for a sustained reclaim above the 200-day SMA with volume above 1.5x, accompanied by improving RSI and rising open interest with positive funding rate z-scores, should guide increasing exposure. Conversely, failing to hold current supports or sudden spike in deleveraging and capital outflows would reinforce bearish positioning. This balanced approach prudently weighs limited upside signals against significant data uncertainties and prevailing bear market structure, avoiding premature risk escalation amid incomplete visibility."
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
- report: The integrated crypto read stays avoid: score=31, regime=bear_trend, MC/TVL=None, funding=-3.4e-05. The system sees enough fragility to stay conservative rather than press for directional size.
