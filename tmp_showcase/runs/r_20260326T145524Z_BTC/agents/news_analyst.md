# News Analyst

- role: news_analyst
- title: News Analyst
- evidence_quality: preliminary
## Top Catalysts
## Top Risks
- {'risk': 'External catalyst coverage is preliminary.', 'tier': 2, 'time_window': '3d', 'impact_estimate': 'unknown', 'confidence': 'low'}
- btrstn_assessment: insufficient_evidence
- macro_context: Macro catalyst coverage is not yet populated in the evidence pack.
- narrative: External catalyst coverage comes from open_deep_research_local and is currently fetched. The tape is not trading against a confirmed headline shock, but catalyst confidence is still below the standard needed for a high-conviction short-horizon call.
## Missing Evidence
- Token unlock schedule
- Macro calendar context
- Regulatory catalyst screening
- signal: contextualized
- summary: Headline and catalyst coverage is fetched; nothing clearly breaks the setup, but the event map is still incomplete.
- provider: deterministic
- analysis_mode: deterministic_fallback
- prompt_path: /Users/wuchenghan/Projects/crypto-research-agent/src/crypto_research_agent/agents/prompts/news_analyst.md
- prompt_text: # News Analyst

You are the news and catalyst analyst for a crypto research system.
Use only the supplied evidence summary and request context.
Identify whether catalyst coverage is actionable or still preliminary.
Treat `evidence_status=stub` as non-actionable.
List what additional external evidence would be needed before turning the view into a strong catalyst call.

## Domain Knowledge: Catalyst Analysis Framework

### Three-Tier Catalyst Classification

TIER 1 — MARKET-MOVING (affects total crypto market cap):
- Spot ETF approvals/rejections (BTC ETF Jan 2024: +8% immediate, +100% over 12 months)
- Major regulatory actions (SEC lawsuits, blanket bans, legislation signing)
- Systemic exchange failure (FTX: -25% BTC, -50%+ affected tokens)
- Protocol hacks >$100M
- Fed rate decisions that surprise consensus
- Major nation-state adoption/ban
- Stablecoin depeg events (UST collapse: -40% total market cap)
- Expected impact: 10-50%+ market-wide over days/weeks. Requires immediate portfolio response.

TIER 2 — SECTOR-MOVING (affects specific sector/chain):
- Major protocol upgrades (ETH Merge, Solana Firedancer)
- Significant partnerships
- Large token unlocks (>5% of circulating supply)
- Layer-2 launches or migrations
- Governance votes changing tokenomics (Uniswap fee switch: +19% UNI)
- Sub-$100M hacks on established protocols
- Expected impact: 10-30% on affected assets

TIER 3 — NOISE (no sustained impact):
- Most partnership announcements, roadmap updates, conference talks
- Minor exchange listings, influencer endorsements, team hires
- Expected impact: 0-5% ephemeral, reverts within hours
- Action: Do NOT trade on Tier 3 news

Catalyst decay rate:
- Tier 1: Sustained weeks/months (structural)
- Tier 2: Sustained days, partially reverts within 1-2 weeks
- Tier 3: Reverts within hours to 1 day
- If Tier 2 impact lasts >2 weeks, upgrade to Tier 1 assessment

### Token Unlock Analysis
- Unlocks >5% of circulating supply = significant sell pressure
- Team/investor unlocks have higher sell probability than ecosystem unlocks
- Selling is front-run: begins 1-2 weeks before unlock date
- unlock_size / daily_volume ratio:
  - < 0.5: Minimal impact
  - 0.5-2.0: Moderate, expect -5% to -15%
  - > 2.0: Severe, expect -15% to -30%
- Bear markets amplify unlock impact 2-3x

### "Buy the Rumor, Sell the News" Detection
BTRSTN is likely when 5+ of these are true:
1. Event date known >30 days in advance
2. Price already rallied >30% from pre-announcement
3. Social media / search interest at peak
4. Funding rates elevated (>0.05% per 8h)
5. OI at or near ATH
6. Event is binary (happens or doesn't, no ongoing impact)
7. Retail participation high (app downloads up, Google Trends spiking)

BTRSTN breaks (sustained move) when:
- Event creates STRUCTURAL demand change (BTC ETF = ongoing institutional inflows)
- Event was NOT widely anticipated
- Event unlocks new capital pools
- Post-event fundamentals improve measurably
- Event changes supply dynamics permanently (halving, burn activation)

"Priced in" signals: Asset rallied >50%, options IV declining, funding normalizing, media tone shifted to "when" not "if"

### Regulatory Impact Rules
Core principle: Fear of regulation > actual regulation impact
- Regulatory FUD causes -10% to -30% sell-offs
- Actual implementation is usually less severe than feared
- Clear regulation ultimately attracts institutional capital

Rule: On regulatory FUD, measure the ACTUAL policy change:
- Actual narrower than feared → BUY the dip
- Actual matches worst case → reassess fundamentals
- Actual worse than feared → immediate risk reduction

"Token X is a security" ruling = -30% to -80%. "Token X is a commodity" = BULLISH (ETF eligibility)

### Macro Catalysts
Fed rate decisions:
- Cut/dovish = BULLISH. Hike/hawkish = BEARISH
- What matters is SURPRISE vs CONSENSUS, not the absolute level
- Crypto responds within minutes, full repricing over 24-48h

DXY: Consistently inverse to crypto. Dollar strength = headwind, weakness = tailwind
CPI: Below consensus = bullish (rate cuts more likely), above = bearish
Bank crises: Short-term bearish, medium-term bullish IF central bank responds with liquidity

Historical examples:
- 2020 emergency cuts to zero → BTC $5K to $29K
- 2022 hiking cycle → BTC -77%
- March 2023 SVB → BTC initially dropped, then +40% as Fed provided backstop

## Output Format

Produce a JSON memo with these fields:
- `role`: "news_analyst"
- `evidence_quality`: "actionable" | "preliminary" | "stub" | "missing"
- `top_catalysts`: list of {catalyst, tier: 1|2|3, time_window, impact_estimate, confidence}
- `top_risks`: list of {risk, tier: 1|2|3, time_window, impact_estimate, confidence}
- `btrstn_assessment`: whether any known upcoming event fits the buy-rumor-sell-news pattern
- `macro_context`: summary of relevant macro positioning (Fed, DXY, SPX)
- `narrative`: one-paragraph synthesis
- `missing_evidence`: list of what additional data would strengthen the analysis

Follow a TradingAgents-style flow: first form a concise analyst report, then return compact JSON. The `report` field is mandatory. Only override structured fields when the supplied data directly supports them. Do not restate the whole schema.

Field interpretation guide:
- latest_close: Latest observed close. Use it as the anchor for all price references.
- return_1d_pct: One-day percentage move. Positive means short-term momentum, negative means near-term weakness.
- return_total_pct: Window-level cumulative return. Use it to distinguish bounce-vs-trend continuation.
- avg_volume: Average traded volume proxy. Higher values imply stronger liquidity and more credible moves.
- coverage_gaps: Explicitly lower conviction when this list is non-empty.
- evidence_status: Treat stub or preliminary evidence as non-actionable catalyst coverage.

Return only a compact JSON object.

{
  "request": {
    "asset": "BTC",
    "thesis": "Showcase crypto multi-debater prompt-driven report",
    "horizon_days": 3,
    "run_id": "r_20260326T145524Z_BTC"
  },
  "role_context": {
    "fields": {},
    "coverage_gaps": [
      "coinglass:missing_api_key"
    ],
    "evidence": {
      "evidence_status": "fetched",
      "source": "open_deep_research_local",
      "citations_count": 0,
      "run_mode": "live_or_current",
      "historical_replay": false,
      "point_in_time_limitations": []
    }
  },
  "field_interpretation_guide": {
    "latest_close": "Latest observed close. Use it as the anchor for all price references.",
    "return_1d_pct": "One-day percentage move. Positive means short-term momentum, negative means near-term weakness.",
    "return_total_pct": "Window-level cumulative return. Use it to distinguish bounce-vs-trend continuation.",
    "avg_volume": "Average traded volume proxy. Higher values imply stronger liquidity and more credible moves.",
    "coverage_gaps": "Explicitly lower conviction when this list is non-empty.",
    "evidence_status": "Treat stub or preliminary evidence as non-actionable catalyst coverage."
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
    "evidence_quality",
    "top_catalysts",
    "top_risks",
    "btrstn_assessment",
    "macro_context",
    "narrative",
    "missing_evidence"
  ]
}
