# Risk Manager

- role: risk_manager
- title: Risk Manager
## Risk Summary
- {'risk': 'Data coverage gap', 'severity': 'high', 'source_role': 'derivatives_analyst', 'mitigation': 'Reduce size until derivatives context is available.'}
- guardrails: {'max_position_pct': 'quarter', 'stop_logic': ['Use volatility-adjusted stops based on ATR.'], 'sizing_recommendation': 'quarter'}
- cascade_risk_level: elevated
## Operational Risks
- Evidence and derivatives feeds are incomplete.
## Data Quality Flags
- coinglass:missing_api_key
- recommendation: avoid
- risk_bias: elevated
- summary: Position sizing should stay conservative until derivatives and DeFi coverage gaps are closed. Current quantitative score is 37 with low confidence, regime=range_bound, mc_tvl_ratio=2.6097, funding=None.
- provider: deterministic
- analysis_mode: deterministic_fallback
- risk_views: {'aggressive': 'Aggressive Analyst: Technical momentum and a score of 37 leave room to press for upside if the regime (range_bound) stabilizes. Waiting for every feed to clear can mean missing the move.', 'conservative': "Conservative Analyst: Coverage gaps and incomplete derivatives visibility dominate the risk picture. Funding=None and gaps=['coinglass:missing_api_key'] do not justify leaning in.", 'neutral': 'Neutral Analyst: The aggressive case is directionally understandable, but the conservative case is stronger until confirmation improves. Limited size or avoidance remains the balanced posture.'}
- risk_debate_state: {'history': "Aggressive Analyst: Technical momentum and a score of 37 leave room to press for upside if the regime (range_bound) stabilizes. Waiting for every feed to clear can mean missing the move.\nConservative Analyst: Coverage gaps and incomplete derivatives visibility dominate the risk picture. Funding=None and gaps=['coinglass:missing_api_key'] do not justify leaning in.\nNeutral Analyst: The aggressive case is directionally understandable, but the conservative case is stronger until confirmation improves. Limited size or avoidance remains the balanced posture.", 'aggressive_history': 'Aggressive Analyst: Technical momentum and a score of 37 leave room to press for upside if the regime (range_bound) stabilizes. Waiting for every feed to clear can mean missing the move.', 'conservative_history': "Conservative Analyst: Coverage gaps and incomplete derivatives visibility dominate the risk picture. Funding=None and gaps=['coinglass:missing_api_key'] do not justify leaning in.", 'neutral_history': 'Neutral Analyst: The aggressive case is directionally understandable, but the conservative case is stronger until confirmation improves. Limited size or avoidance remains the balanced posture.', 'latest_speaker': 'Neutral', 'current_aggressive_response': 'Aggressive Analyst: Technical momentum and a score of 37 leave room to press for upside if the regime (range_bound) stabilizes. Waiting for every feed to clear can mean missing the move.', 'current_conservative_response': "Conservative Analyst: Coverage gaps and incomplete derivatives visibility dominate the risk picture. Funding=None and gaps=['coinglass:missing_api_key'] do not justify leaning in.", 'current_neutral_response': 'Neutral Analyst: The aggressive case is directionally understandable, but the conservative case is stronger until confirmation improves. Limited size or avoidance remains the balanced posture.', 'count': 3}
- prompt_path: /Users/wuchenghan/Projects/crypto-research-agent/src/crypto_research_agent/agents/prompts/risk_manager.md
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
- Rule: If backtested max drawdown is X, expect 2x in live trading

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
    "thesis": "Showcase crypto multi-debater prompt-driven report",
    "horizon_days": 3,
    "run_id": "r_20260326T145524Z_BTC"
  },
  "role_context": {
    "market_context": {
      "price": {
        "latest_close": 69401.945312,
        "return_1d_pct": -2.675558,
        "return_7d_pct": -1.589052,
        "return_30d_pct": 2.121568,
        "price_vs_sma20_pct": -1.306144,
        "price_vs_sma200_pct": -24.374439,
        "rsi_14": 47.0923,
        "realized_vol_30d": 53.249,
        "volume_ratio": 0.8597,
        "regime": "bear",
        "halving_cycle_day": 706
      },
      "defi": {
        "defi_tvl_total": 526559394089.01,
        "defi_stablecoin_median_apy": 3.32,
        "defi_stablecoin_apy_change_7d": -0.0926,
        "mc_tvl_ratio": 2.6097
      },
      "evidence": {
        "evidence_status": "fetched",
        "source": "open_deep_research_local",
        "citations_count": 0
      },
      "coverage_gaps": [
        "coinglass:missing_api_key"
      ]
    },
    "scorecard": {
      "inputs": {
        "momentum": 30.43,
        "liquidity": 80.0,
        "derivatives": 35.0,
        "defi": 52.0,
        "onchain": 41.0,
        "sentiment": 45.0,
        "data_quality_penalty": -5.0
      },
      "final_score": 37,
      "confidence": "low",
      "score_decision": "avoid"
    },
    "prior_role_memos": {
      "technical_analyst": {
        "summary": "BTC still looks range_bound: momentum has improved, but spot remains -24.374439% away from the 200-day trend and needs follow-through above nearby resistance.",
        "signal": "cautious",
        "confidence": "low",
        "regime": "range_bound",
        "referenced_fields": null,
        "support": 67319.88695264,
        "resistance": 71484.00367136
      },
      "defi_fundamentals_analyst": {
        "summary": "DeFi internals are mixed: MC/TVL sits at 2.6097, while stablecoin yield changes remain mild. That is enough to avoid a hard bearish read, but not enough to call broad-based capital expansion.",
        "signal": "coverage_gap",
        "confidence": null,
        "stablecoin_signals": "Stablecoin median APY is 3.32; 7d APY change is -0.0926; MC/TVL ratio is 2.6097.",
        "data_gaps": [
          "coinglass:missing_api_key"
        ]
      },
      "derivatives_analyst": {
        "summary": "CoinGlass-derived positioning is unavailable, so derivatives conviction remains constrained.",
        "signal": "insufficient_data",
        "confidence": null,
        "positioning_thesis": "CoinGlass-derived positioning is unavailable, so derivatives conviction remains constrained.",
        "data_gaps": [
          "coinglass:missing_api_key"
        ]
      },
      "news_analyst": {
        "summary": "Headline and catalyst coverage is fetched; nothing clearly breaks the setup, but the event map is still incomplete.",
        "signal": "contextualized",
        "confidence": null,
        "evidence_quality": "preliminary",
        "top_risk": "External catalyst coverage is preliminary."
      },
      "bull_researcher": {
        "thesis": "Momentum remains constructive, but needs confirmation.",
        "argument": "Bull Analyst: Momentum remains constructive, but needs confirmation. Missing derivatives data does not automatically invalidate price resilience.",
        "confidence": "low",
        "top_point": "Short-term momentum remains constructive.",
        "top_rebuttal": "Missing derivatives data does not automatically invalidate price resilience.",
        "data_gaps": [
          "coinglass:missing_api_key"
        ]
      },
      "bear_researcher": {
        "thesis": "Coverage gaps and event uncertainty limit conviction.",
        "argument": "Bear Analyst: Coverage gaps and event uncertainty limit conviction. Without derivatives confirmation the move could be fragile.",
        "confidence": "high",
        "top_point": "Coverage gaps make the upside thesis unverifiable.",
        "top_rebuttal": "Without derivatives confirmation the move could be fragile.",
        "data_gaps": [
          "coinglass:missing_api_key"
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
