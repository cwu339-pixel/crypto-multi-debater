# Bull Researcher

- role: bull_researcher
- title: Bull Researcher
- thesis: Momentum remains constructive, but needs confirmation.
## Key Points
- {'point': 'Short-term momentum remains constructive.', 'evidence_source': 'technical_analyst', 'confidence': 'med'}
- {'point': 'No confirmed negative catalyst in evidence pack.', 'evidence_source': 'news_analyst', 'confidence': 'low'}
## Rebuttals To Bear
- {'bear_point': 'Coverage gaps lower conviction', 'rebuttal': 'Missing derivatives data does not automatically invalidate price resilience.', 'evidence_source': 'technical_analyst'}
## Invalidation
- Momentum fails and price loses support with expanding volatility.
- confidence: low
## Data Gaps
- coinglass:missing_api_key
- summary: Momentum remains constructive, but needs confirmation.
- provider: deterministic
- analysis_mode: deterministic_fallback
- speaker: Bull Analyst
- argument: Bull Analyst: Momentum remains constructive, but needs confirmation. Missing derivatives data does not automatically invalidate price resilience.
- counterparty_response: 
- prompt_path: /Users/wuchenghan/Projects/crypto-research-agent/src/crypto_research_agent/agents/prompts/bull_researcher.md
- prompt_text: # Bull Researcher

You are the bull researcher in a crypto research debate.
Use the prior role memos to produce the strongest constructive case.
Do not invent new data sources beyond the provided context.

## Rules of Engagement

1. Build the bullish thesis ONLY from evidence in the prior memos. Do not hallucinate data points.
2. Address the top 3 bearish arguments proactively. Show you understand the risks and explain why the bull case holds despite them.
3. Distinguish between "data supports this" (cite the specific memo and metric) and "this is plausible but unconfirmed" (mark as low confidence).
4. Use domain knowledge to contextualize:
   - Funding rate crowding that HASN'T reached extreme thresholds may actually be healthy (sustained 0.01-0.03% = bullish regime per Glassnode)
   - TVL growth in native token terms is stronger evidence than USD TVL growth
   - Stablecoin supply growth >3% monthly = structural capital inflow
   - Post-halving 12-18 month window is historically the highest-probability bullish period
   - DeFi yields rising from low base = healthy leverage demand, not necessarily overheating
5. State your invalidation conditions clearly — what would flip you bearish.

## Output Format

Produce a JSON memo with these fields:
- `role`: "bull_researcher"
- `thesis`: one-paragraph bull case
- `key_points`: list of {point, evidence_source, confidence: "high"|"med"|"low"}
- `rebuttals_to_bear`: list of {bear_point, rebuttal, evidence_source}
- `invalidation`: list of specific conditions that would break the bull case
- `confidence`: "high" | "med" | "low"
- `data_gaps`: list of missing data that would strengthen the bull case

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
      "investment_debate_state": {
        "history": "",
        "current_response": "",
        "count": 0
      }
    },
    "debate_state": {
      "history": "",
      "current_response": "",
      "count": 0
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
    "thesis",
    "key_points",
    "rebuttals_to_bear",
    "invalidation",
    "data_gaps",
    "speaker",
    "argument",
    "counterparty_response"
  ]
}
- debate_state: {'history': 'Bull Analyst: Momentum remains constructive, but needs confirmation. Missing derivatives data does not automatically invalidate price resilience.', 'bull_history': 'Bull Analyst: Momentum remains constructive, but needs confirmation. Missing derivatives data does not automatically invalidate price resilience.', 'bear_history': '', 'current_response': 'Bull Analyst: Momentum remains constructive, but needs confirmation. Missing derivatives data does not automatically invalidate price resilience.', 'count': 1}
