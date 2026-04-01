from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from urllib import error, request

_PROVIDER_CONFIG = {
    "openai": ("https://api.openai.com/v1", "responses", "OPENAI_API_KEY"),
    "openrouter": ("https://openrouter.ai/api/v1", "chat_completions", "OPENROUTER_API_KEY"),
    "xai": ("https://api.x.ai/v1", "chat_completions", "XAI_API_KEY"),
    "ollama": ("http://localhost:11434/v1", "chat_completions", None),
}


class AnalysisProvider:
    name: str
    _last_meta: dict[str, object]

    def generate(
        self,
        *,
        role: str,
        prompt: str,
        fallback_memo: dict[str, object],
    ) -> dict[str, object]:
        raise NotImplementedError

    @property
    def last_meta(self) -> dict[str, object]:
        return getattr(self, "_last_meta", {})

    def _set_last_meta(self, **meta: object) -> None:
        object.__setattr__(self, "_last_meta", meta)


@dataclass(frozen=True)
class DeterministicAnalysisProvider(AnalysisProvider):
    name: str = "deterministic"

    def generate(
        self,
        *,
        role: str,
        prompt: str,
        fallback_memo: dict[str, object],
    ) -> dict[str, object]:
        self._set_last_meta(status="deterministic", reason="deterministic_provider")
        return {}


@dataclass(frozen=True)
class OpenAICompatibleAnalysisProvider(AnalysisProvider):
    api_key: str
    model: str
    base_url: str
    provider_name: str
    timeout_seconds: int = 30
    max_retries: int = 0

    def generate(
        self,
        *,
        role: str,
        prompt: str,
        fallback_memo: dict[str, object],
    ) -> dict[str, object]:
        endpoint_mode = _PROVIDER_CONFIG.get(self.provider_name, ("", "chat_completions", None))[1]
        payload, endpoint_path = _build_request_payload(
            provider_name=self.provider_name,
            model=self.model,
            prompt=prompt,
        )
        http_request = request.Request(
            url=f"{self.base_url.rstrip('/')}/{endpoint_path}",
            headers=_build_headers(self.api_key),
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
        )
        response_payload = None
        self._set_last_meta(status="started", provider=self.provider_name)
        for attempt in range(self.max_retries + 1):
            try:
                response_payload = _run_provider_request_isolated(
                    http_request=http_request,
                    timeout_seconds=self.timeout_seconds,
                )
                break
            except (ProviderRequestError, json.JSONDecodeError) as exc:
                print(f"[provider] {role} attempt {attempt} failed: {type(exc).__name__}: {exc}", file=sys.stderr)
                if isinstance(exc, ProviderRequestError) and exc.detail:
                    print(f"[provider] response detail: {exc.detail[:500]}", file=sys.stderr)
                if attempt >= self.max_retries:
                    self._set_last_meta(
                        status="error",
                        reason="provider_request_failed",
                        error_type=exc.error_type if isinstance(exc, ProviderRequestError) else type(exc).__name__,
                        detail=exc.detail if isinstance(exc, ProviderRequestError) else str(exc),
                        attempts=attempt + 1,
                    )
                    return {}
        if response_payload is None:
            self._set_last_meta(
                status="error",
                reason="empty_provider_response",
                error_type="EmptyResponse",
                detail="Provider returned no payload",
            )
            return {}

        if endpoint_mode == "responses":
            parsed, raw_text = _parse_responses_api_payload(response_payload)
        else:
            parsed, raw_text = _parse_chat_completions_payload(response_payload)
        if parsed:
            self._set_last_meta(
                status="ok",
                reason="parsed_response",
                keys=sorted(parsed.keys()),
            )
        else:
            self._set_last_meta(
                status="error",
                reason="response_not_json_object",
                error_type="ParseError",
                detail="Provider response could not be normalized into a JSON object",
                raw_text=raw_text,
            )
        return parsed

    @property
    def name(self) -> str:
        return self.provider_name


def default_analysis_provider() -> AnalysisProvider:
    provider_name = str(os.getenv("CRYPTO_RESEARCH_ANALYSIS_PROVIDER", "")).strip().lower()
    if not provider_name:
        if os.getenv("OPENAI_API_KEY"):
            provider_name = "openai"
        elif os.getenv("OPENROUTER_API_KEY"):
            provider_name = "openrouter"
        else:
            return DeterministicAnalysisProvider()
    if provider_name not in _PROVIDER_CONFIG:
        return DeterministicAnalysisProvider()

    api_key = os.getenv("ANALYSIS_API_KEY")
    model = os.getenv("ANALYSIS_MODEL")
    configured_base_url = os.getenv("ANALYSIS_API_BASE_URL")
    default_base_url, _, key_env = _PROVIDER_CONFIG[provider_name]
    if provider_name != "ollama" and not api_key:
        env_key = os.getenv(key_env, "")
        api_key = api_key or env_key
    if provider_name != "ollama" and not api_key:
        return DeterministicAnalysisProvider()
    if not model:
        model = _default_model_for_provider(provider_name)
    timeout_seconds = _env_int("ANALYSIS_TIMEOUT_SECONDS", 30)
    max_retries = _env_int("ANALYSIS_MAX_RETRIES", 0)
    return OpenAICompatibleAnalysisProvider(
        api_key=api_key or "ollama",
        model=model,
        base_url=configured_base_url or default_base_url,
        provider_name=provider_name,
        timeout_seconds=timeout_seconds,
        max_retries=max_retries,
    )


def _build_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


class ProviderRequestError(RuntimeError):
    def __init__(self, error_type: str, detail: str) -> None:
        super().__init__(f"{error_type}: {detail}")
        self.error_type = error_type
        self.detail = detail


_ISOLATED_PROVIDER_RUNNER = r"""
import json
import sys
from urllib import request, error

def build_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

def main() -> int:
    payload = json.loads(sys.stdin.read())
    http_request = request.Request(
        url=payload["url"],
        headers=build_headers(payload["api_key"]),
        data=json.dumps(payload["payload"]).encode("utf-8"),
        method="POST",
    )
    try:
        with request.urlopen(http_request, timeout=payload["timeout_seconds"]) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
        print(json.dumps({"response_payload": response_payload}, default=str))
        return 0
    except Exception as exc:
        detail = str(exc)
        if isinstance(exc, error.HTTPError):
            try:
                detail = exc.read().decode("utf-8", errors="replace")[:1000]
            except Exception:
                pass
        print(json.dumps({"error_type": type(exc).__name__, "detail": detail}, default=str))
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
"""


def _run_provider_request_isolated(
    *,
    http_request: request.Request,
    timeout_seconds: int,
) -> dict[str, object]:
    payload = {
        "url": http_request.full_url,
        "api_key": _extract_api_key(http_request),
        "payload": json.loads(http_request.data.decode("utf-8")),
        "timeout_seconds": timeout_seconds,
    }
    try:
        result = subprocess.run(
            [sys.executable, "-c", _ISOLATED_PROVIDER_RUNNER],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=timeout_seconds + 5,
            env=os.environ.copy(),
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise ProviderRequestError("TimeoutExpired", f"provider timed out after {timeout_seconds}s") from exc

    stdout = (result.stdout or "").strip()
    parsed = json.loads(stdout) if stdout else {}
    if result.returncode != 0:
        error_type = str(parsed.get("error_type") or "ProviderSubprocessError")
        detail = str(parsed.get("detail") or result.stderr or "provider subprocess failed")
        raise ProviderRequestError(error_type, detail)
    response_payload = parsed.get("response_payload")
    if not isinstance(response_payload, dict):
        raise ProviderRequestError("MalformedProviderResponse", "provider subprocess returned no response_payload")
    return response_payload


def _extract_api_key(http_request: request.Request) -> str:
    auth_header = http_request.headers.get("Authorization", "")
    if auth_header.lower().startswith("bearer "):
        return auth_header[7:]
    return auth_header


def _build_request_payload(*, provider_name: str, model: str, prompt: str) -> tuple[dict[str, object], str]:
    system_prompt = (
        "You are a senior crypto research analyst writing for an internal buy-side research system. "
        "Return only compact JSON. Be specific, evidence-based, and crypto-native. "
        "Do not restate every field mechanically. Synthesize them into a trading memo with a clear base case, "
        "what would change your mind, and explicit uncertainty when coverage is missing. "
        "Preserve provided role/title fields if present."
    )
    if provider_name == "openai":
        return (
            {
                "model": model,
                "input": [
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "input_text",
                                "text": system_prompt,
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [{"type": "input_text", "text": prompt}],
                    },
                ],
            },
            "responses",
        )
    return (
        {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
        },
        "chat/completions",
    )


def _parse_chat_completions_payload(response_payload: dict[str, object]) -> tuple[dict[str, object], str | None]:
    try:
        content = response_payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return {}, None
    if not isinstance(content, str):
        return {}, None
    parsed = _parse_json_object_from_text(content)
    return (parsed if isinstance(parsed, dict) else {}, content)


def _parse_responses_api_payload(response_payload: dict[str, object]) -> tuple[dict[str, object], str | None]:
    output = response_payload.get("output")
    if not isinstance(output, list):
        return {}, None
    content = None
    for item in output:
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        for block in item.get("content", []):
            if isinstance(block, dict) and block.get("type") == "output_text":
                content = block.get("text")
                break
        if content:
            break
    if not isinstance(content, str):
        return {}, None
    parsed = _parse_json_object_from_text(content)
    return (parsed if isinstance(parsed, dict) else {}, content)


def _parse_json_object_from_text(content: str) -> dict[str, object]:
    stripped = content.strip()
    if not stripped:
        return {}
    try:
        parsed = json.loads(stripped)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", stripped, re.DOTALL)
    if fenced:
        try:
            parsed = json.loads(fenced.group(1))
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

    start = stripped.find("{")
    end = stripped.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = stripped[start : end + 1]
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            return {}
    return {}
def _default_model_for_provider(provider_name: str) -> str | None:
    defaults = {
        "openai": "gpt-4.1-mini",
        "openrouter": "openai/gpt-5-mini",
        "xai": "grok-4-fast-reasoning",
        "ollama": "llama3.1",
    }
    return defaults.get(provider_name)


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default
