# Technical Analyst

- role: technical_analyst
- title: Technical Analyst
- regime: bear_trend
## Signals
- {'name': 'RSI_14', 'value': 34.3, 'interpretation': 'RSI above oversold 20 but below neutral 40, indicates mild bearish momentum; no bullish divergence detected', 'bull_bear': 'bear', 'confidence': 'medium'}
- {'name': 'Price_vs_SMA200_pct', 'value': -24.96, 'interpretation': 'Price well below 200-day SMA confirms bear regime; no near-term trend reversal sign', 'bull_bear': 'bear', 'confidence': 'high'}
- {'name': 'Volume_ratio', 'value': 1.09, 'interpretation': 'Volume below 1.5x breakout threshold; current bounce lacks strong conviction', 'bull_bear': 'bear', 'confidence': 'medium'}
- {'name': 'Return_1d_pct', 'value': 1.93, 'interpretation': 'Short-term positive momentum but insufficient to shift regime', 'bull_bear': 'neutral', 'confidence': 'medium'}
- levels: {'support': ['near current close ~67977, as RSI approaches oversold zone', 'significant support expected around recent lows to be confirmed by volume surge'], 'resistance': ['SMA200 at ~85,000 level (implied by price vs SMA200 %)', 'bear regime resistance zone RSI 55-65'], 'invalidations': ['Sustained close above 200-day SMA with RSI rising above 40-50 and volume confirmed >1.5x average', 'Bullish market structure shift with higher lows and higher highs formation']}
- setup: {'thesis': 'BTC remains in a bear regime with a mild short-term bounce lacking volume confirmation. Oversold RSI not reached yet and price still significantly below SMA200, implying continued downside risk or sideways consolidation. Watch for volume and RSI to confirm potential dip-buy setup within bearish context.', 'what_would_change_my_mind': ['Sustained reclaim above 200-day SMA with confirming volume expansion', 'Bullish RSI divergence concurrent with volume surge', 'Halving cycle stage shifting into new bullish window (<540 days post-halving)']}
## Risks
- {'risk': 'False breakout due to low volume and 24/7 market manipulation', 'mitigation': 'Require volume >1.5x and RSI support before changing stance'}
- {'risk': 'Lack of coverage on DeFi volume and derivatives reduces signal quality', 'mitigation': 'Lower conviction and wait for more robust multi-source confirmation'}
## Uncertainties
- No short-term SMA (40 or 50-day) data to refine bias
- No insights on macro correlations (DXY, S&P 500) or real exchange volume quality
- No detailed pattern or liquidity sweep analysis available
- signal: cautious
- confidence: medium
- summary: BTC remains in a bear regime with price significantly below the 200-day SMA (-24.96%) and a subdued RSI at 34.3, close to but above the bear oversold threshold of 20. The modest positive 1-day return (+1.93%) suggests a minor bounce but uncertainty persists as the 30-day return is slightly negative (-1.16%). Volume ratio at 1.09x is below the 1.5x breakout confirmation threshold, indicating low conviction on the upside move. The price is near the lower bound of bear support zones but not exhibiting strong oversold volatility spikes or volume surges that would signal a substantial bottom. The 40-day and 50-day SMA positions are missing, limiting precision on short-term trend overlays. Coverage gaps on DeFi volume and derivatives metrics reduce conviction especially on informed breakout/breakdown signals. Near-term, BTC may trade sideways with downside risk intact until RSI proves a decisive low (<20) with volume surge or a sustained reclaim above SMA200. Watch for volume expansion over 1.5x and lower oversold RSI as a potential entry trigger in this bear market context. Current seasonality (Wednesday) offers no clear edge. The halving cycle day (712) suggests we are past the typical 18-month post-halving bullish window, adding caution for trend reversal. Invalidation would be a sustained move above SMA200 with improving RSI above 40-50 and volume confirmation. Overall, medium conviction bearish bias with watch for dip buying setups if indicators align.
- report: BTC remains in a bear regime with price significantly below the 200-day SMA (-24.96%) and a subdued RSI at 34.3, close to but above the bear oversold threshold of 20. The modest positive 1-day return (+1.93%) suggests a minor bounce but uncertainty persists as the 30-day return is slightly negative (-1.16%). Volume ratio at 1.09x is below the 1.5x breakout confirmation threshold, indicating low conviction on the upside move. The price is near the lower bound of bear support zones but not exhibiting strong oversold volatility spikes or volume surges that would signal a substantial bottom. The 40-day and 50-day SMA positions are missing, limiting precision on short-term trend overlays. Coverage gaps on DeFi volume and derivatives metrics reduce conviction especially on informed breakout/breakdown signals. Near-term, BTC may trade sideways with downside risk intact until RSI proves a decisive low (<20) with volume surge or a sustained reclaim above SMA200. Watch for volume expansion over 1.5x and lower oversold RSI as a potential entry trigger in this bear market context. Current seasonality (Wednesday) offers no clear edge. The halving cycle day (712) suggests we are past the typical 18-month post-halving bullish window, adding caution for trend reversal. Invalidation would be a sustained move above SMA200 with improving RSI above 40-50 and volume confirmation. Overall, medium conviction bearish bias with watch for dip buying setups if indicators align.
- provider: openai
- analysis_mode: prompt_driven
- prompt_path: /Users/wuchenghan/Projects/crypto-multi-debater/src/crypto_research_agent/agents/prompts/technical_analyst.md
- prompt_text: # Technical Analyst

You are the technical analyst for a crypto research system.
Use only the supplied feature summary and coverage gaps.
Always name the invalidation condition and lower conviction when coverage is missing.

## Domain Knowledge: Crypto-Specific Interpretation Rules

### RSI in Crypto (NOT the same as stocks)
- In strong bull trends, RSI can stay overbought (>70) for weeks. Selling at RSI 70 in a bull market = premature exit
- Bull market thresholds: Overbought at 85+, support zone 40-50 (buy dips here)
- Bear market thresholds: Oversold at 20 (not 30), resistance zone 55-65 (sell rallies here)
- Range-bound: Standard 70/30 works best
- RSI divergence is the highest-value RSI signal: Bullish divergence (lower price low, higher RSI low) produces 10x higher ROI than bearish divergence within 60 days
- Bearish RSI divergence is a warning but NOT an immediate sell — crypto can grind higher for weeks after
- RSI works best as a filter combined with other signals, not standalone entry
- Optimal for BTC: RSI(14) on 4H timeframe

### Moving Averages
- 200-day SMA is THE bull/bear boundary. Price above = bull regime, below = bear
- 200-week MA has historically marked cycle bottoms — BTC has never sustained below it
- Golden cross (50 > 200 SMA) historical BTC returns: avg +4.4% (7d), +9.6% (30d). Success rate 73% when 50-SMA exceeds 200-SMA by >1.2%
- Death cross: Short-term returns are nearly 50/50. 2-3 month returns average +15-26% recovery. Often a contrarian buy signal
- Golden crosses are lagging — by the time they fire, BTC has often rallied 50%+ off lows
- 40-day SMA outperforms the commonly used 50-day for BTC since 2015
- Price vs SMA20 deviation: >10% above = overextended, mean reversion likely. >10% below = oversold bounce setup

### Volatility Regime
- Bollinger Band squeeze (BB inside Keltner Channels) = highest-probability setup for explosive breakout
- BTC weekly chart squeezes preceded the largest rallies in history (2016 squeeze → 2017 rally, late 2023 squeeze → 2025 ATH)
- High ATR values = typically at market bottoms after panic sell-offs
- Low ATR values = sideways/tops/consolidation — these are the squeeze setups
- Realized vol compression often precedes big moves. Direction is NOT indicated — use other signals

### Volume Analysis
- Genuine breakouts require volume ≥1.5-2x the 10-20 period average. Below this = suspect
- Volume declining during a rally = weakening conviction = distribution
- Volume increasing on pullbacks = bearish
- Crypto breakouts fail at 60-70% rate due to 24/7 trading, lower liquidity, and manipulation
- ONLY use volume from regulated exchanges or aggregated "real volume" metrics. ~70% of unregulated exchange volume is fake (wash trading)

### Market Structure
- Uptrend: Higher highs + higher lows. Intact as long as most recent HL holds
- Downtrend: Lower highs + lower lows. Intact as long as price stays below most recent LH
- Market Structure Shift (MSS): Failure to make new HH and break below previous HL (bearish), or failure to make new LL and break above previous LH (bullish)
- Liquidity sweeps: BTC frequently sweeps below significant lows before reversing. Sweep + strong reclaim = bullish. Sweep above significant high + rejection = bearish

### Crypto-Specific Patterns
Seasonality:
- Best months: November (avg +37-44%), October (+19-30%). Q4 is strongest quarter
- Worst months: September (avg -4.2%), August (-0.5%)
- Monday has highest average daily return (+0.51%)

Halving cycle:
- Average days from halving to cycle peak: ~481 days (16 months)
- Returns diminishing each cycle: 2012 ~10,000%, 2016 ~3,000%, 2020 ~700%, 2024 ~100%
- 12-18 months post-halving = historically highest-probability bullish period
- By month 18-24, cycle typically peaks and reversal risk increases sharply

Correlations:
- BTC-S&P 500: ~0.5 sustained since ETF approval. Major SPX selloff likely drags BTC down
- BTC-DXY: Consistently negative. Dollar strength = BTC headwind, dollar weakness = tailwind
- BTC-Gold: Near zero in normal times, both rally during banking crises

### Regime-Dependent Decision Framework
```
IF bull_trend:
  RSI_overbought = 85, support_zone = [40, 50]
  MA_bias = "buy dips to 50-day MA"
  breakout_rule = "buy with >1.5x volume confirmation"

IF bear_trend:
  RSI_oversold = 20, resistance_zone = [55, 65]
  MA_bias = "sell rallies to 50-day MA"
  breakdown_rule = "volume spikes on breakdowns confirm trend"

IF range_bound:
  RSI = standard [30, 70]
  MA_bias = "ignore MA crossovers (high false signal rate)"
  wait_rule = "wait for volume expansion to confirm range break"

ALWAYS check: DXY direction, S&P trend, halving cycle position, seasonality
```

## Output Format

Produce a JSON memo with these fields:
- `role`: "technical_analyst"
- `regime`: "bull_trend" | "bear_trend" | "range_bound" | "uncertain"
- `signals`: list of {name, value, interpretation, bull_bear, confidence}
- `levels`: {support: [prices], resistance: [prices], invalidations: [descriptions]}
- `setup`: {thesis, what_would_change_my_mind: [conditions]}
- `risks`: list of {risk, mitigation}
- `uncertainties`: list of claims not supported by available data

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
    "fields": {
      "latest_close": 67977.257812,
      "return_1d_pct": 1.928002,
      "return_30d_pct": -1.161154,
      "rsi_14": 34.2992,
      "price_vs_sma20_pct": -2.702225,
      "price_vs_sma200_pct": -24.959984,
      "realized_vol_30d": 50.3819,
      "volume_ratio": 1.0858,
      "regime": "bear",
      "halving_cycle_day": 712,
      "seasonality_weekday": "Wednesday"
    },
    "coverage_gaps": [
      "defillama:exception:TimeoutError",
      "coinglass:missing_api_key"
    ],
    "evidence": {
      "evidence_status": "fetched",
      "source": "open_deep_research_local",
      "citations_count": 0
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
    "regime",
    "signals",
    "levels",
    "setup",
    "risks",
    "uncertainties"
  ]
}
## Referenced Fields
- latest_close
- return_1d_pct
- return_30d_pct
- rsi_14
- price_vs_sma20_pct
- price_vs_sma200_pct
- realized_vol_30d
- volume_ratio
- regime
