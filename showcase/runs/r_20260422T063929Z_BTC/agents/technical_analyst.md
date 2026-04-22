# Technical Analyst

- role: technical_analyst
- title: Technical Analyst
- regime: bear_trend
## Signals
- {'name': 'RSI_14', 'value': 68.37, 'interpretation': 'Approaching bear market resistance zone (55-65), short-term momentum but not overbought', 'bull_bear': 'bear', 'confidence': 'medium'}
- {'name': 'Price_vs_SMA200_pct', 'value': -9.24, 'interpretation': 'Price well below 200-day SMA; confirms bear trend regime', 'bull_bear': 'bear', 'confidence': 'high'}
- {'name': 'Volume_ratio', 'value': 1.19, 'interpretation': 'Below threshold for breakout confirmation; rally lacks conviction', 'bull_bear': 'bear', 'confidence': 'medium'}
- {'name': 'Return_1d_pct', 'value': 2.09, 'interpretation': 'Short-term positive momentum; typical for bear trend bounce', 'bull_bear': 'bear', 'confidence': 'medium'}
- {'name': 'Halving_cycle_day', 'value': 733, 'interpretation': 'Cycle advanced beyond 18-24 month peak window; higher trend reversal risk', 'bull_bear': 'bear', 'confidence': 'medium'}
- levels: {'support': ['Most recent higher low (not specified in data)', 'SMA20 vicinity (~72,800 based on 6.8% above SMA20 implied price)'], 'resistance': ['Bear market RSI resistance zone: 55-65', '200-day SMA (~around $85,800 price implied by 9.2% below current price)', 'Psychological round levels near $78,000-$80,000'], 'invalidations': ['Price breaks and sustains >200-day SMA with volume >1.5x avg', 'RSI sustains >70-85 in a bull trend regime with corresponding bullish price action']}
- setup: {'thesis': 'BTC is in a bear trend bounce phase with moderate upward momentum but lacks volume to confirm breakout. Likely to face resistance near the 200-day SMA and RSI resistance zone. Remains a sell-rally scenario until clear breakout confirmation.', 'what_would_change_my_mind': ['Sustained price breakout above 200-day SMA with volume >1.5x average confirming bullish trend change', 'RSI maintains above 70-85 thresholds indicating bull momentum', 'Fundamental reversal catalysts or halving cycle confirms new bull trend']}
## Risks
- {'risk': 'Volume data quality gap due to missing Coinglass API key', 'mitigation': 'Cross-validate volume signals with alternative regulated exchange data or third-party aggregators'}
- {'risk': 'Unexpected macro shocks (SPX selloff or USD strength weakening BTC)', 'mitigation': 'Monitor BTC correlation with S&P 500 and DXY closely'}
## Uncertainties
- Volume quality confirmation incomplete due to coverage gap
- No explicit recent market structure lows or highs defined in data (unclear liquidity sweep signals)
- No detailed intraday RSI or 4H RSI data to refine short-term momentum assessment
- signal: cautious
- confidence: medium
- summary: BTC remains in a bear trend with price below the 200-day SMA by about 9.2%, confirming bearish regime bias. The RSI near 68 is approaching the bear market resistance zone (55-65) but has not definitively triggered an overbought sell signal, suggesting some remaining short-term upside momentum. Volume is below the 1.5x threshold required for confident breakout confirmation, indicating any rally may lack strong conviction and be vulnerable to failure or distribution. The 1-day return of +2.1% and 30-day return of +10.5% suggest a moderate bounce rather than a sustained trend reversal at this point. Given the cycle day 733 post-halving (beyond the 18-24 month peak window), risk of trend reversal remains elevated. Coverage gaps on volume quality reduce conviction further. BTC’s price running 6.8% above the 20-day SMA implies no significant overextension yet, so mean reversion down is not guaranteed. The current setup is likely a bear-trend rally/sell zone rather than a new bull run start. Confirmation of sustained trend change requires volume surge >1.5x average and RSI breaching above resistance zone (>65) with price reclaiming above 200-day SMA. Invalidations include price breaking above the 200-day SMA with strong volume and RSI sustaining >70 in bull thresholds. Lower conviction due to missing real volume API data.
- report: BTC remains in a bear trend with price below the 200-day SMA by about 9.2%, confirming bearish regime bias. The RSI near 68 is approaching the bear market resistance zone (55-65) but has not definitively triggered an overbought sell signal, suggesting some remaining short-term upside momentum. Volume is below the 1.5x threshold required for confident breakout confirmation, indicating any rally may lack strong conviction and be vulnerable to failure or distribution. The 1-day return of +2.1% and 30-day return of +10.5% suggest a moderate bounce rather than a sustained trend reversal at this point. Given the cycle day 733 post-halving (beyond the 18-24 month peak window), risk of trend reversal remains elevated. Coverage gaps on volume quality reduce conviction further. BTC’s price running 6.8% above the 20-day SMA implies no significant overextension yet, so mean reversion down is not guaranteed. The current setup is likely a bear-trend rally/sell zone rather than a new bull run start. Confirmation of sustained trend change requires volume surge >1.5x average and RSI breaching above resistance zone (>65) with price reclaiming above 200-day SMA. Invalidations include price breaking above the 200-day SMA with strong volume and RSI sustaining >70 in bull thresholds. Lower conviction due to missing real volume API data.
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
    "thesis": "Assess BTC setup as of 2026-04-22",
    "horizon_days": 3,
    "run_id": "r_20260422T063929Z_BTC"
  },
  "role_context": {
    "fields": {
      "latest_close": 77949.132812,
      "return_1d_pct": 2.090768,
      "return_30d_pct": 10.538144,
      "rsi_14": 68.3739,
      "price_vs_sma20_pct": 6.83896,
      "price_vs_sma200_pct": -9.239627,
      "realized_vol_30d": 40.8088,
      "volume_ratio": 1.1934,
      "regime": "bear",
      "halving_cycle_day": 733,
      "seasonality_weekday": "Wednesday"
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
