# Bear Researcher

- role: bear_researcher
- title: Bear Researcher
- thesis: Coverage gaps and event uncertainty limit conviction.
## Key Points
- {'point': 'Coverage gaps make the upside thesis unverifiable.', 'evidence_source': 'derivatives_analyst', 'confidence': 'high'}
- {'point': 'DeFi signals remain incomplete.', 'evidence_source': 'defi_fundamentals_analyst', 'confidence': 'med'}
## Rebuttals To Bull
- {'bull_point': 'Momentum remains constructive', 'rebuttal': 'Without derivatives confirmation the move could be fragile.', 'evidence_source': 'derivatives_analyst'}
## Invalidation
- Derivatives and DeFi data both confirm constructive participation.
- confidence: high
## Data Gaps
- coinglass:missing_api_key
- summary: Coverage gaps and event uncertainty limit conviction.
- provider: deterministic
- analysis_mode: deterministic_fallback
- speaker: Bear Analyst
- argument: Bear Analyst: Coverage gaps and event uncertainty limit conviction. Without derivatives confirmation the move could be fragile.
- counterparty_response: Bull Analyst: Momentum remains constructive, but needs confirmation. Missing derivatives data does not automatically invalidate price resilience.
- prompt_path: /Users/wuchenghan/Projects/crypto-research-agent/src/crypto_research_agent/agents/prompts/bear_researcher.md
- prompt_text: # Bear Researcher

You are the bear researcher in a crypto research debate.
Use the prior role memos to produce the strongest skeptical case.
Focus on weak evidence, missing coverage, and failure modes.

## Rules of Engagement

1. Build the bearish thesis ONLY from evidence in the prior memos and identifiable gaps. Do not hallucinate data points.
2. Address the top 3 bullish arguments proactively. Show you understand the bull case and explain why it is flawed or incomplete.
3. Distinguish between "data contradicts the bull case" (cite the specific memo and metric) and "data is missing so the bull case is unverifiable" (different kind of risk).
4. Use domain knowledge to challenge:
   - Elevated funding rates (>0.03%) with rising OI = crowded long, historically reverts. The "healthy" framing only holds below 0.03%
   - TVL growth in USD only (not native token) is inflated, not real capital inflow
   - Crypto breakouts fail 60-70% of the time. Volume confirmation is essential
   - Post-halving returns are diminishing each cycle (10,000% → 3,000% → 700% → ~100%). Don't assume historical pattern repeats at same magnitude
   - BTC-SPX correlation ~0.5. If macro deteriorates, crypto is NOT a safe haven
   - MC/TVL > 1.0 = potentially overvalued. Check if protocol revenue justifies the premium
   - "Buy the dip" at -20% can become catching a knife to -80%
5. State what would flip you bullish — what data would prove the bear case wrong.

## Output Format

Produce a JSON memo with these fields:
- `role`: "bear_researcher"
- `thesis`: one-paragraph bear case
- `key_points`: list of {point, evidence_source, confidence: "high"|"med"|"low"}
- `rebuttals_to_bull`: list of {bull_point, rebuttal, evidence_source}
- `invalidation`: list of specific conditions that would break the bear case
- `confidence`: "high" | "med" | "low"
- `data_gaps`: list of missing data that would strengthen the bear case

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
      "investment_debate_state": {
        "history": "Bull Analyst: Momentum remains constructive, but needs confirmation. Missing derivatives data does not automatically invalidate price resilience.",
        "current_response": "Bull Analyst: Momentum remains constructive, but needs confirmation. Missing derivatives data does not automatically invalidate price resilience.",
        "count": 1
      }
    },
    "debate_state": {
      "history": "Bull Analyst: Momentum remains constructive, but needs confirmation. Missing derivatives data does not automatically invalidate price resilience.",
      "current_response": "Bull Analyst: Momentum remains constructive, but needs confirmation. Missing derivatives data does not automatically invalidate price resilience.",
      "count": 1
    },
    "bull_key_points_to_rebut": [
      {
        "point": "Short-term momentum remains constructive.",
        "evidence_source": "technical_analyst",
        "confidence": "med"
      },
      {
        "point": "No confirmed negative catalyst in evidence pack.",
        "evidence_source": "news_analyst",
        "confidence": "low"
      }
    ]
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
    "rebuttals_to_bull",
    "invalidation",
    "data_gaps",
    "speaker",
    "argument",
    "counterparty_response"
  ]
}
- debate_state: {'history': 'Bull Analyst: Momentum remains constructive, but needs confirmation. Missing derivatives data does not automatically invalidate price resilience.\nBear Analyst: Coverage gaps and event uncertainty limit conviction. Without derivatives confirmation the move could be fragile.', 'bull_history': 'Bull Analyst: Momentum remains constructive, but needs confirmation. Missing derivatives data does not automatically invalidate price resilience.', 'bear_history': 'Bear Analyst: Coverage gaps and event uncertainty limit conviction. Without derivatives confirmation the move could be fragile.', 'current_response': 'Bear Analyst: Coverage gaps and event uncertainty limit conviction. Without derivatives confirmation the move could be fragile.', 'count': 2}
