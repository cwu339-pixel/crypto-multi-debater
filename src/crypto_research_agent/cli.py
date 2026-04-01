from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

# Load .env from project root if present
_env_file = Path(__file__).resolve().parents[2] / ".env"
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

from crypto_research_agent.config import default_sources_config_path, load_yaml_config
from crypto_research_agent.health.preflight import run_preflight
from crypto_research_agent.orchestration.graph import run_workflow
from crypto_research_agent.review_loop.service import run_pending_reviews
from crypto_research_agent.schemas import ResearchRequest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="crypto-multi-debater",
        description="Run crypto multi-debater research workflows.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a single research job.")
    run_parser.add_argument("--asset", required=True, help="Primary asset symbol.")
    run_parser.add_argument(
        "--horizon-days",
        required=True,
        type=int,
        help="Review horizon in calendar days.",
    )
    run_parser.add_argument("--thesis", required=True, help="Research thesis prompt.")
    run_parser.add_argument(
        "--as-of-date",
        help="Point-in-time date for the run in YYYY-MM-DD format. Price features are sliced to this date.",
    )
    run_parser.add_argument(
        "--sources-config",
        default=str(default_sources_config_path()),
        help="Path to the YAML source configuration.",
    )
    run_parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory where run artifacts should be written.",
    )
    run_parser.set_defaults(command="run")

    review_parser = subparsers.add_parser(
        "run-pending-reviews",
        help="Run all reviews whose due time has passed.",
    )
    review_parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory where review artifacts should be written.",
    )
    review_parser.set_defaults(command="run_pending_reviews")

    preflight_parser = subparsers.add_parser(
        "preflight",
        help="Run environment and dependency checks before a live research run.",
    )
    preflight_parser.set_defaults(command="preflight")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "run":
        request = ResearchRequest(
            asset=args.asset,
            thesis=args.thesis,
            horizon_days=args.horizon_days,
            run_id=_build_run_id(args.asset),
            as_of_utc=_parse_as_of_date(args.as_of_date),
        )
        sources_config = load_yaml_config(args.sources_config)
        result = run_workflow(
            request=request,
            sources_config=sources_config,
            output_root=Path(args.output_dir),
        )
        print(json.dumps(_jsonify(result)))
        return 0

    if args.command == "run_pending_reviews":
        result = run_pending_reviews(output_root=Path(args.output_dir))
        print(json.dumps(_jsonify(result)))
        return 0

    if args.command == "preflight":
        result = run_preflight()
        print(json.dumps(_jsonify(result)))
        return 0

    raise ValueError(f"Unsupported command: {args.command}")


def _build_run_id(asset: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"r_{timestamp}_{asset.upper()}"


def _parse_as_of_date(raw_date: str | None) -> datetime:
    if not raw_date:
        return datetime.now(timezone.utc)
    return datetime.fromisoformat(raw_date).replace(tzinfo=timezone.utc)


def _jsonify(value):
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {key: _jsonify(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonify(item) for item in value]
    return value


if __name__ == "__main__":
    raise SystemExit(main())
