import json
from datetime import datetime, timezone
from pathlib import Path

from crypto_research_agent.orchestration.graph import run_workflow
from crypto_research_agent.schemas import EvidencePack, FeatureBundle, RawDataBundle, ResearchRequest, RoleAnalysisBundle, SourceResult


def test_run_workflow_writes_framework_artifacts(tmp_path) -> None:
    request = ResearchRequest(
        asset="BTC",
        thesis="Assess reversal risk",
        horizon_days=3,
        run_id="r_framework_test",
        as_of_utc=datetime(2026, 3, 25, 9, 30, tzinfo=timezone.utc),
    )

    def fake_collect_market_data(request, sources_config, output_root):
        return RawDataBundle(
            run_id=request.run_id,
            source_results={
                "openbb": SourceResult(
                    source="openbb",
                    status="fetched",
                    reason=None,
                    artifact_paths=[],
                )
            },
            coverage_gaps=[],
            provenance_path=output_root / "runs" / request.run_id / "provenance.jsonl",
        )

    def fake_build_feature_bundle(request, raw_data, output_root):
        return FeatureBundle(
            run_id=request.run_id,
            summary={"asset": request.asset, "feature_status": "complete"},
            coverage_gaps=[],
            features_path=output_root / "runs" / request.run_id / "features" / "summary.json",
            notes_path=output_root / "runs" / request.run_id / "features" / "notes.md",
        )

    def fake_build_evidence_pack(request, raw_data, features, output_root):
        return EvidencePack(
            run_id=request.run_id,
            summary={"evidence_status": "stub"},
            markdown_path=output_root / "runs" / request.run_id / "evidence" / "evidence.md",
            json_path=output_root / "runs" / request.run_id / "evidence" / "evidence.json",
        )

    def fake_run_multi_role_analysis(request, features, evidence, output_root, provider):
        agents_dir = output_root / "runs" / request.run_id / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        (agents_dir / "call_log.jsonl").write_text(
            '{"role":"technical_analyst","provider":"fake","analysis_mode":"prompt_driven","timeout_seconds":12,"duration_ms":5,"validation_error":null}\n',
            encoding="utf-8",
        )
        return RoleAnalysisBundle(
            run_id=request.run_id,
            role_memos={"final_arbiter": {"decision": {"action": "hold", "direction": "neutral", "horizon_days": 3, "position_size": "half"}, "decision_label": "hold", "scorecard": {"inputs": {"momentum": 68.0, "liquidity": 80.0, "derivatives": 55.0, "defi": 52.0, "onchain": 60.0, "sentiment": 58.0, "data_quality_penalty": -5.0}, "final_score": 62, "confidence": "medium", "score_decision": "hold"}}},
            markdown_paths={
                "final_arbiter": output_root / "runs" / request.run_id / "agents" / "final_arbiter.md"
            },
            json_paths={
                "final_arbiter": output_root / "runs" / request.run_id / "agents" / "final_arbiter.json"
            },
            index_path=output_root / "runs" / request.run_id / "agents" / "index.json",
        )

    def fake_schedule_review(*, request, output_root):
        review_path = output_root / "reviews" / "pending" / f"{request.run_id}.json"
        review_path.parent.mkdir(parents=True, exist_ok=True)
        review_path.write_text('{"status":"pending"}', encoding="utf-8")
        return review_path

    result = run_workflow(
        request=request,
        sources_config={"sources": {"openbb": {"enabled": True}}},
        output_root=tmp_path,
        collect_market_data_fn=fake_collect_market_data,
        build_feature_bundle_fn=fake_build_feature_bundle,
        build_evidence_pack_fn=fake_build_evidence_pack,
        run_multi_role_analysis_fn=fake_run_multi_role_analysis,
        schedule_review_fn=fake_schedule_review,
    )

    assert result["status"] == "framework_ready"
    assert result["run_id"] == "r_framework_test"
    assert result["artifacts"]["run_json"].exists()
    assert result["artifacts"]["research_card"].exists()
    assert result["artifacts"]["artifact_index"].exists()
    assert result["artifacts"]["roles_call_log"].exists()
    assert Path(result["artifacts"]["review_task"]).exists()

    run_payload = json.loads(result["artifacts"]["run_json"].read_text(encoding="utf-8"))
    assert run_payload["request"]["asset"] == "BTC"
    assert run_payload["stages"]["data_collection"] == "completed"
    assert run_payload["stages"]["feature_engineering"] == "completed"
    assert run_payload["stages"]["evidence_collection"] == "completed"
    assert run_payload["stages"]["multi_role_analysis"] == "completed"
    assert run_payload["stages"]["review_loop"] == "scheduled"
    assert run_payload["features_path"].endswith("summary.json")
    assert run_payload["roles_index_path"].endswith("index.json")
    assert run_payload["scorecard"]["final_score"] == 62

    card_text = result["artifacts"]["research_card"].read_text(encoding="utf-8")
    assert "# BTC Research Report" in card_text
    assert "Processed signal: HOLD" in card_text
    assert "1. Verdict" in card_text
    assert "2. Case File" in card_text
    assert "3. Bench Evidence" in card_text
    assert "4. Prosecution" in card_text
    assert "5. Defense" in card_text
    assert "6. Sentencing / Guardrails" in card_text
    assert "7. Judge's Ruling" in card_text
    assert "8. Appeal Conditions" in card_text
    assert "9. Data Quality Footnote" in card_text
    assert "How To Read This Verdict" in card_text
    assert "Action Score is the baseline action signal, not a return forecast." in card_text
    assert "Confidence measures agreement across core market signals" in card_text
    assert "Supplementary gaps contribute at most a single -5 penalty." in card_text
    assert "Total: 62/100" in card_text
    assert "Momentum:" in card_text
    assert "Derivatives:" in card_text
    assert "Data quality penalty:" in card_text


def test_run_workflow_persists_run_artifacts_before_review_scheduling(tmp_path) -> None:
    request = ResearchRequest(
        asset="BTC",
        thesis="Assess reversal risk",
        horizon_days=3,
        run_id="r_framework_persist_before_review",
        as_of_utc=datetime(2026, 3, 25, 9, 30, tzinfo=timezone.utc),
    )

    def fake_collect_market_data(request, sources_config, output_root):
        return RawDataBundle(
            run_id=request.run_id,
            source_results={
                "openbb": SourceResult(source="openbb", status="fetched", reason=None, artifact_paths=[]),
            },
            coverage_gaps=[],
            provenance_path=output_root / "runs" / request.run_id / "provenance.jsonl",
        )

    def fake_build_feature_bundle(request, raw_data, output_root):
        return FeatureBundle(
            run_id=request.run_id,
            summary={"asset": request.asset, "feature_status": "complete"},
            coverage_gaps=[],
            features_path=output_root / "runs" / request.run_id / "features" / "summary.json",
            notes_path=output_root / "runs" / request.run_id / "features" / "notes.md",
        )

    def fake_build_evidence_pack(request, raw_data, features, output_root):
        return EvidencePack(
            run_id=request.run_id,
            summary={"evidence_status": "stub"},
            markdown_path=output_root / "runs" / request.run_id / "evidence" / "evidence.md",
            json_path=output_root / "runs" / request.run_id / "evidence" / "evidence.json",
        )

    def fake_run_multi_role_analysis(request, features, evidence, output_root, provider):
        agents_dir = output_root / "runs" / request.run_id / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        return RoleAnalysisBundle(
            run_id=request.run_id,
            role_memos={
                "final_arbiter": {
                    "decision": {"action": "hold", "direction": "neutral", "horizon_days": 3, "position_size": "half"},
                    "decision_label": "hold",
                    "scorecard": {"final_score": 62, "confidence": "medium", "score_decision": "hold"},
                }
            },
            markdown_paths={"final_arbiter": agents_dir / "final_arbiter.md"},
            json_paths={"final_arbiter": agents_dir / "final_arbiter.json"},
            index_path=agents_dir / "index.json",
        )

    def failing_schedule_review(*, request, output_root):
        raise RuntimeError("review scheduler unavailable")

    run_json = tmp_path / "runs" / request.run_id / "run.json"

    try:
        run_workflow(
            request=request,
            sources_config={"sources": {"openbb": {"enabled": True}}},
            output_root=tmp_path,
            collect_market_data_fn=fake_collect_market_data,
            build_feature_bundle_fn=fake_build_feature_bundle,
            build_evidence_pack_fn=fake_build_evidence_pack,
            run_multi_role_analysis_fn=fake_run_multi_role_analysis,
            schedule_review_fn=failing_schedule_review,
        )
    except RuntimeError as exc:
        assert str(exc) == "review scheduler unavailable"
    else:
        raise AssertionError("run_workflow should surface review scheduling errors")

    assert run_json.exists()
    run_payload = json.loads(run_json.read_text(encoding="utf-8"))
    assert run_payload["status"] == "failed"
    assert run_payload["failed_stage"] == "review_loop"
    assert run_payload["stages"]["review_loop"] == "failed"
    assert run_payload["final_decision"] == "hold"


def test_run_workflow_persists_partial_state_when_feature_stage_fails(tmp_path) -> None:
    request = ResearchRequest(
        asset="BTC",
        thesis="Assess reversal risk",
        horizon_days=3,
        run_id="r_framework_feature_failure",
        as_of_utc=datetime(2026, 3, 25, 9, 30, tzinfo=timezone.utc),
    )

    def fake_collect_market_data(request, sources_config, output_root):
        return RawDataBundle(
            run_id=request.run_id,
            source_results={
                "openbb": SourceResult(source="openbb", status="fetched", reason=None, artifact_paths=[]),
            },
            coverage_gaps=[],
            provenance_path=output_root / "runs" / request.run_id / "provenance.jsonl",
        )

    def failing_build_feature_bundle(request, raw_data, output_root):
        raise RuntimeError("feature stage failed")

    run_json = tmp_path / "runs" / request.run_id / "run.json"

    try:
        run_workflow(
            request=request,
            sources_config={"sources": {"openbb": {"enabled": True}}},
            output_root=tmp_path,
            collect_market_data_fn=fake_collect_market_data,
            build_feature_bundle_fn=failing_build_feature_bundle,
        )
    except RuntimeError as exc:
        assert str(exc) == "feature stage failed"
    else:
        raise AssertionError("run_workflow should surface feature stage errors")

    assert run_json.exists()
    run_payload = json.loads(run_json.read_text(encoding="utf-8"))
    assert run_payload["status"] == "failed"
    assert run_payload["failed_stage"] == "feature_engineering"
    assert run_payload["stages"]["data_collection"] == "completed"
    assert run_payload["stages"]["feature_engineering"] == "failed"
    assert run_payload["provenance_path"].endswith("provenance.jsonl")
    assert run_payload["features_path"] is None


def test_run_workflow_renders_research_card_when_technical_levels_are_strings(tmp_path) -> None:
    request = ResearchRequest(
        asset="BTC",
        thesis="Assess historical replay",
        horizon_days=3,
        run_id="r_framework_string_levels_test",
        as_of_utc=datetime(2025, 10, 5, 0, 0, tzinfo=timezone.utc),
    )

    def fake_collect_market_data(request, sources_config, output_root):
        return RawDataBundle(
            run_id=request.run_id,
            source_results={
                "openbb": SourceResult(source="openbb", status="fetched", reason=None, artifact_paths=[]),
            },
            coverage_gaps=[],
            provenance_path=output_root / "runs" / request.run_id / "provenance.jsonl",
        )

    def fake_build_feature_bundle(request, raw_data, output_root):
        return FeatureBundle(
            run_id=request.run_id,
            summary={"asset": request.asset, "feature_status": "complete", "latest_close": 123.0},
            coverage_gaps=[],
            features_path=output_root / "runs" / request.run_id / "features" / "summary.json",
            notes_path=output_root / "runs" / request.run_id / "features" / "notes.md",
        )

    def fake_build_evidence_pack(request, raw_data, features, output_root):
        return EvidencePack(
            run_id=request.run_id,
            summary={"evidence_status": "stub"},
            markdown_path=output_root / "runs" / request.run_id / "evidence" / "evidence.md",
            json_path=output_root / "runs" / request.run_id / "evidence" / "evidence.json",
        )

    def fake_run_multi_role_analysis(request, features, evidence, output_root, provider):
        agents_dir = output_root / "runs" / request.run_id / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        (agents_dir / "call_log.jsonl").write_text("", encoding="utf-8")
        role_memos = {
            "technical_analyst": {
                "summary": "BTC technical setup remains constructive.",
                "levels": {"support": ["67000"], "resistance": ["73000"]},
            },
            "defi_fundamentals_analyst": {"summary": "DeFi view."},
            "derivatives_analyst": {"summary": "Derivatives view."},
            "news_analyst": {
                "summary": "News view.",
                "evidence_quality": "actionable",
                "top_risks": [{"risk": "Regulatory deadline risk"}],
                "narrative": "BTC broke above $35,000 and now faces resistance at $37,500.",
            },
            "bull_researcher": {"summary": "Bull view."},
            "bear_researcher": {"summary": "Bear view."},
            "risk_manager": {"summary": "Risk view."},
            "final_arbiter": {
                "decision": {"action": "hold", "direction": "neutral", "horizon_days": 3, "position_size": "half"},
                "decision_label": "hold",
                "scorecard": {"final_score": 62, "confidence": "medium", "score_decision": "hold"},
                "key_factors": [],
                "rationale": ["score=62"],
            },
        }
        return RoleAnalysisBundle(
            run_id=request.run_id,
            role_memos=role_memos,
            markdown_paths={role: agents_dir / f"{role}.md" for role in role_memos},
            json_paths={role: agents_dir / f"{role}.json" for role in role_memos},
            index_path=agents_dir / "index.json",
        )

    def fake_schedule_review(*, request, output_root):
        review_path = output_root / "reviews" / "pending" / f"{request.run_id}.json"
        review_path.parent.mkdir(parents=True, exist_ok=True)
        review_path.write_text('{"status":"pending"}', encoding="utf-8")
        return review_path

    result = run_workflow(
        request=request,
        sources_config={"sources": {"openbb": {"enabled": True}}},
        output_root=tmp_path,
        collect_market_data_fn=fake_collect_market_data,
        build_feature_bundle_fn=fake_build_feature_bundle,
        build_evidence_pack_fn=fake_build_evidence_pack,
        run_multi_role_analysis_fn=fake_run_multi_role_analysis,
        schedule_review_fn=fake_schedule_review,
    )

    card_text = result["artifacts"]["research_card"].read_text(encoding="utf-8")
    assert "# BTC Research Report" in card_text
    assert "Processed signal: HOLD" in card_text
    assert "1. Verdict" in card_text


def test_run_workflow_renders_historical_replay_note_in_research_card(tmp_path) -> None:
    request = ResearchRequest(
        asset="BTC",
        thesis="Assess historical replay",
        horizon_days=3,
        run_id="r_framework_historical_note_test",
        as_of_utc=datetime(2020, 1, 1, 0, 0, tzinfo=timezone.utc),
    )

    def fake_collect_market_data(request, sources_config, output_root):
        return RawDataBundle(
            run_id=request.run_id,
            source_results={
                "openbb": SourceResult(source="openbb", status="fetched", reason=None, artifact_paths=[]),
            },
            coverage_gaps=[],
            provenance_path=output_root / "runs" / request.run_id / "provenance.jsonl",
        )

    def fake_build_feature_bundle(request, raw_data, output_root):
        return FeatureBundle(
            run_id=request.run_id,
            summary={"asset": request.asset, "feature_status": "complete", "latest_close": 123.0},
            coverage_gaps=[],
            features_path=output_root / "runs" / request.run_id / "features" / "summary.json",
            notes_path=output_root / "runs" / request.run_id / "features" / "notes.md",
        )

    def fake_build_evidence_pack(request, raw_data, features, output_root):
        return EvidencePack(
            run_id=request.run_id,
            summary={
                "evidence_status": "stub",
                "source": "local_stub",
                "run_mode": "historical_replay",
                "historical_replay": True,
                "point_in_time_note": "Price features are sliced to the requested date. Evidence and non-price inputs are not guaranteed historical snapshots.",
                "point_in_time_limitations": ["evidence_not_historically_replayed"],
            },
            markdown_path=output_root / "runs" / request.run_id / "evidence" / "evidence.md",
            json_path=output_root / "runs" / request.run_id / "evidence" / "evidence.json",
        )

    def fake_run_multi_role_analysis(request, features, evidence, output_root, provider):
        agents_dir = output_root / "runs" / request.run_id / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        (agents_dir / "call_log.jsonl").write_text("", encoding="utf-8")
        role_memos = {
            "technical_analyst": {"summary": "BTC technical setup remains constructive."},
            "defi_fundamentals_analyst": {"summary": "DeFi view."},
            "derivatives_analyst": {"summary": "Derivatives view."},
            "news_analyst": {"summary": "News view."},
            "bull_researcher": {"summary": "Bull view."},
            "bear_researcher": {"summary": "Bear view."},
            "risk_manager": {"summary": "Risk view."},
            "final_arbiter": {
                "decision": {"action": "hold", "direction": "neutral", "horizon_days": 3, "position_size": "half"},
                "decision_label": "hold",
                "scorecard": {"final_score": 62, "confidence": "medium", "score_decision": "hold"},
                "key_factors": [],
                "rationale": ["score=62"],
            },
        }
        return RoleAnalysisBundle(
            run_id=request.run_id,
            role_memos=role_memos,
            markdown_paths={role: agents_dir / f"{role}.md" for role in role_memos},
            json_paths={role: agents_dir / f"{role}.json" for role in role_memos},
            index_path=agents_dir / "index.json",
        )

    def fake_schedule_review(*, request, output_root):
        review_path = output_root / "reviews" / "pending" / f"{request.run_id}.json"
        review_path.parent.mkdir(parents=True, exist_ok=True)
        review_path.write_text('{"status":"pending"}', encoding="utf-8")
        return review_path

    result = run_workflow(
        request=request,
        sources_config={"sources": {"openbb": {"enabled": True}}},
        output_root=tmp_path,
        collect_market_data_fn=fake_collect_market_data,
        build_feature_bundle_fn=fake_build_feature_bundle,
        build_evidence_pack_fn=fake_build_evidence_pack,
        run_multi_role_analysis_fn=fake_run_multi_role_analysis,
        schedule_review_fn=fake_schedule_review,
    )

    card_text = result["artifacts"]["research_card"].read_text(encoding="utf-8")
    assert "Run Mode: historical_replay" in card_text
    assert (
        "Point-in-time Note: Price features are sliced to the requested date. Evidence and non-price inputs are not guaranteed historical snapshots."
        in card_text
    )


def test_run_workflow_renders_debate_summary_in_research_card(tmp_path) -> None:
    request = ResearchRequest(
        asset="BTC",
        thesis="Assess debate rendering",
        horizon_days=3,
        run_id="r_framework_debate_render_test",
        as_of_utc=datetime(2026, 3, 25, 9, 30, tzinfo=timezone.utc),
    )

    def fake_collect_market_data(request, sources_config, output_root):
        return RawDataBundle(
            run_id=request.run_id,
            source_results={
                "openbb": SourceResult(source="openbb", status="fetched", reason=None, artifact_paths=[]),
            },
            coverage_gaps=[],
            provenance_path=output_root / "runs" / request.run_id / "provenance.jsonl",
        )

    def fake_build_feature_bundle(request, raw_data, output_root):
        return FeatureBundle(
            run_id=request.run_id,
            summary={"asset": request.asset, "feature_status": "complete", "latest_close": 123.0},
            coverage_gaps=[],
            features_path=output_root / "runs" / request.run_id / "features" / "summary.json",
            notes_path=output_root / "runs" / request.run_id / "features" / "notes.md",
        )

    def fake_build_evidence_pack(request, raw_data, features, output_root):
        return EvidencePack(
            run_id=request.run_id,
            summary={"evidence_status": "stub"},
            markdown_path=output_root / "runs" / request.run_id / "evidence" / "evidence.md",
            json_path=output_root / "runs" / request.run_id / "evidence" / "evidence.json",
        )

    def fake_run_multi_role_analysis(request, features, evidence, output_root, provider):
        agents_dir = output_root / "runs" / request.run_id / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        (agents_dir / "call_log.jsonl").write_text("", encoding="utf-8")
        role_memos = {
            "technical_analyst": {"summary": "BTC technical setup remains constructive."},
            "defi_fundamentals_analyst": {"summary": "DeFi view."},
            "derivatives_analyst": {"summary": "Derivatives view."},
            "news_analyst": {"summary": "News view."},
            "bull_researcher": {
                "summary": "Bull view.",
                "argument": "Bull Analyst: Momentum and cycle structure still favor continuation.",
            },
            "bear_researcher": {
                "summary": "Bear view.",
                "argument": "Bear Analyst: The move is still vulnerable without broader confirmation.",
            },
            "risk_manager": {
                "summary": "Risk view.",
                "risk_views": {
                    "aggressive": "Aggressive Analyst: Lean in while structure is intact.",
                    "conservative": "Conservative Analyst: Missing coverage still argues for smaller size.",
                    "neutral": "Neutral Analyst: Split the difference and stay disciplined.",
                },
            },
            "final_arbiter": {
                "decision": {"action": "hold", "direction": "neutral", "horizon_days": 3, "position_size": "half"},
                "decision_label": "hold",
                "scorecard": {"final_score": 62, "confidence": "medium", "score_decision": "hold"},
                "key_factors": [],
                "rationale": ["score=62"],
            },
        }
        return RoleAnalysisBundle(
            run_id=request.run_id,
            role_memos=role_memos,
            markdown_paths={role: agents_dir / f"{role}.md" for role in role_memos},
            json_paths={role: agents_dir / f"{role}.json" for role in role_memos},
            index_path=agents_dir / "index.json",
        )

    def fake_schedule_review(*, request, output_root):
        review_path = output_root / "reviews" / "pending" / f"{request.run_id}.json"
        review_path.parent.mkdir(parents=True, exist_ok=True)
        review_path.write_text('{"status":"pending"}', encoding="utf-8")
        return review_path

    result = run_workflow(
        request=request,
        sources_config={"sources": {"openbb": {"enabled": True}}},
        output_root=tmp_path,
        collect_market_data_fn=fake_collect_market_data,
        build_feature_bundle_fn=fake_build_feature_bundle,
        build_evidence_pack_fn=fake_build_evidence_pack,
        run_multi_role_analysis_fn=fake_run_multi_role_analysis,
        schedule_review_fn=fake_schedule_review,
    )

    card_text = result["artifacts"]["research_card"].read_text(encoding="utf-8")
    assert "3. Bench Evidence" in card_text
    assert "4. Prosecution" in card_text
    assert "5. Defense" in card_text
    assert "6. Sentencing / Guardrails" in card_text
    assert "Bull Analyst: Momentum and cycle structure still favor continuation." in card_text
    assert "Bear Analyst: The move is still vulnerable without broader confirmation." in card_text
    assert "Aggressive Analyst: Lean in while structure is intact." in card_text
    assert "Conservative Analyst: Missing coverage still argues for smaller size." in card_text
    assert "Neutral Analyst: Split the difference and stay disciplined." in card_text
    assert "$35,000" not in card_text
    assert "$37,500" not in card_text
