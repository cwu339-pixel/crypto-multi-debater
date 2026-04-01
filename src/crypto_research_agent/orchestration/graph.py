from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from crypto_research_agent.agents.provider import default_analysis_provider
from crypto_research_agent.agents.runner import final_decision_label, run_multi_role_analysis
from crypto_research_agent.data_layer.service import collect_market_data
from crypto_research_agent.data_prep.features import build_feature_bundle
from crypto_research_agent.logging.run_logger import persist_run_state
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
    raw_data = collect_market_data_fn(
        request=request,
        sources_config=sources_config,
        output_root=output_root,
    )
    features = build_feature_bundle_fn(
        request=request,
        raw_data=raw_data,
        output_root=output_root,
    )
    evidence = build_evidence_pack_fn(
        request=request,
        raw_data=raw_data,
        features=features,
        output_root=output_root,
    )
    analysis_provider = default_analysis_provider()
    role_analysis = run_multi_role_analysis_fn(
        request=request,
        features=features,
        evidence=evidence,
        output_root=output_root,
        provider=analysis_provider,
    )
    review_task_path = schedule_review_fn(
        request=request,
        output_root=output_root,
    )
    stages = {
        "data_collection": "completed",
        "feature_engineering": "completed",
        "evidence_collection": "completed",
        "multi_role_analysis": "completed",
        "decisioning": "completed",
        "review_loop": "scheduled",
    }
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
    return {
        "status": "framework_ready",
        "run_id": state.request.run_id,
        "request": {
            "asset": state.request.asset,
            "horizon_days": state.request.horizon_days,
            "thesis": state.request.thesis,
        },
        "sources": {
            source: result.to_dict()
            for source, result in state.raw_data.source_results.items()
        },
        "coverage_gaps": state.raw_data.coverage_gaps,
        "feature_summary": state.features.summary,
        "evidence_summary": state.evidence.summary,
        "final_decision": final_decision_label(state.role_analysis.role_memos["final_arbiter"]),
        "artifacts": {
            "run_json": state.artifacts.run_json,
            "artifact_index": state.artifacts.artifact_index,
            "research_card": state.artifacts.research_card,
            "provenance": state.raw_data.provenance_path,
            "features": state.features.features_path,
            "feature_notes": state.features.notes_path,
            "evidence_markdown": state.evidence.markdown_path,
            "evidence_json": state.evidence.json_path,
            "roles_index": state.role_analysis.index_path,
            "roles_call_log": state.role_analysis.index_path.parent / "call_log.jsonl",
            "review_task": review_task_path,
            "review_status_path": display_artifacts["review_status"],
        },
    }
