<div align="center">

# Crypto Multi-Debater

### Debate-Driven Multi-Agent Crypto Research Product

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![CI](https://github.com/cwu339-pixel/crypto-multi-debater/actions/workflows/ci.yml/badge.svg)](https://github.com/cwu339-pixel/crypto-multi-debater/actions/workflows/ci.yml)
[![OpenBB](https://img.shields.io/badge/Data-OpenBB-0A7B83)](https://openbb.co/)
[![DefiLlama](https://img.shields.io/badge/Data-DefiLlama-111111)](https://defillama.com/)
[![Research](https://img.shields.io/badge/Evidence-open__deep__research-6B46C1)](https://github.com/)

</div>

---

# Crypto Multi-Debater: Multi-Agent Crypto Research Framework

## News
- [2026-03] Refocused as a dedicated `crypto multi-debater research product` instead of a mixed benchmark / backtest repo.
- [2026-03] Full prompt-driven analyst, debate, risk, and final-arbiter stack landed in the live workflow.
- [2026-03] `open_deep_research` live evidence path stabilized with readable fallback diagnostics.
- [2026-04] Homepage showcase refreshed to today's live BTC debate report.

<div align="center">

`Overview` | `Framework` | `Installation` | `Quickstart` | `Demo Cases` | `Inspired By`

</div>

## Overview

Crypto Multi-Debater is a crypto-specific research product that adapts the debate-oriented architecture of `TradingAgents` to the crypto domain.

Instead of treating crypto as generic financial text generation, this repo uses:

- crypto-native data sources
- crypto-specific analyst roles
- sequential bull/bear and risk debates
- a final arbiter that turns debate into a trading-style research report
- auditable artifacts and review tasks

This project is strongest as a **crypto multi-debater research product**, not as an auto-trading system or backtesting lab.

## Framework

The system turns a market question into a structured research flow:

`thesis -> data snapshots -> feature summary -> evidence pack -> analyst stack -> bull/bear debate -> risk debate -> final arbiter -> research report`

### Analyst Team

- `Technical Analyst`: reads crypto regime, volatility, RSI, SMA structure, and halving-cycle context
- `DeFi Fundamentals Analyst`: reads TVL, stablecoin yields, MC/TVL, and protocol-level capital signals
- `Derivatives Analyst`: reads funding, OI, liquidation stress, and leverage structure when available
- `News Analyst`: interprets crypto catalysts, regulation, unlocks, and macro spillover from the evidence layer

### Debate Layer

- `Bull Researcher`: argues for continuation, asymmetry, and upside path
- `Bear Researcher`: argues for fragility, regime failure, and downside path

These roles are sequential, not parallel summaries. Each side responds to the other side's latest case.

### Risk Layer

- `Aggressive`, `Conservative`, and `Neutral` risk views are synthesized inside the risk stage
- `Risk Manager` converts the debate into sizing, invalidation, and posture constraints

### Final Arbiter

- reads the analyst stack, bull/bear debate, and risk debate
- produces the final trading-style report
- exposes decision, rationale, key factors, and hard rules

## Why It Is More Crypto-Specific Than Generic Trading Agents

- It uses `OpenBB`, `DefiLlama`, and `open_deep_research` instead of generic equity-oriented analyst inputs.
- Its analyst roles are written for crypto market structure rather than stock research metaphors.
- It produces a crypto trading-style memo, not just a chat transcript or a generic LLM summary.
- It preserves research artifacts so the run can be inspected later.

## Current Live Capabilities

- `OpenBB` live market data fetch
- `DefiLlama` live protocol and yield data fetch
- `open_deep_research` live evidence collection with explicit fallback reasons
- prompt-driven first-order analyst outputs
- prompt-driven bull/bear debate
- prompt-driven risk layer and final arbiter
- rendered trading-style research report
- post-horizon review task generation

## Repo Boundaries

To keep the repository auditable, this repo separates maintained source code from reference and showcase output:

- `src/`, `tests/`, `config/`, and `docs/` are the maintained project sources
- `tmp_showcase/` contains committed example run artifacts used for homepage and demo-case inspection
- `external/open_deep_research/` is an upstream reference checkout, not the core local implementation

The main engineering changes should land in source directories. Showcase refreshes and upstream syncs should stay intentionally scoped so review diffs remain readable.

## Best Showcase Right Now

If you want one file that best represents the repo today, open this case:

- run: [`tmp_showcase/runs/r_20260401T031358Z_BTC/run.json`](tmp_showcase/runs/r_20260401T031358Z_BTC/run.json)
- report: [`tmp_showcase/research_cards/2026-04-01/BTC_r_20260401T031358Z_BTC.md`](tmp_showcase/research_cards/2026-04-01/BTC_r_20260401T031358Z_BTC.md)
- call log: [`tmp_showcase/runs/r_20260401T031358Z_BTC/agents/call_log.jsonl`](tmp_showcase/runs/r_20260401T031358Z_BTC/agents/call_log.jsonl)

That showcase includes:

- live OpenBB + DefiLlama ingestion
- live evidence collection
- crypto-specific analyst memos
- bull/bear debate
- risk debate
- prompt-driven final arbiter
- rendered report with visible debate structure

## Demo Cases

- [Full Multi-Debater BTC Report](docs/demo_cases/01-full-multi-debater-btc-report.md)
- [Prompt-Driven BTC Analyst Stack](docs/demo_cases/02-prompt-driven-btc-report.md)
- [Review Loop Example](docs/demo_cases/03-review-loop-example.md)

## Installation

Clone the repo:

```bash
git clone <your-repo-url>
cd crypto-multi-debater
```

Create a virtual environment:

```bash
uv venv .venv
```

Install the package and dev dependencies:

```bash
uv pip install --python .venv/bin/python -e '.[dev]'
uv pip install --python .venv/bin/python openbb
.venv/bin/openbb-build
```

Copy the environment template:

```bash
cp .env.example .env
```

## Quickstart

Run tests:

```bash
PYTHONPATH=src .venv/bin/python -m pytest -q
```

Run a live research job:

```bash
crypto-multi-debater run --asset BTC --horizon-days 3 --thesis "Assess BTC after recent rally"
```

Run pending reviews:

```bash
crypto-multi-debater run-pending-reviews --output-dir .
```

## Data And Evidence Modes

- `OpenBB`: live price history
- `DefiLlama`: live protocol and yield data
- `CoinGlass`: optional derivatives adapter, graceful when unavailable
- `open_deep_research`: preferred evidence layer, with explicit fallback reasons when collection fails

## Current Limitations

- `CoinGlass` may be missing in live runs
- historical replay is strict for price, but not yet a full point-in-time replay for all sources
- evidence quality still depends on `open_deep_research` stability and source quality
- report tone is improving, but still less polished than a mature PM-authored memo
- this is not an auto-trading system

## Inspired By

- `TradingAgents`: debate-oriented analyst architecture
- `OpenBB`: market data access
- `DefiLlama`: DeFi and protocol datasets
- `open_deep_research`: evidence collection pattern

The contribution here is not inventing every component from scratch. The contribution is adapting the `TradingAgents` debate idea into a crypto-native research product with better crypto inputs, clearer artifacts, and a more auditable report flow.
