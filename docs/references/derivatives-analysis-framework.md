# Crypto Derivatives Analysis Framework: Quantitative Rules

## 1. FUNDING RATE INTERPRETATION

### Threshold Levels (per 8-hour period, standard perpetual swap)

| Funding Rate | Annualized Equivalent | Interpretation | Signal |
|---|---|---|---|
| 0.0000% to 0.0050% | 0% to 5.5% | Neutral equilibrium | No signal |
| 0.0050% to 0.0100% | 5.5% to 10.95% | Mild long bias | Normal trending market |
| 0.0100% to 0.0300% | 10.95% to 32.85% | Moderate long crowding | Early warning; monitor |
| 0.0300% to 0.0500% | 32.85% to 54.75% | Heavy long crowding | Elevated correction risk |
| 0.0500% to 0.1000% | 54.75% to 109.5% | Extreme long crowding | High probability of mean reversion; historically precedes 5-10% retracements within 72 hours ~60% of the time |
| >0.1000% | >109.5% | Parabolic/unsustainable | Imminent liquidation cascade risk; historically top-decile rates precede sharp corrections |
| -0.0050% to 0.0000% | -5.5% to 0% | Mild short bias | Normal ranging market |
| -0.0100% to -0.0050% | -10.95% to -5.5% | Moderate short crowding | Potential short squeeze setup |
| < -0.0300% | < -32.85% | Extreme short crowding | High probability short squeeze; historically coincides with local bottoms |

### Key Rules:
- **Glassnode's 0.01% signal line**: A sustained break above 0.01% (7-day MA) historically marks the transition into a bullish regime. Failure to sustain above 0.01% indicates the market lacks conviction for a sustained uptrend.
- **Annualization formula**: `Annualized Rate = Funding Rate x 3 x 365` (3 payments per day).
- **Duration matters**: A single spike to 0.05% is less significant than 3+ consecutive days above 0.03%. Use the 7-day moving average to filter noise.
- **Cross-exchange divergence**: If Binance funding is 0.05% but Bybit is 0.01%, it signals exchange-specific positioning, not market-wide crowding. Use the volume-weighted average across top 3 exchanges.

## 2. FUNDING RATE Z-SCORE

### Calculation:
```
z_score = (current_funding_rate - rolling_mean) / rolling_std_dev
```
- Use a **30-day rolling window** for the mean and standard deviation.
- Calculate on the 8-hour funding rate (not annualized).

### Interpretation Thresholds:

| Z-Score | Interpretation | Action Signal |
|---|---|---|
| > +3.0 | Extreme long crowding; parabolic | Strong contrarian short / exit longs |
| > +2.0 | Crowded long trade | Reduce long exposure; tighten stops |
| +1.0 to +2.0 | Above-average bullish positioning | Monitor for deterioration |
| -1.0 to +1.0 | Normal range | No signal |
| -1.0 to -2.0 | Above-average bearish positioning | Monitor for reversal |
| < -2.0 | Crowded short trade | Reduce short exposure; consider longs |
| < -3.0 | Extreme short crowding; capitulation | Strong contrarian long / exit shorts |

### Key Rules:
- Z-score > +2 or < -2 historically reverts to the mean within 3-7 days approximately 70% of the time.
- The z-score is more reliable on higher timeframes (daily > 8-hourly).
- Combine with OI: if z-score > +2 AND OI is at 30-day highs, the crowding signal is stronger.

## 3. OPEN INTEREST (OI) INTERPRETATION

### The Four Quadrants:

| Scenario | Price | OI | Meaning | Strength Signal |
|---|---|---|---|---|
| **New Longs Opening** | Rising | Rising | Fresh capital entering long; new money bullish | Strong trend if CVD confirms |
| **Shorts Closing** | Rising | Falling | Short squeeze; covering rally | Weaker rally; likely exhaustible |
| **New Shorts Opening** | Falling | Rising | Fresh capital entering short; new money bearish | Strong downtrend if CVD confirms |
| **Longs Closing** | Falling | Falling | Long liquidation / profit-taking | Weaker decline; likely exhaustible |

### Quantitative OI Thresholds:

- **OI/Market Cap Ratio**: Track the ratio of total BTC futures OI to BTC market cap.
  - **< 2%**: Low leverage environment; derivatives unlikely to drive price.
  - **2-3%**: Normal range.
  - **3-5%**: Elevated leverage; increased volatility risk.
  - **> 5%**: Extreme leverage; historically coincides with major deleveraging events (Nov 2022 FTX, late 2021 peak).
- **OI Change Rate**: A single-day OI increase of >10% signals a significant influx of new leveraged positions and heightened liquidation risk.
- **OI at ATH + Negative Funding**: This divergence (lots of new positions but shorts paying longs) signals heavy short opening -- potential short squeeze setup.
- **OI at ATH + Funding > 0.05%**: Maximum fragility; the market is a loaded spring for a liquidation cascade in either direction.

### Estimated Leverage Ratio (ELR) -- CryptoQuant:
- **Formula**: Exchange OI / Exchange BTC Reserve
- **< 0.15**: Low leverage, healthy market.
- **0.15-0.20**: Normal range.
- **0.20-0.22**: Elevated leverage; increased crash sensitivity.
- **> 0.22**: Historical all-time high territory (Jan 2022 peak was ~0.224). Extremely fragile; small price moves trigger cascading liquidations.
- **Historical pattern**: Whenever ELR reaches local peaks, price has subsequently reversed trend.

## 4. LIQUIDATION ANALYSIS

### Significance Thresholds (BTC, 24-hour):

| 24h Liquidation Volume | Significance | Historical Context |
|---|---|---|
| < $100M | Normal market noise | Daily average in calm markets |
| $100M - $300M | Elevated; notable but not extreme | Typical in volatile weeks |
| $300M - $500M | Significant deleveraging event | Occurs monthly on average |
| $500M - $1B | Major liquidation event | Occurs a few times per year |
| $1B - $2B | Severe cascade | Nov 2025: $1.7-2B, 396K traders liquidated |
| > $2B | Extreme / historic | Oct 2025: $3.21B erased in ~60 seconds; $19B OI wiped in 36 hours |

### Long/Short Liquidation Ratio:

| Ratio (Long:Short) | Interpretation |
|---|---|
| ~1:1 | Balanced market; both sides equally positioned |
| 2:1 to 3:1 | Market was leaning long; longs caught offside |
| > 5:1 | Overwhelmingly long-positioned market caught completely offside; signals potential capitulation bottom for longs |
| 1:2 to 1:3 | Market was leaning short; shorts squeezed |
| < 1:5 | Massive short squeeze; potential blow-off top signal |

### Liquidation Cascade Detection Rules:
1. **Pre-condition**: OI/spot volume ratio > 2-3x the 30-day average daily spot volume.
2. **Trigger zone**: Price approaching a cluster of liquidation levels visible on heatmaps (Coinglass, Hyblock).
3. **Cascade in progress**: Liquidation volume accelerating (each 5-minute candle has more liquidations than the previous) + price moving parabolically + OI dropping rapidly.
4. **Cascade exhaustion signal**: Liquidation rate decelerating + funding rate flipping to the opposite extreme + OI stabilizing.

## 5. BASIS / PREMIUM (Futures vs Spot)

### Annualized Basis Thresholds:

| Annualized Basis | Market State | Interpretation |
|---|---|---|
| > 30% | Extreme contango | Euphoric/parabolic bull; historically coincides with cycle tops |
| 15% to 30% | High contango | Strong bullish sentiment; greed territory (Fear & Greed > 75) |
| 10% to 15% | Elevated contango | Bullish with moderate optimism |
| 5% to 10% | Normal contango | Neutral to mildly bullish; reflects standard carry cost |
| 0% to 5% | Flat / compressed | Low sentiment; basis trade profitability declining |
| < 0% (Backwardation) | Backwardation | Extreme bearish sentiment; forced de-risking. Historically appears at major bottoms: Nov 2022 (FTX), Mar 2023, Aug 2023, Dec 2025 |

### Key Rules:
- **Contango > 20% = structural top warning**: Signals willingness to pay extreme premium for leveraged longs; unsustainable.
- **Backwardation = capitulation signal**: In crypto, backwardation is purely sentiment-driven and signals extreme fear/forced selling.
- **CME vs offshore basis divergence**: If CME basis is significantly higher than Binance/Bybit basis, it signals institutional FOMO (ETF-driven demand). If CME basis collapses while offshore stays elevated, institutions are de-risking.
- **Basis compression from high levels**: A rapid drop from >20% to <10% within days signals institutional unwind of basis trades.

## 6. CVD (CUMULATIVE VOLUME DELTA)

### Core Interpretation Matrix:

| Price | OI | CVD | Interpretation | Confidence |
|---|---|---|---|---|
| Rising | Rising | Rising | New long positions opening; genuine bullish trend | HIGH |
| Rising | Rising | Falling | Price rising but net selling; likely short squeeze or manipulation | LOW |
| Rising | Falling | Rising | Shorts closing + buying pressure; healthy but limited fuel | MEDIUM |
| Rising | Falling | Falling | Price rising on position closure, no new buying | LOW |
| Falling | Rising | Falling | New short positions opening; genuine bearish trend | HIGH |
| Falling | Rising | Rising | Price falling but net buying; possible bear trap / accumulation | LOW |
| Falling | Falling | Falling | Long liquidation cascade; selling begets selling | HIGH |
| Falling | Falling | Rising | Longs closing but buying emerging; potential bottom forming | MEDIUM |

### CVD Divergence Rules:
1. **Bearish CVD divergence**: Price makes a new high, but CVD does not. Historically precedes pullbacks, especially on 4H+ timeframes.
2. **Bullish CVD divergence**: Price makes a new low, but CVD does not decline correspondingly. More reliable when accompanied by funding rate flipping negative.
3. **Timeframe hierarchy**: Confirm CVD divergences on higher timeframes. Daily CVD divergence is the strongest signal.
4. **Liquidity caveat**: CVD signals are most reliable for BTC and ETH. For altcoins with < $50M daily volume, CVD can be erratic.

## COMPOSITE SIGNAL FRAMEWORK

### Maximum Bullish (Contrarian -- after extreme bearish conditions):
- Funding rate < -0.03% (z-score < -2)
- Futures in backwardation
- OI dropping rapidly (longs already liquidated)
- Long/short liquidation ratio > 5:1 in recent cascade
- CVD showing bullish divergence
- ELR dropping below 0.15

### Maximum Bearish (Contrarian -- after extreme bullish conditions):
- Funding rate > 0.05% (z-score > +2)
- Annualized basis > 20%
- OI at all-time highs
- ELR > 0.22
- CVD showing bearish divergence
- Dense long liquidation clusters just below current price

### Neutral / No-Trade Zone:
- Funding rate z-score between -1 and +1
- Basis 5-10% (normal carry)
- OI stable, no divergences
- CVD tracking price (no divergence)
- ELR in 0.15-0.20 range

## Sources
- Glassnode: Funding rates, ELR, leverage analysis
- Amberdata: Liquidation cascade analysis, $3.21B Oct 2025 crash
- CoinGlass: Price/OI/CVD interpretation guide
- CryptoQuant: ELR documentation
- CF Benchmarks: Bitcoin basis analysis
- CoinDesk: Backwardation since FTX
- CME Group: Basis trading with spot ETFs
- SSRN: Anatomy of Oct 2025 liquidation cascade
- LuxAlgo/PipPenguin: CVD trading methodology
- MDPI: Funding rate market structure research
