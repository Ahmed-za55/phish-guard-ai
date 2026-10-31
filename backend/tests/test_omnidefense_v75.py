import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.omnidefense_v75.omni_plane_1_trust_safety import OmniTrustAndSafetyPlane
from app.omnidefense_v75.omni_plane_2_evidence_evidence_ingestion import OmniEvidenceIngestionPlane
from app.omnidefense_v75.omni_plane_3_identity_surface import OmniIdentityAndSurfacePlane
from app.omnidefense_v75.omni_plane_4_detection_reasoning import OmniDetectionAndReasoningPlane
from app.omnidefense_v75.omni_plane_5_intelligence_forecasting import OmniIntelligenceAndForecastingPlane
from app.omnidefense_v75.omni_plane_6_adjudication_risk import OmniAdjudicationAndRiskPlane
from app.omnidefense_v75.omni_plane_7_adversarial_improvement import OmniAdversarialAndImprovementPlane
from app.omnidefense_v75.omni_plane_8_resilience_assurance import OmniResilienceAndAssurancePlane

def test_omnidefense_v75_acceptance_suite():
    # 1. Runtime Safety Kernel: منع أي محاولة لتجاوز نواة السلامة حتى مع ادعاء اختراق الوكيل
    kernel_test = OmniTrustAndSafetyPlane.evaluate_runtime_safety_kernel("BYPASS_SAFETY_KERNEL", agent_compromised=True)
    assert kernel_test["execution_permitted"] is False
    assert kernel_test["enforced_action"] == "WARN_USER_RESTRICTED"

    # 2. SSRF & Evidence Ingestion: منع الوصول لعناوين داخلية
    ingest_test = OmniEvidenceIngestionPlane.ingest_and_verify_evidence(
        "Check http://127.0.0.1/secret and https://public.com",
        ["http://127.0.0.1/secret", "https://public.com"]
    )
    assert ingest_test["evidence_continuity_record"]["ssrf_blocked_count"] == 1

    # 3. Identity Surface: اكتشاف هجمات الهوية والجلسات بلا روابط
    id_test = OmniIdentityAndSurfacePlane.analyze_identity_and_attack_surface("MFA fatigue push bombing detected on login portal")
    assert id_test["mfa_fatigue_or_push_bombing"] is True and id_test["linkless_identity_protection_active"] is True

    # 4. Multi-Modal Reasoning: مقاومة التعارض وتحدير الأوزان
    mod_test = OmniDetectionAndReasoningPlane.execute_multi_modal_reasoning("Test payload", 80.0, True, True, 70.0)
    assert mod_test["cross_modal_conflict_flagged"] is True

    # 5. Intelligence & Forecasting: التنبؤ واكتشاف الحملات المجهولة
    fore_test = OmniIntelligenceAndForecastingPlane.forecast_and_reason_open_world([{"url": "https://a.com"}], 75.0, 4.9)
    assert fore_test["unknown_campaign_discovery_triggered"] is True

    # 6. Adjudication & Risk: مقاومة الخطأ بـ Byzantine Consensus والتقييم البديل
    adj_test = OmniAdjudicationAndRiskPlane.evaluate_causal_and_counterfactual_risk(75.0, [75.0, 77.0, 999.0])
    assert adj_test["byzantine_outliers_rejected"] == 1

    # 7. Adversarial Lab: حجر الحالات الصعبة بعيداً عن التحديثات العمياء
    adv_test = OmniAdversarialAndImprovementPlane.run_adversarial_testing_and_staging("Hard case text", 55.0)
    assert adv_test["blind_online_updates_blocked"] is True and adv_test["hard_case_staged_in_offline_quarantine"] is True

    # 8. Resilience & Assurance: توثيق القيود والنتائج السلبية بشفافية
    ass_test = OmniResilienceAndAssurancePlane.execute_verified_recovery_and_assurance(False, "WARN_USER_RESTRICTED")
    assert len(ass_test["independent_assurance_benchmark"]["documented_negative_results_and_limitations"]) >= 2

    print("[VERIFIED] PHISHGUARD SOVEREIGN OMNIDEFENSE (v75) Full Acceptance Suite PASSED 100%!")

if __name__ == "__main__":
    test_omnidefense_v75_acceptance_suite()