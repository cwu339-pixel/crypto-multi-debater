from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable
from urllib.request import Request, urlopen

from crypto_research_agent.schemas import ResearchRequest


def fetch_evidence_markdown(
    *,
    base_url: str,
    request: ResearchRequest,
    http_post: Callable[[str, dict[str, Any], dict[str, str]], dict[str, Any]] | None = None,
) -> str:
    post = http_post or _default_http_post
    payload = {
        "asset": request.asset,
        "thesis": request.thesis,
        "horizon_days": request.horizon_days,
        "run_id": request.run_id,
        "as_of_utc": request.as_of_utc.isoformat(),
    }
    response = post(
        f"{base_url.rstrip('/')}/research",
        payload,
        {"Content-Type": "application/json"},
    )
    return str(response["markdown"])


def fetch_evidence_markdown_local(
    *,
    request: ResearchRequest,
    project_root: str | Path | None = None,
    graph_runner: Callable[[ResearchRequest, Path], str] | None = None,
) -> str:
    root = _resolve_local_project_root(project_root)
    runner = graph_runner or _default_local_graph_runner
    return runner(request, root)


def fetch_evidence_markdown_isolated(
    *,
    request: ResearchRequest,
    base_url: str | None = None,
    project_root: str | Path | None = None,
    timeout_seconds: int | None = None,
) -> tuple[str, str]:
    effective_timeout = timeout_seconds or int(os.getenv("EVIDENCE_TIMEOUT_SECONDS", "50"))
    payload = {
        "request": {
            "asset": request.asset,
            "thesis": request.thesis,
            "horizon_days": request.horizon_days,
            "run_id": request.run_id,
            "as_of_utc": request.as_of_utc.isoformat(),
        },
        "base_url": base_url,
        "project_root": str(project_root) if project_root is not None else None,
    }
    try:
        child = subprocess.run(
            [sys.executable, "-c", _ISOLATED_EVIDENCE_RUNNER],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            timeout=effective_timeout,
            env=os.environ.copy(),
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"evidence subprocess timed out after {effective_timeout}s"
        ) from exc
    if child.returncode != 0:
        stderr = child.stderr.strip()[:500]
        raise RuntimeError(f"evidence subprocess failed: {stderr or 'unknown error'}")
    result = json.loads(child.stdout)
    markdown = str(result.get("markdown", "")).strip()
    if not markdown:
        raise ValueError("evidence subprocess returned empty markdown")
    return markdown, str(result.get("source", "unknown"))


def _default_http_post(url: str, payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    timeout_seconds = int(os.getenv("ODR_HTTP_TIMEOUT_SECONDS", "30"))
    with urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310
        return json.loads(response.read().decode("utf-8"))


def _resolve_local_project_root(project_root: str | Path | None) -> Path:
    if project_root is not None:
        return Path(project_root)

    env_root = os.getenv("ODR_LOCAL_PROJECT_ROOT")
    if env_root:
        return Path(env_root)

    return Path(__file__).resolve().parents[3] / "external" / "open_deep_research"


def _default_local_graph_runner(request: ResearchRequest, project_root: Path) -> str:
    if not project_root.exists():
        raise FileNotFoundError(f"open_deep_research checkout not found: {project_root}")

    source_root = project_root / "src"
    prompt = _build_local_research_prompt(request)
    timeout_seconds = int(os.getenv("ODR_TIMEOUT_SECONDS", "45"))
    max_retries = int(os.getenv("ODR_MAX_RETRIES", "1"))
    config = {
        "configurable": {
            "allow_clarification": False,
            "search_api": os.getenv("ODR_SEARCH_API", "openai"),
            "research_model": os.getenv("ODR_RESEARCH_MODEL", "openai:gpt-4.1-mini"),
            "summarization_model": os.getenv("ODR_SUMMARIZATION_MODEL", "openai:gpt-4.1-mini"),
            "compression_model": os.getenv("ODR_COMPRESSION_MODEL", "openai:gpt-4.1-mini"),
            "final_report_model": os.getenv("ODR_FINAL_REPORT_MODEL", "openai:gpt-4.1-mini"),
            "max_concurrent_research_units": int(os.getenv("ODR_MAX_CONCURRENT_RESEARCH_UNITS", "1")),
            "max_researcher_iterations": int(os.getenv("ODR_MAX_RESEARCHER_ITERATIONS", "1")),
            "max_react_tool_calls": int(os.getenv("ODR_MAX_REACT_TOOL_CALLS", "1")),
        }
    }
    payload = {
        "source_root": str(source_root),
        "prompt": prompt,
        "config": config,
        "timeout_seconds": timeout_seconds,
    }
    last_exc: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            child = subprocess.run(
                [sys.executable, "-c", _LOCAL_ODR_RUNNER],
                input=json.dumps(payload),
                text=True,
                capture_output=True,
                timeout=timeout_seconds + 5,
                env=os.environ.copy(),
            )
        except subprocess.TimeoutExpired as exc:
            last_exc = RuntimeError(
                f"open_deep_research subprocess timed out after {timeout_seconds + 5}s on attempt {attempt + 1}"
            )
            if attempt >= max_retries:
                raise last_exc
            continue

        if child.returncode != 0:
            stderr = child.stderr.strip()[:500]
            last_exc = RuntimeError(
                f"open_deep_research subprocess failed on attempt {attempt + 1}: {stderr or 'unknown error'}"
            )
            if attempt >= max_retries:
                raise last_exc
            continue

        result = json.loads(child.stdout)
        final_report = str(result.get("final_report", "")).strip()
        if final_report:
            return final_report
        last_exc = ValueError(f"open_deep_research returned an empty final_report on attempt {attempt + 1}")
        if attempt >= max_retries:
            raise last_exc

    assert last_exc is not None
    raise last_exc


def _build_local_research_prompt(request: ResearchRequest) -> str:
    return (
        f"Research the crypto asset {request.asset} for a {request.horizon_days}-day horizon.\n\n"
        f"Primary thesis to evaluate: {request.thesis}\n\n"
        "Produce a concise markdown research brief for an internal crypto research system. Focus on:\n"
        "1. Near-term catalysts and bearish/bullish drivers.\n"
        "2. Market structure, macro or regulatory events, token-specific or protocol-specific risks.\n"
        "3. Actionable evidence only; avoid generic education.\n"
        "4. Include source links inline in markdown where possible.\n"
        "5. End with a short section called 'Bottom Line' with 3-5 bullets.\n"
    )


_LOCAL_ODR_RUNNER = r"""
import asyncio
import json
import sys
from pathlib import Path

payload = json.loads(sys.stdin.read())
source_root = Path(payload["source_root"])
if str(source_root) not in sys.path:
    sys.path.insert(0, str(source_root))

from langchain_core.messages import HumanMessage
from open_deep_research.deep_researcher import deep_researcher

prompt = payload["prompt"]
config = payload["config"]
timeout_seconds = int(payload["timeout_seconds"])

async def _run():
    return await asyncio.wait_for(
        deep_researcher.ainvoke({"messages": [HumanMessage(content=prompt)]}, config=config),
        timeout=timeout_seconds,
    )

result = asyncio.run(_run())
sys.stdout.write(json.dumps({"final_report": str(result.get("final_report", ""))}))
"""


_ISOLATED_EVIDENCE_RUNNER = r"""
import json
from datetime import datetime
from pathlib import Path

from crypto_research_agent.research.open_deep_research_client import (
    fetch_evidence_markdown,
    fetch_evidence_markdown_local,
)
from crypto_research_agent.schemas import ResearchRequest

payload = json.loads(input())
request_payload = payload["request"]
request = ResearchRequest(
    asset=request_payload["asset"],
    thesis=request_payload["thesis"],
    horizon_days=int(request_payload["horizon_days"]),
    run_id=request_payload["run_id"],
    as_of_utc=datetime.fromisoformat(request_payload["as_of_utc"]),
)
base_url = payload.get("base_url")
project_root = payload.get("project_root")
if base_url:
    markdown = fetch_evidence_markdown(base_url=base_url, request=request)
    source = "open_deep_research_http"
else:
    markdown = fetch_evidence_markdown_local(
        request=request,
        project_root=Path(project_root) if project_root else None,
    )
    source = "open_deep_research_local"
print(json.dumps({"markdown": markdown, "source": source}))
"""
