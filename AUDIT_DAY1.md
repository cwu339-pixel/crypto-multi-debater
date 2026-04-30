# Day 1 Audit: crypto-multi-debater

Date: 2026-04-19
Reviewer: Claude (outside-in, simulating a JD3 interviewer opening the repo for the first time)

Time-boxed: 45 min read
Scope: only the GitHub-visible surface (README, docs/, tmp_showcase/). Not a code review.

---

## TL;DR

**The project is much stronger than you think.** The positioning ("Court-Style Debate-Driven Crypto Research Product") is the best framing I've seen in any of your work. The system is real, the outputs are substantive, and a skilled reader would see an end-to-end multi-agent system with auditable artifacts.

**But the packaging is leaking signal in ~10 specific places.** None are hard to fix. Most are 5-30 minute edits. Fixing them will meaningfully raise the perceived quality tier from "promising side project" to "portfolio-grade work."

**Recommendation**: spend the 8-day window (4/27-5/3) doing targeted polish, not a rewrite. The substance is there. Stop treating this like a work-in-progress.

---

## Strengths (don't touch these)

1. **Court metaphor is load-bearing and distinctive.** "Analyst stack → bull/bear debate → risk debate → final arbiter" mirrors how real investment committees work. This is differentiation that generic "CrewAI demo" repos don't have.

2. **Scorecard separation is sophisticated.** Action Score vs. Confidence vs. Data Quality being three distinct axes shows mature thinking. Most LLM projects collapse these into a single vague "confidence."

3. **Real artifacts, not chat logs.** `runs/` contains `run.json`, `call_log.jsonl`, research cards. This proves reproducibility and auditability, which is exactly what JD3 companies care about.

4. **Data source choices match positioning.** OpenBB + DefiLlama + open_deep_research is a crypto-native stack, not generic finance. The README calls this out explicitly — good.

5. **Current Limitations section is honest.** Listing gaps (CoinGlass missing, replay not point-in-time, tone not PM-grade) signals engineering maturity. Don't remove this.

---

## Weaknesses (ranked by severity)

### P0 — blocks credibility on first scan

**W1. "tmp_showcase/" as the homepage showcase path.**
The README's "Best Showcase Right Now" section links to `tmp_showcase/runs/...`. A sophisticated reader sees `tmp_` and assumes "this is a temporary folder the author forgot to clean up."
- **Fix**: rename `tmp_showcase/` → `showcase/` and update README links. 5 min.

**W2. H1 header appears twice.**
Line 3: `# Crypto Multi-Debater`
Line 16: `# Crypto Multi-Debater: Court-Style Crypto Research Product`
GitHub renders both. Looks like you forgot to delete one.
- **Fix**: delete line 16, merge subtitle into line 5 area or drop. 1 min.

**W3. Literal placeholder in install instructions.**
```bash
git clone <your-repo-url>
```
This is the sentence every reader copies first. Leaving `<your-repo-url>` signals "never tested from a fresh clone."
- **Fix**: replace with `git clone https://github.com/cwu339-pixel/crypto-multi-debater.git`. 30 sec.

**W4. Showcase run is 18 days stale.**
README bullet says "[2026-04] Homepage showcase refreshed to today's live BTC debate report" but the referenced run is `r_20260401T031358Z_BTC` (April 1). You have `tmp_today_btc_2026_04_13/` sitting there. The "today" in the news bullet is false as of reading.
- **Fix**: either regenerate showcase from `tmp_today_btc_2026_04_13/` (or a fresh run) and update link, OR change the news bullet to match reality. 15 min.

### P1 — missing signals that sophisticated readers expect

**W5. No architecture diagram.**
Reader has to construct the flow mentally from prose. One Mermaid or Excalidraw diagram showing `thesis → data → evidence → analysts → debate → risk → arbiter → report` would let a busy interviewer understand the system in 10 seconds.
- **Fix**: embed a Mermaid diagram in the "Courtroom Structure" section. 45 min.

**W6. No visual of actual output.**
Reader sees 230 lines of prose, zero screenshots. A single image of the rendered research card (or the call_log timeline) would make the work feel real.
- **Fix**: add 1-2 screenshots to "Best Showcase Right Now" section. 20 min.

**W7. No "Why not CrewAI / AutoGen / LangGraph" section.**
You compete with these frameworks for attention. Interviewers will ask "why didn't you just use CrewAI?" You need a pre-written answer in the README.
- **Fix**: add a "Why Custom, Not CrewAI" section with 3-4 bullet points on why you needed sequential bull/bear + court structure + auditable artifacts specifically. 30 min.

**W8. "Inspired By" wording is too apologetic.**
> "The contribution here is not inventing every component from scratch."
This is technically honest but tonally submissive. A reader skimming ends the README on a self-deprecating note.
- **Fix**: rewrite as claim-forward: "**My contribution is the court-style adaptation**: the bull/bear sequential debate, three-axis scorecard, and auditable research card format are designed for crypto research specifically, not inherited from TradingAgents." 10 min.

### P2 — polish that compounds

**W9. Git history is 2 commits.**
Visible at `github.com/.../commits/main`. Signals "I force-pushed this after cleanup." Not fatal, but a tell.
- **Fix**: going forward, make real commits. Don't rewrite history now — looks worse if you fake it. Accept the cost and move on.

**W10. No cost/ops section.**
Every LLM-system interviewer will ask "how much does one run cost?" Not in README.
- **Fix**: add 2 lines to "Current Live Capabilities": "A full run = ~8 LLM calls, ~$0.X with gpt-X, completes in X min." 10 min.

**W11. "News" section as opener is noise.**
First-time reader hits "News" before understanding what the project is. Move Overview up.
- **Fix**: reorder: Overview → Positioning → Courtroom Structure → News (or drop News entirely). 5 min.

**W12. Report body itself shows AI-generation tells.**
The showcase card has `Judge's Ruling > Ruling` and `Judge's Ruling > Thesis` as **word-for-word identical paragraphs**. Reader spots this in 3 seconds. Suggests the final arbiter prompt isn't deduplicating outputs.
- **Fix**: this is a **code fix**, not README. Arbiter should separate "Ruling" (one-sentence verdict) from "Thesis" (multi-factor rationale). 1-2 hours code work if you choose to do it; skip if time-bound.

---

## What to do in the 8-day window

Priority order, deliverable-first:

| Day | Task | Time | Source |
|-----|------|------|--------|
| 1 | Fix W1, W2, W3, W11 (trivial cleanups) | 30 min | This audit |
| 2 | Regenerate showcase from fresh run, fix W4 | 45 min | W4 |
| 3 | Architecture diagram (Mermaid), fix W5 | 45 min | W5 |
| 4 | Screenshots + "Why not CrewAI" section, fix W6+W7 | 1.5 hr | W6, W7 |
| 5 | Rewrite "Inspired By" tone, fix W8 | 15 min | W8 |
| 6 | Cost/ops section + 2-min Loom demo | 1.5 hr | W10 |
| 7 | Fix the W12 arbiter prompt bug (if time) | 2 hr | W12 |
| 8 | X thread + LinkedIn post + send to 3 startups | 2 hr | — |

Total: ~9 hours. Matches the original 10-hour budget.

**Drop W9 (git history)**. Not worth the cost of faking.
**Consider dropping W12** if interview prep eats time. It's a nice-to-have; the README fix is more urgent than the code fix.

---

## One meta-observation

The repo has a pattern: **substance is 80% there, presentation is 40% there**. This is the opposite of most junior portfolio projects (where presentation is 90%, substance is 20%).

For JD3 interviewers, this pattern signals: "builder, not marketer." That's the RIGHT side to err on, but you're leaving free credibility on the table by not fixing the trivial packaging issues.

**Fix the packaging. Don't build anything new.**

---

## Immediate next action (when you resume 4/27)

Start with the 30-minute trivial cleanups: W1, W2, W3, W11. These alone will raise perceived quality noticeably. You'll feel momentum. Everything else builds from there.
