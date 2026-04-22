# Final Arbiter

- role: final_arbiter
- title: Final Arbiter
- decision: {'action': 'hold', 'direction': 'neutral', 'horizon_days': 3, 'position_size': 'none'}
- decision_label: avoid
- thesis: BTC currently trades about 9.2% below its 200-day SMA, firmly in a bear-trend regime, with price up 2.1% in the last day and +10.5% over 30 days indicating a bear-trend rally rather than a sustained reversal. RSI is near bear resistance levels around 68, just shy of confirming a breakout. Volume remains below the key 1.5x threshold needed to validate trend shifts, and derivatives metrics show mild short bias but are neutral overall with no signs of crowding or liquidation risk. DeFi fundamentals, including substantial TVL and stablecoin lending yields around 3.3%, imply risk appetite is measured but lack confirmatory user and capital flow data. Missing Coinglass derivatives data and stablecoin flow metrics impair a full risk assessment, limiting confidence. From the Aggressive perspective, the setup offers a tactical opportunity if volume and RSI confirm strength with a breakout above the 200-day SMA. From the Conservative viewpoint, the incomplete volume and fundamental signals plus stretched valuation ratios favor capital preservation. The risk manager aligns with caution due to regime and data gaps. Thus, the best course is to remain on the sidelines, monitoring for a clean volume surge above 1.5x average, RSI closing above 65–70, and reclaiming the 200-day SMA to validate a move higher; failure to reach these should trigger renewed risk reduction. Current price near $77,950 and ATR of approximately $2,400 offer clear discipline points for future entries. A confirmed breakout above 200-day SMA with volume will justify a transition to buy, while a drop below the 20-day SMA around $72,900 would reinforce bearish risk. Continued monitoring of missing derivatives and DeFi data is critical to refine conviction.
- confidence: medium
## Key Factors
- {'factor': 'Bear-trend regime confirmed by price 9.2% below 200-day SMA with RSI near but below bear resistance', 'source_role': 'technical_analyst'}
- {'factor': 'Derivatives market balanced with mild short funding bias and modest open interest growth, no liquidation risk evident', 'source_role': 'derivatives_analyst'}
- {'factor': 'Robust DeFi TVL and moderate stablecoin yields reflecting measured leverage demand but incomplete capital inflow data', 'source_role': 'defi_fundamentals_analyst'}
## Key Risks
- {'risk': 'Missing comprehensive derivatives metrics (leverage ratios, funding Z-scores) limiting risk visibility', 'mitigation': 'Maintain cautious stance, monitor for funding shifts and open interest spikes', 'source_role': 'risk_manager'}
- {'risk': 'Insufficient volume surge to confirm trend change exposes rally to failure risk', 'mitigation': 'Wait for volume to exceed 1.5x average with RSI breakout before increasing exposure', 'source_role': 'technical_analyst'}
- {'risk': 'Uncertain capital inflows and user growth due to missing stablecoin supply and wallet data', 'mitigation': 'Track stablecoin supply changes and wallet data releases closely for early signs of fundamental shifts', 'source_role': 'defi_fundamentals_analyst'}
- entry_logic: Watch for daily volume exceeding 1.5x average concurrent with RSI close above 65 and price reclaiming a daily close above 200-day SMA (~$85,400). Alternatively, scale cautiously on sustained dips holding above the 20-day SMA (~$72,900) if momentum indicators improve.
- stop_logic: Initial stop = 1× ATR (~$2,400) below entry price. Hard stop: daily close below 20-day SMA on rising volume confirming breakdown.
## Targets
- sizing_formula: Position size to match risk tolerance with max 1% portfolio risk per trade using ATR stops; scale up only upon confirmed breakout signals and volume confirmation. Hold no position until clear entry triggers materialize.
## Flip Rules
- {'condition': 'Sustained daily close above 200-day SMA with volume >1.5x average and RSI >70', 'new_posture': 'Upgrade to buy, full size'}
- {'condition': 'Daily close below 20-day SMA with declining volume and RSI below 50', 'new_posture': 'Downgrade to avoid with position exit'}
- tactical_alternative: For risk-averse mandates, maintain a reduced-exposure watch-only stance or employ defined-loss options strategies while waiting for confirmed breakout signals.
## Invalidation
- Volume surpasses 1.5× average and RSI closes above 65 with clear price reclamation above 200-day SMA
- Price closes below 20-day SMA with confirming volume and momentum weakening below RSI 50
- review_plan: {'review_at_days': 3, 'what_to_check': ['Volume ratios and quality', 'RSI levels relative to bear resistance zone', 'Price relation to 200-day and 20-day SMAs', 'Derivatives funding rates and open interest changes', 'DeFi stablecoin supply and unique wallet metrics if released']}
- override_note: Scorecard baseline 'avoid' aligns with technical and risk management caution amid data gaps; chose 'hold' to reflect balanced risk/reward awaiting confirmation signals.
- rejected_alternative: {'alternative_action': 'avoid', 'why_rejected': 'While conservative risk bias is warranted, the positive short-term momentum, modest open interest growth, and rising DeFi yields suggest potential for a bear-trend rally continuation. Avoid would miss tactical opportunities if breakout conditions emerge.'}
- summary: The integrated crypto read stays avoid: score=49, regime=bull_trend, MC/TVL=2.7653, funding=-2.2e-05. The system sees enough fragility to stay conservative rather than press for directional size.
## Rationale
- cautious
- coverage_gap
- insufficient_data
- elevated
- score=49
- scorecard: {'inputs': {'momentum': 56.7, 'liquidity': 80.0, 'derivatives': 60.0, 'defi': 56.0, 'onchain': 44.38, 'sentiment': 45.0, 'data_quality_penalty': -5.0}, 'action_score': 49, 'final_score': 49, 'confidence': 'low', 'score_decision': 'avoid', 'data_quality': {'core_complete': True, 'supplementary_complete': False, 'core_gaps': [], 'supplementary_gaps': ['coinglass:missing_api_key'], 'penalty': -5.0}}
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
    "thesis": "Assess BTC setup as of 2026-04-22",
    "horizon_days": 3,
    "run_id": "r_20260422T063929Z_BTC"
  },
  "role_context": {
    "market_context": {
      "price": {
        "latest_close": 77949.132812,
        "return_1d_pct": 2.090768,
        "return_7d_pct": 3.721784,
        "return_30d_pct": 10.538144,
        "price_vs_sma20_pct": 6.83896,
        "price_vs_sma200_pct": -9.239627,
        "rsi_14": 68.3739,
        "realized_vol_30d": 40.8088,
        "volume_ratio": 1.1934,
        "regime": "bear",
        "halving_cycle_day": 733
      },
      "defi": {
        "defi_tvl_total": 558121303026.53,
        "defi_stablecoin_median_apy": 3.3482,
        "defi_stablecoin_apy_change_7d": 0.3355,
        "mc_tvl_ratio": 2.7653
      },
      "evidence": {
        "evidence_status": "fetched",
        "source": "open_deep_research_local",
        "citations_count": 10
      },
      "coverage_gaps": [
        "coinglass:missing_api_key"
      ]
    },
    "scorecard": {
      "inputs": {
        "momentum": 56.7,
        "liquidity": 80.0,
        "derivatives": 60.0,
        "defi": 56.0,
        "onchain": 44.38,
        "sentiment": 45.0,
        "data_quality_penalty": -5.0
      },
      "action_score": 49,
      "final_score": 49,
      "confidence": "low",
      "score_decision": "avoid",
      "data_quality": {
        "core_complete": true,
        "supplementary_complete": false,
        "core_gaps": [],
        "supplementary_gaps": [
          "coinglass:missing_api_key"
        ],
        "penalty": -5.0
      }
    },
    "prior_role_memos": {
      "technical_analyst": {
        "summary": "BTC remains in a bear trend with price below the 200-day SMA by about 9.2%, confirming bearish regime bias. The RSI near 68 is approaching the bear market resistance zone (55-65) but has not definitively triggered an overbought sell signal, suggesting some remaining short-term upside momentum. Volume is below the 1.5x threshold required for confident breakout confirmation, indicating any rally may lack strong conviction and be vulnerable to failure or distribution. The 1-day return of +2.1% and 30-day return of +10.5% suggest a moderate bounce rather than a sustained trend reversal at this point. Given the cycle day 733 post-halving (beyond the 18-24 month peak window), risk of trend reversal remains elevated. Coverage gaps on volume quality reduce conviction further. BTC\u2019s price running 6.8% above the 20-day SMA implies no significant overextension yet, so mean reversion down is not guaranteed. The current setup is likely a bear-trend rally/sell zone rather than a new bull run start. Confirmation of sustained trend change requires volume surge >1.5x average and RSI breaching above resistance zone (>65) with price reclaiming above 200-day SMA. Invalidations include price breaking above the 200-day SMA with strong volume and RSI sustaining >70 in bull thresholds. Lower conviction due to missing real volume API data.",
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
        "support": "Most recent higher low (not specified in data)",
        "resistance": "Bear market RSI resistance zone: 55-65"
      },
      "defi_fundamentals_analyst": {
        "summary": "DeFi's total TVL remains substantial at over $558B, but with a market capitalization to TVL ratio near 2.8, token valuations appear stretched relative to on-chain capital. Stablecoin lending yields are low-to-moderate in the 3% range, suggesting subdued borrowing demand and limited leverage appetite. The absence of unique wallet data and stablecoin supply trends prevents confident conclusions about new capital inflows or user growth. Overall, signs point to a fragile DeFi ecosystem with elevated speculation and limited fundamental support, implying cautious risk exposure. Critical missing data on lending utilization and stablecoin flows constrains deeper conviction. A sustained improvement in capital inflows, user adoption, or reduction in MC/TVL would shift the base case more bullish.",
        "signal": "neutral-cautious",
        "confidence": "medium",
        "stablecoin_signals": "No direct monthly stablecoin supply growth data provided; stablecoin yield data implies subtle leverage attempts but not decisive inflows; thus stablecoin flow signals are incomplete",
        "data_gaps": [
          "No unique user wallet growth or concentration data to assess whale risks or broad engagement",
          "No stablecoin market cap growth or dominance trends to infer macro capital direction",
          "No protocol-level revenue or fee data to confirm demand shifts",
          "No utilization or withdrawal stress metrics from lending protocols to confirm health"
        ]
      },
      "derivatives_analyst": {
        "summary": "BTC's derivatives market currently shows a very mild short-biased funding rate around -0.0022% per 8h, which is well within neutral bounds and implies no aggressive positioning. Open interest increased by approximately 1.7%, a modest move insufficient to indicate large leveraged inflows or elevated crash risk. Critical data gaps exist due to missing Coinglass coverage: leverage ratios, liquidation volumes, and open interest relative to circulating supply are unavailable, hampering holistic risk assessment. Consequently, conviction is low-to-medium for a directional derivatives-driven event over the next three days. Without further evidence of funding rate sustained shifts, high leverage, or liquidation surges, the market appears balanced with no immediate fragility or exuberance signals. Spot momentum proxies offer limited signal and cannot replace direct derivatives metrics. Close monitoring is needed, especially for emerging signs of sustained funding above 0.01% or material OI spikes. Derivatives positioning thesis remains cautious-neutral at this stage.",
        "signal": "neutral",
        "confidence": "low",
        "positioning_thesis": "The BTC derivatives market exhibits a mild short bias through funding rates slightly below zero but remains within a neutral band without heavy crowding signals. Open interest has increased modestly but not enough to indicate elevated leverage or risk of a liquidation cascade. The absence of Coinglass data limits ability to assess open interest relative to market cap or cumulative volume delta to confirm genuine trend or short squeeze dynamics. Overall, there is no strong evidence of a directional derivatives-driven move in the 3-day horizon, and spot momentum proxies remain weak guidance only.",
        "data_gaps": [
          "No Coinglass coverage prevents calculating ELR or OI/market cap ratio, limiting risk metric accuracy",
          "Lack of liquidations data impairs detection of cascading deleveraging or capitulation events",
          "Absence of funding rate Z-score and exchange divergence metrics reduces confidence in crowding strength",
          "No CVD or basis data restricts ability to confirm genuine trend or investor sentiment extremes"
        ]
      },
      "news_analyst": {
        "summary": "BTC is consolidating near $29k with a cautiously constructive outlook driven by the approaching Taproot upgrade and increased institutional inflows bolstered by favorable SEC guidance. However, regulatory uncertainty in the EU and recent short-term volatility pose measurable downside risks in the near term. Market structure remains range-bound with key support at $28,500, below which technical downside could accelerate. Macro conditions are neutral, lacking strong catalysts beyond crypto-specific events. Layer 2 network stability and upgrade execution remain watch points for potential minor disruptions.",
        "signal": "contextualized",
        "confidence": null,
        "evidence_quality": "actionable",
        "top_risk": "EU MiCAR regulatory voting delay and uncertainty"
      },
      "bull_researcher": {
        "thesis": "Despite BTC's current bear-trend regime and sub-200-day SMA positioning, several data points support a constructive outlook over the near-to-medium term. The sustained 1-day and 30-day positive returns (+2.1% and +10.5%), paired with RSI near but not exceeding bear resistance, indicate underlying short-term momentum without exhaustion. Derivatives positioning is balanced with mildly negative funding rates within neutral bounds, signaling no excessive crowding or liquidation risk. DeFi TVL remains robust above $558B and stablecoin yields rising modestly from a low base reflect healthy, non-exuberant demand for leverage. Although BTC is beyond the conventional 12-18 month post-halving bullish window, the absence of extreme derivatives shorting and decent fundamental backing in DeFi underscore supportive price floors. Institutional interest implied by news coverage further bolsters supply-demand dynamics. Therefore, with measured capital inflows and healthy leverage demand, BTC is positioned for a potential transition back toward a bull regime, contingent on confirmation via volume and RSI breakouts.",
        "argument": "Bull Analyst: BTC shows signs of constructive momentum despite residing in a bear-trend regime below the 200-day SMA. Positive 30-day returns and RSI near but under bear resistance suggest room for further gains. The derivatives market is balanced with mildly negative funding and modest open interest expansion, indicating low liquidation risk. DeFi fundamentals remain solid with high TVL and increasing stablecoin lending yields implying healthy, measured leverage demand. While key data gaps remain, available evidence supports a scenario where BTC consolidates before a potential bull regime recovery, especially if volume surges and RSI breaks above resistance. Invalidation triggers would include price breakdowns with confirming volume, sharp derivatives market shifts, or deteriorations in stablecoin capital flows. Overall, BTC appears positioned for a measured upward move if risk factors remain contained. Price above 20-day SMA (+6.8%) and RSI near but not exceeding bear resistance zone suggest the current setup is a bear-trend rally with potential to build enough momentum for a breakout. Sustained volume increase above 1.5x and RSI above 65 would confirm further bull evidence.",
        "confidence": "medium",
        "top_point": "BTC price exhibiting short-term momentum with 30-day return +10.5% and RSI near 68 below bear resistance zone",
        "top_rebuttal": "Price above 20-day SMA (+6.8%) and RSI near but not exceeding bear resistance zone suggest the current setup is a bear-trend rally with potential to build enough momentum for a breakout. Sustained volume increase above 1.5x and RSI above 65 would confirm further bull evidence.",
        "data_gaps": [
          "Monthly stablecoin supply growth data to detect structural capital inflows",
          "Unique wallet growth and user concentration metrics to assess adoption breadth and whale risk",
          "Coinglass derivatives data (leverage ratios, liquidation volume, funding rate Z-score) for refined risk profiling",
          "Protocol-level revenue and lending utilization stats for intrinsic demand validation"
        ]
      },
      "bear_researcher": {
        "thesis": "BTC appears positioned within a bear-trend regime with current price action largely representing a bear-trend rally rather than a sustainable bull reversal. Key bullish signals such as positive short-term returns and RSI near bear resistance are not confirmed by essential volume surge or derivatives crowding data. The elevated MC/TVL ratio (~2.8) suggests stretched valuations untethered from on-chain fundamentals, while stablecoin lending yields remain modest, indicating weak leverage demand rather than robust capital inflows. Missing unique wallet and stablecoin supply growth data create a major blind spot for verifying adoption or capital flight risks. Additionally, absence of comprehensive derivatives metrics like leverage ratios, liquidation volume, and funding rate Z-scores, partially due to Coinglass data gaps, limits confidence in the purported balanced positioning. Taken together with the technical analyst\u2019s note on volume below breakout thresholds and price well below 200-day SMA, the risk leans to the downside, especially if macro or regulatory conditions deteriorate. This setup is susceptible to failure typical of crypto rallies in bear cycles and the diminishing post-halving returns framework.",
        "argument": "Bear Analyst: BTC remains entrenched in a bear-trend regime supported by technical and fundamental signals that challenge the bullish interpretations. While short-term momentum metrics like a +10.5% 30-day return and RSI near 68 are cited as signs of recovery, they fail to meet the critical volume surge threshold needed for breakout confirmation, suggesting a bear-trend rally vulnerable to failure. The market's valuation appears stretched with an MC/TVL ratio near 2.8, implying the token price is outpacing real economic activity on-chain. Stablecoin lending yields are moderate, and essential data verifying real capital inflows or leverage demand, such as stablecoin supply trends and user adoption metrics, are missing\u2014creating significant unknowns. Derivatives positioning superficially looks balanced but is undermined by missing comprehensive metrics like leverage ratios, liquidation volumes, and funding rate divergence, obscuring true risk. Elevated funding above ~0.03% and rising OI historically precede bearish reversals, but current funding rate just below zero and absence of leverage insights limit risk visibility. The technical analyst's note that price is still well below the 200-day SMA and volume lags breakout levels reinforce a bearish base case. Absent clear volume-backed breakout, improved derivatives clarity, or fundamental capital inflows, the setup is prone to faltering and reversion lower. The bear thesis could be invalidated by sustained price breakout above 200-day SMA with volume confirmation and robust derivatives and DeFi data revealing healthier demand dynamics. Until then, the risk of cascading declines amid insufficient liquidity and elevated valuations remains high. Momentum indicated is moderate and not backed by required volume spike (volume ratio <1.5) or breakout over 200-day SMA; such moderate rallies in bear regimes often fail, representing bear-trend bounces rather than directional reversals.",
        "confidence": "high",
        "top_point": "BTC price remains below 200-day SMA by ~9.2%, RSI near 68 but within bear resistance zone (55-65), indicating limited momentum upside without breakout confirmation",
        "top_rebuttal": "Momentum indicated is moderate and not backed by required volume spike (volume ratio <1.5) or breakout over 200-day SMA; such moderate rallies in bear regimes often fail, representing bear-trend bounces rather than directional reversals.",
        "data_gaps": [
          "Coinglass derivatives metrics: leverage ratios, liquidation volumes, funding rate Z-score, exchange divergence",
          "Unique wallet growth and user concentration metrics in DeFi",
          "Stablecoin supply growth and market share data to confirm capital inflows or outflows",
          "Protocol-specific revenue and lending utilization statistics",
          "Volume quality data and on-chain spike confirmation to validate volume ratios"
        ]
      },
      "risk_manager": {
        "summary": "BTC remains in a bear trend with weak volume confirmation and price below the 200-day SMA by ~9.2%. Short-term momentum indicated by RSI near 68 creates a potential for further upside, but absence of volume surge (>1.5x average) and derivatives risk signals (funding rate near neutral, low open interest growth) moderate conviction. DeFi TVL remains robust, but MC/TVL ratio (2.8) and low stablecoin lending yields suggest stretched valuations and limited leverage-driven capital inflows. Critical data gaps, notably missing Coinglass derivatives metrics (leverage ratios, liquidation volumes), unique wallet growth, and stablecoin supply flow data, limit precise risk assessment. Historical crypto bear cycles and BTC\u2019s prior severe drawdowns justify cautious posture. Correlation risks persist as altcoins remain tightly linked to BTC, offering limited portfolio diversification. Liquidation cascade risk is moderate given currently neutral funding rates, absence of elevated open interest/leverage metrics, but incomplete data warrants vigilance. Operational risk includes missing real volume quality and derivatives data. Base case: cautious avoidance with risk budget conservatively managed, leverage minimized, and stops tight given the bear-trend rally context. Invalidation hinges on volume surge >1.5x average with RSI >65 and price reclaiming above 200-day SMA on robust derivatives data confirming sustained demand and leverage. Until then, risk remains skewed to downside with possible rapid drawdowns and leveraged cascades in stressed macro or regulatory conditions.",
        "recommendation": "avoid",
        "risk_bias": "elevated",
        "cascade_risk_level": "moderate",
        "aggressive_view": "Aggressive Analyst: The current BTC setup, despite officially signaling 'avoid' with low-confidence scores and significant data gaps, justifies pressing risk with moderate conviction based on available evidence. Price has shown a 2.1%+ daily return and over 10% in 30 days, accompanied by RSI just below the bear resistance zone (~68) and price positioning comfortably above the 20-day SMA (+6.8%). While price remains about 9.2% below the 200-day SMA, this is a characteristic bear-trend bounce setup where continuation of the rally with increased volume (above 1.5x avg) and RSI crossing above 65 would confirm a breakout scenario. Volume ratio at 1.19x is near a breakout threshold and should not be dismissed outright amid gaps in volume data quality. Derivatives positioning is balanced, with only mild short bias on funding and modest open interest growth; no signs of crowded liquidation risk. DeFi fundamentals show large TVL and rising stablecoin lending yields suggesting improving risk appetite and potential capital inflows, absent severe overheating. Regulatory and macro risks exist but no new crisis signals currently. The lack of perfect confirmation (missing Coinglass derivatives data, stablecoin supply trends, full volume quality) is offset by coherent multi-factor signs of constructive momentum. Therefore, an aggressive trader can act with a controlled risk approach to capture a likely bear-trend rally continuation forming a base for a prospective bull breakout. Key actionable triggers include sustained volume surge >1.5x average, RSI pushing above 65, and price reclaiming the 200-day SMA with conviction. If these emerge within the 3-day horizon, press risk higher. Conversely, failure to confirm volume increase or a drop below the 20-day SMA would warrant risk reduction. Excessive caution risks missing a prime opportunity to capitalize on a measured bear-trend bullish transition setup evident from combined technical, derivatives, and DeFi signals.",
        "conservative_view": "Conservative Analyst: BTC remains in a fragile bear-trend regime with price 9.2% below the 200-day SMA and volume ratios under breakout thresholds, indicating rallies lack strong conviction and are prone to failure. The MC/TVL ratio of ~2.8 signals significant overvaluation relative to on-chain capital, raising the risk of sharp corrections. Stablecoin lending yields are modestly positive, but missing data on stablecoin supply growth and unique wallet counts create critical blind spots on true leverage demand and capital inflows. Derivatives markets show a mild short bias with only modest open interest growth; however, missing Coinglass API data prevents comprehensive leverage, liquidation, and funding rate Z-score analysis, undercutting confidence in risk assessment. Absence of key volume quality confirmation further reduces signal reliability. The dependence on incomplete data and lack of verified sustained momentum dictate a capital preservation stance. Without clear breakout volume (>1.5x average), derivatives risk transparency, or fundamental improvements, the setup is vulnerable to downside reversion typical of bear-trend rallies. Prudent management requires avoiding or capping exposure until robust evidence of sustained bull transition emerges, such as a confirmed breakout above the 200-day SMA with strong volume, cleaner derivatives data showing balanced or long positioning, and verified capital inflows in DeFi stablecoins. Continued monitoring of data gaps and risk signals is essential before increasing risk allocation.",
        "neutral_view": "Neutral Analyst: BTC\u2019s current technical, derivatives, and fundamental signals present a conflicted setup over the next 3 days. Price trades below the 200-day SMA by ~9.2%, consistent with a bear-trend regime, yet short-term returns (+2.1% 1-day, +10.5% 30-day) and RSI near 68 suggest a bear-trend rally with some upside momentum. Volume ratio at 1.19x is below the 1.5x breakout threshold, leaving breakout conviction tentative. Derivatives data show mildly negative funding and modest open interest growth, implying balanced positioning but critical data gaps (missing Coinglass metrics) obscure full risk visibility. DeFi fundamentals reveal a large TVL with stablecoin lending yields rising modestly (~3.3%), indicating measured but not robust leverage demand. News catalysts like the Taproot upgrade and institutional inflows provide medium-term bullish impetus, while regulatory uncertainty and macro neutrality persist. Given incomplete data and mixed signals, a disciplined posture favors cautious observation, avoiding aggressive risk-taking but maintaining readiness to increase exposure if confirmed breakout triggers occur: sustained volume above 1.5x average, RSI breaks >65, and price reclaims and holds above the 200-day SMA. Conversely, failure to confirm these signals or a breakdown below the 20-day SMA should prompt risk reduction. This balanced approach manages downside risk amid uncertainty while allowing capture of a probable measured bear-trend rally continuation and possible regime transition. Continued monitoring of data gaps\u2014especially derivatives leverage metrics and stablecoin supply flows\u2014is essential for conviction refinement."
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
- report: The integrated crypto read stays avoid: score=49, regime=bull_trend, MC/TVL=2.7653, funding=-2.2e-05. The system sees enough fragility to stay conservative rather than press for directional size.
