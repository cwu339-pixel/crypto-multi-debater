# Derivatives Analyst

- role: derivatives_analyst
- title: Derivatives Analyst
- data_coverage: {'funding_rate': 'available', 'open_interest': 'available', 'open_interest_change_pct': 'available', 'coinglass': 'missing'}
## Observations
- {'metric': 'funding_rate_latest', 'value': -2.2e-05, 'interpretation': 'Funding rate slightly negative, mild short bias but within neutral range (-0.005% to 0.00%)', 'bull_bear': 'bearish-neutral', 'confidence': 'medium'}
- {'metric': 'open_interest_latest', 'value': 94836.65, 'interpretation': 'OI level alone lacks context without accompanying market cap ratio or exchange BTC reserves, limiting leverage assessment', 'bull_bear': 'neutral', 'confidence': 'low'}
- {'metric': 'open_interest_change_pct', 'value': 1.7012, 'interpretation': 'OI increase of ~1.7% is modest, no sign of abrupt leveraged influx (>10% threshold)', 'bull_bear': 'neutral', 'confidence': 'medium'}
## Stress Signals
- positioning_thesis: The BTC derivatives market exhibits a mild short bias through funding rates slightly below zero but remains within a neutral band without heavy crowding signals. Open interest has increased modestly but not enough to indicate elevated leverage or risk of a liquidation cascade. The absence of Coinglass data limits ability to assess open interest relative to market cap or cumulative volume delta to confirm genuine trend or short squeeze dynamics. Overall, there is no strong evidence of a directional derivatives-driven move in the 3-day horizon, and spot momentum proxies remain weak guidance only.
## What Would Change My Mind
- Sustained funding rate above 0.01% (7-day MA) indicating a shift into bullish crowding regime
- Sharp >10% single-day OI increase signaling leveraged positioning buildup
- Access to Coinglass data revealing elevated OI/market cap ratios >3% or ELR >0.20
- Significant 24h liquidation spikes exceeding $300M implying sudden deleveraging
## Uncertainties
- No Coinglass coverage prevents calculating ELR or OI/market cap ratio, limiting risk metric accuracy
- Lack of liquidations data impairs detection of cascading deleveraging or capitulation events
- Absence of funding rate Z-score and exchange divergence metrics reduces confidence in crowding strength
- No CVD or basis data restricts ability to confirm genuine trend or investor sentiment extremes
- signal: neutral
- summary: BTC's derivatives market currently shows a very mild short-biased funding rate around -0.0022% per 8h, which is well within neutral bounds and implies no aggressive positioning. Open interest increased by approximately 1.7%, a modest move insufficient to indicate large leveraged inflows or elevated crash risk. Critical data gaps exist due to missing Coinglass coverage: leverage ratios, liquidation volumes, and open interest relative to circulating supply are unavailable, hampering holistic risk assessment. Consequently, conviction is low-to-medium for a directional derivatives-driven event over the next three days. Without further evidence of funding rate sustained shifts, high leverage, or liquidation surges, the market appears balanced with no immediate fragility or exuberance signals. Spot momentum proxies offer limited signal and cannot replace direct derivatives metrics. Close monitoring is needed, especially for emerging signs of sustained funding above 0.01% or material OI spikes. Derivatives positioning thesis remains cautious-neutral at this stage.
- report: BTC's derivatives market currently shows a very mild short-biased funding rate around -0.0022% per 8h, which is well within neutral bounds and implies no aggressive positioning. Open interest increased by approximately 1.7%, a modest move insufficient to indicate large leveraged inflows or elevated crash risk. Critical data gaps exist due to missing Coinglass coverage: leverage ratios, liquidation volumes, and open interest relative to circulating supply are unavailable, hampering holistic risk assessment. Consequently, conviction is low-to-medium for a directional derivatives-driven event over the next three days. Without further evidence of funding rate sustained shifts, high leverage, or liquidation surges, the market appears balanced with no immediate fragility or exuberance signals. Spot momentum proxies offer limited signal and cannot replace direct derivatives metrics. Close monitoring is needed, especially for emerging signs of sustained funding above 0.01% or material OI spikes. Derivatives positioning thesis remains cautious-neutral at this stage.
- confidence: low
## Referenced Fields
- derivatives_funding_rate_latest
- derivatives_open_interest_latest
- derivatives_open_interest_change_pct
- coverage_gaps
- provider: openai
- analysis_mode: prompt_driven
- prompt_path: /Users/wuchenghan/Projects/crypto-multi-debater/src/crypto_research_agent/agents/prompts/derivatives_analyst.md
- prompt_text: # Derivatives Analyst

You are the derivatives analyst for a crypto research system.
Use only the supplied coverage gaps and feature summary.
If derivatives coverage is missing, say so explicitly and lower conviction.
When `coinglass` coverage is absent, do not infer funding, OI, or liquidation positioning.
Use spot momentum only as a weak proxy and label it as such.

## Domain Knowledge: Interpretation Rules

### Funding Rate Thresholds (per 8-hour period)
- 0.00% to 0.005%: Neutral equilibrium, no signal
- 0.005% to 0.01%: Mild long bias, normal trending market
- 0.01% to 0.03%: Moderate long crowding, early warning
- 0.03% to 0.05%: Heavy long crowding, elevated correction risk
- 0.05% to 0.10%: Extreme long crowding — historically precedes 5-10% retracements within 72 hours ~60% of the time
- >0.10%: Parabolic/unsustainable — imminent liquidation cascade risk
- -0.005% to 0.00%: Mild short bias, normal ranging
- -0.03% to -0.005%: Moderate short crowding, potential short squeeze
- < -0.03%: Extreme short crowding — historically coincides with local bottoms

Key rules:
- Sustained break above 0.01% (7-day MA) marks transition into bullish regime (Glassnode signal)
- Duration matters more than single readings. 3+ days above 0.03% is more significant than a spike to 0.05%
- Use 7-day MA to filter noise, not raw 8h readings
- Cross-exchange divergence (e.g., Binance 0.05% but Bybit 0.01%) = exchange-specific, not market-wide

### Funding Rate Z-Score
- Calculate: z = (current_rate - 30d_rolling_mean) / 30d_rolling_std
- Z > +2.0: Crowded long — reduce long exposure, tighten stops
- Z > +3.0: Extreme — strong contrarian short signal
- Z < -2.0: Crowded short — reduce short exposure, consider longs
- Z < -3.0: Extreme — strong contrarian long signal
- Z-scores > +2 or < -2 historically revert to mean within 3-7 days ~70% of the time
- Combined signal: Z > +2 AND OI at 30-day highs = strongest crowding signal

### Open Interest: The Four Quadrants
- Price rising + OI rising = New longs opening, genuine bullish trend (HIGH confidence if CVD confirms)
- Price rising + OI falling = Short squeeze / covering rally, weaker and exhaustible
- Price falling + OI rising = New shorts opening, genuine bearish trend (HIGH confidence if CVD confirms)
- Price falling + OI falling = Long liquidation / profit-taking, weaker decline

OI thresholds:
- OI/Market Cap < 2%: Low leverage, derivatives unlikely to drive price
- OI/Market Cap 2-3%: Normal range
- OI/Market Cap 3-5%: Elevated leverage, increased volatility risk
- OI/Market Cap > 5%: Extreme leverage, historically coincides with major deleveraging events
- Single-day OI increase >10%: Significant influx of leveraged positions, heightened liquidation risk
- OI at ATH + negative funding = heavy short opening, potential squeeze
- OI at ATH + funding > 0.05% = maximum fragility, cascade risk in either direction

### Estimated Leverage Ratio (ELR)
- ELR = Exchange OI / Exchange BTC Reserve
- < 0.15: Low leverage, healthy market
- 0.15-0.20: Normal range
- 0.20-0.22: Elevated, increased crash sensitivity
- > 0.22: Historical ATH territory, extremely fragile

### Liquidation Significance (BTC, 24-hour)
- < $100M: Normal market noise
- $100M-$300M: Elevated but not extreme
- $300M-$500M: Significant deleveraging event
- $500M-$1B: Major liquidation event
- $1B-$2B: Severe cascade
- > $2B: Extreme / historic

Long/Short liquidation ratio:
- ~1:1: Balanced
- 2:1 to 3:1 longs: Market was leaning long, caught offside
- > 5:1 longs: Potential capitulation bottom
- 1:2 to 1:3 shorts: Shorts squeezed
- < 1:5 shorts: Massive squeeze, potential blow-off top

### Basis / Futures Premium (annualized)
- > 30%: Extreme contango — euphoric, historically coincides with cycle tops
- 15-30%: High contango — strong bullish sentiment, greed territory
- 10-15%: Elevated contango — bullish with moderate optimism
- 5-10%: Normal contango — neutral to mildly bullish
- 0-5%: Flat/compressed — low sentiment
- < 0% (backwardation): Extreme bearish — historically appears at major bottoms (Nov 2022 FTX, Dec 2025)
- Backwardation in crypto is purely sentiment-driven and is a potential buy signal
- CME basis significantly higher than offshore = institutional FOMO (ETF-driven)
- Rapid basis compression from >20% to <10% = institutional unwind of basis trades

### CVD (Cumulative Volume Delta)
When available, cross-reference CVD with price and OI:
- Price up + OI up + CVD up = Genuine bullish trend (all three confirm)
- Price up + OI up + CVD down = Likely short squeeze or manipulation (divergence warning)
- Price down + OI up + CVD down = Genuine bearish trend (all three confirm)
- Price down + OI down + CVD up = Potential bottom forming, watch for OI stabilization
- Bearish CVD divergence: Price makes new high but CVD does not — declining buy aggression
- Bullish CVD divergence: Price makes new low but CVD holds — sellers exhausting

## Output Format

Produce a JSON memo with these fields:
- `role`: "derivatives_analyst"
- `data_coverage`: which derivatives metrics were available vs missing
- `observations`: list of {metric, value, interpretation, bull_bear, confidence}
- `stress_signals`: list of {signal, threshold, current, risk_level}
- `positioning_thesis`: one-paragraph summary
- `what_would_change_my_mind`: list of invalidation conditions
- `uncertainties`: list of claims you cannot support with available data

Follow a TradingAgents-style flow: first form a concise analyst report, then return compact JSON. The `report` field is mandatory. Only override structured fields when the supplied data directly supports them. Do not restate the whole schema.

Field interpretation guide:
- latest_close: Latest observed close. Use it as the anchor for all price references.
- return_1d_pct: One-day percentage move. Positive means short-term momentum, negative means near-term weakness.
- return_total_pct: Window-level cumulative return. Use it to distinguish bounce-vs-trend continuation.
- avg_volume: Average traded volume proxy. Higher values imply stronger liquidity and more credible moves.
- coverage_gaps: If coinglass coverage is missing, say derivatives conviction is constrained.
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
    "fields": {
      "derivatives_funding_rate_latest": -2.2e-05,
      "derivatives_open_interest_latest": 94836.65,
      "derivatives_open_interest_change_pct": 1.7012
    },
    "coverage_gaps": [
      "coinglass:missing_api_key"
    ],
    "evidence": {
      "evidence_status": "fetched",
      "source": "open_deep_research_local",
      "citations_count": 10
    }
  },
  "field_interpretation_guide": {
    "latest_close": "Latest observed close. Use it as the anchor for all price references.",
    "return_1d_pct": "One-day percentage move. Positive means short-term momentum, negative means near-term weakness.",
    "return_total_pct": "Window-level cumulative return. Use it to distinguish bounce-vs-trend continuation.",
    "avg_volume": "Average traded volume proxy. Higher values imply stronger liquidity and more credible moves.",
    "coverage_gaps": "If coinglass coverage is missing, say derivatives conviction is constrained.",
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
    "data_coverage",
    "observations",
    "stress_signals",
    "positioning_thesis",
    "what_would_change_my_mind",
    "uncertainties"
  ]
}
