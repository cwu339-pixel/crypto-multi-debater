from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from crypto_research_agent.agents.runner import final_decision_label, risk_bias_label, role_summary_text
from crypto_research_agent.orchestration.state import RunArtifacts, RunState


def resolve_display_artifact_paths(*, output_root: Path, asset: str, run_id: str) -> dict[str, Path | None]:
    review_completed = Path(output_root) / "reviews" / "completed" / f"{run_id}.json"
    review_pending = Path(output_root) / "reviews" / "pending" / f"{run_id}.json"
    return {
        "review_status": review_completed if review_completed.exists() else review_pending if review_pending.exists() else None,
    }


def write_partial_run_artifacts(
    *,
    request,
    output_root: Path,
    stages: dict[str, str],
    raw_data=None,
    features=None,
    evidence=None,
    role_analysis=None,
    status: str = "running",
    failed_stage: str | None = None,
    error_type: str | None = None,
    error_detail: str | None = None,
) -> RunArtifacts:
    run_root = Path(output_root) / "runs" / request.run_id
    run_root.mkdir(parents=True, exist_ok=True)

    card_dir = Path(output_root) / "research_cards" / request.as_of_utc.date().isoformat()
    card_dir.mkdir(parents=True, exist_ok=True)

    run_json = run_root / "run.json"
    artifact_index = run_root / "artifacts.json"
    research_card = card_dir / f"{request.asset}_{request.run_id}.md"
    display_paths = resolve_display_artifact_paths(
        output_root=output_root,
        asset=request.asset,
        run_id=request.run_id,
    )

    run_payload = {
        "run_id": request.run_id,
        "request": {
            "asset": request.asset,
            "thesis": request.thesis,
            "horizon_days": request.horizon_days,
            "as_of_utc": request.as_of_utc.isoformat(),
        },
        "status": status,
        "failed_stage": failed_stage,
        "error_type": error_type,
        "error_detail": error_detail,
        "stages": stages,
        "coverage_gaps": list(raw_data.coverage_gaps) if raw_data is not None else [],
        "provenance_path": str(raw_data.provenance_path) if raw_data is not None else None,
        "features_path": str(features.features_path) if features is not None else None,
        "evidence_path": str(evidence.json_path) if evidence is not None else None,
        "roles_index_path": str(role_analysis.index_path) if role_analysis is not None else None,
        "roles_call_log_path": (
            str(role_analysis.index_path.parent / "call_log.jsonl")
            if role_analysis is not None
            else None
        ),
        "roles_debate_log_path": (
            str(role_analysis.index_path.parent / "debate_log.jsonl")
            if role_analysis is not None
            else None
        ),
        "final_decision": final_decision_label(role_analysis.role_memos.get("final_arbiter", {}))
        if role_analysis is not None
        else None,
        "scorecard": (
            role_analysis.role_memos.get("final_arbiter", {}).get("scorecard")
            if role_analysis is not None
            else None
        ),
        "review_status_path": str(display_paths["review_status"]) if display_paths["review_status"] else None,
    }
    run_json.write_text(json.dumps(run_payload, indent=2), encoding="utf-8")

    artifact_index_payload = {
        "run_json": str(run_json),
        "provenance": str(raw_data.provenance_path) if raw_data is not None else None,
        "features": str(features.features_path) if features is not None else None,
        "feature_notes": str(features.notes_path) if features is not None else None,
        "evidence_markdown": str(evidence.markdown_path) if evidence is not None else None,
        "evidence_json": str(evidence.json_path) if evidence is not None else None,
        "roles_index": str(role_analysis.index_path) if role_analysis is not None else None,
        "roles_call_log": str(role_analysis.index_path.parent / "call_log.jsonl") if role_analysis is not None else None,
        "roles_debate_log": str(role_analysis.index_path.parent / "debate_log.jsonl") if role_analysis is not None else None,
        "research_card": str(research_card),
        "review_status": str(display_paths["review_status"]) if display_paths["review_status"] else None,
        "scorecard": role_analysis.role_memos.get("final_arbiter", {}).get("scorecard") if role_analysis is not None else None,
        "raw_data": (
            {
                source: [str(path) for path in result.artifact_paths]
                for source, result in raw_data.source_results.items()
            }
            if raw_data is not None
            else {}
        ),
        "roles": (
            {
                role: {
                    "markdown_path": str(role_analysis.markdown_paths[role]),
                    "json_path": str(role_analysis.json_paths[role]),
                }
                for role in role_analysis.role_memos
            }
            if role_analysis is not None
            else {}
        ),
    }
    artifact_index.write_text(json.dumps(artifact_index_payload, indent=2), encoding="utf-8")

    if role_analysis is not None:
        state = RunState(
            request=request,
            raw_data=raw_data,
            features=features,
            evidence=evidence,
            role_analysis=role_analysis,
            artifacts=RunArtifacts(run_json=run_json, artifact_index=artifact_index, research_card=research_card),
            stages=stages,
        )
        research_card.write_text(_render_framework_card(state=state, output_root=output_root), encoding="utf-8")

    return RunArtifacts(
        run_json=run_json,
        artifact_index=artifact_index,
        research_card=research_card,
    )


def write_run_artifacts(state: RunState, *, output_root: Path) -> RunArtifacts:
    return write_partial_run_artifacts(
        request=state.request,
        output_root=output_root,
        stages=state.stages,
        raw_data=state.raw_data,
        features=state.features,
        evidence=state.evidence,
        role_analysis=state.role_analysis,
        status="completed",
    )


def refresh_research_card_from_run(*, run_json_path: Path, output_root: Path) -> Path:
    run_payload = json.loads(Path(run_json_path).read_text(encoding="utf-8"))
    request = run_payload.get("request", {})
    request_asset = str(request.get("asset", "UNKNOWN"))
    request_run_id = _resolve_run_id(run_payload=run_payload, run_json_path=run_json_path)
    request_date = str(request.get("as_of_utc", "unknown"))[:10]
    research_card = (
        Path(output_root)
        / "research_cards"
        / request_date
        / f"{request_asset}_{request_run_id}.md"
    )
    research_card.parent.mkdir(parents=True, exist_ok=True)
    research_card.write_text(
        _render_framework_card_from_payload(run_payload=run_payload, output_root=output_root),
        encoding="utf-8",
    )
    return research_card


def _render_framework_card(*, state: RunState, output_root: Path) -> str:
    run_payload = {
        "run_id": state.request.run_id,
        "request": {
            "asset": state.request.asset,
            "thesis": state.request.thesis,
            "horizon_days": state.request.horizon_days,
            "as_of_utc": state.request.as_of_utc.isoformat(),
        },
        "stages": state.stages,
        "coverage_gaps": state.raw_data.coverage_gaps,
        "features_path": str(state.features.features_path),
        "evidence_path": str(state.evidence.json_path),
        "roles_index_path": str(state.role_analysis.index_path),
        "roles_call_log_path": str(_roles_call_log_path(state)),
        "roles_debate_log_path": str(_roles_debate_log_path(state)),
        "final_decision": final_decision_label(state.role_analysis.role_memos.get("final_arbiter", {})),
        "scorecard": state.role_analysis.role_memos.get("final_arbiter", {}).get("scorecard"),
        "feature_summary": state.features.summary,
        "evidence_summary": state.evidence.summary,
        "role_memos": state.role_analysis.role_memos,
    }
    return _render_framework_card_from_payload(run_payload=run_payload, output_root=output_root)


def _render_framework_card_from_payload(*, run_payload: dict[str, Any], output_root: Path) -> str:
    request = run_payload.get("request", {})
    asset = str(request.get("asset", "UNKNOWN"))
    run_id = _resolve_run_id(run_payload=run_payload, run_json_path=None)
    request_date = str(request.get("as_of_utc", "unknown"))[:10]
    feature_summary = _load_feature_summary(run_payload)
    evidence_summary = _load_evidence_summary(run_payload)
    role_memos = _load_role_memos(run_payload)
    coverage_gaps = list(run_payload.get("coverage_gaps", []))
    stages = run_payload.get("stages", {})
    final_decision = final_decision_label(role_memos.get("final_arbiter", {})) or str(
        run_payload.get("final_decision", "unknown")
    )
    final_arbiter = role_memos.get("final_arbiter", {})
    scorecard = final_arbiter.get("scorecard") or run_payload.get("scorecard", {})
    call_log_path = _resolve_call_log_path(run_payload)
    review_payload = _load_review_payload(output_root=Path(output_root), run_id=run_id)

    rating_label = final_decision.upper()
    horizon = request.get("horizon_days")

    confidence = _resolve_confidence(final_arbiter)
    confidence_display = {"high": "High", "med": "Medium", "medium": "Medium", "low": "Low"}.get(
        confidence.lower(), confidence.capitalize()
    )

    sections = [
        f"# {asset} Research Report",
        "",
        f"Processed signal: {rating_label}",
        "",
        "1. Verdict",
        _render_verdict_strip(
            horizon=horizon,
            rating_label=rating_label,
            confidence_display=confidence_display,
            scorecard=scorecard,
        ),
        "",
        "How To Read This Verdict",
        _render_verdict_guide(scorecard),
        "",
        "2. Case File",
        _render_case_file(
            asset=asset,
            request=request,
            final_decision=final_decision,
            final_arbiter=final_arbiter,
            horizon=horizon,
        ),
        "",
        "3. Bench Evidence",
        _render_bench_evidence(role_memos),
        "",
        "4. Prosecution",
        f"- {_debate_argument_text(role_memos.get('bear_researcher', {}))}",
        "",
        "5. Defense",
        f"- {_debate_argument_text(role_memos.get('bull_researcher', {}))}",
        "",
        "6. Sentencing / Guardrails",
        _render_sentencing_guardrails(final_arbiter=final_arbiter, role_memos=role_memos),
        "",
        "7. Judge's Ruling",
        _render_judges_ruling(
            final_arbiter=final_arbiter,
            role_memos=role_memos,
            asset=asset,
            horizon=horizon,
        ),
        "",
        "8. Appeal Conditions",
        _render_appeal_conditions(final_arbiter, review_payload),
        "",
        "9. Data Quality Footnote",
        _render_data_quality(coverage_gaps, feature_summary, evidence_summary),
        "",
        "Score Breakdown",
        _render_score_breakdown(scorecard, coverage_gaps),
        "",
    ]
    return "\n".join(sections)


def _str_field(memo: dict[str, Any], key: str, fallback: str = "n/a") -> str:
    value = memo.get(key)
    return str(value).strip() if isinstance(value, str) and value.strip() else fallback


def _truncate_to_sentences(text: str, n: int = 2) -> str:
    """Return first n sentences of text."""
    import re
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return " ".join(sentences[:n])


def _exec_action_line(
    final_arbiter: dict[str, Any],
    final_decision: str,
    asset: str,
    horizon: Any,
) -> str:
    decision = final_arbiter.get("decision") or {}
    confidence = _resolve_confidence(final_arbiter)
    direction = decision.get("direction", "") if isinstance(decision, dict) else ""
    direction_str = f" ({direction})" if direction and direction != "neutral" else ""
    return f"Tactical {final_decision.upper()}{direction_str} — {asset} over {horizon}d. Confidence: {confidence}."


def _render_targets(targets: Any) -> str:
    if not isinstance(targets, list) or not targets:
        return "none (avoid/hold posture)"
    parts = []
    for t in targets:
        if isinstance(t, dict):
            price = t.get("price_target", "n/a")
            pct = t.get("pct_position_to_exit", "")
            rationale = t.get("rationale", "")
            parts.append(f"{price} ({pct}{'; ' + rationale if rationale else ''})")
    return " → ".join(parts) if parts else "none"


def _render_flip_rules(final_arbiter: dict[str, Any]) -> str:
    rules = final_arbiter.get("flip_rules")
    if not isinstance(rules, list) or not rules:
        invalidation = final_arbiter.get("invalidation")
        if isinstance(invalidation, list) and invalidation:
            return "\n".join(f"- {item}" for item in invalidation)
        return "- No hard rules defined."
    lines = []
    for rule in rules:
        if isinstance(rule, dict):
            cond = rule.get("condition", "")
            posture = rule.get("new_posture", "")
            lines.append(f"- If {cond} → {posture}")
        else:
            lines.append(f"- {rule}")
    return "\n".join(lines)


def _investment_thesis_block(
    final_arbiter: dict[str, Any],
    role_memos: dict[str, dict[str, Any]],
) -> str:
    thesis = final_arbiter.get("thesis")
    if isinstance(thesis, str) and len(thesis.strip()) > 60:
        return thesis.strip()
    # fallback: synthesise from role summaries
    bull_summary = role_summary_text(role_memos.get("bull_researcher", {}))
    bear_summary = role_summary_text(role_memos.get("bear_researcher", {}))
    risk_summary = role_summary_text(role_memos.get("risk_manager", {}))
    decision = final_decision_label(final_arbiter)
    return (
        f"Decision: {decision}. "
        f"Bull case — {bull_summary} "
        f"Bear case — {bear_summary} "
        f"Risk reconciliation — {risk_summary}"
    )


def _render_gaps(gaps: list[str]) -> str:
    if not gaps:
        return "- none"
    return "\n".join(f"- {gap}" for gap in gaps)


def _render_evidence_replay_lines(evidence_summary: dict[str, Any]) -> str:
    run_mode = evidence_summary.get("run_mode")
    if not run_mode:
        return ""
    lines = [f"- Run Mode: {run_mode}"]
    note = evidence_summary.get("point_in_time_note")
    if note:
        lines.append(f"- Point-in-time Note: {note}")
    limitations = evidence_summary.get("point_in_time_limitations")
    if isinstance(limitations, list) and limitations:
        lines.append("- Point-in-time Limitations:")
        lines.extend(f"- {item}" for item in limitations)
    return "\n".join(lines)


def _render_evidence_fallback_lines(evidence_summary: dict[str, Any]) -> str:
    reason = evidence_summary.get("fallback_reason")
    if not reason:
        return ""
    lines = [f"- Evidence Fallback Reason: {reason}"]
    error_type = evidence_summary.get("fallback_error_type")
    if error_type:
        lines.append(f"- Evidence Fallback Error Type: {error_type}")
    detail = evidence_summary.get("fallback_detail")
    if detail:
        lines.append(f"- Evidence Fallback Detail: {detail}")
    return "\n".join(lines)


def _render_stage_lines(stages: dict[str, str]) -> str:
    return "\n".join(f"- {name}: {status}" for name, status in stages.items())


def _roles_call_log_path(state: RunState) -> Path:
    return state.role_analysis.index_path.parent / "call_log.jsonl"


def _roles_debate_log_path(state: RunState) -> Path:
    return state.role_analysis.index_path.parent / "debate_log.jsonl"


def _render_role_execution(call_log_path: Path | None) -> str:
    if call_log_path is None:
        return "- unavailable"
    if not call_log_path.exists():
        return "- unavailable"
    lines = call_log_path.read_text(encoding="utf-8").splitlines()
    if not lines:
        return "- unavailable"
    rendered = []
    for line in lines:
        row = json.loads(line)
        rendered.append(
            f"- {row['role']}: {row['analysis_mode']} via {row['provider']} ({row['duration_ms']} ms)"
        )
    return "\n".join(rendered)


def _render_final_rationale(final_arbiter_memo: dict[str, Any]) -> str:
    rationale = final_arbiter_memo.get("rationale")
    if not rationale:
        return "Unavailable."
    if isinstance(rationale, list):
        return ", ".join(str(item) for item in rationale)
    return str(rationale)


def _technical_display(memo: dict[str, Any]) -> str:
    thesis = _truncate_to_sentences(role_summary_text(memo), 2)
    levels = memo.get("levels", {})
    support = levels.get("support", []) if isinstance(levels, dict) else []
    resistance = levels.get("resistance", []) if isinstance(levels, dict) else []
    if support or resistance:
        extras = []
        if support:
            extras.append(f"support {_format_level(support[0])}")
        if resistance:
            extras.append(f"resistance {_format_level(resistance[0])}")
        return f"{thesis} Key levels: {', '.join(extras)}."
    return thesis


def _format_level(value: Any) -> str:
    if isinstance(value, (int, float)):
        return f"{value:.2f}"
    return str(value)


def _defi_display(memo: dict[str, Any]) -> str:
    return _truncate_to_sentences(role_summary_text(memo), 2)


def _derivatives_display(memo: dict[str, Any]) -> str:
    return _truncate_to_sentences(role_summary_text(memo), 2)


def _news_display(memo: dict[str, Any]) -> str:
    evidence_quality = memo.get("evidence_quality")
    top_catalysts = memo.get("top_catalysts")
    top_risks = memo.get("top_risks")
    catalyst_text = "No clear near-term catalyst."
    if isinstance(top_catalysts, list) and top_catalysts:
        first_catalyst = top_catalysts[0]
        if isinstance(first_catalyst, dict) and first_catalyst.get("catalyst"):
            catalyst_text = str(first_catalyst["catalyst"])
    catalyst_text = _sanitize_news_catalyst_text(catalyst_text)
    quality_text = f"Evidence quality is {evidence_quality}." if evidence_quality else ""
    if isinstance(top_risks, list) and top_risks:
        first = top_risks[0]
        if isinstance(first, dict) and first.get("risk"):
            return f"{quality_text} {catalyst_text}. Top risk: {first['risk']}".strip()
    return f"{quality_text} {catalyst_text}".strip()


def _sanitize_news_catalyst_text(text: str) -> str:
    lowered = text.lower()
    if "$" in text or "resistance" in lowered or "breakout" in lowered:
        return "No confirmed near-term catalyst with a clean price-aligned trigger"
    return text


def _debate_display(memo: dict[str, Any]) -> str:
    thesis = role_summary_text(memo)
    key_points = memo.get("key_points")
    if isinstance(key_points, list) and key_points:
        first = key_points[0]
        if isinstance(first, dict) and first.get("point"):
            return f"{thesis} Lead point: {first['point']}"
    return thesis


def _risk_display(memo: dict[str, Any]) -> str:
    summary = _truncate_to_sentences(role_summary_text(memo), 1)
    guardrails = memo.get("guardrails")
    if isinstance(guardrails, dict) and guardrails.get("sizing_recommendation"):
        return f"{summary} Suggested sizing: {guardrails['sizing_recommendation']}."
    return summary


def _debate_lead(memo: dict[str, Any]) -> str:
    """Return the lead thesis sentence only — no full argument paragraphs."""
    key_points = memo.get("key_points")
    if isinstance(key_points, list) and key_points:
        first = key_points[0]
        if isinstance(first, dict) and first.get("point"):
            return first["point"]
    return role_summary_text(memo)


def _fmt_price(value: Any) -> str:
    if isinstance(value, (int, float)):
        return f"${value:,.0f}"
    return str(value) if value is not None else "n/a"


def _fmt_pct(value: Any) -> str:
    if isinstance(value, (int, float)):
        sign = "+" if value > 0 else ""
        return f"{sign}{value:.2f}%"
    return str(value) if value is not None else "n/a"


def _render_coverage_line(gaps: list[str]) -> str:
    if not gaps:
        return "- Coverage: all sources fetched"
    labels = [g.split(":")[0] for g in gaps]
    return f"- Coverage gaps: {', '.join(labels)}"


def _render_conclusion(
    final_arbiter: dict[str, Any],
    final_decision: str,
    asset: str,
    horizon: Any,
) -> str:
    # Prefer the arbiter's one-line `summary` so the Ruling stays a verdict,
    # leaving the longer `thesis` field exclusively for the Thesis section
    # (avoids word-for-word duplication between Ruling and Thesis).
    summary = _strip_data_gap_language(_str_field(final_arbiter, "summary"))
    if len(summary) > 40:
        return summary
    thesis = _strip_data_gap_language(_str_field(final_arbiter, "thesis"))
    if len(thesis) > 80:
        return thesis
    return f"Recommendation: {final_decision.upper()} {asset} over {horizon}d horizon."


def _resolve_confidence(final_arbiter: dict[str, Any]) -> str:
    scorecard = final_arbiter.get("scorecard")
    if isinstance(scorecard, dict):
        card_confidence = scorecard.get("confidence")
        if isinstance(card_confidence, str) and card_confidence.strip():
            return card_confidence.strip()
    confidence = final_arbiter.get("confidence")
    if isinstance(confidence, str) and confidence.strip():
        return confidence.strip()
    decision = final_arbiter.get("decision")
    if isinstance(decision, dict):
        return str(decision.get("confidence", "unknown"))
    return "unknown"


def _render_executive_summary(
    *,
    asset: str,
    horizon: Any,
    final_decision: str,
    confidence_display: str,
    final_arbiter: dict[str, Any],
    scorecard: dict[str, Any],
    coverage_gaps: list[str],
) -> str:
    lines = [
        f"- Immediate posture: {_exec_action_line(final_arbiter, final_decision, asset, horizon)}",
        f"- Confidence: {confidence_display}",
    ]
    action_score = scorecard.get("action_score", scorecard.get("final_score"))
    if action_score is not None:
        lines.append(f"- Action score: {action_score}/100")
    conclusion = _render_conclusion(final_arbiter, final_decision, asset, horizon)
    if conclusion:
        lines.append(f"- Conclusion: {conclusion}")
    return "\n".join(lines)


def _render_verdict_strip(
    *,
    horizon: Any,
    rating_label: str,
    confidence_display: str,
    scorecard: dict[str, Any],
) -> str:
    lines = [
        f"- Verdict: {rating_label.title()}",
        f"- Confidence: {confidence_display}",
        f"- Horizon: {horizon}d" if horizon is not None else "- Horizon: n/a",
    ]
    action_score = scorecard.get("action_score", scorecard.get("final_score"))
    if action_score is not None:
        lines.append(f"- Action Score: {action_score}/100")
    return "\n".join(lines)


def _render_verdict_guide(scorecard: dict[str, Any]) -> str:
    data_quality = scorecard.get("data_quality") if isinstance(scorecard, dict) else None
    core_complete = data_quality.get("core_complete") if isinstance(data_quality, dict) else None
    supplementary_complete = data_quality.get("supplementary_complete") if isinstance(data_quality, dict) else None
    inputs = scorecard.get("inputs") if isinstance(scorecard, dict) else None
    data_quality_penalty = inputs.get("data_quality_penalty") if isinstance(inputs, dict) else None
    lines = [
        "- Action Score is the baseline action signal, not a return forecast.",
        "- Confidence measures agreement across core market signals, not how many supplementary APIs responded.",
    ]
    if core_complete is False:
        lines.append("- Core data is incomplete, so confidence should be treated as structurally weak.")
    elif supplementary_complete is False:
        lines.append("- Supplementary gaps contribute at most a single -5 penalty.")
    elif isinstance(data_quality_penalty, (int, float)) and data_quality_penalty < 0:
        lines.append("- Supplementary gaps contribute at most a single -5 penalty.")
    else:
        lines.append("- Data quality is clean enough that the action signal should be read on its own merits.")
    return "\n".join(lines)


def _render_case_file(
    *,
    asset: str,
    request: dict[str, Any],
    final_decision: str,
    final_arbiter: dict[str, Any],
    horizon: Any,
) -> str:
    as_of = str(request.get("as_of_utc", "unknown"))[:10]
    thesis = str(request.get("thesis", "n/a"))
    lines = [
        f"- As of: {as_of}",
        f"- Issue: whether to {final_decision.lower()} or buy {asset} over the next {horizon} days",
        f"- Thesis: {thesis}",
    ]
    conclusion = _render_conclusion(final_arbiter, final_decision, asset, horizon)
    if conclusion:
        lines.append(f"- Immediate posture: {conclusion}")
    return "\n".join(lines)


def _render_investment_thesis(
    *,
    final_arbiter: dict[str, Any],
    role_memos: dict[str, dict[str, Any]],
) -> str:
    lines = [_strip_data_gap_language(_investment_thesis_block(final_arbiter, role_memos))]
    key_factors = _render_key_factors(final_arbiter)
    if key_factors != "Unavailable.":
        lines.extend(["", "Key drivers:", f"- {key_factors}"])
    rejected = final_arbiter.get("rejected_alternative")
    if isinstance(rejected, dict) and rejected.get("alternative_action") and rejected.get("why_rejected"):
        lines.extend(
            [
                "",
                "Rejected alternative:",
                f"- {str(rejected['alternative_action']).upper()} — {_strip_data_gap_language(str(rejected['why_rejected']))}",
            ]
        )
    return "\n".join(lines)


def _render_judges_ruling(
    *,
    final_arbiter: dict[str, Any],
    role_memos: dict[str, dict[str, Any]],
    asset: str,
    horizon: Any,
) -> str:
    lines = [
        f"- Ruling: {_render_conclusion(final_arbiter, final_decision_label(final_arbiter), asset, horizon)}",
        f"- Thesis: {_strip_data_gap_language(_investment_thesis_block(final_arbiter, role_memos))}",
    ]
    key_factors = _render_key_factors(final_arbiter)
    if key_factors != "Unavailable.":
        lines.append(f"- Key factors: {key_factors}")
    rejected = final_arbiter.get("rejected_alternative")
    if isinstance(rejected, dict) and rejected.get("alternative_action") and rejected.get("why_rejected"):
        lines.append(
            f"- Rejected alternative: {str(rejected['alternative_action']).upper()} — "
            f"{_strip_data_gap_language(str(rejected['why_rejected']))}"
        )
    hard_rules = _render_flip_rules(final_arbiter)
    if hard_rules:
        lines.extend(["- Hard rules:", hard_rules])
    return "\n".join(lines)


def _render_bench_evidence(role_memos: dict[str, dict[str, Any]]) -> str:
    technical = _technical_display(role_memos.get("technical_analyst", {}))
    defi = _defi_display(role_memos.get("defi_fundamentals_analyst", {}))
    derivatives = _derivatives_display(role_memos.get("derivatives_analyst", {}))
    news = _news_display(role_memos.get("news_analyst", {}))

    lines = [
        f"- Technical Analyst: {technical}",
        f"- DeFi Analyst: {defi}",
        f"- Derivatives Analyst: {derivatives}",
        f"- News Analyst: {news}",
    ]
    return "\n".join(lines)


def _render_sentencing_guardrails(
    *,
    final_arbiter: dict[str, Any],
    role_memos: dict[str, dict[str, Any]],
) -> str:
    risk = role_memos.get("risk_manager", {})
    risk_views = risk.get("risk_views") if isinstance(risk, dict) else {}

    lines = []
    if isinstance(risk_views, dict) and risk_views:
        lines.append("- Risk roundtable:")
        if risk_views.get("aggressive"):
            lines.append(f"- {risk_views['aggressive']}")
        if risk_views.get("conservative"):
            lines.append(f"- {risk_views['conservative']}")
        if risk_views.get("neutral"):
            lines.append(f"- {risk_views['neutral']}")
        lines.append("")

    lines.append(_render_risk_controls(final_arbiter=final_arbiter, role_memos=role_memos))
    return "\n".join(lines)


def _render_risk_controls(
    *,
    final_arbiter: dict[str, Any],
    role_memos: dict[str, dict[str, Any]],
) -> str:
    lines = []
    sizing_formula = _str_field(final_arbiter, "sizing_formula")
    stop_logic = _str_field(final_arbiter, "stop_logic")
    entry_logic = _str_field(final_arbiter, "entry_logic")
    tactical_alternative = _str_field(final_arbiter, "tactical_alternative")

    if entry_logic != "n/a":
        lines.append(f"- Entry logic: {entry_logic}")
    if stop_logic != "n/a":
        lines.append(f"- Stop logic: {stop_logic}")
    if sizing_formula != "n/a":
        lines.append(f"- Sizing: {sizing_formula}")

    targets = _render_targets(final_arbiter.get("targets"))
    lines.append(f"- Targets: {targets}")

    flip_rules = _render_flip_rules(final_arbiter)
    if flip_rules:
        lines.extend(["- Hard rules that flip posture:", flip_rules])

    if tactical_alternative != "n/a":
        lines.append(f"- Tactical alternative: {tactical_alternative}")

    risk_view = _render_risk_view(final_arbiter, role_memos)
    if risk_view:
        lines.extend(["", "Current risk posture:", risk_view])

    return "\n".join(lines)


def _render_appeal_conditions(
    final_arbiter: dict[str, Any],
    review_payload: dict[str, Any] | None,
) -> str:
    lines = [_render_what_would_change(final_arbiter)]
    review_block = _render_review_plan(final_arbiter, review_payload)
    if review_block:
        lines.extend(["", review_block])
    return "\n".join(lines)


def _render_why_now(
    final_arbiter: dict[str, Any],
    role_memos: dict[str, dict[str, Any]],
) -> str:
    key_factors = final_arbiter.get("key_factors")
    if isinstance(key_factors, list) and key_factors:
        lines = []
        for i, factor in enumerate(key_factors[:3], 1):
            if isinstance(factor, dict) and factor.get("factor"):
                lines.append(f"{i}. {factor['factor']}")
            elif isinstance(factor, str):
                lines.append(f"{i}. {factor}")
        if lines:
            return "\n".join(lines)
    # fallback: extract from thesis
    thesis = final_arbiter.get("thesis", "")
    if isinstance(thesis, str) and len(thesis.strip()) > 60:
        sentences = thesis.strip().split(". ")
        lines = []
        for i, s in enumerate(sentences[:3], 1):
            s = s.strip().rstrip(".")
            if s:
                lines.append(f"{i}. {s}.")
        if lines:
            return "\n".join(lines)
    return "1. Insufficient data to summarize key factors."


def _render_what_would_change(final_arbiter: dict[str, Any]) -> str:
    lines = ["Re-evaluate only if all of the following happen:"]
    flip_rules = final_arbiter.get("flip_rules")
    if isinstance(flip_rules, list) and flip_rules:
        for rule in flip_rules:
            if isinstance(rule, dict) and rule.get("condition"):
                lines.append(f"- {rule['condition']}")
            elif isinstance(rule, str):
                lines.append(f"- {rule}")
        return "\n".join(lines)
    invalidation = final_arbiter.get("invalidation")
    if isinstance(invalidation, list) and invalidation:
        for item in invalidation:
            lines.append(f"- {item}")
        return "\n".join(lines)
    entry = _str_field(final_arbiter, "entry_logic")
    if entry != "n/a":
        lines.append(f"- {entry}")
        return "\n".join(lines)
    return "No specific invalidation conditions defined."


def _render_score_breakdown(
    scorecard: dict[str, Any],
    coverage_gaps: list[str],
) -> str:
    if not scorecard:
        return "Score data unavailable."
    lines = []
    sub_scores = scorecard.get("inputs") or scorecard.get("sub_scores") or scorecard.get("components") or {}
    if isinstance(sub_scores, dict) and sub_scores:
        score_labels = {
            "momentum": "Momentum",
            "liquidity": "Liquidity",
            "derivatives": "Derivatives",
            "defi": "Fundamentals / Flows",
            "onchain": "Trend / Regime",
            "sentiment": "Macro / News",
            "data_quality_penalty": "Data quality penalty",
        }
        for label in ("momentum", "liquidity", "derivatives", "defi", "onchain", "sentiment", "data_quality_penalty"):
            if label in sub_scores:
                lines.append(f"- {score_labels[label]}: {sub_scores[label]}")
    data_quality = scorecard.get("data_quality")
    if isinstance(data_quality, dict):
        core_complete = data_quality.get("core_complete")
        supplementary_complete = data_quality.get("supplementary_complete")
        penalty = data_quality.get("penalty")
        if core_complete is not None:
            lines.append(f"- Core data complete: {core_complete}")
        if supplementary_complete is not None:
            lines.append(f"- Supplementary data complete: {supplementary_complete}")
        if penalty is not None and "data_quality_penalty" not in sub_scores:
            lines.append(f"- Data quality penalty: {penalty}")
    # Flat -5 penalty for any supplementary gaps (capped, not per-source)
    core_gaps, supp_gaps = _classify_gaps(coverage_gaps)
    if core_gaps and "data_quality_penalty" not in sub_scores:
        lines.append(f"- Core data penalty: -{len(core_gaps) * 10}")
    if supp_gaps and "data_quality_penalty" not in sub_scores:
        lines.append("- Supplementary data penalty: -5")
    final_score = scorecard.get("final_score")
    if final_score is not None:
        lines.append(f"- Total: {final_score}/100")
    if not lines:
        final_score = scorecard.get("final_score", "n/a")
        return f"- Total: {final_score}/100"
    return "\n".join(lines)


def _classify_gaps(coverage_gaps: list[str]) -> tuple[list[str], list[str]]:
    """Split gaps into core (price/volume) vs supplementary (everything else)."""
    core_keywords = {"price", "ohlcv", "candle", "volume"}
    core: list[str] = []
    supplementary: list[str] = []
    for gap in coverage_gaps:
        label = gap.split(":")[0].lower()
        if any(kw in label for kw in core_keywords):
            core.append(gap)
        else:
            supplementary.append(gap)
    return core, supplementary


def _render_data_quality(
    coverage_gaps: list[str],
    feature_summary: dict[str, Any],
    evidence_summary: dict[str, Any] | None = None,
) -> str:
    lines = []
    if not coverage_gaps:
        lines.append("Overall: Good — all sources fetched.")
    else:
        core_gaps, supp_gaps = _classify_gaps(coverage_gaps)
        if core_gaps:
            lines.append("Overall: Low — core price data missing.")
            lines.append("")
            lines.append("Missing core inputs:")
            for g in core_gaps:
                lines.append(f"- {g.split(':')[0]}")
        else:
            lines.append("Overall: Mixed — core data is intact, but supplementary flow and catalyst inputs are partial.")
        if supp_gaps:
            lines.append("")
            lines.append("Supplementary sources not available:")
            for g in supp_gaps:
                lines.append(f"- {g.split(':')[0]}")
    if evidence_summary:
        run_mode = evidence_summary.get("run_mode")
        if run_mode:
            lines.append(f"\nRun Mode: {run_mode}")
        note = evidence_summary.get("point_in_time_note")
        if note:
            lines.append(f"Point-in-time Note: {note}")
        limitations = evidence_summary.get("point_in_time_limitations")
        if isinstance(limitations, list) and limitations:
            lines.append("Point-in-time Limitations:")
            for item in limitations:
                lines.append(f"- {item}")
    return "\n".join(lines)


def _strip_data_gap_language(text: str) -> str:
    if not text:
        return text
    sentences = [segment.strip() for segment in text.replace("\n", " ").split(". ") if segment.strip()]
    filtered: list[str] = []
    drop_markers = (
        "data gap",
        "data gaps",
        "missing ",
        "unavailable",
        "insufficient evidence",
        "coverage gap",
        "coverage gaps",
        "critical gaps",
        "incomplete defi",
        "incomplete de-fi",
    )
    for sentence in sentences:
        lowered = sentence.lower()
        if any(marker in lowered for marker in drop_markers):
            continue
        filtered.append(sentence.rstrip("."))
    if not filtered:
        return text
    rebuilt = ". ".join(filtered).strip()
    return rebuilt if rebuilt.endswith(".") else f"{rebuilt}."


def _render_risk_view(
    final_arbiter: dict[str, Any],
    role_memos: dict[str, dict[str, Any]],
) -> str:
    risk_memo = role_memos.get("risk_manager", {})
    decision = final_arbiter.get("decision") or {}
    action = decision.get("action", "avoid") if isinstance(decision, dict) else "avoid"

    lines = ["Current posture:"]
    if action in ("avoid", "hold"):
        lines.append("- No new long entry")
        lines.append("- Do not chase upside without confirmation")
        lines.append("- Stay on watchlist only")
    elif action == "buy":
        size = decision.get("position_size", "half") if isinstance(decision, dict) else "half"
        lines.append(f"- Enter long, {size} size")
        lines.append(f"- Stops: {_str_field(final_arbiter, 'stop_logic')}")
    elif action == "sell":
        lines.append("- Exit or reduce exposure")
        lines.append(f"- Stops: {_str_field(final_arbiter, 'stop_logic')}")

    # Key risks
    key_risks = final_arbiter.get("key_risks")
    if isinstance(key_risks, list) and key_risks:
        lines.append("")
        lines.append("Main risks to this stance:")
        for risk_item in key_risks[:3]:
            if isinstance(risk_item, dict) and risk_item.get("risk"):
                lines.append(f"- {risk_item['risk']}")
            elif isinstance(risk_item, str):
                lines.append(f"- {risk_item}")

    return "\n".join(lines)


def _render_review_plan(
    final_arbiter: dict[str, Any],
    review_payload: dict[str, Any] | None,
) -> str:
    review_plan = final_arbiter.get("review_plan")
    lines = []
    review_due_added = False
    if isinstance(review_plan, dict):
        days = review_plan.get("review_at_days")
        if days:
            lines.append(f"Review due: {days} days from now")
            review_due_added = True
        checks = review_plan.get("what_to_check")
        if isinstance(checks, list) and checks:
            lines.append("")
            lines.append("At review, check:")
            for check in checks:
                lines.append(f"- {check}")
    if review_payload:
        review_status = str(review_payload.get("review_status") or review_payload.get("status") or "pending")
        if review_payload.get("due_at_utc") and not review_due_added:
            lines.append(f"\nReview due: {review_payload['due_at_utc']}")
        lines.append(f"Latest review: {review_status}")
    if not lines:
        lines.append("No review plan defined.")
    return "\n".join(lines)


def _render_debate_summary(role_memos: dict[str, dict[str, Any]]) -> str:
    bull = role_memos.get("bull_researcher", {})
    bear = role_memos.get("bear_researcher", {})
    risk = role_memos.get("risk_manager", {})
    lines = [
        f"- Bull Debate: {_debate_argument_text(bull)}",
        f"- Bear Debate: {_debate_argument_text(bear)}",
    ]
    risk_views = risk.get("risk_views")
    if isinstance(risk_views, dict):
        if risk_views.get("aggressive"):
            lines.append(f"- Aggressive Risk: {risk_views['aggressive']}")
        if risk_views.get("conservative"):
            lines.append(f"- Conservative Risk: {risk_views['conservative']}")
        if risk_views.get("neutral"):
            lines.append(f"- Neutral Risk: {risk_views['neutral']}")
    return "\n".join(lines)


def _debate_argument_text(memo: dict[str, Any]) -> str:
    argument = memo.get("argument")
    if isinstance(argument, str) and argument.strip():
        return argument
    return role_summary_text(memo)


def _render_key_factors(memo: dict[str, Any]) -> str:
    factors = memo.get("key_factors")
    if not isinstance(factors, list) or not factors:
        return "Unavailable."
    rendered = []
    for item in factors[:4]:
        if isinstance(item, dict) and item.get("factor"):
            rendered.append(f"{item['factor']} ({item.get('source_role', 'unknown')})")
    return ", ".join(rendered) if rendered else "Unavailable."


def _load_feature_summary(run_payload: dict[str, Any]) -> dict[str, Any]:
    inline_summary = run_payload.get("feature_summary")
    if isinstance(inline_summary, dict):
        return inline_summary
    return _load_json_file(run_payload.get("features_path"))


def _load_evidence_summary(run_payload: dict[str, Any]) -> dict[str, Any]:
    inline_summary = run_payload.get("evidence_summary")
    if isinstance(inline_summary, dict):
        return inline_summary
    return _load_json_file(run_payload.get("evidence_path"))


def _load_role_memos(run_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    inline_role_memos = run_payload.get("role_memos")
    if isinstance(inline_role_memos, dict):
        return {
            str(role): memo
            for role, memo in inline_role_memos.items()
            if isinstance(memo, dict)
        }

    roles_index = _load_json_file(run_payload.get("roles_index_path"))
    role_memos: dict[str, dict[str, Any]] = {}
    roles = roles_index.get("roles", {})
    if not isinstance(roles, dict):
        return role_memos
    for role, details in roles.items():
        if not isinstance(details, dict):
            continue
        memo = _load_json_file(details.get("json_path"))
        if memo:
            role_memos[str(role)] = memo
    return role_memos


def _load_json_file(path_value: object) -> dict[str, Any]:
    if not path_value:
        return {}
    path = Path(str(path_value))
    if not path.exists():
        return {}
    loaded = json.loads(path.read_text(encoding="utf-8"))
    return loaded if isinstance(loaded, dict) else {}


def _resolve_call_log_path(run_payload: dict[str, Any]) -> Path | None:
    direct_path = run_payload.get("roles_call_log_path")
    if direct_path:
        return Path(str(direct_path))
    roles_index_path = run_payload.get("roles_index_path")
    if roles_index_path:
        return Path(str(roles_index_path)).parent / "call_log.jsonl"
    return None


def _resolve_run_id(*, run_payload: dict[str, Any], run_json_path: Path | None) -> str:
    run_id = run_payload.get("run_id")
    if isinstance(run_id, str) and run_id:
        return run_id
    if run_json_path is not None:
        return run_json_path.parent.name
    features_path = run_payload.get("features_path")
    if features_path:
        return Path(str(features_path)).parents[1].name
    roles_index_path = run_payload.get("roles_index_path")
    if roles_index_path:
        return Path(str(roles_index_path)).parents[1].name
    return "unknown_run"


def _load_review_payload(*, output_root: Path, run_id: str) -> dict[str, Any] | None:
    completed_path = output_root / "reviews" / "completed" / f"{run_id}.json"
    if completed_path.exists():
        return json.loads(completed_path.read_text(encoding="utf-8"))
    pending_path = output_root / "reviews" / "pending" / f"{run_id}.json"
    if pending_path.exists():
        return json.loads(pending_path.read_text(encoding="utf-8"))
    return None


def _render_review_lines(review_payload: dict[str, Any] | None) -> str:
    if not review_payload:
        return "- Latest Review: unavailable"

    review_status = str(review_payload.get("review_status") or review_payload.get("status") or "pending")
    lines = [f"- Latest Review: {review_status}"]
    if review_payload.get("due_at_utc"):
        lines.append(f"- Review Due: {review_payload['due_at_utc']}")
    if review_payload.get("reviewed_at_utc"):
        lines.append(f"- Reviewed At: {review_payload['reviewed_at_utc']}")

    decision_outcome = review_payload.get("decision_outcome", {})
    if isinstance(decision_outcome, dict) and decision_outcome:
        decision_correct = decision_outcome.get("decision_correct")
        if decision_correct is True:
            lines.append("- Decision outcome: correct")
        elif decision_correct is False:
            lines.append("- Decision outcome: incorrect")
        if decision_outcome.get("future_return_pct") is not None:
            lines.append(f"- Observed forward return (%): {decision_outcome['future_return_pct']}")

    if review_payload.get("summary"):
        lines.append(f"- Review Summary: {review_payload['summary']}")
    return "\n".join(lines)
