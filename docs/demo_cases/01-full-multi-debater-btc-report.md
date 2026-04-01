# Demo Case 1: Full Multi-Debater BTC Report

## Goal

Show the current mainline state of the repo: a crypto-specific multi-debater that runs end-to-end with live data, prompt-driven roles, visible debate structure, and a final research card.

## Source Run

- Run ID: `r_20260326T145524Z_BTC`
- Run payload: [`tmp_showcase/runs/r_20260326T145524Z_BTC/run.json`](../../tmp_showcase/runs/r_20260326T145524Z_BTC/run.json)
- Research card: [`tmp_showcase/research_cards/2026-03-26/BTC_r_20260326T145524Z_BTC.md`](../../tmp_showcase/research_cards/2026-03-26/BTC_r_20260326T145524Z_BTC.md)
- Role call log: [`tmp_showcase/runs/r_20260326T145524Z_BTC/agents/call_log.jsonl`](../../tmp_showcase/runs/r_20260326T145524Z_BTC/agents/call_log.jsonl)

## What Happened

- Asset: `BTC`
- Horizon: `3d`
- Thesis: `Showcase crypto multi-debater prompt-driven report`
- Final decision: `avoid`
- Quant score: `40`
- Coverage gap: `coinglass:missing_api_key`

All eight top-level roles completed as `prompt_driven via openai`:

- `technical_analyst`
- `defi_fundamentals_analyst`
- `derivatives_analyst`
- `news_analyst`
- `bull_researcher`
- `bear_researcher`
- `risk_manager`
- `final_arbiter`

## Why This Matters

This is the cleanest current showcase that the repo is no longer just multi-role scaffolding. It behaves like a real crypto debate system:

- first-order analysts produce crypto-specific memos
- bull and bear explicitly argue against each other
- risk is debated through aggressive / conservative / neutral stances
- the final arbiter synthesizes the stack into one constrained decision

## What To Look At In The Report

The most important sections in the card are:

- `Analyst Stack`
- `Debate Summary`
- `Decision Framework`

The report shows that the project is doing more than field translation:

- technical reasoning is framed in crypto bear-regime language
- DeFi reasoning uses `MC/TVL` and stablecoin lending yield context
- the bull case argues for post-halving recovery potential
- the bear case challenges that optimism with weak volume and missing derivatives confirmation
- the risk debate explains why the final answer stays conservative

## Current Limitation Exposed By This Case

This run is still not a full crypto desk view because:

- `CoinGlass` is missing, so short-horizon leverage and liquidation structure are not visible
- evidence is present, but citation quality is still thinner than a fully curated analyst workflow

That limitation is visible in the card itself, which is the point: the system shows its own uncertainty instead of hiding it.
