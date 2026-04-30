from crypto_research_agent.scoring import ScoreInputs, build_scorecard, compute_weighted_score


def test_compute_weighted_score_matches_report_example() -> None:
    result = compute_weighted_score(
        ScoreInputs(
            momentum=65,
            liquidity=80,
            derivatives=40,
            defi=70,
            onchain=55,
            sentiment=60,
            data_quality_penalty=-10,
        )
    )

    assert result.final_score == 47
    assert result.confidence == "low"


def test_build_scorecard_from_pipeline_inputs() -> None:
    scorecard = build_scorecard(
        feature_summary={
            "feature_status": "complete",
            "latest_close": 100.0,
            "return_1d_pct": 5.0,
            "return_total_pct": 20.0,
            "avg_volume": 1000.0,
        },
        coverage_gaps=["coinglass:missing_api_key"],
        evidence_summary={"evidence_status": "stub", "source": "local_stub"},
    )

    assert scorecard["final_score"] == 51
    assert scorecard["action_score"] == 51
    assert scorecard["confidence"] == "medium"
    assert scorecard["score_decision"] == "avoid"
    assert scorecard["data_quality"]["penalty"] == -5.0


def test_build_scorecard_uses_enriched_derivatives_and_technical_fields() -> None:
    scorecard = build_scorecard(
        feature_summary={
            "feature_status": "complete",
            "latest_close": 100.0,
            "return_1d_pct": 2.0,
            "return_total_pct": 8.0,
            "return_30d_pct": 15.0,
            "price_vs_sma200_pct": 12.0,
            "rsi_14": 62.0,
            "avg_volume": 1_000_000.0,
            "derivatives_funding_rate_latest": 0.006,
            "derivatives_open_interest_change_pct": 4.0,
            "derivatives_total_liquidation_usd_24h": 50_000_000.0,
            "mc_tvl_ratio": 0.8,
            "defi_tvl_change_7d_pct": 5.0,
            "defi_stablecoin_apy_change_7d": 0.15,
            "halving_cycle_window": "post_halving_sweet_spot",
        },
        coverage_gaps=[],
        evidence_summary={"evidence_status": "stub", "source": "local_stub"},
    )

    assert scorecard["inputs"]["momentum"] > 60
    assert scorecard["inputs"]["derivatives"] > 60
    assert scorecard["inputs"]["defi"] > 60
    assert scorecard["inputs"]["onchain"] > 60
    assert scorecard["final_score"] >= 55
    assert scorecard["score_decision"] == "hold"


def test_build_scorecard_avoid_on_weak_inputs() -> None:
    scorecard = build_scorecard(
        feature_summary={
            "feature_status": "complete",
            "latest_close": 100.0,
            "return_1d_pct": -3.0,
            "return_total_pct": -25.0,
            "avg_volume": 100.0,
        },
        coverage_gaps=["coinglass:missing_api_key", "defillama:missing_api_key"],
        evidence_summary={"evidence_status": "stub", "source": "local_stub"},
    )

    assert scorecard["final_score"] < 50
    assert scorecard["score_decision"] == "avoid"
    assert scorecard["data_quality"]["penalty"] == -5.0


def test_build_scorecard_can_be_high_confidence_avoid() -> None:
    scorecard = build_scorecard(
        feature_summary={
            "feature_status": "complete",
            "latest_close": 100.0,
            "return_1d_pct": -6.0,
            "return_total_pct": -35.0,
            "return_30d_pct": -18.0,
            "price_vs_sma200_pct": -20.0,
            "rsi_14": 40.0,
            "avg_volume": 1_000_000.0,
            "regime": "bear",
            "derivatives_funding_rate_latest": -0.002,
            "derivatives_open_interest_change_pct": -2.0,
            "defi_tvl_change_7d_pct": -8.0,
            "mc_tvl_ratio": 3.1,
            "defi_stablecoin_apy_change_7d": -0.1,
        },
        coverage_gaps=[],
        evidence_summary={"evidence_status": "complete", "source": "live"},
    )

    assert scorecard["final_score"] < 55
    assert scorecard["score_decision"] == "avoid"
    assert scorecard["confidence"] == "high"


def test_build_scorecard_core_data_failure_forces_low_confidence() -> None:
    scorecard = build_scorecard(
        feature_summary={
            "feature_status": "incomplete",
            "latest_close": 0.0,
            "avg_volume": 0.0,
        },
        coverage_gaps=["openbb:missing_price_feed"],
        evidence_summary={"evidence_status": "complete", "source": "live"},
    )

    assert scorecard["confidence"] == "low"
    assert scorecard["data_quality"]["core_complete"] is False


def test_build_scorecard_ignores_historical_unavailable_gaps() -> None:
    scorecard = build_scorecard(
        feature_summary={
            "feature_status": "complete",
            "latest_close": 100.0,
            "return_1d_pct": 1.0,
            "return_total_pct": 5.0,
            "avg_volume": 1000.0,
        },
        coverage_gaps=["coinglass:historical_unavailable", "defillama:historical_unavailable"],
        evidence_summary={"evidence_status": "stub", "source": "historical_backtest"},
    )

    assert scorecard["inputs"]["derivatives"] == 60.0
    assert scorecard["inputs"]["defi"] == 60.0
    assert scorecard["inputs"]["data_quality_penalty"] == 0.0
    assert scorecard["score_decision"] == "hold"
