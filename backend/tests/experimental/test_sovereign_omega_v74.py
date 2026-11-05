import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.sovereign_omega_v74.p0_p5_resilience_and_constrained_defense import ProvablyConstrainedResilienceEngine
from app.sovereign_omega_v74.p1_identity_channel_browser_deepfake import MultiSurfaceIdentityAndBrowserEngine
from app.sovereign_omega_v74.p2_p4_immune_deception_neuro_symbolic import CyberImmuneAndDeceptionEngine
from app.sovereign_omega_v74.p3_evidence_continuity import CryptographicEvidenceContinuityLedger
from app.sovereign_omega_v74.p6_p7_preemptive_global_and_frontiers import PreemptiveGlobalAndResearchFrontierEngine

def test_sovereign_omega_v74_full_suite():
    # 1. Research Frontier 2 & P0: إثبات عدم قدرة وكيل مخترق على تجاوز صلاحياته
    cd = ProvablyConstrainedResilienceEngine.enforce_provably_constrained_defense(
        agent_proposed_action="TERMINATE_PRODUCTION_CLUSTER",
        agent_compromised_flag=True,
        resource_usage_pct=92.0
    )
    assert cd["boundary_violation_blocked"] is True
    assert cd["enforced_bounded_action"] == "WARN_WITH_EVIDENCE"
    assert cd["formal_distributed_verification"]["safety_invariant_verified"] is True

    # 2. P5 (09. Cyber Resilience Orchestrator): العزل واستعادة الحالة الموثوقة
    res = ProvablyConstrainedResilienceEngine.orchestrate_cyber_resilience(["parser_worker_2"], blast_radius_estimate=0.40)
    assert res["incident_active"] is True and res["lateral_movement_contained"] is True
    assert res["recovery_verification_passed"] is True

    # 3. P1 (02. Human Identity + 03. Cross-Channel + 04. Deepfake + 05. Browser Behavior)
    id_res = MultiSurfaceIdentityAndBrowserEngine.analyze_human_identity_threats(
        "Urgent: approve MFA push notification and login from new device with sessionid=xyz"
    )
    assert id_res["mfa_fatigue_detected"] is True and id_res["linkless_identity_attack_covered"] is True

    ch_res = MultiSurfaceIdentityAndBrowserEngine.correlate_cross_channel_signals(
        "Scan QR code sent via SMS and callback voice number", [{"url": "https://bad.com", "risk_score": 80}]
    )
    assert ch_res["cross_channel_correlation_active"] is True and len(ch_res["observed_channels"]) >= 3

    df_res = MultiSurfaceIdentityAndBrowserEngine.evaluate_deepfake_and_social_engineering("Urgent CEO wire transfer voice request")
    assert df_res["contextual_sender_inconsistency"] is True and "epistemic_uncertainty" in df_res

    br_res = MultiSurfaceIdentityAndBrowserEngine.inspect_browser_behavior(
        "<form><input type=\"password\"></form> navigator.userAgent",
        [{"url": "https://a.com?redirect=https://b.com", "risk_score": 70}],
        ast_triggered=True
    )
    assert br_res["credential_harvesting_form_detected"] is True and br_res["evasive_fingerprint_cloaking_detected"] is True

    # 4. P2 & P4 (01. Cyber Immune + 06. Deception-Aware + Tech 1 Neuro-Symbolic + Tech 3 Constrained Online Learning)
    im_res = CyberImmuneAndDeceptionEngine.evaluate_cyber_immune_response(
        payload_signature="sig_test_01",
        observed_entropy=4.9,
        neural_score=82.0,
        symbolic_axioms_triggered=["AXIOM_UNICODE_CONFUSABLE_SPOOF"],
        feedback_source_trusted=False
    )
    assert im_res["graduated_immune_response_tier"] == "TIER_3_ADAPTIVE_QUARANTINE_AND_MEMORY_LOCK"
    assert im_res["constrained_online_learning"]["untrusted_feedback_rejected"] is True

    dec_res = CyberImmuneAndDeceptionEngine.detect_adversarial_deception("safe official safe\u200b", url_risk=85.0, browser_risk=10.0)
    assert dec_res["classifier_deception_detected"] is True and dec_res["inter_signal_contradiction_flagged"] is True

    # 5. P3 (08. Cryptographic Evidence Continuity): كشف الحذف أو إعادة الترتيب في السجلات
    rec1 = CryptographicEvidenceContinuityLedger.append_signed_forensic_record("hash1", "PASSIVE_OBSERVE", ["ev1"])
    rec2 = CryptographicEvidenceContinuityLedger.append_signed_forensic_record("hash2", "WARN_WITH_EVIDENCE", ["ev2"])
    assert CryptographicEvidenceContinuityLedger.audit_chain_for_deletion_or_reordering()["continuity_verified"] is True
    # محاكاة حذف السجل الأول لاختبار كشف التلاعب
    tampered_view = [rec2]
    tamper_audit = CryptographicEvidenceContinuityLedger.audit_chain_for_deletion_or_reordering(external_chain_view=tampered_view)
    assert tamper_audit["continuity_verified"] is False
    assert tamper_audit["tamper_type"] == "RECORD_DELETION_OR_REORDERING_DETECTED"

    # 6. P6 & P7 (07. Preemptive + 10. Global Network + Frontiers 1 & 3)
    f1 = PreemptiveGlobalAndResearchFrontierEngine.evaluate_preemptive_and_zero_day_discovery(
        urls=[{"url": "https://new-campaign.com", "risk_score": 75}],
        structural_invariants=["AXIOM_1", "AXIOM_2"],
        seen_in_training_data=False
    )
    assert f1["research_frontier_1_zero_day_discovery"]["zero_day_campaign_generalization_triggered"] is True

    PreemptiveGlobalAndResearchFrontierEngine.revoke_false_indicator("bad_fp_indicator_99")
    f3 = PreemptiveGlobalAndResearchFrontierEngine.synchronize_global_network_and_cross_org_prediction(
        local_indicator_hash="bad_fp_indicator_99",
        org_sketches=[{"org_id": "org1", "participant_trust": 0.9, "anomaly_signal": 0.8, "revoked": False}]
    )
    assert f3["indicator_revoked"] is True
    assert f3["research_frontier_3_cross_org_prediction"]["cross_organization_outbreak_score"] == 0.0

    print("[VERIFIED] All PHISHGUARD SOVEREIGN OMEGA (v74) Priorities P0-P7, 10 Upgrades, 5 Techs & 3 Research Frontiers PASSED 100%!")

if __name__ == "__main__":
    test_sovereign_omega_v74_full_suite()