#!/bin/bash
# Daily BTC research run + commit to GitHub.
# Triggered by ~/Library/LaunchAgents/com.cwu339.crypto-daily.plist at 22:00 local.

set -e
cd /Users/wuchenghan/Projects/crypto-multi-debater

# 1. Pull latest (in case GH Actions also pushed something)
git pull --ff-only --rebase=false 2>&1 || echo "git pull failed, continuing"

# 2. Load env vars
set -a
source .env
set +a
export CRYPTO_RESEARCH_ANALYSIS_PROVIDER=openai
export ODR_LOCAL_PROJECT_ROOT=/Users/wuchenghan/Projects/crypto-multi-debater/external/open_deep_research

# 3. Run research
DATE=$(date -u +%Y-%m-%d)
ASSET="BTC"
HORIZON="7"
OUT_DIR="daily_runs/$DATE"

mkdir -p "$OUT_DIR"
.venv/bin/python -m crypto_research_agent.cli run \
  --asset "$ASSET" --horizon-days "$HORIZON" \
  --thesis "Automated daily research for $ASSET on $DATE" \
  --output-dir "$OUT_DIR"

# 4. Curate artifacts to docs/daily/
CURATED="docs/daily/$DATE"
mkdir -p "$CURATED"
find "$OUT_DIR/research_cards" -name "*.md" -exec cp {} "$CURATED/${ASSET}_card.md" \;
find "$OUT_DIR/runs" -name "summary.json" -path "*/features/*" -exec cp {} "$CURATED/${ASSET}_features.json" \;
find "$OUT_DIR/runs" -name "final_arbiter.md" -exec cp {} "$CURATED/${ASSET}_arbiter.md" \;
find "$OUT_DIR/runs" -name "final_arbiter.json" -exec cp {} "$CURATED/${ASSET}_arbiter.json" \;

# 5. Update README badge
ARBITER_PATH="$CURATED/${ASSET}_arbiter.json" \
  README_DATE="$DATE" README_ASSET="$ASSET" README_HORIZON="$HORIZON" \
  python3 .github/scripts/update_readme_badge.py

# 6. Commit & push
git add docs/daily/ README.md
if git diff --cached --quiet; then
  echo "$(date) - no changes to commit"
else
  git commit -m "daily: $ASSET $DATE (local mac)"
  git push
fi

echo "$(date) - done"
