# Demo Case 3: Review Loop Example

## Goal

Show that the project does not stop at report generation. It can revisit a prior call and decide whether the decision was correct.

## Source Review

- Completed review: [`tmp_showcase/reviews/completed/r_20260326T145524Z_BTC.json`](../../tmp_showcase/reviews/completed/r_20260326T145524Z_BTC.json)
- Original run: [`tmp_showcase/runs/r_20260326T145524Z_BTC/run.json`](../../tmp_showcase/runs/r_20260326T145524Z_BTC/run.json)

## What Happened

- Initial decision: `avoid`
- Review result: `decision_correct = true`

## Why This Matters

Most multi-agent trading demos stop at “interesting output.” This project carries the process one step further:

- save the original decision
- wait for the horizon to pass
- fetch the realized outcome
- mark the call as right or wrong

That gives the system a real memory of performance instead of a pile of unreviewed memos.
