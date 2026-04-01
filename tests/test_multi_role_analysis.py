import json
from typing import Any
from datetime import datetime, timezone
from pathlib import Path

from crypto_research_agent.agents.runner import (
    FIRST_ORDER_ROLES,
    ROLE_ORDER,
    SECOND_ORDER_ROLES,
    _check_citation_coverage,
    run_multi_role_analysis,
)
from crypto_research_agent.schemas import EvidencePack, FeatureBundle, ResearchRequest, RoleAnalysisBundle


def make_request() -> ResearchRequest:
    return ResearchRequest(
        asset="BTC",
        thesis="Assess reversal risk",
        horizon_days=3,
        run_id="r_roles_test",
        as_of_utc=datetime(2026, 3, 25, 9, 30, tzinfo=timezone.utc),
    )


def make_features(tmp_path: Path) -> FeatureBundle:
    return FeatureBundle(
        run_id="r_roles_test",
        summary={
            "asset": "BTC",
            "feature_status": "complete",
            "latest_close": 100.0,
            "return_1d_pct": 5.0,
            "return_30d_pct": 12.0,
            "return_total_pct": 20.0,
            "avg_volume": 1000.0,
            "rsi_14": 58.0,
            "price_vs_sma20_pct": 3.0,
            "price_vs_sma200_pct": 10.0,
            "realized_vol_30d": 45.0,
            "volume_ratio": 1.6,
            "regime": "bull",
            "mc_tvl_ratio": 1.2,
            "defi_stablecoin_apy_change_7d": 0.1,
        },
        coverage_gaps=["coinglass:missing_api_key"],
        features_path=tmp_path / "runs" / "r_roles_test" / "features" / "summary.json",
        notes_path=tmp_path / "runs" / "r_roles_test" / "features" / "notes.md",
    )


def make_evidence(tmp_path: Path) -> EvidencePack:
    return EvidencePack(
        run_id="r_roles_test",
        summary={"evidence_status": "stub", "source": "local_stub"},
        markdown_path=tmp_path / "runs" / "r_roles_test" / "evidence" / "evidence.md",
        json_path=tmp_path / "runs" / "r_roles_test" / "evidence" / "evidence.json",
    )


def test_run_multi_role_analysis_writes_role_artifacts(tmp_path: Path) -> None:
    bundle = run_multi_role_analysis(
        request=make_request(),
        features=make_features(tmp_path),
        evidence=make_evidence(tmp_path),
        output_root=tmp_path,
    )

    assert isinstance(bundle, RoleAnalysisBundle)
    assert set(bundle.role_memos) == {
        "technical_analyst",
        "defi_fundamentals_analyst",
        "derivatives_analyst",
        "news_analyst",
        "bull_researcher",
        "bear_researcher",
        "risk_manager",
        "final_arbiter",
    }
    assert bundle.index_path.exists()
    assert bundle.role_memos["final_arbiter"]["decision"]["action"] in {"hold", "avoid"}
    assert bundle.role_memos["final_arbiter"]["scorecard"]["final_score"] >= 0
    assert bundle.role_memos["technical_analyst"]["regime"] in {"bull_trend", "bear_trend", "range_bound", "uncertain"}

    role_file = bundle.markdown_paths["technical_analyst"]
    assert role_file.exists()
    assert "Technical Analyst" in role_file.read_text(encoding="utf-8")

    index_payload = json.loads(bundle.index_path.read_text(encoding="utf-8"))
    assert "final_arbiter" in index_payload["roles"]


def test_run_multi_role_analysis_uses_prompt_provider_for_debate_roles_and_risk_manager(tmp_path: Path) -> None:
    class FakeProvider:
        name = "fake_provider"
        timeout_seconds = 12

        def __init__(self) -> None:
            self.calls: list[tuple[str, str]] = []

        def generate(self, *, role: str, prompt: str, fallback_memo: dict[str, object]) -> dict[str, object]:
            self.calls.append((role, prompt))
            if role in {"bull_researcher", "bear_researcher", "risk_manager", "final_arbiter"}:
                return {
                    "report": f"{role} narrative report built from crypto debate context.",
                    "signal": "neutral",
                    "confidence": "medium",
                    "referenced_fields": ["coverage_gaps"],
                }
            if role in {
                "aggressive_risk_analyst",
                "conservative_risk_analyst",
                "neutral_risk_analyst",
            }:
                return {
                    "report": f"{role} risk stance report.",
                    "confidence": "medium",
                }
            payload = {
                key: value
                for key, value in fallback_memo.items()
                if key not in {"title", "summary", "provider", "analysis_mode", "prompt_path", "prompt_text", "validation_error", "decision_label", "risk_bias", "rationale", "signal", "confidence"}
            }
            if role == "technical_analyst":
                payload["setup"] = {
                    **payload["setup"],
                    "thesis": f"provider summary for {role}",
                }
            return payload

    provider = FakeProvider()

    bundle = run_multi_role_analysis(
        request=make_request(),
        features=make_features(tmp_path),
        evidence=make_evidence(tmp_path),
        output_root=tmp_path,
        provider=provider,
    )

    assert {role for role, _ in provider.calls} == {
        *FIRST_ORDER_ROLES,
        "bull_researcher",
        "bear_researcher",
        "aggressive_risk_analyst",
        "conservative_risk_analyst",
        "neutral_risk_analyst",
        "risk_manager",
        "final_arbiter",
    }
    technical = bundle.role_memos["technical_analyst"]
    assert technical["provider"] == "fake_provider"
    assert technical["analysis_mode"] == "prompt_driven"
    assert technical["setup"]["thesis"] == "provider summary for technical_analyst"
    assert "referenced_fields" in technical
    assert "rsi_14" in technical["referenced_fields"]
    assert technical["prompt_path"].endswith("technical_analyst.md")
    assert "Assess reversal risk" in technical["prompt_text"]
    assert "latest_close" in technical["prompt_text"]
    assert "return_1d_pct" in technical["prompt_text"]
    assert "avg_volume" in technical["prompt_text"]
    assert "Field interpretation guide" in technical["prompt_text"]
    assert technical["signals"][0]["name"] == "rsi_14"
    assert technical["summary"].startswith("BTC technical setup remains")

    news = bundle.role_memos["news_analyst"]
    assert news["provider"] == "fake_provider"
    assert news["analysis_mode"] == "prompt_driven"
    assert "latest_close" in news["prompt_text"]
    assert "price_vs_sma200_pct" in news["prompt_text"]
    assert "Do not invent absolute price levels" in news["prompt_text"]

    bull = bundle.role_memos["bull_researcher"]
    assert bull["provider"] == "fake_provider"
    assert bull["analysis_mode"] == "prompt_driven"
    assert bull["report"].startswith("bull_researcher narrative report")
    assert "technical_analyst" in bull["prompt_text"]
    assert "\"prompt_text\"" not in bull["prompt_text"]
    assert "The `report` field is mandatory." in bull["prompt_text"]
    assert "\"signals\"" not in bull["prompt_text"]
    assert "\"levels\"" not in bull["prompt_text"]
    assert "\"setup\"" not in bull["prompt_text"]

    bear = bundle.role_memos["bear_researcher"]
    assert bear["provider"] == "fake_provider"
    assert bear["analysis_mode"] == "prompt_driven"
    assert "Bull Analyst:" in bear["prompt_text"]

    risk_manager = bundle.role_memos["risk_manager"]
    assert risk_manager["provider"] == "fake_provider"
    assert risk_manager["analysis_mode"] == "prompt_driven"
    assert risk_manager["report"].startswith("risk_manager narrative report")
    assert risk_manager["risk_views"]["aggressive"].startswith("Aggressive Analyst:")
    assert risk_manager["risk_views"]["conservative"].startswith("Conservative Analyst:")
    assert risk_manager["risk_views"]["neutral"].startswith("Neutral Analyst:")
    assert "\"aggressive_history\"" not in risk_manager["prompt_text"]
    assert "\"current_aggressive_response\"" not in risk_manager["prompt_text"]

    final_arbiter = bundle.role_memos["final_arbiter"]
    assert final_arbiter["provider"] == "fake_provider"
    assert final_arbiter["analysis_mode"] == "prompt_driven"
    assert final_arbiter["report"].startswith("final_arbiter narrative report")
    assert final_arbiter["decision"]["action"] in {"hold", "avoid"}
    assert "\"prompt_text\"" not in final_arbiter["prompt_text"]
    assert final_arbiter["scorecard"]["final_score"] == 54
    assert final_arbiter["scorecard"]["confidence"] == "medium"
    assert "final_score" in final_arbiter["prompt_text"]
    assert "score_decision" in final_arbiter["prompt_text"]
    assert "The `report` field is mandatory." in final_arbiter["prompt_text"]
    assert final_arbiter["key_factors"]
    assert "\"aggressive_history\"" not in final_arbiter["prompt_text"]

    call_log_path = tmp_path / "runs" / "r_roles_test" / "agents" / "call_log.jsonl"
    assert call_log_path.exists()
    call_rows = [
        json.loads(line)
        for line in call_log_path.read_text(encoding="utf-8").splitlines()
    ]
    assert len(call_rows) == len(ROLE_ORDER)
    prompt_driven_rows = call_rows
    assert all(row["analysis_mode"] == "prompt_driven" for row in prompt_driven_rows)
    assert all(row["provider"] == "fake_provider" for row in prompt_driven_rows)
    assert all(row["duration_ms"] >= 0 for row in call_rows)
    assert all(row["timeout_seconds"] == 12 for row in prompt_driven_rows)


def test_run_multi_role_analysis_falls_back_when_provider_output_misses_required_fields(tmp_path: Path) -> None:
    class FakeProvider:
        name = "fake_provider"
        timeout_seconds = 9

        def generate(self, *, role: str, prompt: str, fallback_memo: dict[str, object]) -> dict[str, object]:
            return {
                "report": f"invalid for {role}",
                "signal": ["not-a-string"],
            }

    bundle = run_multi_role_analysis(
        request=make_request(),
        features=make_features(tmp_path),
        evidence=make_evidence(tmp_path),
        output_root=tmp_path,
        provider=FakeProvider(),
    )

    technical = bundle.role_memos["technical_analyst"]
    assert technical["provider"] == "deterministic"
    assert technical["analysis_mode"] == "deterministic_fallback"
    assert technical["summary"].startswith("BTC still looks")
    assert technical["validation_error"] == "invalid_field_type"

    call_log_path = tmp_path / "runs" / "r_roles_test" / "agents" / "call_log.jsonl"
    first_row = json.loads(call_log_path.read_text(encoding="utf-8").splitlines()[0])
    assert first_row["validation_error"] == "invalid_field_type"
    assert first_row["fallback_reason"] == "invalid_field_type"


def test_run_multi_role_analysis_accepts_narrative_first_provider_output_for_first_order_roles(tmp_path: Path) -> None:
    class FakeProvider:
        name = "fake_provider"
        timeout_seconds = 9

        def generate(self, *, role: str, prompt: str, fallback_memo: dict[str, object]) -> dict[str, object]:
            return {
                "report": (
                    f"{role} narrative report: BTC looks constructive but still needs confirmation "
                    "from adjacent crypto-specific signals before conviction can increase."
                ),
                "signal": "bullish",
                "confidence": "medium",
                "referenced_fields": ["latest_close", "rsi_14", "price_vs_sma200_pct"],
            }

    bundle = run_multi_role_analysis(
        request=make_request(),
        features=make_features(tmp_path),
        evidence=make_evidence(tmp_path),
        output_root=tmp_path,
        provider=FakeProvider(),
    )

    technical = bundle.role_memos["technical_analyst"]
    assert technical["provider"] == "fake_provider"
    assert technical["analysis_mode"] == "prompt_driven"
    assert technical["report"].startswith("technical_analyst narrative report")
    assert technical["summary"].startswith("technical_analyst narrative report")
    assert technical["referenced_fields"] == ["latest_close", "rsi_14", "price_vs_sma200_pct"]


def test_run_multi_role_analysis_accepts_news_narrative_field_without_report(tmp_path: Path) -> None:
    class FakeProvider:
        name = "fake_provider"
        timeout_seconds = 9

        def generate(self, *, role: str, prompt: str, fallback_memo: dict[str, object]) -> dict[str, object]:
            if role == "news_analyst":
                return {
                    "narrative": "Macro and catalyst coverage remains preliminary, so no clean event-driven upside case is established.",
                    "signal": "monitor",
                    "confidence": "low",
                }
            return {
                "report": f"{role} report",
                "signal": "neutral",
                "confidence": "medium",
            }

    bundle = run_multi_role_analysis(
        request=make_request(),
        features=make_features(tmp_path),
        evidence=make_evidence(tmp_path),
        output_root=tmp_path,
        provider=FakeProvider(),
    )

    news = bundle.role_memos["news_analyst"]
    assert news["provider"] == "fake_provider"
    assert news["analysis_mode"] == "prompt_driven"
    assert news["report"].startswith("Macro and catalyst coverage remains preliminary")
    assert news["summary"].startswith("Macro and catalyst coverage remains preliminary")


def test_run_multi_role_analysis_accepts_report_only_for_final_arbiter(tmp_path: Path) -> None:
    class FakeProvider:
        name = "fake_provider"
        timeout_seconds = 9

        def generate(self, *, role: str, prompt: str, fallback_memo: dict[str, object]) -> dict[str, object]:
            if role == "final_arbiter":
                return {
                    "report": (
                        "PM verdict: avoid for now. The score sits below threshold, derivatives confirmation is missing, "
                        "and the cleanest expression is to wait for better alignment before taking risk."
                    ),
                }
            return {
                "report": f"{role} report",
                "signal": "neutral",
                "confidence": "medium",
            }

    bundle = run_multi_role_analysis(
        request=make_request(),
        features=make_features(tmp_path),
        evidence=make_evidence(tmp_path),
        output_root=tmp_path,
        provider=FakeProvider(),
    )

    final_arbiter = bundle.role_memos["final_arbiter"]
    assert final_arbiter["provider"] == "fake_provider"
    assert final_arbiter["analysis_mode"] == "prompt_driven"
    assert final_arbiter["report"].startswith("PM verdict: avoid for now")
    assert final_arbiter["summary"].startswith("PM verdict: avoid for now")
    assert final_arbiter["decision"]["action"] in {"hold", "avoid"}


def test_run_multi_role_analysis_ignores_invalid_optional_structured_fields_for_defi_and_news(tmp_path: Path) -> None:
    class FakeProvider:
        name = "fake_provider"
        timeout_seconds = 9

        def generate(self, *, role: str, prompt: str, fallback_memo: dict[str, object]) -> dict[str, object]:
            if role == "defi_fundamentals_analyst":
                return {
                    "report": "DeFi memo: capital efficiency is mixed and does not confirm broad expansion.",
                    "signal": "coverage_gap",
                    "confidence": "medium",
                    "data_coverage": "partial",  # wrong type: fallback expects dict
                    "protocol_metrics": "thin",  # wrong type: fallback expects list
                    "referenced_fields": ["mc_tvl_ratio"],
                }
            if role == "news_analyst":
                return {
                    "report": "News memo: catalyst map is incomplete and should not raise conviction yet.",
                    "signal": "monitor",
                    "confidence": "low",
                    "top_risks": "macro uncertainty",  # wrong type: fallback expects list
                    "macro_context": {"fed": "upcoming"},  # wrong type: fallback expects str
                    "referenced_fields": ["evidence_status"],
                }
            return {
                "report": f"{role} report",
                "signal": "neutral",
                "confidence": "medium",
            }

    bundle = run_multi_role_analysis(
        request=make_request(),
        features=make_features(tmp_path),
        evidence=make_evidence(tmp_path),
        output_root=tmp_path,
        provider=FakeProvider(),
    )

    defi = bundle.role_memos["defi_fundamentals_analyst"]
    assert defi["provider"] == "fake_provider"
    assert defi["analysis_mode"] == "prompt_driven"
    assert defi["report"].startswith("DeFi memo:")
    assert isinstance(defi["data_coverage"], dict)
    assert isinstance(defi["protocol_metrics"], list)

    news = bundle.role_memos["news_analyst"]
    assert news["provider"] == "fake_provider"
    assert news["analysis_mode"] == "prompt_driven"
    assert news["report"].startswith("News memo:")
    assert isinstance(news["top_risks"], list)
    assert isinstance(news["macro_context"], str)

def test_run_multi_role_analysis_salvages_plain_text_for_narrative_roles(tmp_path: Path) -> None:
    class FakeProvider:
        name = "fake_provider"
        timeout_seconds = 9

        def __init__(self) -> None:
            self.last_meta: dict[str, object] = {}

        def generate(self, *, role: str, prompt: str, fallback_memo: dict[str, object]) -> dict[str, object]:
            if role == "bear_researcher":
                self.last_meta = {
                    "reason": "response_not_json_object",
                    "error_type": "ParseError",
                    "detail": "Provider response could not be normalized into a JSON object",
                    "raw_text": "Bear case: momentum is overstated and leverage confirmation is still missing.",
                }
                return {}
            self.last_meta = {"status": "ok"}
            return {
                "report": f"{role} report",
                "signal": "neutral",
                "confidence": "medium",
            }

    bundle = run_multi_role_analysis(
        request=make_request(),
        features=make_features(tmp_path),
        evidence=make_evidence(tmp_path),
        output_root=tmp_path,
        provider=FakeProvider(),
    )

    bear = bundle.role_memos["bear_researcher"]
    assert bear["provider"] == "fake_provider"
    assert bear["analysis_mode"] == "prompt_driven"
    assert bear["report"].startswith("Bear case: momentum is overstated")


def test_run_multi_role_analysis_uses_scorecard_to_constrain_final_decision(tmp_path: Path) -> None:
    low_score_features = FeatureBundle(
        run_id="r_roles_test",
        summary={
            "asset": "BTC",
            "feature_status": "complete",
            "latest_close": 100.0,
            "return_1d_pct": -3.0,
            "return_total_pct": -25.0,
            "avg_volume": 100.0,
        },
        coverage_gaps=["coinglass:missing_api_key", "defillama:missing_api_key"],
        features_path=tmp_path / "runs" / "r_roles_test" / "features" / "summary.json",
        notes_path=tmp_path / "runs" / "r_roles_test" / "features" / "notes.md",
    )

    bundle = run_multi_role_analysis(
        request=make_request(),
        features=low_score_features,
        evidence=make_evidence(tmp_path),
        output_root=tmp_path,
    )

    final_arbiter = bundle.role_memos["final_arbiter"]
    assert final_arbiter["scorecard"]["final_score"] < 50
    assert final_arbiter["scorecard"]["score_decision"] == "avoid"
    assert final_arbiter["decision"]["action"] == "avoid"


def test_run_multi_role_analysis_builds_sequential_bull_bear_debate_state(tmp_path: Path) -> None:
    bundle = run_multi_role_analysis(
        request=make_request(),
        features=make_features(tmp_path),
        evidence=make_evidence(tmp_path),
        output_root=tmp_path,
    )

    bull = bundle.role_memos["bull_researcher"]
    bear = bundle.role_memos["bear_researcher"]
    risk = bundle.role_memos["risk_manager"]

    assert bull["debate_state"]["count"] == 1
    assert bull["debate_state"]["current_response"].startswith("Bull Analyst:")
    assert "Bull Analyst:" in bull["debate_state"]["history"]

    assert bear["debate_state"]["count"] == 2
    assert bear["debate_state"]["current_response"].startswith("Bear Analyst:")
    assert "Bull Analyst:" in bear["debate_state"]["history"]
    assert "Bear Analyst:" in bear["debate_state"]["history"]
    assert bear["counterparty_response"].startswith("Bull Analyst:")

    assert "Bull Analyst:" in risk["prompt_text"]
    assert "Bear Analyst:" in risk["prompt_text"]


def test_run_multi_role_analysis_builds_sequential_risk_debate_state(tmp_path: Path) -> None:
    bundle = run_multi_role_analysis(
        request=make_request(),
        features=make_features(tmp_path),
        evidence=make_evidence(tmp_path),
        output_root=tmp_path,
    )

    risk = bundle.role_memos["risk_manager"]
    final_arbiter = bundle.role_memos["final_arbiter"]
    risk_debate_state = risk["risk_debate_state"]

    assert risk_debate_state["count"] == 3
    assert risk_debate_state["latest_speaker"] == "Neutral"
    assert "Aggressive Analyst:" in risk_debate_state["history"]
    assert "Conservative Analyst:" in risk_debate_state["history"]
    assert "Neutral Analyst:" in risk_debate_state["history"]
    assert risk["risk_views"]["aggressive"].startswith("Aggressive Analyst:")
    assert risk["risk_views"]["conservative"].startswith("Conservative Analyst:")
    assert risk["risk_views"]["neutral"].startswith("Neutral Analyst:")
    assert "Aggressive Analyst:" in final_arbiter["prompt_text"]
    assert "Neutral Analyst:" in final_arbiter["prompt_text"]


# ── KPI 2: Bear sees bull's full key_points ──────────────────────────────────

def test_bear_prompt_contains_bull_key_points_to_rebut(tmp_path: Path) -> None:
    """Bear's prompt context must include the bull's full key_points list."""
    bundle = run_multi_role_analysis(
        request=make_request(),
        features=make_features(tmp_path),
        evidence=make_evidence(tmp_path),
        output_root=tmp_path,
    )

    bear = bundle.role_memos["bear_researcher"]
    # bull_key_points_to_rebut must appear in the serialised prompt JSON
    assert "bull_key_points_to_rebut" in bear["prompt_text"]
    # And the fallback bull key_point text must be present too
    assert "Short-term momentum remains constructive" in bear["prompt_text"]


# ── KPI 3: Citation coverage warning ─────────────────────────────────────────

def test_check_citation_coverage_returns_warning_when_evidence_source_missing() -> None:
    memo_missing = {
        "key_points": [
            {"point": "Momentum is strong."},  # no evidence_source
            {"point": "TVL growing.", "evidence_source": "defi_fundamentals_analyst"},
        ]
    }
    warning = _check_citation_coverage("bull_researcher", memo_missing)
    assert warning == "1_of_2_key_points_missing_evidence_source"


def test_check_citation_coverage_returns_none_when_all_cited() -> None:
    memo_cited = {
        "key_points": [
            {"point": "Momentum is strong.", "evidence_source": "technical_analyst"},
            {"point": "TVL growing.", "evidence_source": "defi_fundamentals_analyst"},
        ]
    }
    assert _check_citation_coverage("bull_researcher", memo_cited) is None


def test_check_citation_coverage_skips_non_debate_roles() -> None:
    memo = {"key_points": [{"point": "RSI at 45."}]}
    assert _check_citation_coverage("technical_analyst", memo) is None
    assert _check_citation_coverage("final_arbiter", memo) is None


def test_run_multi_role_analysis_attaches_citation_warning_when_evidence_source_absent(
    tmp_path: Path,
) -> None:
    """If the provider returns key_points without evidence_source, citation_warning is set."""

    class FakeProvider:
        name = "fake_provider"
        timeout_seconds = 9

        def generate(self, *, role: str, prompt: str, fallback_memo: dict[str, object]) -> dict[str, object]:
            if role == "bull_researcher":
                return {
                    "report": "Bull narrative.",
                    "signal": "bullish",
                    "confidence": "medium",
                    "referenced_fields": ["return_1d_pct"],
                    "key_points": [
                        {"point": "Momentum is strong."},  # missing evidence_source
                    ],
                }
            return {
                "report": f"{role} report.",
                "signal": "neutral",
                "confidence": "medium",
            }

    bundle = run_multi_role_analysis(
        request=make_request(),
        features=make_features(tmp_path),
        evidence=make_evidence(tmp_path),
        output_root=tmp_path,
        provider=FakeProvider(),
    )

    bull = bundle.role_memos["bull_researcher"]
    assert bull["provider"] == "fake_provider"
    assert "citation_warning" in bull
    assert "missing_evidence_source" in bull["citation_warning"]


# ── KPI 4: Final arbiter rejected_alternative ────────────────────────────────

def test_final_arbiter_has_rejected_alternative(tmp_path: Path) -> None:
    """Final arbiter memo must contain rejected_alternative with action + reason."""
    bundle = run_multi_role_analysis(
        request=make_request(),
        features=make_features(tmp_path),
        evidence=make_evidence(tmp_path),
        output_root=tmp_path,
    )

    fa = bundle.role_memos["final_arbiter"]
    assert "rejected_alternative" in fa
    alt = fa["rejected_alternative"]
    assert isinstance(alt, dict)
    assert "alternative_action" in alt
    assert "why_rejected" in alt
    assert isinstance(alt["alternative_action"], str)
    assert isinstance(alt["why_rejected"], str)
    # The rejected action must differ from the chosen action
    assert alt["alternative_action"] != fa["decision"]["action"]
