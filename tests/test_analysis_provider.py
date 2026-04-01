import json
import subprocess

from crypto_research_agent.agents import provider as provider_module
from crypto_research_agent.agents.provider import (
    DeterministicAnalysisProvider,
    OpenAICompatibleAnalysisProvider,
    ProviderRequestError,
    _run_provider_request_isolated,
    default_analysis_provider,
)


def test_default_analysis_provider_supports_tradingagents_style_openrouter(monkeypatch) -> None:
    monkeypatch.setenv("CRYPTO_RESEARCH_ANALYSIS_PROVIDER", "openrouter")
    monkeypatch.delenv("ANALYSIS_API_KEY", raising=False)
    monkeypatch.delenv("ANALYSIS_API_BASE_URL", raising=False)
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("ANALYSIS_MODEL", "openai/gpt-5-mini")

    provider = default_analysis_provider()

    assert isinstance(provider, OpenAICompatibleAnalysisProvider)
    assert provider.name == "openrouter"
    assert provider.base_url == "https://openrouter.ai/api/v1"
    assert provider.timeout_seconds == 30
    assert provider.max_retries == 0


def test_default_analysis_provider_defaults_to_openai_when_api_key_present(monkeypatch) -> None:
    monkeypatch.delenv("CRYPTO_RESEARCH_ANALYSIS_PROVIDER", raising=False)
    monkeypatch.delenv("ANALYSIS_API_KEY", raising=False)
    monkeypatch.delenv("ANALYSIS_MODEL", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    provider = default_analysis_provider()

    assert isinstance(provider, OpenAICompatibleAnalysisProvider)
    assert provider.name == "openai"
    assert provider.model == "gpt-4.1-mini"


def test_default_analysis_provider_honors_explicit_timeout_and_retry(monkeypatch) -> None:
    monkeypatch.setenv("CRYPTO_RESEARCH_ANALYSIS_PROVIDER", "openai")
    monkeypatch.delenv("ANALYSIS_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("ANALYSIS_TIMEOUT_SECONDS", "8")
    monkeypatch.setenv("ANALYSIS_MAX_RETRIES", "2")

    provider = default_analysis_provider()

    assert isinstance(provider, OpenAICompatibleAnalysisProvider)
    assert provider.timeout_seconds == 8
    assert provider.max_retries == 2


def test_default_analysis_provider_uses_fast_openai_model_for_analysis(monkeypatch) -> None:
    monkeypatch.setenv("CRYPTO_RESEARCH_ANALYSIS_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.delenv("ANALYSIS_MODEL", raising=False)

    provider = default_analysis_provider()

    assert isinstance(provider, OpenAICompatibleAnalysisProvider)
    assert provider.model == "gpt-4.1-mini"


def test_openai_provider_uses_responses_api_payload(monkeypatch) -> None:
    captured = {}

    def fake_request(http_request, timeout_seconds):
        captured["url"] = http_request.full_url
        captured["body"] = json.loads(http_request.data.decode("utf-8"))
        return {
            "output": [
                {"type": "reasoning", "summary": []},
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [
                        {
                            "type": "output_text",
                            "text": "{\"summary\":\"ok\"}",
                        }
                    ],
                },
            ]
        }

    monkeypatch.setattr(provider_module, "_run_provider_request_isolated", fake_request)

    provider = OpenAICompatibleAnalysisProvider(
        api_key="test-key",
        model="gpt-5-mini",
        base_url="https://api.openai.com/v1",
        provider_name="openai",
    )

    payload = provider.generate(
        role="technical_analyst",
        prompt="Return JSON",
        fallback_memo={"summary": "fallback"},
    )

    assert captured["url"] == "https://api.openai.com/v1/responses"
    assert captured["body"]["model"] == "gpt-5-mini"
    assert "senior crypto research analyst" in captured["body"]["input"][0]["content"][0]["text"]
    assert payload["summary"] == "ok"


def test_openai_provider_retries_once_before_success(monkeypatch) -> None:
    calls = {"count": 0}

    def fake_request(http_request, timeout_seconds):
        calls["count"] += 1
        if calls["count"] == 1:
            raise ProviderRequestError("URLError", "temporary")
        return {
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": "{\"summary\":\"ok\"}"}],
                }
            ]
        }

    monkeypatch.setattr(provider_module, "_run_provider_request_isolated", fake_request)

    provider = OpenAICompatibleAnalysisProvider(
        api_key="test-key",
        model="gpt-5-mini",
        base_url="https://api.openai.com/v1",
        provider_name="openai",
        max_retries=1,
    )

    payload = provider.generate(
        role="technical_analyst",
        prompt="Return JSON",
        fallback_memo={"summary": "fallback"},
    )

    assert calls["count"] == 2
    assert payload["summary"] == "ok"


def test_openai_provider_extracts_json_from_markdown_fence(monkeypatch) -> None:
    monkeypatch.setattr(
        provider_module,
        "_run_provider_request_isolated",
        lambda http_request, timeout_seconds: {
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [
                        {
                            "type": "output_text",
                            "text": "```json\n{\"report\":\"ok\",\"signal\":\"neutral\",\"confidence\":\"medium\"}\n```",
                        }
                    ],
                }
            ]
        },
    )

    provider = OpenAICompatibleAnalysisProvider(
        api_key="test-key",
        model="gpt-4.1-mini",
        base_url="https://api.openai.com/v1",
        provider_name="openai",
    )

    payload = provider.generate(
        role="news_analyst",
        prompt="Return JSON",
        fallback_memo={"summary": "fallback"},
    )

    assert payload["report"] == "ok"
    assert provider.last_meta["status"] == "ok"


def test_openai_provider_records_parse_failure_metadata(monkeypatch) -> None:
    monkeypatch.setattr(
        provider_module,
        "_run_provider_request_isolated",
        lambda http_request, timeout_seconds: {
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": "not json"}],
                }
            ]
        },
    )

    provider = OpenAICompatibleAnalysisProvider(
        api_key="test-key",
        model="gpt-4.1-mini",
        base_url="https://api.openai.com/v1",
        provider_name="openai",
    )

    payload = provider.generate(
        role="news_analyst",
        prompt="Return JSON",
        fallback_memo={"summary": "fallback"},
    )

    assert payload == {}
    assert provider.last_meta["reason"] == "response_not_json_object"


def test_openai_provider_uses_isolated_runner_for_network_requests(monkeypatch) -> None:
    captured = {}

    def fake_run(cmd, *, input, capture_output, text, timeout, env, check):
        captured["cmd"] = cmd
        captured["timeout"] = timeout
        captured["stdin"] = json.loads(input)
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=0,
            stdout=json.dumps(
                {
                    "response_payload": {
                        "output": [
                            {
                                "type": "message",
                                "role": "assistant",
                                "content": [{"type": "output_text", "text": "{\"summary\":\"ok\"}"}],
                            }
                        ]
                    }
                }
            ),
            stderr="",
        )

    monkeypatch.setattr(provider_module.subprocess, "run", fake_run)

    http_request = provider_module.request.Request(
        url="https://api.openai.com/v1/responses",
        headers=provider_module._build_headers("test-key"),
        data=json.dumps({"model": "gpt-4.1-mini"}).encode("utf-8"),
        method="POST",
    )

    payload = _run_provider_request_isolated(http_request=http_request, timeout_seconds=12)

    assert payload["output"][0]["content"][0]["text"] == "{\"summary\":\"ok\"}"
    assert captured["timeout"] == 17
    assert captured["stdin"]["payload"]["model"] == "gpt-4.1-mini"


def test_openai_provider_records_timeout_from_isolated_runner(monkeypatch) -> None:
    def fake_run(cmd, *, input, capture_output, text, timeout, env, check):
        raise subprocess.TimeoutExpired(cmd=cmd, timeout=timeout)

    monkeypatch.setattr(provider_module.subprocess, "run", fake_run)

    http_request = provider_module.request.Request(
        url="https://api.openai.com/v1/responses",
        headers=provider_module._build_headers("test-key"),
        data=json.dumps({"model": "gpt-4.1-mini"}).encode("utf-8"),
        method="POST",
    )

    try:
        _run_provider_request_isolated(http_request=http_request, timeout_seconds=9)
    except ProviderRequestError as exc:
        assert exc.error_type == "TimeoutExpired"
    else:
        raise AssertionError("expected ProviderRequestError")
