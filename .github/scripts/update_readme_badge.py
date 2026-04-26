"""Update the README last-run badge based on the final_arbiter ruling.

Reads the following env vars:
  ARBITER_PATH  - path to final_arbiter.json from the latest run
  README_DATE   - YYYY-MM-DD of the run
  README_ASSET  - asset symbol (e.g. BTC)
  README_HORIZON - horizon in days (e.g. 7)

Replaces the line beginning with `<!-- LAST_RUN -->` in README.md, or appends
one if it does not exist.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

MARKER = "<!-- LAST_RUN -->"
README = Path("README.md")


def _truncate(text: str, limit: int = 70) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def _flip_summary(flip_rules: list, direction: str) -> str:
    if not isinstance(flip_rules, list):
        return "n/a"
    keywords = {
        "up": ("buy", "long", "upgrade", "bullish"),
        "down": ("sell", "short", "exit", "bearish"),
    }[direction]
    for rule in flip_rules:
        if not isinstance(rule, dict):
            continue
        blob = " ".join(str(v).lower() for v in rule.values())
        if any(k in blob for k in keywords):
            return _truncate(rule.get("condition", ""))
    return "n/a"


def build_badge() -> str:
    arbiter_path = os.environ["ARBITER_PATH"]
    date = os.environ["README_DATE"]
    asset = os.environ["README_ASSET"]
    horizon = os.environ["README_HORIZON"]

    data = json.loads(Path(arbiter_path).read_text())
    decision = data.get("decision") if isinstance(data.get("decision"), dict) else {}
    action = decision.get("action") or data.get("decision_label") or "n/a"
    position = decision.get("position_size") or "n/a"
    flip_rules = data.get("flip_rules") or []
    flip_up = _flip_summary(flip_rules, "up")
    flip_down = _flip_summary(flip_rules, "down")

    return (
        f"{MARKER} _Last automated run: **{date}**_ · "
        f"**{asset} {horizon}d** → `{action}` · pos: `{position}` · "
        f"flip ↑: {flip_up} · flip ↓: {flip_down} · "
        f"[card](docs/daily/{date}/{asset}_card.md) · "
        f"[ruling](docs/daily/{date}/{asset}_arbiter.md)"
    )


def main() -> None:
    badge = build_badge()
    content = README.read_text() if README.exists() else ""
    pattern = re.compile(rf"^{re.escape(MARKER)}.*$", re.MULTILINE)
    if pattern.search(content):
        new_content = pattern.sub(badge, content)
    else:
        sep = "" if content.endswith("\n") else "\n"
        new_content = f"{content}{sep}\n{badge}\n"
    README.write_text(new_content)
    print(f"Updated README badge:\n  {badge}")


if __name__ == "__main__":
    main()
