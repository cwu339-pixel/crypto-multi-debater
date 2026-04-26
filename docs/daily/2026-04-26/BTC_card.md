# BTC Research Report

Processed signal: AVOID

1. Rating
Avoid

2. Executive Summary
- Immediate posture: Tactical AVOID — BTC over 7d. Confidence: low.
- Confidence: Low
- Quant score: 28/100
- Conclusion: The integrated crypto read stays avoid: score=28, regime=range_bound, MC/TVL=None, funding=None. The system sees enough fragility to stay conservative rather than press for directional size.

3. Investment Thesis
Net call: avoid over the next 7 days. The quantitative stack prints 28 with low confidence, and the combined read still looks more like risk control than a clean offensive entry.

Key drivers:
- cautious (technical_analyst), coverage_gap (defi_fundamentals_analyst), insufficient_data (derivatives_analyst)

Rejected alternative:
- BUY — Insufficient confirmation from 2+ roles; scorecard threshold not met or coverage gaps dominate the risk picture.

4. Debate Summary
Analyst stack:
- Technical Analyst: BTC still looks range_bound: momentum has improved, but spot remains None% away from the 200-day trend and needs follow-through above nearby resistance.
- DeFi Analyst: DeFi internals are mixed: MC/TVL sits at None, while stablecoin yield changes remain mild. That is enough to avoid a hard bearish read, but not enough to call broad-based capital expansion.
- Derivatives Analyst: CoinGlass-derived positioning is unavailable, so derivatives conviction remains constrained.
- News Analyst: Evidence quality is stub. No clear near-term catalyst.. Top risk: External catalyst coverage is preliminary.

Bull case:
- Bull Analyst: Momentum remains constructive, but needs confirmation. Missing derivatives data does not automatically invalidate price resilience.

Bear case:
- Bear Analyst: Coverage gaps and event uncertainty limit conviction. Without derivatives confirmation the move could be fragile.

Risk roundtable:
- Aggressive Analyst: Technical momentum and a score of 28 leave room to press for upside if the regime (range_bound) stabilizes. Waiting for every feed to clear can mean missing the move.
- Conservative Analyst: Coverage gaps and incomplete derivatives visibility dominate the risk picture. Funding=None and gaps=['openbb:openbb_not_installed', 'coinglass:missing_api_key', 'binance:exception:HTTPError'] do not justify leaning in.
- Neutral Analyst: The aggressive case is directionally understandable, but the conservative case is stronger until confirmation improves. Limited size or avoidance remains the balanced posture.

5. Risk Controls
- Entry logic: Avoid entry. Conditions do not support a long position.
- Stop logic: Initial stop = 1× ATR below entry. Hard structural stop: daily close below SMA50 on expanding volume. If ATR data available: size so 1 ATR stop equals 0.5–1% of portfolio equity.
- Sizing: Risk 0.5–1% of portfolio per trade. Size so 1 ATR stop = that dollar risk amount. Cap total tactical exposure at 0% of portfolio.
- Targets: none (avoid/hold posture)
- Hard rules that flip posture:
- If Daily close below SMA50 on expanding down-volume with MACD turning negative → Immediate full exit; reassess for short setup
- If 5+ consecutive daily closes above 200-SMA with rising MACD and stablecoin inflows confirmed → Upgrade to longer-term Buy at full size
- Tactical alternative: For conservative mandates: use defined-loss call spreads (premium ≤ 0.5% of portfolio) instead of spot exposure. If spot, reduce single-trade risk to 0.25% and widen stops to 1.5× ATR.

Current risk posture:
Current posture:
- No new long entry
- Do not chase upside without confirmation
- Stay on watchlist only

Main risks to this stance:
- Coverage gaps reduce conviction

6. Review Plan
Review due: 7 days from now

At review, check:
- future_return_pct
- scorecard drift
- coverage_gaps
Latest review: pending

7. Data Quality
Overall: Mixed — core data is intact, but supplementary flow and catalyst inputs are partial.

Supplementary sources not available:
- openbb
- coinglass
- binance

Run Mode: live_or_current

Score breakdown
- Momentum: 45.0
- Liquidity: 35.0
- Derivatives: 35.0
- Fundamentals / Flows: 60.0
- Trend / Regime: 45.0
- Macro / News: 50.0
- Data quality penalty: -15.0
- Total: 28/100
