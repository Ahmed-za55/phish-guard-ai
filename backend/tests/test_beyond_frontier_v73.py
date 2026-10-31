import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.beyond_frontier_v73.sovereign_trust_plane import SovereignTrustPlane
from app.beyond_frontier_v73.secure_evidence_ingestion import SecureEvidenceIngestionPlane
from app.beyond_frontier_v73.detection_fabric import BeyondDetectionFabric
from app.beyond_frontier_v73.threat_intelligence_plane import ThreatIntelligencePlane
from app.beyond_frontier_v73.risk_adjudication_plane import RiskAdjudicationPlane
from app.beyond_frontier_v73.adversarial_evolution_lab import AdversarialEvolutionAndSelfImprovementLab
from app.beyond_frontier_v73.policy_gated_response import PolicyGatedResponseAndExchangePlane
from app.beyond_frontier_v73.independent_assurance import IndependentAssuranceAndBenchmarkPlane

def run_beyond_frontier_assurance_suite():
    # 01 & Research (Verified Agent Orchestration): منع مصدر خارجي أو نموذج من تصعيد صلاحياته
    zt = SovereignTrustPlane.verify_zero_trust_identity("external_feed", "PROPOSE_ACTION")
    assert zt["authorized"] is False and zt["privilege_escalation_blocked"] is True

    # 06 (Formal Safety Kernel): منع تعديل نواة السلامة أو الحظر بدون نصاب أدلة
    sk_tamper = SovereignTrustPlane.evaluate_formal_safety_kernel("MODIFY_SAFETY_KERNEL", independent_quorum_met=True, human_approved=True)
    assert sk_tamper["kernel_verdict"] == "DENIED_IMMUTABLE_KERNEL"
    sk_no_quorum = SovereignTrustPlane.evaluate_formal_safety_kernel("BLOCK_AND_QUARANTINE", independent_quorum_met=False)
    assert sk_no_quorum["enforced_action"] == "WARN_USER_RESTRICTED"

    # P1 & 08 & 11 (SSRF Guard, Provenance, Canary System)
    ing = SecureEvidenceIngestionPlane.inspect_and_ingest_evidence(
        "Check http://127.0.0.1:8000/admin and https://evil-login.com",
        ["http://127.0.0.1:8000/admin", "https://evil-login.com"]
    )
    assert ing["ssrf_protection"]["ssrf_attempt_detected"] is True
    assert "http://127.0.0.1:8000/admin" in ing["ssrf_protection"]["blocked_internal_urls"]
    can = SecureEvidenceIngestionPlane.verify_canary_pipeline_integrity("CORRUPTED_CANARY")
    assert can["pipeline_tamper_detected"] is True

    # 02 & Research (Cross-Modal Robustness): عندما يتعارض رابط خبيث جداً (95) مع نص/صورة سليمين (5)
    adj = BeyondDetectionFabric.adjudicate_independent_analyzers(lexical_score=95.0, ast_score=5.0, homograph_score=95.0, vision_score=5.0)
    assert adj["cross_modal_conflict_detected"] is True
    assert adj["adjudicated_risk_score"] >= 80.0  # لا يضيع الخطر في المتوسط البسيط

    # 03 (Unknown-Threat Discovery): رصد شذوذ غير معروف القواعد وتوليد فرضية
    unk = BeyondDetectionFabric.discover_unknown_threats(entropy_val=4.9, tda_score=45.0, known_rule_matched=False)
    assert unk["unknown_threat_candidate"] is True and unk["hypothesis_validated_in_sandbox"] is True

    # 04 & Research (Attack-Path Reconstruction & Missing Evidence Gaps)
    ti = ThreatIntelligencePlane.reconstruct_attack_path_and_causality(
        [{"url": "https://spoof.com", "risk_score": 80}], urgency_present=True, ast_present=False, homograph_present=True
    )
    assert len(ti["missing_evidence_gaps"]) >= 1
    assert ti["early_warning_campaign_forecast"]["early_warning_triggered"] is True

    # 07 & Research (Counterfactual Risk Simulator & Distribution-Free Control)
    cf = RiskAdjudicationPlane.simulate_counterfactual_decisions(adjudicated_risk_score=52.0, disagreement_std=30.0)
    assert cf["distribution_free_risk_control"]["high_uncertainty_abstention_triggered"] is True
    assert cf["counterfactual_optimal_action"] in {"HOLD_FOR_HUMAN_REVIEW", "WARN_USER_RESTRICTED"}

    # 05 & 09 (Adversarial Evolution & Safe Self-Improvement Quarantine)
    adv = AdversarialEvolutionAndSelfImprovementLab.run_adversarial_evolution_tests("Urg\u200bent login", 60.0)
    assert adv["perturbation_Attempt_detected"] is True and adv["zero_width_characters_stripped"] == 1
    ssi = AdversarialEvolutionAndSelfImprovementLab.stage_for_safe_self_improvement("Ambiguous sample", 55.0, 25.0)
    assert ssi["blind_online_learning_disabled"] is True and ssi["hard_case_staged_in_quarantine"] is True

    # 10 & 12 (Privacy Threat Exchange & Independent Assurance Benchmark with Limitations)
    ex = PolicyGatedResponseAndExchangePlane.prepare_privacy_preserving_threat_exchange([{"url": "https://bad.com"}], is_confirmed_threat=True)
    assert ex["raw_payload_shared"] is False and ex["minimized_indicators_count"] == 1
    bench = IndependentAssuranceAndBenchmarkPlane.evaluate_against_strong_baseline(
        "Urgent password", [{"url": "https://bad.com", "risk_score": 85}], "BLOCK_AND_QUARANTINE", 88.0
    )
    assert len(bench["documented_negative_results_and_limitations"]) >= 2

    print("[VERIFIED] All 12 Beyond-Frontier Upgrades + 5 Research Tracks + SSRF/Canary/Kernel Guards PASSED 100%!")

if __name__ == "__main__":
    run_beyond_frontier_assurance_suite()