from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import threading
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from crypto_research_agent.data_layer.binance import fetch_binance_data
from crypto_research_agent.data_layer.coinglass import fetch_coinglass_data
from crypto_research_agent.data_layer.defillama import fetch_defillama_data
from crypto_research_agent.data_layer.openbb_layer import AdapterOutcome, fetch_openbb_data
from crypto_research_agent.data_layer.provenance import append_provenance_record
from crypto_research_agent.data_layer.snapshot import write_snapshot
from crypto_research_agent.schemas import RawDataBundle, ResearchRequest, SourceResult


def collect_market_data(
    *,
    request: ResearchRequest,
    sources_config: dict[str, Any],
    output_root: Path,
    http_get: Callable[..., Any] | None = None,
    openbb_client: Any | None = None,
) -> RawDataBundle:
    http_client = http_get or default_http_get
    use_isolated_adapters = http_get is None and openbb_client is None
    run_root = Path(output_root) / "runs" / request.run_id
    run_root.mkdir(parents=True, exist_ok=True)
    provenance_path = run_root / "provenance.jsonl"
    provenance_path.unlink(missing_ok=True)

    configured_sources = sources_config.get("sources", {})
    source_results: dict[str, SourceResult] = {}
    coverage_gaps: list[str] = []

    adapter_calls = {
        "openbb": (
            configured_sources.get("openbb", {}),
            lambda: fetch_openbb_data(
                request,
                configured_sources.get("openbb", {}),
                openbb_client=openbb_client,
            ),
        ),
        "defillama": (
            configured_sources.get("defillama", {}),
            lambda: fetch_defillama_data(
                request,
                configured_sources.get("defillama", {}),
                http_get=http_client,
            ),
        ),
        "coinglass": (
            configured_sources.get("coinglass", {}),
            lambda: fetch_coinglass_data(
                request,
                configured_sources.get("coinglass", {}),
                http_get=http_client,
            ),
        ),
        "binance": (
            configured_sources.get("binance", {}),
            lambda: fetch_binance_data(
                request,
                configured_sources.get("binance", {}),
                http_get=http_client,
            ),
        ),
    }

    for source, (source_config, adapter_call) in adapter_calls.items():
        try:
            if use_isolated_adapters:
                outcome = _run_adapter_isolated(
                    source=source,
                    request=request,
                    source_config=source_config,
                )
            else:
                adapter_timeout = _env_int("ADAPTER_TIMEOUT_SECONDS", 45)
                with _timeout_guard(adapter_timeout):
                    outcome = adapter_call()
        except Exception as exc:  # noqa: BLE001
            outcome = AdapterOutcome(
                status="error",
                reason=f"exception:{type(exc).__name__}",
                payloads={},
                request_metadata={"exception_message": str(exc)},
                config_metadata={key: value for key, value in source_config.items()},
            )

        source_results[source] = _materialize_outcome(
            source=source,
            outcome=outcome,
            run_root=run_root,
        )
        append_provenance_record(
            provenance_path=provenance_path,
            source=source,
            outcome=outcome,
            result=source_results[source],
        )
        if outcome.status in {"skipped", "error"} and outcome.reason:
            coverage_gaps.append(f"{source}:{outcome.reason}")

    return RawDataBundle(
        run_id=request.run_id,
        source_results=source_results,
        coverage_gaps=coverage_gaps,
        provenance_path=provenance_path,
    )


def default_http_get(url: str, *, headers: dict[str, str], params: dict[str, Any]) -> Any:
    query_string = urlencode(params)
    final_url = f"{url}?{query_string}" if query_string else url
    request = Request(final_url, headers=headers)
    timeout_seconds = _env_int("DATA_SOURCE_TIMEOUT_SECONDS", 20)
    with urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310
        return json.loads(response.read().decode("utf-8"))


def _run_adapter_isolated(
    *,
    source: str,
    request: ResearchRequest,
    source_config: dict[str, Any],
) -> AdapterOutcome:
    adapter_timeout = _env_int("ADAPTER_TIMEOUT_SECONDS", 45)
    payload = {
        "source": source,
        "request": {
            "asset": request.asset,
            "thesis": request.thesis,
            "horizon_days": request.horizon_days,
            "run_id": request.run_id,
            "as_of_utc": request.as_of_utc.isoformat(),
        },
        "source_config": source_config,
    }
    try:
        child = subprocess.run(
            [sys.executable, "-c", _ADAPTER_RUNNER],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            timeout=adapter_timeout,
            env=os.environ.copy(),
        )
    except subprocess.TimeoutExpired as exc:
        raise TimeoutError(f"adapter timed out after {adapter_timeout}s") from exc

    if child.returncode != 0:
        stderr = child.stderr.strip()[:500]
        raise RuntimeError(f"adapter subprocess failed: {stderr or 'unknown error'}")

    result = json.loads(child.stdout)
    return AdapterOutcome(
        status=str(result.get("status")),
        reason=result.get("reason"),
        payloads=result.get("payloads", {}),
        request_metadata=result.get("request_metadata", {}),
        config_metadata=result.get("config_metadata", {}),
    )


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


@contextmanager
def _timeout_guard(seconds: int):
    if seconds <= 0 or threading.current_thread() is not threading.main_thread() or not hasattr(signal, "SIGALRM"):
        yield
        return

    def _handle_timeout(signum, frame):  # noqa: ARG001
        raise TimeoutError(f"adapter timed out after {seconds}s")

    previous_handler = signal.getsignal(signal.SIGALRM)
    signal.signal(signal.SIGALRM, _handle_timeout)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)


def _materialize_outcome(
    *,
    source: str,
    outcome: AdapterOutcome,
    run_root: Path,
) -> SourceResult:
    if outcome.status != "fetched":
        return SourceResult(
            source=source,
            status=outcome.status,
            reason=outcome.reason,
            artifact_paths=[],
        )

    artifact_paths = [
        write_snapshot(
            payload,
            run_root=run_root,
            source=source,
            artifact_name=artifact_name,
        )
        for artifact_name, payload in outcome.payloads.items()
    ]
    return SourceResult(
        source=source,
        status="fetched",
        reason=None,
        artifact_paths=artifact_paths,
    )


_ADAPTER_RUNNER = r"""
import json
from datetime import datetime

from crypto_research_agent.data_layer.binance import fetch_binance_data
from crypto_research_agent.data_layer.coinglass import fetch_coinglass_data
from crypto_research_agent.data_layer.defillama import fetch_defillama_data
from crypto_research_agent.data_layer.openbb_layer import fetch_openbb_data
from crypto_research_agent.data_layer.service import default_http_get
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
source = payload["source"]
config = payload.get("source_config", {})

if source == "openbb":
    outcome = fetch_openbb_data(request, config)
elif source == "defillama":
    outcome = fetch_defillama_data(request, config, http_get=default_http_get)
elif source == "coinglass":
    outcome = fetch_coinglass_data(request, config, http_get=default_http_get)
elif source == "binance":
    outcome = fetch_binance_data(request, config, http_get=default_http_get)
else:
    raise ValueError(f"unknown adapter source: {source}")

print(json.dumps({
    "status": outcome.status,
    "reason": outcome.reason,
    "payloads": outcome.payloads,
    "request_metadata": outcome.request_metadata,
    "config_metadata": outcome.config_metadata,
}, default=str))
"""
