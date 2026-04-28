"""Build a Farcaster cast (≤320 chars) from the latest final_arbiter ruling.

Resolves the latest `docs/daily/<date>/<asset>_arbiter.json` if available; otherwise
parses the structured fields out of the matching `_arbiter.md`. Writes the cast text
to `cast.txt` and echoes it to stdout.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CAST_LIMIT = 320
REPO_URL = "github.com/cwu339-pixel/crypto-multi-debater"


def _latest_arbiter_dir() -> Path:
    daily_root = Path("docs/daily")
    if not daily_root.is_dir():
        sys.exit("docs/daily/ does not exist")
    candidates = sorted(
        (p for p in daily_root.iterdir() if p.is_dir()),
        reverse=True,
    )
    for d in candidates:
        if any(d.glob("*_arbiter.md")):
            return d
    sys.exit("no arbiter file found in docs/daily/*/")


def _load_arbiter(daily_dir: Path) -> tuple[dict, str, str]:
    md = next(daily_dir.glob("*_arbiter.md"))
    asset = md.stem.split("_")[0]
    date = daily_dir.name
    json_path = md.with_suffix(".json")
    if json_path.exists():
        return json.loads(json_path.read_text()), asset, date

    # Fallback: parse the structured md (key: value lines)
    parsed: dict = {}
    for line in md.read_text().splitlines():
        m = re.match(r"^- (\w+): (.+)$", line)
        if not m:
            continue
        key, raw = m.group(1), m.group(2).strip()
        if raw.startswith("{") or raw.startswith("["):
            try:
                parsed[key] = json.loads(raw.replace("'", '"'))
                continue
            except Exception:
                pass
        parsed[key] = raw
    return parsed, asset, date


def _byte_len(text: str) -> int:
    return len(text.encode("utf-8"))


def _truncate(text: str, byte_limit: int) -> str:
    """Trim *text* so it fits within *byte_limit* UTF-8 bytes, ending with `…`."""
    text = text.strip()
    if _byte_len(text) <= byte_limit:
        return text
    ellipsis = "…"
    target = byte_limit - _byte_len(ellipsis)
    encoded = text.encode("utf-8")[:target]
    # Avoid splitting a multi-byte codepoint
    while encoded and (encoded[-1] & 0b11000000) == 0b10000000:
        encoded = encoded[:-1]
    truncated = encoded.decode("utf-8", errors="ignore").rstrip()
    return truncated + ellipsis


def build_cast() -> str:
    daily_dir = _latest_arbiter_dir()
    data, asset, date = _load_arbiter(daily_dir)

    decision = data.get("decision") if isinstance(data.get("decision"), dict) else {}
    action = (decision.get("action") or data.get("decision_label") or "n/a").upper()
    pos = decision.get("position_size") or "n/a"
    score = (data.get("scorecard") or {}).get("final_score") or (data.get("scorecard") or {}).get("action_score")

    # Prefer thesis (usually clean prose) over summary (sometimes a JSON-in-JSON dump)
    def _clean_prose(value: object) -> str:
        text = (value or "").strip() if isinstance(value, str) else ""
        if text.startswith("{") or text.startswith("["):
            return ""
        return text

    summary = (
        _clean_prose(data.get("thesis"))
        or _clean_prose(data.get("summary"))
        or _clean_prose(data.get("report"))
        or ""
    )

    # Pick first flip-up rule for a forward-looking signal
    flip_up = "n/a"
    for rule in data.get("flip_rules") or []:
        if not isinstance(rule, dict):
            continue
        blob = " ".join(str(v).lower() for v in rule.values())
        if any(k in blob for k in ("buy", "long", "upgrade", "bullish", "half-size")):
            flip_up = rule.get("condition", "")
            break

    header = f"📊 {asset} {date} · score {score}/100"
    verdict = f"Verdict: {action} · size: {pos}"
    flip_line = f"Flip ↑: {flip_up}" if flip_up != "n/a" else ""
    footer = f"Full ruling → {REPO_URL}"

    # Reserve room for the structural lines and join the thesis snippet last
    fixed = "\n".join(filter(None, [header, verdict, flip_line, "", footer]))
    budget = CAST_LIMIT - _byte_len(fixed) - 2  # 2 for the blank line around the thesis
    thesis_snippet = _truncate(summary, max(40, budget))

    cast = "\n".join(filter(None, [header, verdict, flip_line, "", thesis_snippet, "", footer]))
    return _truncate(cast, CAST_LIMIT)


def main() -> None:
    cast = build_cast()
    Path("cast.txt").write_text(cast)
    print(cast)
    print(f"\n--- length: {len(cast)} / {CAST_LIMIT} ---", file=sys.stderr)


if __name__ == "__main__":
    main()
