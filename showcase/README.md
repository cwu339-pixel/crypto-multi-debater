# Showcase Artifacts

This directory contains committed example outputs from selected research runs.

## What belongs here

- representative `run.json` payloads
- rendered research cards
- agent memos and call logs that help explain the full workflow
- review artifacts that demonstrate the post-horizon review loop

## Why these files are committed

The repo homepage and demo-case docs link to a small number of concrete artifacts so readers can inspect the system end to end without running the full pipeline first.

## Boundary

Files under `tmp_showcase/` are generated outputs for inspection, not the primary maintained source of the project. Core implementation changes should usually happen in `src/`, `tests/`, `config/`, and `docs/`.

## Update guidance

- Keep showcase updates scoped to a specific run or narrative refresh
- Avoid mixing large showcase refreshes with unrelated source-code changes
- Prefer linking to a small number of representative runs instead of committing every experiment
