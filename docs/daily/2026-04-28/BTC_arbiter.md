# Final Arbiter

- role: final_arbiter
- title: Final Arbiter
- decision: {'action': 'avoid', 'direction': 'neutral', 'horizon_days': 7, 'position_size': 'none'}
- decision_label: avoid
- thesis: From the Conservative perspective, BTC remains technically fragile below its 200-day SMA at 76626 with an RSI near 58 and subpar volume ratio around 0.9, signaling limited momentum and high risk of failed rallies. DeFi valuations are stretched, indicated by an MC/TVL ratio near 2.78, with no strong user growth or fee data to justify elevated token prices. Derivatives positioning appears balanced but incomplete data on funding z-scores, leveraged positioning, and liquidation risk prevent confident risk assessment. The 30-day +15% return reflects a bear market rally rather than sustained uptrend. Additionally, significant regulatory risks from EU MiCA and upcoming US SEC BTC ETF decisions amplify downside uncertainty. While the Aggressive view argues for tactical partial longs on positive institutional catalysts, missing key volume and derivatives data plus weak technicals outweigh these factors, advising capital preservation. Avoiding new exposure while monitoring for a clean break above the 200-day SMA on strong volume (>1.5x average) with improved derivatives visibility would enable reconsideration. A tight ATR-based stop below recent supports would be essential. This stance balances near-term catalyst asymmetry with structural bear signals and data gaps, maintaining optionality without undue risk.
- confidence: high
## Key Factors
- {'factor': 'Technical bear regime confirmed by price below 200-day SMA with weak volume and RSI at 58', 'source_role': 'technical_analyst'}
- {'factor': 'Elevated DeFi valuations (MC/TVL ~2.78) without supportive onchain or user growth data', 'source_role': 'defi_fundamentals_analyst'}
- {'factor': 'Incomplete derivatives data with near-neutral funding but limited tail-risk clarity', 'source_role': 'derivatives_analyst'}
## Key Risks
- {'risk': 'Regulatory developments (EU MiCA tightening, SEC ETF rulings) could trigger sharp negative moves', 'mitigation': 'Maintain close monitoring and limit position size, exit on confirmed bearish breaks', 'source_role': 'news_analyst'}
- {'risk': 'Potential sudden leveraged liquidation due to incomplete derivatives data', 'mitigation': 'Use tight stops and avoid initiating large new long positions until clarity improves', 'source_role': 'risk_manager'}
- {'risk': 'Bear market traps causing failure of rallies despite positive short-term returns', 'mitigation': 'Avoid chasing rallies; wait for technical confirmation of trend reversal', 'source_role': 'bear_researcher'}
- entry_logic: Wait for daily close above 200-day SMA (~76700) with volume exceeding 1.5x average and RSI sustainably moving above 65, accompanied by improving derivatives metrics (confirmed positive funding z-scores and controlled open interest growth). Alternatively, consider scaling in after confirmed sustained price support above 50-day SMA with volume confirming momentum.
- stop_logic: Initial stop at 1× ATR (~price - ATR) below entry price (e.g., ATR ~1000 USD implies stop ~ATR below entry). Hard stop on daily close below recent swing low or below 50-day SMA if holding a position.
## Targets
- sizing_formula: Avoid new positions given current uncertainty. If conditions improve, size trades to risk no more than 0.5% portfolio per trade using ATR-based stop losses, capping total exposure to 2-3% tactically.
## Flip Rules
- {'condition': 'Sustained daily closes above 200-day SMA with volume >1.5x average and RSI >65', 'new_posture': 'Upgrade to hold or buy with half to full position size'}
- {'condition': 'Derivatives funding rate z-score exceeds +2 with rising open interest', 'new_posture': 'Consider tactical short or reduce exposure to longs'}
- tactical_alternative: For risk-averse mandates, consider smaller exposure sizes with wider stops or defined-risk options strategies to participate in potential upside while limiting downside.
## Invalidation
- Daily close sustained above 200-day SMA with strong volume confirmation
- Clear signs of improving derivatives market health (funding positive and structurally supportive)
- Significant onchain user growth and DeFi TVL expansion with stable valuations
- review_plan: {'review_at_days': 7, 'what_to_check': ['Price vs 200-day SMA and volume levels', 'RSI trajectory and momentum indicators', 'Derivatives market indicators including funding rates and open interest', 'Regulatory updates and associated market reactions', 'DeFi TVL, onchain user metrics, and stablecoin flows']}
- override_note: Scorecard baseline 'avoid' is aligned with the comprehensive risk manager and bear analyst views reinforced by weak technicals and stretched DeFi fundamentals; no override applied.
- rejected_alternative: {'alternative_action': 'buy', 'why_rejected': 'Insufficient supportive volume and technical confirmation, insufficient derivatives data to validate tail-risk profile, and regulatory risks preclude confident entry despite some positive catalysts.'}
- summary: The integrated crypto read stays avoid: score=47, regime=bull_trend, MC/TVL=2.7753, funding=-3.2e-05. The system sees enough fragility to stay conservative rather than press for directional size.
## Rationale
- cautious
- coverage_gap
- insufficient_data
- elevated
- score=47
- scorecard: {'inputs': {'momentum': 50.49, 'liquidity': 80.0, 'derivatives': 60.0, 'defi': 52.0, 'onchain': 44.3, 'sentiment': 45.0, 'data_quality_penalty': -5.0}, 'action_score': 47, 'final_score': 47, 'confidence': 'high', 'score_decision': 'avoid', 'data_quality': {'core_complete': True, 'supplementary_complete': False, 'core_gaps': [], 'supplementary_gaps': ['coinglass:missing_api_key'], 'penalty': -5.0}}
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
    "thesis": "Automated daily research for BTC on 2026-04-28",
    "horizon_days": 7,
    "run_id": "r_20260428T094555Z_BTC"
  },
  "role_context": {
    "market_context": {
      "price": {
        "latest_close": 76626.046875,
        "return_1d_pct": -0.957232,
        "return_7d_pct": -2.016614,
        "return_30d_pct": 14.896366,
        "price_vs_sma20_pct": 1.471135,
        "price_vs_sma200_pct": -9.399545,
        "rsi_14": 58.3282,
        "realized_vol_30d": 36.9783,
        "volume_ratio": 0.902,
        "regime": "bear",
        "halving_cycle_day": 739
      },
      "defi": {
        "defi_tvl_total": 546680402667.11,
        "defi_stablecoin_median_apy": 3.65,
        "defi_stablecoin_apy_change_7d": -0.2107,
        "mc_tvl_ratio": 2.7753
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
        "momentum": 50.49,
        "liquidity": 80.0,
        "derivatives": 60.0,
        "defi": 52.0,
        "onchain": 44.3,
        "sentiment": 45.0,
        "data_quality_penalty": -5.0
      },
      "action_score": 47,
      "final_score": 47,
      "confidence": "high",
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
        "summary": "BTC remains in a bear regime as confirmed by price below the 200-day SMA (-9.4%) and an RSI of 58.3, which is within the bear resistance zone (55-65), indicating limited upside momentum. The recent 1-day return of -0.96% suggests short-term weakness, and volume confirmation is suboptimal (volume ratio 0.9 < 1.5), reducing confidence in any breakout attempts. Despite a 30-day return of +14.9%, the RSI and price level indicate these are likely bear market rallies rather than trend reversals. The halving cycle day at 739 (beyond typical bullish 12-18 month window) implies increasing reversal risk. Seasonality impact is negligible as it is a Tuesday. Given the volume and technicals, selling rallies toward the 50-day SMA is the preferred strategy. Key invalidation includes a sustained break above 200-day SMA and RSI moving decisively above 65 with strong volume, which would signal regime change. Coverage gap on real volume data due to missing Coinglass API lowers conviction on breakout/breakdown signals. Without clearer fundamental or sentiment catalysts, a cautious bearish stance is warranted.",
        "signal": "cautious",
        "confidence": "low",
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
        "support": null,
        "resistance": "50-day SMA (approx. level requires updated data)"
      },
      "defi_fundamentals_analyst": {
        "summary": "DeFi fundamentals currently show a mixed picture: while total TVL remains elevated above $546B, the lack of breakdown in native token terms and absence of user growth data limit confidence in the quality and sustainability of this liquidity. The MC/TVL ratio near 2.78 points to significant overvaluation of DeFi protocol tokens relative to their locked capital, raising caution about speculative excess. Stablecoin lending yields around 3.9% suggest moderate leverage demand without signs of a risk-on binge. However, key metrics such as lending utilization, unique wallet growth, and stablecoin macro flows are missing, constraining thorough risk assessment. In sum, DeFi pricing appears stretched, with fundamentals not yet confirming robust organic growth or capital inflows. Traders should watch for valuation multiple contraction, wallet expansion, or rising stablecoin supply as potential green flags; conversely, persistent coverage gaps mean latent risks like liquidity stress or mercenary capital remain. Current stance is neutral given this data-limited environment.",
        "signal": "neutral",
        "confidence": "medium",
        "stablecoin_signals": "Stablecoin APYs near 3.9% imply moderate demand for stablecoin lending; lack of supply growth and dominance info limits inference on net capital flow direction. Overall, stablecoin data is insufficient to confirm macro inflow or outflow trend.",
        "data_gaps": [
          "No data on user count trends or wallet activity to assess true capital breadth and concentration risks",
          "No lending protocol utilization rates to evaluate possible stress or liquidity shortages",
          "No stablecoin supply growth or dominance metrics to assert directional macro capital flow",
          "Limited fee and revenue data to assess protocol health and user engagement dynamics"
        ]
      },
      "derivatives_analyst": {
        "summary": "BTC derivatives data shows a near-neutral funding rate slightly negative, suggesting mild short bias without material crowding. Open interest rose modestly by 1.4%, implying moderate new position entry but leverage level and risk profile are unclear without market cap or exchange-level breakdown. The lack of coinglass coverage especially restricts ability to confidently assess funding rate z-scores, multi-exchange positioning divergences, and liquidation cascades that historically inform short-term risk scenarios. Given these constraints, derivatives markets appear balanced with low conviction to expect near-term tail risk from leveraged longs or shorts. Additional data like OI ratios, ELR, or significant liquidation events would be needed to form a higher-confidence directional thesis. For now, derivatives positioning is neutral to mildly bearish with moderate caution advised if OI growth trends continue.",
        "signal": "neutral",
        "confidence": "low",
        "positioning_thesis": "Due to missing coinglass data, derivatives conviction is constrained. Funding rate around zero with a slight negative reading suggests no strong crowding in longs or shorts. Open interest is growing moderately, indicating some fresh positioning but without leverage ratios or liquidation stats, derivatives risk cannot be fully gauged. Spot momentum may provide weak proxy signals but is insufficient to build a confident bullish or bearish thesis on derivatives-driven price moves. Overall, the market appears balanced with mild short bias and moderate risk of increased volatility if OI growth continues.",
        "data_gaps": [
          "No coinglass coverage limits ability to analyze funding rate z-score, multi-exchange divergence, leveraged positioning, and liquidation flows",
          "Lack of OI market cap ratio and ELR reduces confidence in assessing leverage risks",
          "Absence of liquidation data prevents judgment on recent deleveraging or capitulation signals",
          "No CVD data unavailable to confirm the quality of OI and price moves"
        ]
      },
      "news_analyst": {
        "summary": "BTC is supported near-term by clear institutional adoption signals, including an upcoming major bank integration and a technical upgrade (Taproot v1.2) improving network efficiency and privacy. Concurrently, rising whale accumulation and steady futures call interest reinforce positive positioning. However, regulatory headwinds are material and imminent\u2014EU's MiCA tightening and pending US SEC statements on BTC ETFs introduce elevated risk of market sentiment deterioration. Liquidity is mildly constrained due to withdrawal issues on major exchanges, and mining difficulty spikes create caution around miner sell-offs. Macroeconomic stability without fresh monetary surprises underpins a steady baseline but limits rapid price acceleration. Overall, catalysts are actionable with high regulatory risk; close monitoring over the next week is warranted.",
        "signal": "contextualized",
        "confidence": null,
        "evidence_quality": "actionable",
        "top_risk": "Regulatory tightening in EU (MiCA) and looming SEC announcements on BTC spot ETFs"
      },
      "bull_researcher": {
        "thesis": "Despite near-term technical bearishness and elevated DeFi valuations, BTC's longer-term fundamentals remain constructive supported by moderate derivatives positioning, steady DeFi TVL, stablecoin yields indicating healthy leverage demand, and institutional interest including upcoming technical upgrades. The modest negative funding rates and moderate open interest growth suggest no excessive crowding, implying stability with room for upside. The post-halving window has passed but the latest 30-day +15% gain signals resilience beyond typical bear rallies, supported by steady TVL and moderate stablecoin APYs. Regulatory risks remain, but ongoing technical enhancements and whale accumulation underpin a sustained constructive outlook in a balanced environment.",
        "argument": "Bull Analyst: BTC currently trades in a delicate balance beneath its 200-day SMA, with RSI indicating limited momentum but a strong 30-day total return (+15%) that defies pure bear market expectations. Derivatives positioning remains balanced, reflected in near-neutral funding rates and moderate open interest growth, signaling stable leverage without excess crowding. DeFi fundamentals reveal mixed signals: elevated TVL supports underlying demand while high token valuations warrant caution, though moderate stablecoin yields (~3.9%) evidence healthy leverage activity rather than frothy speculation. Upcoming institutional catalysts, including major bank integrations and the Taproot upgrade, provide potential triggers for renewed investor confidence. While regulatory risks warrant vigilance, the current data supports a constructive outlook grounded in fundamental stability and measured market positioning. Key risks to watch include sustained failure to breach critical technical resistance, negative shifts in DeFi capital flows, and spikes in derivatives-driven volatility. Resolving these data gaps on user engagement, stablecoin supply trends, and detailed derivatives metrics will improve conviction ahead of possible trend shifts. While price is below 200-day SMA, the sustained 30-day +15% return and moderate RSI near resistance show resilience; sub-extreme volume ratio reflects healthy consolidation, not capitulation. This sets the stage for a base build poised for eventual breakouts if catalysts materialize.",
        "confidence": "med",
        "top_point": "BTC price is consolidating slightly below 200-day SMA with RSI in bear resistance zone, but 30-day +15% return demonstrates underlying strength beyond typical bear rallies.",
        "top_rebuttal": "While price is below 200-day SMA, the sustained 30-day +15% return and moderate RSI near resistance show resilience; sub-extreme volume ratio reflects healthy consolidation, not capitulation. This sets the stage for a base build poised for eventual breakouts if catalysts materialize.",
        "data_gaps": [
          "User growth and wallet activity metrics to confirm breadth and sustainability of liquidity in DeFi.",
          "Stablecoin supply growth and dominance data to clarify macro capital flow direction.",
          "More granular derivatives data including funding z-scores, OI market cap ratios, and liquidation events for definitive risk profiling."
        ]
      },
      "bear_researcher": {
        "thesis": "BTC remains vulnerable below its 200-day SMA with bearish technicals, muted volume confirmation, and stretched DeFi valuations that lack native token inflows or user growth confirmation. The modest 30-day return masks typical bear market rallies prone to failure given weak volume and unresolved derivatives risks exacerbated by significant data gaps. Elevated MC/TVL ratios near 2.78 imply overvaluation unsupported by fee or revenue data. Funding rates near neutral but with rising OI lack leverage and liquidation depth needed to assure stability and crowding is uncertain due to missing coinglass metrics. Regulatory headwinds and macro risk remain material. Without clear breakout volume, sustained technical breach, or robust onchain/user evidence, BTC is exposed to downside rallies and broken support traps.",
        "argument": "Bear Analyst: BTC's current position below the 200-day SMA, weak technical momentum, and lacking volume confirmation after a +15% 30-day rally strongly suggest a bear market trap rather than genuine rebound. The DeFi market's high MC/TVL ratio and absence of critical onchain user and revenue data point to valuations that are potentially overstretched and speculative. While derivatives funding rates appear balanced, critical datasets on leverage, liquidation events, and OI relative to market capitalization remain missing and prevent confident assessment of risk exposure. Elevated open interest combined with limited leverage transparency historically signals crowded longs prone to correction. Regulatory uncertainty and macro risks compound these vulnerabilities. Thus, the case for sustainable upside is unproven absent clear fundamental and technical breakouts. A risk-managed approach favors selling rallies and treating dips cautiously until robust breakout confirmation and comprehensive data fill gaps. Such rallies are frequent in bear markets and often fail without volume confirmation; volume ratio below 1.0 signals weak participation and risk of reversal rather than trend reversal.",
        "confidence": "high",
        "top_point": "BTC currently trades ~9.4% below its 200-day SMA with RSI near bear resistance (58-60), indicating weak technical momentum; volume ratio ~0.9 confirms lack of strong breakout volume.",
        "top_rebuttal": "Such rallies are frequent in bear markets and often fail without volume confirmation; volume ratio below 1.0 signals weak participation and risk of reversal rather than trend reversal.",
        "data_gaps": [
          "Lack of coinglass or equivalent derivatives data on funding rate z-scores, liquidation volumes, and leverage ratios limits ability to assess short-term tail risk.",
          "Absence of native-token denominated TVL, protocol revenue, and user engagement data restricts interpretation of DeFi fundamental strength.",
          "Missing stablecoin supply growth and dominance metrics constrain macro capital flow and leverage demand assessment.",
          "No granular metrics on wallet growth and lending utilization rates limit evaluation of genuine capital base and liquidity stress signals."
        ]
      },
      "risk_manager": {
        "summary": "BTC remains in a fragile bear regime trading ~9.4% below its 200-day SMA with RSI in bear resistance zone (~58), and a recent 1-day loss (-0.96%) signaling near-term technical weakness. The volume ratio under 1.0 (0.9) reflects muted participation, increasing risk of failed bear rallies. Despite a strong 30-day return (+15%), this likely reflects bear market chops rather than trend reversal. DeFi fundamentals show stretched valuations (MC/TVL ~2.78) without clear user growth or fee data, limiting confidence in sustainable demand. Moderately negative funding rates and small OI growth suggest mild short bias but no excess leveraged crowding, though key derivatives data (funding z-scores, liquidation stats, ELR) are missing due to Coinglass API gap, restricting tail-risk assessment. Regulatory headwinds from EU MiCA tightening and US SEC ETF scrutiny pose material downside catalysts. Operational risks include mild liquidity constraints and mining sell pressure. Correlations remain high with BTC dominating risks; no diversification benefits assumed. Liquidation cascade risk is moderate with no clear leveraged extremes but data gaps impede confidence. Position sizing should remain prudent given current environment. Key invalidation for bearish thesis is sustained break above 200-day SMA with increasing volume and improving RSI. Until then, risk-managed approach favors avoiding new entries and reducing exposure where appropriate given regulatory and technical uncertainty.",
        "recommendation": "avoid",
        "risk_bias": "elevated",
        "cascade_risk_level": "moderate",
        "aggressive_view": "Aggressive Analyst: BTC's price action below the 200-day SMA (-9.4%) alongside a moderate RSI (~58) and volume ratio (~0.9) signals technically bearish conditions but not outright collapse. The 30-day +15% return evidences resilient demand amid bear rallies, a setup warranting immediate press of risk despite lacking ideal volume confirmation. While WoC data gaps (missing Coinglass for derivatives funding z-scores, and user growth in DeFi) limit perfect clarity, limited confirmation exists: stable moderate open interest growth (~1.4%), near-neutral funding rate (-0.0032%), and elevated but steady DeFi TVL (~$546B) with stablecoin APYs (~3.9%) suggest measured risk appetite, not panicked liquidation. Institutional and technical catalysts in the short window\u2014major bank integration with BTC treasury and Taproot v1.2 upgrade\u2014are actionable positive drivers that can break the stalemate. Regulatory risks (EU MiCA, SEC ETF decisions) pose acute downside scenarios but have not yet triggered capitulation. Waiting for ideal breakout volume or daily closes >200-day SMA at >1.5x volume in this week-long horizon forfeits opportunity, given the asymmetric potential from catalysts and the persistent risk of sudden regime shifts implied by volume and derivatives ambiguity. The prudent aggressive stance is to press risk on partial signals now, using tight stops below current supports and monitoring quickly evolving derivatives and regulatory updates to exit early if invalidation thresholds breach. This tactical engagement balances incomplete data with concrete actionable positives. A failed breakout or volume surge to downside would then validate swift pivot to protective posture. In sum, current limited confirmation is enough to justify an aggressive partial long with tight risk control rather than blanket avoidance or defensive passivity.",
        "conservative_view": "Conservative Analyst: Despite some positive signals like a recent 30-day +15% BTC price gain and institutional catalyst announcements, significant risks and data gaps argue strongly for capital preservation. BTC remains nearly 9.4% below its 200-day SMA with an RSI in a bear resistance zone (~58), supported by sub-par volume (volume ratio ~0.9), highlighting fragile technical structure prone to failed rallies and downside traps. DeFi valuations are elevated with an MC/TVL ratio around 2.78, signaling speculative risk unsupported by user growth or revenue data, while absence of native-token TVL and lending utilization information limits confidence in sustainable capital inflows. Derivatives market data is incomplete due to missing coinglass metrics, obscuring leverage, funding rate extremes, liquidation events, and open interest relative risk. Moderately rising open interest and near-neutral funding rates offer limited comfort given this opacity. Regulatory uncertainties, notably EU MiCA and pending US SEC BTC ETF decisions, create material downside risks that could quickly trigger capitulation, especially under fragile structural conditions. The missing data on derivatives crowding and DeFi user engagement compounds risk assessment uncertainty, suggesting latent vulnerabilities. Therefore, without sustained price and volume breakout above 200-day SMA confirmed by healthy volume (>1.5x avg), and clearer fundamental confirmation via onchain user growth and risk-on derivatives signals, it is prudent to avoid or cap exposure to BTC over the next 7 days. Preservation of capital through risk-managed positioning and tight stops is recommended until robust data or technical validation emerges.",
        "neutral_view": "Neutral Analyst: BTC exhibits a technical regime of caution: price remains ~9.4% below its 200-day SMA with RSI in a bear resistance zone and volume ratio below 1.0, signaling weak breakout momentum and risk of failed rallies. Despite a resilient 30-day price return of +15%, this mirrors typical bear market rallies lacking volume or broad participation. DeFi fundamentals show mixed signals: an elevated MC/TVL ratio (~2.78) implies speculative pricing unbacked by native token inflows or onchain user growth data, while stablecoin lending APYs near 3.9% suggest moderate leverage demand without overheating. Derivatives positioning is neutral to mildly bearish with near-zero funding rates and moderately rising open interest, but the absence of granular coinglass data (funding z-scores, liquidations, leverage ratios) limits risk clarity. Institutional catalysts\u2014major bank BTC integration and Taproot 1.2 upgrade\u2014offer positive near-term upside, yet looming regulatory risks (EU MiCA, SEC ETF decisions) heighten downside vulnerability. Given incomplete derivatives and user engagement data, the environment lacks robust confirmation for sustained upside. The prudent stance is disciplined neutrality: avoid aggressive longs; maintain minimal exposure with tight stop-losses, selling rallies and preserving capital until clear technical breakouts above 200-day SMA with supporting volume, improved derivatives visibility, or definitive fundamental evidence of organic capital inflow emerge. Close monitoring of regulatory developments and derivatives metrics is essential. This posture balances the asymmetric potential of catalysts against structural technical and fundamental uncertainties, mitigating downside while preserving optionality for upside should conditions improve."
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
- report: The integrated crypto read stays avoid: score=47, regime=bull_trend, MC/TVL=2.7753, funding=-3.2e-05. The system sees enough fragility to stay conservative rather than press for directional size.
