# Demo Case 2: Prompt-Driven BTC Analyst Stack

## Goal

Show the earlier milestone where the first-order analyst stack was already producing real provider output before the full multi-debater layer was stabilized.

## Source Run

- Run ID: `r_20260326T022729Z_BTC`
- This milestone is described as an internal evolution note.
- In the trimmed repo, use Demo Case 1 for the current end-to-end showcase.

## What Happened

- Asset: `BTC`
- Horizon: `3d`
- Thesis: `Assess real provider memo quality uplift v5`
- Final decision: `avoid`
- Quant score: `40`

The first-order roles all completed as `prompt_driven via openai`:

- `technical_analyst`
- `defi_fundamentals_analyst`
- `derivatives_analyst`
- `news_analyst`

## Why This Matters

This case isolates the analyst layer before the repo fully leaned into the TradingAgents-style debate flow.

It shows:

- the system can already write crypto-specific analyst memos
- output quality is not limited to deterministic fallback
- the artifact chain is already stable even before the full debate layer is considered

## Notable Output

From the report:

- technical reasoning stayed bearish because BTC remained roughly `-23%` below the `200-day SMA`
- DeFi stayed cautious because `MC/TVL` remained above `2.6`
- catalyst coverage explicitly said the event map was preliminary and non-actionable
