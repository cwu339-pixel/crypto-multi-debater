# Risk Manager

- role: risk_manager
- title: Risk Manager
## Risk Summary
- {'risk': 'High drawdown risk due to bear regime and weak technical base', 'severity': 'high', 'source_role': 'technical_analyst', 'mitigation': 'Strict position sizing with stops at 10-15%; avoid large exposures'}
- {'risk': 'Leverage and liquidation unseen due to derivatives data gaps', 'severity': 'high', 'source_role': 'derivatives_analyst', 'mitigation': 'Maintain conservative leverage, monitor for sudden funding/funding z-score changes'}
- {'risk': 'Fundamental uncertainty from incomplete DeFi metrics', 'severity': 'med', 'source_role': 'defi_fundamentals_analyst', 'mitigation': 'Limit speculative exposure until data clarity improves'}
- {'risk': 'Regulatory tightening and macro uncertainties pressing downside', 'severity': 'med', 'source_role': 'news_analyst', 'mitigation': 'Reduce size or hedge during macro events; avoid high leverage'}
- {'risk': 'Correlation concentration risk treating all crypto as BTC-beta', 'severity': 'med', 'source_role': 'risk_manager', 'mitigation': 'Use portfolio-level crypto risk sizing; avoid over-diversification in altcoins'}
- guardrails: {'max_position_pct': {'BTC': '10%-20% of crypto allocation', 'mid_cap': '3%-5%', 'small_cap_defi': '1%-2%', 'micro_cap_speculative': '0.5%-1%'}, 'stop_logic': ['Single position loss capped at 10%-15% for swing trades', 'Stop tightened at 5% portfolio drawdown by reviewing thesis', 'Reduce sizes by 50% at 10% drawdown, close speculative at 15%'], 'sizing_recommendation': 'Use half Kelly (25%-50% of full Kelly) with volatility scaling; avoid >1-2% portfolio risk per trade'}
- cascade_risk_level: moderate
## Operational Risks
- Incomplete DeFi and derivatives data reduce visibility on systemic leverage and stress
- Regulatory risks from EU AML tightening liquidity
- Potential exchange risk not flagged but maintain <25% assets per exchange
- Bridge and stablecoin risks unresolved due to data gaps
## Data Quality Flags
- Missing derivatives funding rate z-score and liquidation volume data (coinglass API key missing)
- Defillama data gaps impacting TVL, lending utilization, and user growth metrics
- No comprehensive cross-chain capital flow or stablecoin yield data
- recommendation: avoid
- risk_bias: elevated
- summary: BTC remains in a bear regime with price well below the 200-day SMA and relatively subdued RSI, signaling weak technical support despite a minor 1-day bounce. Volume remains low for a sustained reversal, and derivatives data—although neutral—lack key metrics (funding rate z-score, liquidation volumes) that limit leverage stress visibility. DeFi data gaps (TVL, user growth, fee trends) further obscure fundamental health assessment. Regulatory tightening and macro uncertainties amplify downside risk. Current position sizing must factor in these incomplete signals and elevated uncertainty, emphasizing tight stops and low concentration. Cascade risk is moderate given stable but slightly declining open interest and neutral funding rates. Without clear volume-backed trend strength, leverage expansion, or fundamental inflows, the setup favors caution, with any recovery contingent on closing above SMA200 and improved derivatives transparency. Key invalidation includes sustained price and volume breakout with healthy leverage expansion and no liquidation stress.
- provider: openai
- analysis_mode: prompt_driven
- risk_views: {'aggressive': 'Aggressive Analyst: The current BTC setup, despite low aggregate score and cautious technical analyst stance, justifies pressing risk from an aggressive perspective. The 1.93% 1-day return combined with volume ratio at 1.09x (close to breakout threshold) and RSI at 34.3 indicate short-term bullish momentum emerging within a bear regime, signaling an early dip-buy entry opportunity before full oversold confirmation or large volume surge. While data gaps (DeFi TVL, derivatives liquidation metrics) limit full conviction, the slight return and stable funding rate (-0.0034%) argue against immediate deleveraging cascade, confirming controlled risk. News catalysts of institutional demand resurgence and dovish Fed commentary support a 3-day horizon upside of 10-20%. Excessive caution ignores these early signals and misses cost-effective entry points—the required confirmation is not perfect volume spikes or deeply oversold RSI below 20; a moderate bounce with stable volume in a bear trend can justify agile risk-taking to capitalize on short-term range reversion or relief rallies. Key invalidation triggers remain a sustained close below current support levels with volume collapse or sudden spike in deleveraging indicators. In sum, risk pressing today is warranted, with position sizing calibrated for medium confidence and awareness of data limitations; waiting for perfect confirmation risks worse entry levels or missed upside setups.', 'conservative': 'Conservative Analyst: BTC currently trades well below its 200-day SMA (-25%), deep in a bear regime with weak momentum indicated by RSI near 34.3 and a volume ratio (1.09x) insufficient to confirm a sustainable breakout. Short-term returns show a modest bounce (+1.93%), but 30-day returns remain negative and realized volatility is elevated, indicative of ongoing market fragility. Derivative markets present mild deleveraging signals via declining open interest (-0.81%) and nearly neutral funding rates (-0.0034%), yet critical data gaps persist, notably missing liquidation metrics and leverage z-scores, which obscures true risk of cascade liquidations or crowded positioning. DeFi fundamental data coverage is notably incomplete, with missing TVL and user growth figures, undermining confidence in capital inflow narratives and leaving protocol health unverifiable. Regulatory tightening in the EU and macro uncertainty compound downside risks. Combined, this fragile and data-limited structure argues strongly for capital preservation and avoidance of increased exposure until clear evidence emerges. Specifically, entries should wait for confirmatory signals such as sustained price reclaim above the 200-day SMA with volume exceeding 1.5x norm, clear increases in derivatives open interest accompanied by positive funding rate z-scores, and robust fundamental data confirming capital inflows and ecosystem health. Absent these, aggressive risk-taking exposes portfolios to downside traps and leverage-induced drawdowns not visible in current partial metrics. The prudent stance is to cap exposure and prioritize preservation over speculation in the near term.', 'neutral': 'Neutral Analyst: BTC is currently entrenched in a bear regime, trading about 25% below its 200-day SMA with an RSI near 34, reflecting mild bearish momentum but no oversold capitulation. A modest 1.93% one-day bounce and volume ratio around 1.09x indicate tentative short-term relief without strong breakout conviction. Derivatives data show a near-neutral funding rate (-0.0034%) and slight open interest decline (-0.81%), consistent with cautious deleveraging rather than fresh leveraged longs or panic liquidations. However, critical gaps in liquidation metrics and leverage z-scores limit leverage risk assessment. DeFi fundamentals lack key TVL, user growth, and fee signals due to coverage issues, restricting confidence in ecosystem health and fresh capital inflows. News catalysts present a mixed picture: institutional demand and dovish Fed tone support upside potential, but regulatory tightening in the EU and macro uncertainties weigh on liquidity and add downside risk. The debate contrasts an aggressive stance favoring calibrated dip-buying on early bullish signals and a conservative posture emphasizing capital preservation until more robust multi-source confirmations emerge. Given the incomplete data, subdued volume, and protracted bear regime, the neutral, disciplined recommendation is to maintain a cautious or reduced risk stance near-term. Close monitoring for a sustained reclaim above the 200-day SMA with volume above 1.5x, accompanied by improving RSI and rising open interest with positive funding rate z-scores, should guide increasing exposure. Conversely, failing to hold current supports or sudden spike in deleveraging and capital outflows would reinforce bearish positioning. This balanced approach prudently weighs limited upside signals against significant data uncertainties and prevailing bear market structure, avoiding premature risk escalation amid incomplete visibility.'}
- risk_debate_state: {'history': 'Aggressive Analyst: The current BTC setup, despite low aggregate score and cautious technical analyst stance, justifies pressing risk from an aggressive perspective. The 1.93% 1-day return combined with volume ratio at 1.09x (close to breakout threshold) and RSI at 34.3 indicate short-term bullish momentum emerging within a bear regime, signaling an early dip-buy entry opportunity before full oversold confirmation or large volume surge. While data gaps (DeFi TVL, derivatives liquidation metrics) limit full conviction, the slight return and stable funding rate (-0.0034%) argue against immediate deleveraging cascade, confirming controlled risk. News catalysts of institutional demand resurgence and dovish Fed commentary support a 3-day horizon upside of 10-20%. Excessive caution ignores these early signals and misses cost-effective entry points—the required confirmation is not perfect volume spikes or deeply oversold RSI below 20; a moderate bounce with stable volume in a bear trend can justify agile risk-taking to capitalize on short-term range reversion or relief rallies. Key invalidation triggers remain a sustained close below current support levels with volume collapse or sudden spike in deleveraging indicators. In sum, risk pressing today is warranted, with position sizing calibrated for medium confidence and awareness of data limitations; waiting for perfect confirmation risks worse entry levels or missed upside setups.\nConservative Analyst: BTC currently trades well below its 200-day SMA (-25%), deep in a bear regime with weak momentum indicated by RSI near 34.3 and a volume ratio (1.09x) insufficient to confirm a sustainable breakout. Short-term returns show a modest bounce (+1.93%), but 30-day returns remain negative and realized volatility is elevated, indicative of ongoing market fragility. Derivative markets present mild deleveraging signals via declining open interest (-0.81%) and nearly neutral funding rates (-0.0034%), yet critical data gaps persist, notably missing liquidation metrics and leverage z-scores, which obscures true risk of cascade liquidations or crowded positioning. DeFi fundamental data coverage is notably incomplete, with missing TVL and user growth figures, undermining confidence in capital inflow narratives and leaving protocol health unverifiable. Regulatory tightening in the EU and macro uncertainty compound downside risks. Combined, this fragile and data-limited structure argues strongly for capital preservation and avoidance of increased exposure until clear evidence emerges. Specifically, entries should wait for confirmatory signals such as sustained price reclaim above the 200-day SMA with volume exceeding 1.5x norm, clear increases in derivatives open interest accompanied by positive funding rate z-scores, and robust fundamental data confirming capital inflows and ecosystem health. Absent these, aggressive risk-taking exposes portfolios to downside traps and leverage-induced drawdowns not visible in current partial metrics. The prudent stance is to cap exposure and prioritize preservation over speculation in the near term.\nNeutral Analyst: BTC is currently entrenched in a bear regime, trading about 25% below its 200-day SMA with an RSI near 34, reflecting mild bearish momentum but no oversold capitulation. A modest 1.93% one-day bounce and volume ratio around 1.09x indicate tentative short-term relief without strong breakout conviction. Derivatives data show a near-neutral funding rate (-0.0034%) and slight open interest decline (-0.81%), consistent with cautious deleveraging rather than fresh leveraged longs or panic liquidations. However, critical gaps in liquidation metrics and leverage z-scores limit leverage risk assessment. DeFi fundamentals lack key TVL, user growth, and fee signals due to coverage issues, restricting confidence in ecosystem health and fresh capital inflows. News catalysts present a mixed picture: institutional demand and dovish Fed tone support upside potential, but regulatory tightening in the EU and macro uncertainties weigh on liquidity and add downside risk. The debate contrasts an aggressive stance favoring calibrated dip-buying on early bullish signals and a conservative posture emphasizing capital preservation until more robust multi-source confirmations emerge. Given the incomplete data, subdued volume, and protracted bear regime, the neutral, disciplined recommendation is to maintain a cautious or reduced risk stance near-term. Close monitoring for a sustained reclaim above the 200-day SMA with volume above 1.5x, accompanied by improving RSI and rising open interest with positive funding rate z-scores, should guide increasing exposure. Conversely, failing to hold current supports or sudden spike in deleveraging and capital outflows would reinforce bearish positioning. This balanced approach prudently weighs limited upside signals against significant data uncertainties and prevailing bear market structure, avoiding premature risk escalation amid incomplete visibility.', 'aggressive_history': 'Aggressive Analyst: The current BTC setup, despite low aggregate score and cautious technical analyst stance, justifies pressing risk from an aggressive perspective. The 1.93% 1-day return combined with volume ratio at 1.09x (close to breakout threshold) and RSI at 34.3 indicate short-term bullish momentum emerging within a bear regime, signaling an early dip-buy entry opportunity before full oversold confirmation or large volume surge. While data gaps (DeFi TVL, derivatives liquidation metrics) limit full conviction, the slight return and stable funding rate (-0.0034%) argue against immediate deleveraging cascade, confirming controlled risk. News catalysts of institutional demand resurgence and dovish Fed commentary support a 3-day horizon upside of 10-20%. Excessive caution ignores these early signals and misses cost-effective entry points—the required confirmation is not perfect volume spikes or deeply oversold RSI below 20; a moderate bounce with stable volume in a bear trend can justify agile risk-taking to capitalize on short-term range reversion or relief rallies. Key invalidation triggers remain a sustained close below current support levels with volume collapse or sudden spike in deleveraging indicators. In sum, risk pressing today is warranted, with position sizing calibrated for medium confidence and awareness of data limitations; waiting for perfect confirmation risks worse entry levels or missed upside setups.', 'conservative_history': 'Conservative Analyst: BTC currently trades well below its 200-day SMA (-25%), deep in a bear regime with weak momentum indicated by RSI near 34.3 and a volume ratio (1.09x) insufficient to confirm a sustainable breakout. Short-term returns show a modest bounce (+1.93%), but 30-day returns remain negative and realized volatility is elevated, indicative of ongoing market fragility. Derivative markets present mild deleveraging signals via declining open interest (-0.81%) and nearly neutral funding rates (-0.0034%), yet critical data gaps persist, notably missing liquidation metrics and leverage z-scores, which obscures true risk of cascade liquidations or crowded positioning. DeFi fundamental data coverage is notably incomplete, with missing TVL and user growth figures, undermining confidence in capital inflow narratives and leaving protocol health unverifiable. Regulatory tightening in the EU and macro uncertainty compound downside risks. Combined, this fragile and data-limited structure argues strongly for capital preservation and avoidance of increased exposure until clear evidence emerges. Specifically, entries should wait for confirmatory signals such as sustained price reclaim above the 200-day SMA with volume exceeding 1.5x norm, clear increases in derivatives open interest accompanied by positive funding rate z-scores, and robust fundamental data confirming capital inflows and ecosystem health. Absent these, aggressive risk-taking exposes portfolios to downside traps and leverage-induced drawdowns not visible in current partial metrics. The prudent stance is to cap exposure and prioritize preservation over speculation in the near term.', 'neutral_history': 'Neutral Analyst: BTC is currently entrenched in a bear regime, trading about 25% below its 200-day SMA with an RSI near 34, reflecting mild bearish momentum but no oversold capitulation. A modest 1.93% one-day bounce and volume ratio around 1.09x indicate tentative short-term relief without strong breakout conviction. Derivatives data show a near-neutral funding rate (-0.0034%) and slight open interest decline (-0.81%), consistent with cautious deleveraging rather than fresh leveraged longs or panic liquidations. However, critical gaps in liquidation metrics and leverage z-scores limit leverage risk assessment. DeFi fundamentals lack key TVL, user growth, and fee signals due to coverage issues, restricting confidence in ecosystem health and fresh capital inflows. News catalysts present a mixed picture: institutional demand and dovish Fed tone support upside potential, but regulatory tightening in the EU and macro uncertainties weigh on liquidity and add downside risk. The debate contrasts an aggressive stance favoring calibrated dip-buying on early bullish signals and a conservative posture emphasizing capital preservation until more robust multi-source confirmations emerge. Given the incomplete data, subdued volume, and protracted bear regime, the neutral, disciplined recommendation is to maintain a cautious or reduced risk stance near-term. Close monitoring for a sustained reclaim above the 200-day SMA with volume above 1.5x, accompanied by improving RSI and rising open interest with positive funding rate z-scores, should guide increasing exposure. Conversely, failing to hold current supports or sudden spike in deleveraging and capital outflows would reinforce bearish positioning. This balanced approach prudently weighs limited upside signals against significant data uncertainties and prevailing bear market structure, avoiding premature risk escalation amid incomplete visibility.', 'latest_speaker': 'Neutral', 'current_aggressive_response': 'Aggressive Analyst: The current BTC setup, despite low aggregate score and cautious technical analyst stance, justifies pressing risk from an aggressive perspective. The 1.93% 1-day return combined with volume ratio at 1.09x (close to breakout threshold) and RSI at 34.3 indicate short-term bullish momentum emerging within a bear regime, signaling an early dip-buy entry opportunity before full oversold confirmation or large volume surge. While data gaps (DeFi TVL, derivatives liquidation metrics) limit full conviction, the slight return and stable funding rate (-0.0034%) argue against immediate deleveraging cascade, confirming controlled risk. News catalysts of institutional demand resurgence and dovish Fed commentary support a 3-day horizon upside of 10-20%. Excessive caution ignores these early signals and misses cost-effective entry points—the required confirmation is not perfect volume spikes or deeply oversold RSI below 20; a moderate bounce with stable volume in a bear trend can justify agile risk-taking to capitalize on short-term range reversion or relief rallies. Key invalidation triggers remain a sustained close below current support levels with volume collapse or sudden spike in deleveraging indicators. In sum, risk pressing today is warranted, with position sizing calibrated for medium confidence and awareness of data limitations; waiting for perfect confirmation risks worse entry levels or missed upside setups.', 'current_conservative_response': 'Conservative Analyst: BTC currently trades well below its 200-day SMA (-25%), deep in a bear regime with weak momentum indicated by RSI near 34.3 and a volume ratio (1.09x) insufficient to confirm a sustainable breakout. Short-term returns show a modest bounce (+1.93%), but 30-day returns remain negative and realized volatility is elevated, indicative of ongoing market fragility. Derivative markets present mild deleveraging signals via declining open interest (-0.81%) and nearly neutral funding rates (-0.0034%), yet critical data gaps persist, notably missing liquidation metrics and leverage z-scores, which obscures true risk of cascade liquidations or crowded positioning. DeFi fundamental data coverage is notably incomplete, with missing TVL and user growth figures, undermining confidence in capital inflow narratives and leaving protocol health unverifiable. Regulatory tightening in the EU and macro uncertainty compound downside risks. Combined, this fragile and data-limited structure argues strongly for capital preservation and avoidance of increased exposure until clear evidence emerges. Specifically, entries should wait for confirmatory signals such as sustained price reclaim above the 200-day SMA with volume exceeding 1.5x norm, clear increases in derivatives open interest accompanied by positive funding rate z-scores, and robust fundamental data confirming capital inflows and ecosystem health. Absent these, aggressive risk-taking exposes portfolios to downside traps and leverage-induced drawdowns not visible in current partial metrics. The prudent stance is to cap exposure and prioritize preservation over speculation in the near term.', 'current_neutral_response': 'Neutral Analyst: BTC is currently entrenched in a bear regime, trading about 25% below its 200-day SMA with an RSI near 34, reflecting mild bearish momentum but no oversold capitulation. A modest 1.93% one-day bounce and volume ratio around 1.09x indicate tentative short-term relief without strong breakout conviction. Derivatives data show a near-neutral funding rate (-0.0034%) and slight open interest decline (-0.81%), consistent with cautious deleveraging rather than fresh leveraged longs or panic liquidations. However, critical gaps in liquidation metrics and leverage z-scores limit leverage risk assessment. DeFi fundamentals lack key TVL, user growth, and fee signals due to coverage issues, restricting confidence in ecosystem health and fresh capital inflows. News catalysts present a mixed picture: institutional demand and dovish Fed tone support upside potential, but regulatory tightening in the EU and macro uncertainties weigh on liquidity and add downside risk. The debate contrasts an aggressive stance favoring calibrated dip-buying on early bullish signals and a conservative posture emphasizing capital preservation until more robust multi-source confirmations emerge. Given the incomplete data, subdued volume, and protracted bear regime, the neutral, disciplined recommendation is to maintain a cautious or reduced risk stance near-term. Close monitoring for a sustained reclaim above the 200-day SMA with volume above 1.5x, accompanied by improving RSI and rising open interest with positive funding rate z-scores, should guide increasing exposure. Conversely, failing to hold current supports or sudden spike in deleveraging and capital outflows would reinforce bearish positioning. This balanced approach prudently weighs limited upside signals against significant data uncertainties and prevailing bear market structure, avoiding premature risk escalation amid incomplete visibility.', 'count': 3}
- report: BTC remains in a bear regime with price well below the 200-day SMA and relatively subdued RSI, signaling weak technical support despite a minor 1-day bounce. Volume remains low for a sustained reversal, and derivatives data—although neutral—lack key metrics (funding rate z-score, liquidation volumes) that limit leverage stress visibility. DeFi data gaps (TVL, user growth, fee trends) further obscure fundamental health assessment. Regulatory tightening and macro uncertainties amplify downside risk. Current position sizing must factor in these incomplete signals and elevated uncertainty, emphasizing tight stops and low concentration. Cascade risk is moderate given stable but slightly declining open interest and neutral funding rates. Without clear volume-backed trend strength, leverage expansion, or fundamental inflows, the setup favors caution, with any recovery contingent on closing above SMA200 and improved derivatives transparency. Key invalidation includes sustained price and volume breakout with healthy leverage expansion and no liquidation stress.
- signal: avoid
- confidence: low
## Referenced Fields
- latest_close
- return_1d_pct
- rsi_14
- price_vs_sma200_pct
- volume_ratio
- funding_rate
- open_interest
- coverage_gaps
- regime
- prompt_path: /Users/wuchenghan/Projects/crypto-multi-debater/src/crypto_research_agent/agents/prompts/risk_manager.md
- prompt_text: # Risk Manager

You are the risk manager for a crypto research system.
Use the prior role memos to define risk bias, key constraints, and invalidation conditions.
Keep the output operational rather than narrative.

## Domain Knowledge: Risk Management Framework

### Position Sizing Rules
- Max 1-2% of portfolio RISK per trade (risk = position size * stop distance, not position size itself)
- Max 5% of portfolio in a single asset for concentrated conviction trades
- Use fractional Kelly (25-50% of full Kelly). Full Kelly is dangerous in crypto — can suggest 15-40% positions
- Half Kelly retains 75% of max growth rate while reducing variance to 25%

Tiered sizing by asset class:
- BTC/ETH: up to 10-20% of crypto allocation
- Mid-cap (top 20): max 3-5% per position
- Small-cap / DeFi: max 1-2% per position
- Micro-cap / speculative: max 0.5-1% ("lottery ticket" sizing)

Volatility scaling: Position_Size = Risk_Budget / (ATR * Multiplier). Higher vol = smaller position automatically.

### Drawdown Thresholds and Actions
- -5% portfolio: REVIEW — reassess all positions, check if thesis intact
- -10% portfolio: REDUCE — cut position sizes by 50%, tighten all stops
- -15% portfolio: DEFENSIVE — close speculative positions, core holdings only
- -20% portfolio: HALT — stop trading, full strategy review before resuming
- -25% portfolio: RESET — close all positions, requires formal re-entry plan

Single position stops:
- Swing trades: hard stop at -10% to -15%
- Never let a single position lose >20% without thesis-driven reason

Critical context — crypto drawdowns are NOT like stocks:
- BTC historical: -93% (2011), -86% (2014), -84% (2018), -77% (2022). These are NORMAL
- Altcoins: -90% to -99% common, many never recover
- A -50% drawdown requires +100% to break even. A -75% requires +300%
- Rule: If simulated or observed max drawdown is X, expect materially worse drawdown in live trading

### Correlation Risk
- Most altcoins are 0.7-0.9 correlated with BTC in normal markets
- During market stress, correlations spike toward 1.0
- A portfolio of 10 altcoins is NOT diversified — it is concentrated BTC-beta
- Treat total crypto allocation as ONE correlated position for risk budgeting
- BTC-SPX correlation ~0.5 post-ETF. Major SPX selloff likely drags crypto down

Actual hedging:
- Works: BTC put options, short futures as hedge, 15-30% stablecoin allocation, DXY-inverse
- Does NOT work: Multiple altcoins, "sector diversification" within crypto

### Liquidation Cascade Risk Assessment
Pre-conditions for cascade:
- Funding rate > 0.05% (8h) — overheated longs
- OI at ATH or rising rapidly
- OI/Market Cap > 3% — excessive leverage
- Long-short ratio >70% one side
- Dense liquidation clusters visible on heatmaps near current price
- ELR (Estimated Leverage Ratio) > 0.22

Historical cascade examples to reference:
- March 2020: -50% in 24h, $1.1B liquidated. Exogenous shock + leverage
- May 2021: -30% in 48h, $10B+ liquidated. Multiple negative catalysts
- Nov 2022 (FTX): -25%, $8B+ cascade. Counterparty/exchange risk
- Oct 2025: $19-20B liquidated (largest ever)

Rule: REDUCE leverage before known macro risk events (FOMC, elections, CPI)
Rule: When 2+ negative catalysts align, cut leverage to zero IMMEDIATELY
Rule: Never have >25% of assets on a single exchange

### Operational Risks to Flag
Exchange risk:
- Commingling of funds, related-party trading, native token as collateral (>10% of balance sheet = reduce exposure)
- Withdrawal delays, unusual spread widening = red flags

Smart contract risk tiers:
- Tier 1 (lowest): Battle-tested >2 years, multiple audits (Aave, Uniswap, MakerDAO)
- Tier 2: Audited, 6-24 months, significant TVL
- Tier 3: <6 months, single audit, novel mechanism
- Tier 4 (highest): Unaudited, forked, anonymous team

Stablecoin risk: Diversify across 2-3 types, max 50% in single issuer. Algorithmic stablecoins = speculative, not safe havens
Bridge risk: Cross-chain bridges are #1 exploit target (>$2.5B stolen). Max 5% of portfolio in bridged assets

### Risk-Adjusted Return Benchmarks
- Sharpe > 1.0 over 3+ years = genuinely good in crypto
- Sharpe > 1.5 sustained = excellent, competitive with top funds
- BTC buy-and-hold long-term Sharpe: ~0.8-1.0
- Use Sortino ratio over Sharpe for crypto (Sharpe penalizes upside vol equally)
- A strategy with high Sharpe but -60% max drawdown is still dangerous

Strategy quality checklist:
- Sharpe > 1.0 over 2+ years
- Max drawdown < 30% (or <50% if long-only including 2022 bear)
- Calmar ratio > 1.0
- Survives at least 2 regime changes
- Sharpe > 0.7 in out-of-sample

## Output Format

Produce a JSON memo with these fields:
- `role`: "risk_manager"
- `risk_summary`: list of {risk, severity: "high"|"med"|"low", source_role, mitigation}
- `guardrails`: {max_position_pct, stop_logic: [conditions], sizing_recommendation}
- `cascade_risk_level`: "low" | "moderate" | "elevated" | "extreme" with reasoning
- `operational_risks`: list of specific operational risks identified
- `data_quality_flags`: list of data gaps that affect risk assessment
- `recommendation`: "proceed" | "reduce_size" | "avoid" with one-line reasoning

Follow a TradingAgents-style flow: first form a concise analyst report, then return compact JSON. The `report` field is mandatory. Only override structured fields when the supplied data directly supports them. Do not restate the whole schema.

Field interpretation guide:
- latest_close: Latest observed close. Use it as the anchor for all price references.
- return_1d_pct: One-day percentage move. Positive means short-term momentum, negative means near-term weakness.
- return_total_pct: Window-level cumulative return. Use it to distinguish bounce-vs-trend continuation.
- avg_volume: Average traded volume proxy. Higher values imply stronger liquidity and more credible moves.
- coverage_gaps: Explicitly lower conviction when this list is non-empty.
- evidence_status: Indicates whether external catalyst coverage is complete, preliminary, or missing.

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
      }
    }
  },
  "field_interpretation_guide": {
    "latest_close": "Latest observed close. Use it as the anchor for all price references.",
    "return_1d_pct": "One-day percentage move. Positive means short-term momentum, negative means near-term weakness.",
    "return_total_pct": "Window-level cumulative return. Use it to distinguish bounce-vs-trend continuation.",
    "avg_volume": "Average traded volume proxy. Higher values imply stronger liquidity and more credible moves.",
    "coverage_gaps": "Explicitly lower conviction when this list is non-empty.",
    "evidence_status": "Indicates whether external catalyst coverage is complete, preliminary, or missing."
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
    "risk_summary",
    "guardrails",
    "cascade_risk_level",
    "operational_risks",
    "data_quality_flags",
    "recommendation",
    "risk_views",
    "risk_debate_state"
  ]
}
