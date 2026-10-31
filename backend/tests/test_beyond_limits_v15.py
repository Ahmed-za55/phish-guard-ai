import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.beyond_limits_v15.pillar_1_crime_scene_reconstruction import DigitalCrimeSceneReconstructor
from app.beyond_limits_v15.pillar_2_research_scientist import AutonomousSecurityResearchScientist
from app.beyond_limits_v15.pillar_3_verifiable_defense import VerifiableAutonomousDefenseKernel
from app.beyond_limits_v15.pillar_4_civilization_resilience import CivilizationAndFailureIntelligence
from app.beyond_limits_v15.beyond_limits_master import BeyondTheLimitsMasterNexusV15

def test_beyond_the_limits_v15_suite():
    print("=" * 88)
    print(" PHISHGUARD SOVEREIGN v15.0 — EMPIRICAL VERIFICATION OF THE 3 CORE PILLARS")
    print("=" * 88)

    # -------------------------------------------------------------------------
    # 1. Test Crime Scene Reconstruction (Out-of-Order Logs + Missing Stages + Contradictions)
    # -------------------------------------------------------------------------
    raw_logs = [
        {"event_id": "e3", "timestamp": 300.0, "stage": "TOKEN_ISSUANCE", "source": "idp_sensor", "actor_entity": "victim_host", "target_entity": "cloud_idp", "source_reliability": 0.95, "claim": "MALICIOUS"},
        {"event_id": "e1", "timestamp": 100.0, "stage": "INITIAL_LURE", "source": "email_gw", "actor_entity": "attacker_infra", "target_entity": "victim_host", "source_reliability": 0.90, "claim": "MALICIOUS"},
        {"event_id": "e2_conflict", "timestamp": 150.0, "stage": "INITIAL_LURE", "source": "stale_allowlist", "actor_entity": "attacker_infra", "target_entity": "victim_host", "source_reliability": 0.30, "claim": "BENIGN"}
    ]
    scene = DigitalCrimeSceneReconstructor.reconstruct_crime_scene(raw_logs)

    # يجب أن يرتب الأحداث زمنياً (e1 ثم e2_conflict ثم e3)
    assert scene["unified_timeline"][0]["event_id"] == "e1"
    assert scene["unified_timeline"][-1]["event_id"] == "e3"

    # يجب أن يكتشف المرحلتين المفقودتين بين INITIAL_LURE و TOKEN_ISSUANCE
    missing_stages = [g["missing_kill_chain_stage"] for g in scene["inferred_evidence_gaps"]]
    assert "LINK_EXECUTION" in missing_stages
    assert "CREDENTIAL_SUBMISSION" in missing_stages

    # يجب أن يحسم التناقض لصالح MALICIOUS بسبب وزن الموثوقية (0.90 مقابل 0.30)
    assert scene["contradiction_resolutions"][0]["resolved_state"] == "MALICIOUS"
    print(f" [PILLAR 1 PASSED] Reconstructed timeline, resolved contradiction, and inferred {len(missing_stages)} missing kill-chain stages!")

    # -------------------------------------------------------------------------
    # 2. Test Autonomous Security Research Scientist (Empirical Gain & Reproducibility)
    # -------------------------------------------------------------------------
    study = AutonomousSecurityResearchScientist.conduct_autonomous_research_study(seed=20261031)
    assert study["f1_improvement"] > 0.15, f"Expected significant F1 gain, got {study['f1_improvement']}"
    assert study["hypothesis_results"]["fpr"] <= 0.02, f"Expected FPR <= 2%, got {study['hypothesis_results']['fpr']}"
    assert study["statistically_significant_p001"] is True
    assert study["reproducibility_verified"] is True
    assert study["autonomous_production_push_allowed"] is False
    print(f" [PILLAR 2 PASSED] Research Scientist proved F1 gain +{study['f1_improvement']*100:.1f}% (Z={study['z_score_significance']}) with 100% reproducibility!")

    # -------------------------------------------------------------------------
    # 3. Test Verifiable Autonomous Defense (Rejected Alternatives + Deterministic Replay)
    # -------------------------------------------------------------------------
    evidence = [
        {"source": "dom_inspector", "severity": 0.95, "reliability": 0.98, "verified": True},
        {"source": "crime_scene_graph", "severity": 0.92, "reliability": 0.95, "verified": True}
    ]
    decision = VerifiableAutonomousDefenseKernel.execute_verifiable_decision(
        executing_component="enforcer_gateway_01",
        evidence_items=evidence,
        ai_recommended_risk=0.94,
        uncertainty_level=0.10
    )
    assert decision["selected_action"] == "BLOCK_DOMAIN"
    assert len(decision["rejected_alternatives"]) == 3
    
    # اختبار إعادة التشغيل الحتمية (Replay Verification)
    replay = VerifiableAutonomousDefenseKernel.replay_and_verify_decision(decision, raw_ai_risk=0.94)
    assert replay["replay_verified"] is True

    # اختبار منع مكون غير مصرح له من تنفيذ الحظر
    unauth_decision = VerifiableAutonomousDefenseKernel.execute_verifiable_decision(
        executing_component="enforcer_readonly_02",
        evidence_items=evidence,
        ai_recommended_risk=0.94,
        uncertainty_level=0.10
    )
    assert unauth_decision["component_authorized"] is False
    assert unauth_decision["execution_outcome"] == "HALTED_UNAUTHORIZED_COMPONENT"
    print(f" [PILLAR 3 PASSED] Verifiable Defense logged {len(decision['rejected_alternatives'])} rejected alternatives & verified SHA-256 replay!")

    # -------------------------------------------------------------------------
    # 4. Test Civilization Cascade & Dynamic Trust Lease
    # -------------------------------------------------------------------------
    civ = CivilizationAndFailureIntelligence.analyze_civilization_cascade_and_fragility(
        dependency_graph={"org_a": ["idp_x"], "org_b": ["org_a"]},
        compromised_provider="idp_x",
        cert_days_remaining=3,
        single_provider_dependencies=["idp_x"]
    )
    assert civ["blast_radius_count"] == 2
    assert civ["pre_attack_failure_probability"] > 0.50

    lease = CivilizationAndFailureIntelligence.negotiate_dynamic_trust_lease(
        peer_id="partner_agent_01",
        identity_proof_verified=True,
        source_reliability=0.88,
        requested_permissions=["READ_IOC", "WRITE_KERNEL", "QUERY_GRAPH"],
        minimum_required_permissions=["READ_IOC", "QUERY_GRAPH"]
    )
    assert lease["trust_granted"] is True
    assert "WRITE_KERNEL" in lease["Excess_permissions_stripped"]
    print(" [PILLAR 4 PASSED] Civilization Cascade Graph & Least-Privilege Trust Negotiation Verified!")

    print("=" * 88)
    print(" [100% VERIFIED] PHISHGUARD SOVEREIGN v15.0 (BEYOND THE LIMITS) ALL TESTS PASSED!")
    print("=" * 88)

if __name__ == "__main__":
    test_beyond_the_limits_v15_suite()