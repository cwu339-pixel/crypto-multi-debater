from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from crypto_research_agent.agents.provider import default_analysis_provider
from crypto_research_agent.agents.runner import final_decision_label, run_multi_role_analysis
from crypto_research_agent.data_layer.service import collect_market_data
from crypto_research_agent.data_prep.features import build_feature_bundle
from crypto_research_agent.logging.run_logger import persist_partial_run_state, persist_run_state
from crypto_research_agent.orchestration.state import RunArtifacts, RunState
from crypto_research_agent.review_loop.service import schedule_review
from crypto_research_agent.research.evidence_pack import build_evidence_pack
from crypto_research_agent.storage.artifacts import resolve_display_artifact_paths
from crypto_research_agent.schemas import (
    EvidencePack,
    FeatureBundle,
    RawDataBundle,
    ResearchRequest,
    RoleAnalysisBundle,
)


def run_workflow(
    *,
    request: ResearchRequest,
    sources_config: dict[str, Any],
    output_root: Path,
    collect_market_data_fn: Callable[..., RawDataBundle] = collect_market_data,
    build_feature_bundle_fn: Callable[..., FeatureBundle] = build_feature_bundle,
    build_evidence_pack_fn: Callable[..., EvidencePack] = build_evidence_pack,
    run_multi_role_analysis_fn: Callable[..., RoleAnalysisBundle] = run_multi_role_analysis,
    schedule_review_fn: Callable[..., Path] = schedule_review,
) -> dict[str, Any]:
    stages = {
        "data_collection": "pending",
        "feature_engineering": "pending",
        "evidence_collection": "pending",
        "multi_role_analysis": "pending",
        "decisioning": "pending",
        "review_loop": "pending",
    }
    persist_partial_run_state(
        request=request,
        output_root=output_root,
        stages=stages,
        status="running",
    )

    raw_data = None
    features = None
    evidence = None
    role_analysis = None
    review_task_path = None

    try:
        stages["data_collection"] = "in_progress"
        persist_partial_run_state(
            request=request,
            output_root=output_root,
            stages=stages,
            status="running",
        )
        raw_data = collect_market_data_fn(
            request=request,
            sources_config=sources_config,
            output_root=output_root,
        )
        stages["data_collection"] = "completed"
        persist_partial_run_state(
            request=request,
            output_root=output_root,
            stages=stages,
            raw_data=raw_data,
            status="running",
        )

        stages["feature_engineering"] = "in_progress"
        persist_partial_run_state(
            request=request,
            output_root=output_root,
            stages=stages,
            raw_data=raw_data,
            status="running",
        )
        features = build_feature_bundle_fn(
            request=request,
            raw_data=raw_data,
            output_root=output_root,
        )
        stages["feature_engineering"] = "completed"
        persist_partial_run_state(
            request=request,
            output_root=output_root,
            stages=stages,
            raw_data=raw_data,
            features=features,
            status="running",
        )

        stages["evidence_collection"] = "in_progress"
        persist_partial_run_state(
            request=request,
            output_root=output_root,
            stages=stages,
            raw_data=raw_data,
            features=features,
            status="running",
        )
        evidence = build_evidence_pack_fn(
            request=request,
            raw_data=raw_data,
            features=features,
            output_root=output_root,
        )
        stages["evidence_collection"] = "completed"
        persist_partial_run_state(
            request=request,
            output_root=output_root,
            stages=stages,
            raw_data=raw_data,
            features=features,
            evidence=evidence,
            status="running",
        )

        stages["multi_role_analysis"] = "in_progress"
        persist_partial_run_state(
            request=request,
            output_root=output_root,
            stages=stages,
            raw_data=raw_data,
            features=features,
            evidence=evidence,
            status="running",
        )
        analysis_provider = default_analysis_provider()
        role_analysis = run_multi_role_analysis_fn(
            request=request,
            features=features,
            evidence=evidence,
            output_root=output_root,
            provider=analysis_provider,
        )
        stages["multi_role_analysis"] = "completed"
        stages["decisioning"] = "in_progress"
        stages["decisioning"] = "completed"
        initial_state = RunState(
            request=request,
            raw_data=raw_data,
            features=features,
            evidence=evidence,
            role_analysis=role_analysis,
            artifacts=RunArtifacts(
                run_json=Path(),
                artifact_index=Path(),
                research_card=Path(),
            ),
            stages=stages,
        )
        artifacts = persist_run_state(initial_state, output_root=output_root)

        stages["review_loop"] = "in_progress"
        review_task_path = schedule_review_fn(
            request=request,
            output_root=output_root,
        )
        stages["review_loop"] = "scheduled"
        display_artifacts = resolve_display_artifact_paths(
            output_root=output_root,
            asset=request.asset,
            run_id=request.run_id,
        )
        state = RunState(
            request=request,
            raw_data=raw_data,
            features=features,
            evidence=evidence,
            role_analysis=role_analysis,
            artifacts=artifacts,
            stages=stages,
        )
        artifacts = persist_run_state(state, output_root=output_root)
    except Exception as exc:
        failed_stage = next((name for name, value in stages.items() if value == "in_progress"), "unknown")
        stages[failed_stage] = "failed"
        persist_partial_run_state(
            request=request,
            output_root=output_root,
            stages=stages,
            raw_data=raw_data,
            features=features,
            evidence=evidence,
            role_analysis=role_analysis,
            status="failed",
            failed_stage=failed_stage,
            error_type=type(exc).__name__,
            error_detail=str(exc),
        )
        raise

    return {
        "status": "framework_ready",
        "run_id": request.run_id,
        "request": {
            "asset": request.asset,
            "horizon_days": request.horizon_days,
            "thesis": request.thesis,
        },
        "sources": {
            source: result.to_dict()
            for source, result in raw_data.source_results.items()
        },
        "coverage_gaps": raw_data.coverage_gaps,
        "feature_summary": features.summary,
        "evidence_summary": evidence.summary,
        "final_decision": final_decision_label(role_analysis.role_memos["final_arbiter"]),
        "artifacts": {
            "run_json": artifacts.run_json,
            "artifact_index": artifacts.artifact_index,
            "research_card": artifacts.research_card,
            "provenance": raw_data.provenance_path,
            "features": features.features_path,
            "feature_notes": features.notes_path,
            "evidence_markdown": evidence.markdown_path,
            "evidence_json": evidence.json_path,
            "roles_index": role_analysis.index_path,
            "roles_call_log": role_analysis.index_path.parent / "call_log.jsonl",
            "roles_debate_log": role_analysis.index_path.parent / "debate_log.jsonl",
            "review_task": review_task_path,
            "review_status_path": display_artifacts["review_status"],
        },
    }
