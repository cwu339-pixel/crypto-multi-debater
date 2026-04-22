# Risk Manager

- role: risk_manager
- title: Risk Manager
## Risk Summary
- {'risk': 'Bear-trend rally vulnerable to failure due to weak volume and below 200-day SMA', 'severity': 'high', 'source_role': 'technical_analyst', 'mitigation': 'Maintain hard stops at -10% to -15%, size positions per volatility scaling'}
- {'risk': 'Elevated valuation risk from stretched MC/TVL ratio and subdued stablecoin leverage demand', 'severity': 'med', 'source_role': 'defi_fundamentals_analyst', 'mitigation': 'Cap position sizing to 3-5% for BTC, tighten risk budgets during fragile fundamentals'}
- {'risk': 'Incomplete derivatives data (leverage ratio, liquidation volume, funding rate Z-score), limiting risk visibility', 'severity': 'high', 'source_role': 'derivatives_analyst', 'mitigation': 'Defer sizing increases until data coverage improves; use conservative leverage; monitor alternative signals'}
- {'risk': 'Concentrated crypto beta correlation risk, altcoins strongly correlated 0.7-0.9 with BTC; crypto is one correlated asset class', 'severity': 'high', 'source_role': 'risk_manager', 'mitigation': 'Treat entire crypto allocation as single correlated position; limit single asset exposure accordingly'}
- {'risk': 'Potential liquidation cascade risk if macro shocks or regulatory events increase leverage crowding', 'severity': 'med', 'source_role': 'risk_manager', 'mitigation': 'Reduce leverage prior to known macro events, cut leverage immediately if 2+ negative catalysts align'}
- guardrails: {'max_position_pct': {'BTC': '5%', 'mid-cap': '3-5%', 'small-cap': '1-2%', 'micro-cap': '0.5-1%'}, 'stop_logic': ['Hard stop loss at -10% to -15% on single positions', 'Never allow single position loss >20% without thesis justification', 'Reduce position sizes by 50% if portfolio drawdown hits -10%', 'Close speculative positions if portfolio drawdown exceeds -15%', 'Halt trading at portfolio drawdown -20%'], 'sizing_recommendation': 'Apply fractional Kelly between 25-50% to limit position volatility; scale position size inversely with ATR-based volatility'}
- cascade_risk_level: moderate
## Operational Risks
- Missing Coinglass API impairs leverage ratio and liquidation volume monitoring
- Lack of stablecoin supply flow and unique wallet growth metrics limit capital flow insight
- No volume quality or exchange withdrawal spread data reduces confidence in liquidity assessment
## Data Quality Flags
- Missing Coinglass derivatives coverage (leverage ratios, liquidation volumes, funding rate Z-score)
- No unique wallet growth or concentration data in DeFi
- No stablecoin supply/dominance data
- Absence of protocol-level revenue and lending utilization stats
- Volume quality data gap prevents confirmation of volume surge
- recommendation: avoid
- risk_bias: elevated
- summary: BTC remains in a bear trend with weak volume confirmation and price below the 200-day SMA by ~9.2%. Short-term momentum indicated by RSI near 68 creates a potential for further upside, but absence of volume surge (>1.5x average) and derivatives risk signals (funding rate near neutral, low open interest growth) moderate conviction. DeFi TVL remains robust, but MC/TVL ratio (2.8) and low stablecoin lending yields suggest stretched valuations and limited leverage-driven capital inflows. Critical data gaps, notably missing Coinglass derivatives metrics (leverage ratios, liquidation volumes), unique wallet growth, and stablecoin supply flow data, limit precise risk assessment. Historical crypto bear cycles and BTC’s prior severe drawdowns justify cautious posture. Correlation risks persist as altcoins remain tightly linked to BTC, offering limited portfolio diversification. Liquidation cascade risk is moderate given currently neutral funding rates, absence of elevated open interest/leverage metrics, but incomplete data warrants vigilance. Operational risk includes missing real volume quality and derivatives data. Base case: cautious avoidance with risk budget conservatively managed, leverage minimized, and stops tight given the bear-trend rally context. Invalidation hinges on volume surge >1.5x average with RSI >65 and price reclaiming above 200-day SMA on robust derivatives data confirming sustained demand and leverage. Until then, risk remains skewed to downside with possible rapid drawdowns and leveraged cascades in stressed macro or regulatory conditions.
- provider: openai
- analysis_mode: prompt_driven
- risk_views: {'aggressive': "Aggressive Analyst: The current BTC setup, despite officially signaling 'avoid' with low-confidence scores and significant data gaps, justifies pressing risk with moderate conviction based on available evidence. Price has shown a 2.1%+ daily return and over 10% in 30 days, accompanied by RSI just below the bear resistance zone (~68) and price positioning comfortably above the 20-day SMA (+6.8%). While price remains about 9.2% below the 200-day SMA, this is a characteristic bear-trend bounce setup where continuation of the rally with increased volume (above 1.5x avg) and RSI crossing above 65 would confirm a breakout scenario. Volume ratio at 1.19x is near a breakout threshold and should not be dismissed outright amid gaps in volume data quality. Derivatives positioning is balanced, with only mild short bias on funding and modest open interest growth; no signs of crowded liquidation risk. DeFi fundamentals show large TVL and rising stablecoin lending yields suggesting improving risk appetite and potential capital inflows, absent severe overheating. Regulatory and macro risks exist but no new crisis signals currently. The lack of perfect confirmation (missing Coinglass derivatives data, stablecoin supply trends, full volume quality) is offset by coherent multi-factor signs of constructive momentum. Therefore, an aggressive trader can act with a controlled risk approach to capture a likely bear-trend rally continuation forming a base for a prospective bull breakout. Key actionable triggers include sustained volume surge >1.5x average, RSI pushing above 65, and price reclaiming the 200-day SMA with conviction. If these emerge within the 3-day horizon, press risk higher. Conversely, failure to confirm volume increase or a drop below the 20-day SMA would warrant risk reduction. Excessive caution risks missing a prime opportunity to capitalize on a measured bear-trend bullish transition setup evident from combined technical, derivatives, and DeFi signals.", 'conservative': 'Conservative Analyst: BTC remains in a fragile bear-trend regime with price 9.2% below the 200-day SMA and volume ratios under breakout thresholds, indicating rallies lack strong conviction and are prone to failure. The MC/TVL ratio of ~2.8 signals significant overvaluation relative to on-chain capital, raising the risk of sharp corrections. Stablecoin lending yields are modestly positive, but missing data on stablecoin supply growth and unique wallet counts create critical blind spots on true leverage demand and capital inflows. Derivatives markets show a mild short bias with only modest open interest growth; however, missing Coinglass API data prevents comprehensive leverage, liquidation, and funding rate Z-score analysis, undercutting confidence in risk assessment. Absence of key volume quality confirmation further reduces signal reliability. The dependence on incomplete data and lack of verified sustained momentum dictate a capital preservation stance. Without clear breakout volume (>1.5x average), derivatives risk transparency, or fundamental improvements, the setup is vulnerable to downside reversion typical of bear-trend rallies. Prudent management requires avoiding or capping exposure until robust evidence of sustained bull transition emerges, such as a confirmed breakout above the 200-day SMA with strong volume, cleaner derivatives data showing balanced or long positioning, and verified capital inflows in DeFi stablecoins. Continued monitoring of data gaps and risk signals is essential before increasing risk allocation.', 'neutral': 'Neutral Analyst: BTC’s current technical, derivatives, and fundamental signals present a conflicted setup over the next 3 days. Price trades below the 200-day SMA by ~9.2%, consistent with a bear-trend regime, yet short-term returns (+2.1% 1-day, +10.5% 30-day) and RSI near 68 suggest a bear-trend rally with some upside momentum. Volume ratio at 1.19x is below the 1.5x breakout threshold, leaving breakout conviction tentative. Derivatives data show mildly negative funding and modest open interest growth, implying balanced positioning but critical data gaps (missing Coinglass metrics) obscure full risk visibility. DeFi fundamentals reveal a large TVL with stablecoin lending yields rising modestly (~3.3%), indicating measured but not robust leverage demand. News catalysts like the Taproot upgrade and institutional inflows provide medium-term bullish impetus, while regulatory uncertainty and macro neutrality persist. Given incomplete data and mixed signals, a disciplined posture favors cautious observation, avoiding aggressive risk-taking but maintaining readiness to increase exposure if confirmed breakout triggers occur: sustained volume above 1.5x average, RSI breaks >65, and price reclaims and holds above the 200-day SMA. Conversely, failure to confirm these signals or a breakdown below the 20-day SMA should prompt risk reduction. This balanced approach manages downside risk amid uncertainty while allowing capture of a probable measured bear-trend rally continuation and possible regime transition. Continued monitoring of data gaps—especially derivatives leverage metrics and stablecoin supply flows—is essential for conviction refinement.'}
- risk_debate_state: {'history': "Aggressive Analyst: The current BTC setup, despite officially signaling 'avoid' with low-confidence scores and significant data gaps, justifies pressing risk with moderate conviction based on available evidence. Price has shown a 2.1%+ daily return and over 10% in 30 days, accompanied by RSI just below the bear resistance zone (~68) and price positioning comfortably above the 20-day SMA (+6.8%). While price remains about 9.2% below the 200-day SMA, this is a characteristic bear-trend bounce setup where continuation of the rally with increased volume (above 1.5x avg) and RSI crossing above 65 would confirm a breakout scenario. Volume ratio at 1.19x is near a breakout threshold and should not be dismissed outright amid gaps in volume data quality. Derivatives positioning is balanced, with only mild short bias on funding and modest open interest growth; no signs of crowded liquidation risk. DeFi fundamentals show large TVL and rising stablecoin lending yields suggesting improving risk appetite and potential capital inflows, absent severe overheating. Regulatory and macro risks exist but no new crisis signals currently. The lack of perfect confirmation (missing Coinglass derivatives data, stablecoin supply trends, full volume quality) is offset by coherent multi-factor signs of constructive momentum. Therefore, an aggressive trader can act with a controlled risk approach to capture a likely bear-trend rally continuation forming a base for a prospective bull breakout. Key actionable triggers include sustained volume surge >1.5x average, RSI pushing above 65, and price reclaiming the 200-day SMA with conviction. If these emerge within the 3-day horizon, press risk higher. Conversely, failure to confirm volume increase or a drop below the 20-day SMA would warrant risk reduction. Excessive caution risks missing a prime opportunity to capitalize on a measured bear-trend bullish transition setup evident from combined technical, derivatives, and DeFi signals.\nConservative Analyst: BTC remains in a fragile bear-trend regime with price 9.2% below the 200-day SMA and volume ratios under breakout thresholds, indicating rallies lack strong conviction and are prone to failure. The MC/TVL ratio of ~2.8 signals significant overvaluation relative to on-chain capital, raising the risk of sharp corrections. Stablecoin lending yields are modestly positive, but missing data on stablecoin supply growth and unique wallet counts create critical blind spots on true leverage demand and capital inflows. Derivatives markets show a mild short bias with only modest open interest growth; however, missing Coinglass API data prevents comprehensive leverage, liquidation, and funding rate Z-score analysis, undercutting confidence in risk assessment. Absence of key volume quality confirmation further reduces signal reliability. The dependence on incomplete data and lack of verified sustained momentum dictate a capital preservation stance. Without clear breakout volume (>1.5x average), derivatives risk transparency, or fundamental improvements, the setup is vulnerable to downside reversion typical of bear-trend rallies. Prudent management requires avoiding or capping exposure until robust evidence of sustained bull transition emerges, such as a confirmed breakout above the 200-day SMA with strong volume, cleaner derivatives data showing balanced or long positioning, and verified capital inflows in DeFi stablecoins. Continued monitoring of data gaps and risk signals is essential before increasing risk allocation.\nNeutral Analyst: BTC’s current technical, derivatives, and fundamental signals present a conflicted setup over the next 3 days. Price trades below the 200-day SMA by ~9.2%, consistent with a bear-trend regime, yet short-term returns (+2.1% 1-day, +10.5% 30-day) and RSI near 68 suggest a bear-trend rally with some upside momentum. Volume ratio at 1.19x is below the 1.5x breakout threshold, leaving breakout conviction tentative. Derivatives data show mildly negative funding and modest open interest growth, implying balanced positioning but critical data gaps (missing Coinglass metrics) obscure full risk visibility. DeFi fundamentals reveal a large TVL with stablecoin lending yields rising modestly (~3.3%), indicating measured but not robust leverage demand. News catalysts like the Taproot upgrade and institutional inflows provide medium-term bullish impetus, while regulatory uncertainty and macro neutrality persist. Given incomplete data and mixed signals, a disciplined posture favors cautious observation, avoiding aggressive risk-taking but maintaining readiness to increase exposure if confirmed breakout triggers occur: sustained volume above 1.5x average, RSI breaks >65, and price reclaims and holds above the 200-day SMA. Conversely, failure to confirm these signals or a breakdown below the 20-day SMA should prompt risk reduction. This balanced approach manages downside risk amid uncertainty while allowing capture of a probable measured bear-trend rally continuation and possible regime transition. Continued monitoring of data gaps—especially derivatives leverage metrics and stablecoin supply flows—is essential for conviction refinement.", 'aggressive_history': "Aggressive Analyst: The current BTC setup, despite officially signaling 'avoid' with low-confidence scores and significant data gaps, justifies pressing risk with moderate conviction based on available evidence. Price has shown a 2.1%+ daily return and over 10% in 30 days, accompanied by RSI just below the bear resistance zone (~68) and price positioning comfortably above the 20-day SMA (+6.8%). While price remains about 9.2% below the 200-day SMA, this is a characteristic bear-trend bounce setup where continuation of the rally with increased volume (above 1.5x avg) and RSI crossing above 65 would confirm a breakout scenario. Volume ratio at 1.19x is near a breakout threshold and should not be dismissed outright amid gaps in volume data quality. Derivatives positioning is balanced, with only mild short bias on funding and modest open interest growth; no signs of crowded liquidation risk. DeFi fundamentals show large TVL and rising stablecoin lending yields suggesting improving risk appetite and potential capital inflows, absent severe overheating. Regulatory and macro risks exist but no new crisis signals currently. The lack of perfect confirmation (missing Coinglass derivatives data, stablecoin supply trends, full volume quality) is offset by coherent multi-factor signs of constructive momentum. Therefore, an aggressive trader can act with a controlled risk approach to capture a likely bear-trend rally continuation forming a base for a prospective bull breakout. Key actionable triggers include sustained volume surge >1.5x average, RSI pushing above 65, and price reclaiming the 200-day SMA with conviction. If these emerge within the 3-day horizon, press risk higher. Conversely, failure to confirm volume increase or a drop below the 20-day SMA would warrant risk reduction. Excessive caution risks missing a prime opportunity to capitalize on a measured bear-trend bullish transition setup evident from combined technical, derivatives, and DeFi signals.", 'conservative_history': 'Conservative Analyst: BTC remains in a fragile bear-trend regime with price 9.2% below the 200-day SMA and volume ratios under breakout thresholds, indicating rallies lack strong conviction and are prone to failure. The MC/TVL ratio of ~2.8 signals significant overvaluation relative to on-chain capital, raising the risk of sharp corrections. Stablecoin lending yields are modestly positive, but missing data on stablecoin supply growth and unique wallet counts create critical blind spots on true leverage demand and capital inflows. Derivatives markets show a mild short bias with only modest open interest growth; however, missing Coinglass API data prevents comprehensive leverage, liquidation, and funding rate Z-score analysis, undercutting confidence in risk assessment. Absence of key volume quality confirmation further reduces signal reliability. The dependence on incomplete data and lack of verified sustained momentum dictate a capital preservation stance. Without clear breakout volume (>1.5x average), derivatives risk transparency, or fundamental improvements, the setup is vulnerable to downside reversion typical of bear-trend rallies. Prudent management requires avoiding or capping exposure until robust evidence of sustained bull transition emerges, such as a confirmed breakout above the 200-day SMA with strong volume, cleaner derivatives data showing balanced or long positioning, and verified capital inflows in DeFi stablecoins. Continued monitoring of data gaps and risk signals is essential before increasing risk allocation.', 'neutral_history': 'Neutral Analyst: BTC’s current technical, derivatives, and fundamental signals present a conflicted setup over the next 3 days. Price trades below the 200-day SMA by ~9.2%, consistent with a bear-trend regime, yet short-term returns (+2.1% 1-day, +10.5% 30-day) and RSI near 68 suggest a bear-trend rally with some upside momentum. Volume ratio at 1.19x is below the 1.5x breakout threshold, leaving breakout conviction tentative. Derivatives data show mildly negative funding and modest open interest growth, implying balanced positioning but critical data gaps (missing Coinglass metrics) obscure full risk visibility. DeFi fundamentals reveal a large TVL with stablecoin lending yields rising modestly (~3.3%), indicating measured but not robust leverage demand. News catalysts like the Taproot upgrade and institutional inflows provide medium-term bullish impetus, while regulatory uncertainty and macro neutrality persist. Given incomplete data and mixed signals, a disciplined posture favors cautious observation, avoiding aggressive risk-taking but maintaining readiness to increase exposure if confirmed breakout triggers occur: sustained volume above 1.5x average, RSI breaks >65, and price reclaims and holds above the 200-day SMA. Conversely, failure to confirm these signals or a breakdown below the 20-day SMA should prompt risk reduction. This balanced approach manages downside risk amid uncertainty while allowing capture of a probable measured bear-trend rally continuation and possible regime transition. Continued monitoring of data gaps—especially derivatives leverage metrics and stablecoin supply flows—is essential for conviction refinement.', 'latest_speaker': 'Neutral', 'current_aggressive_response': "Aggressive Analyst: The current BTC setup, despite officially signaling 'avoid' with low-confidence scores and significant data gaps, justifies pressing risk with moderate conviction based on available evidence. Price has shown a 2.1%+ daily return and over 10% in 30 days, accompanied by RSI just below the bear resistance zone (~68) and price positioning comfortably above the 20-day SMA (+6.8%). While price remains about 9.2% below the 200-day SMA, this is a characteristic bear-trend bounce setup where continuation of the rally with increased volume (above 1.5x avg) and RSI crossing above 65 would confirm a breakout scenario. Volume ratio at 1.19x is near a breakout threshold and should not be dismissed outright amid gaps in volume data quality. Derivatives positioning is balanced, with only mild short bias on funding and modest open interest growth; no signs of crowded liquidation risk. DeFi fundamentals show large TVL and rising stablecoin lending yields suggesting improving risk appetite and potential capital inflows, absent severe overheating. Regulatory and macro risks exist but no new crisis signals currently. The lack of perfect confirmation (missing Coinglass derivatives data, stablecoin supply trends, full volume quality) is offset by coherent multi-factor signs of constructive momentum. Therefore, an aggressive trader can act with a controlled risk approach to capture a likely bear-trend rally continuation forming a base for a prospective bull breakout. Key actionable triggers include sustained volume surge >1.5x average, RSI pushing above 65, and price reclaiming the 200-day SMA with conviction. If these emerge within the 3-day horizon, press risk higher. Conversely, failure to confirm volume increase or a drop below the 20-day SMA would warrant risk reduction. Excessive caution risks missing a prime opportunity to capitalize on a measured bear-trend bullish transition setup evident from combined technical, derivatives, and DeFi signals.", 'current_conservative_response': 'Conservative Analyst: BTC remains in a fragile bear-trend regime with price 9.2% below the 200-day SMA and volume ratios under breakout thresholds, indicating rallies lack strong conviction and are prone to failure. The MC/TVL ratio of ~2.8 signals significant overvaluation relative to on-chain capital, raising the risk of sharp corrections. Stablecoin lending yields are modestly positive, but missing data on stablecoin supply growth and unique wallet counts create critical blind spots on true leverage demand and capital inflows. Derivatives markets show a mild short bias with only modest open interest growth; however, missing Coinglass API data prevents comprehensive leverage, liquidation, and funding rate Z-score analysis, undercutting confidence in risk assessment. Absence of key volume quality confirmation further reduces signal reliability. The dependence on incomplete data and lack of verified sustained momentum dictate a capital preservation stance. Without clear breakout volume (>1.5x average), derivatives risk transparency, or fundamental improvements, the setup is vulnerable to downside reversion typical of bear-trend rallies. Prudent management requires avoiding or capping exposure until robust evidence of sustained bull transition emerges, such as a confirmed breakout above the 200-day SMA with strong volume, cleaner derivatives data showing balanced or long positioning, and verified capital inflows in DeFi stablecoins. Continued monitoring of data gaps and risk signals is essential before increasing risk allocation.', 'current_neutral_response': 'Neutral Analyst: BTC’s current technical, derivatives, and fundamental signals present a conflicted setup over the next 3 days. Price trades below the 200-day SMA by ~9.2%, consistent with a bear-trend regime, yet short-term returns (+2.1% 1-day, +10.5% 30-day) and RSI near 68 suggest a bear-trend rally with some upside momentum. Volume ratio at 1.19x is below the 1.5x breakout threshold, leaving breakout conviction tentative. Derivatives data show mildly negative funding and modest open interest growth, implying balanced positioning but critical data gaps (missing Coinglass metrics) obscure full risk visibility. DeFi fundamentals reveal a large TVL with stablecoin lending yields rising modestly (~3.3%), indicating measured but not robust leverage demand. News catalysts like the Taproot upgrade and institutional inflows provide medium-term bullish impetus, while regulatory uncertainty and macro neutrality persist. Given incomplete data and mixed signals, a disciplined posture favors cautious observation, avoiding aggressive risk-taking but maintaining readiness to increase exposure if confirmed breakout triggers occur: sustained volume above 1.5x average, RSI breaks >65, and price reclaims and holds above the 200-day SMA. Conversely, failure to confirm these signals or a breakdown below the 20-day SMA should prompt risk reduction. This balanced approach manages downside risk amid uncertainty while allowing capture of a probable measured bear-trend rally continuation and possible regime transition. Continued monitoring of data gaps—especially derivatives leverage metrics and stablecoin supply flows—is essential for conviction refinement.', 'count': 3}
- report: BTC remains in a bear trend with weak volume confirmation and price below the 200-day SMA by ~9.2%. Short-term momentum indicated by RSI near 68 creates a potential for further upside, but absence of volume surge (>1.5x average) and derivatives risk signals (funding rate near neutral, low open interest growth) moderate conviction. DeFi TVL remains robust, but MC/TVL ratio (2.8) and low stablecoin lending yields suggest stretched valuations and limited leverage-driven capital inflows. Critical data gaps, notably missing Coinglass derivatives metrics (leverage ratios, liquidation volumes), unique wallet growth, and stablecoin supply flow data, limit precise risk assessment. Historical crypto bear cycles and BTC’s prior severe drawdowns justify cautious posture. Correlation risks persist as altcoins remain tightly linked to BTC, offering limited portfolio diversification. Liquidation cascade risk is moderate given currently neutral funding rates, absence of elevated open interest/leverage metrics, but incomplete data warrants vigilance. Operational risk includes missing real volume quality and derivatives data. Base case: cautious avoidance with risk budget conservatively managed, leverage minimized, and stops tight given the bear-trend rally context. Invalidation hinges on volume surge >1.5x average with RSI >65 and price reclaiming above 200-day SMA on robust derivatives data confirming sustained demand and leverage. Until then, risk remains skewed to downside with possible rapid drawdowns and leveraged cascades in stressed macro or regulatory conditions.
- signal: neutral-bear
- confidence: medium
## Referenced Fields
- latest_close
- return_1d_pct
- return_30d_pct
- rsi_14
- price_vs_sma20_pct
- price_vs_sma200_pct
- volume_ratio
- regime
- defi_tvl_total
- mc_tvl_ratio
- defi_stablecoin_median_apy
- funding_rate_8h
- open_interest_pct_change
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
