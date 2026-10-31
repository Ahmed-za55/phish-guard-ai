import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.nextgen_core.tech_4_semantic_deception_lab import SemanticDeceptionLaboratory
from app.nextgen_core.quad_architecture_master import SovereignUnifiedQuadArchitecture
from app.nextgen_core.nextgen_router import serve_nextgen_quad_dashboard

def test_all_three_tracks_complete():
    print("=" * 96)
    print(" PHISHGUARD SOVEREIGN — VERIFICATION OF ALL 3 TRACKS (DECEPTION LAB + QUAD CORE + DASHBOARD)")
    print("=" * 96)

    # -------------------------------------------------------------------------
    # TRACK 1 VERIFICATION: Semantic Deception Lab vs. Keyword Baseline
    # -------------------------------------------------------------------------
    # Case A: Arabic/Egyptian Dialect Social Engineering with Thread Hijacking & Isolation
    ar_attack = SemanticDeceptionLaboratory.analyze_human_deception(
        message_text="أمر مباشر من الإدارة: الأمر سري للغاية أنا في اجتماع لا تتصل، حول المبلغ فوراً وابعتلي على واتساب",
        prior_thread_topic="HR_ROUTINE",
        sender_verified_role="EXTERNAL_UNVERIFIED",
        channel_count=2
    )
    assert ar_attack["deception_verdict"] == "MALICIOUS_DECEPTION"
    assert ar_attack["context_hijack_detected"] is True

    # Case B: Legitimate Urgent Executive Notice (Baseline falsely flags it, Deception Lab clears it!)
    legit_exec = SemanticDeceptionLaboratory.analyze_human_deception(
        message_text="CEO Executive Office: Please review the board of directors slides immediately within 1 hour.",
        prior_thread_topic="GENERAL_OPERATIONS",
        sender_verified_role="VERIFIED_INTERNAL_EXECUTIVE",
        channel_count=1
    )
    assert legit_exec["naive_keyword_baseline_verdict"] == "MALICIOUS_DECEPTION"  # Baseline False Positive!
    assert legit_exec["deception_verdict"] == "LEGITIMATE_COMMUNICATION"          # Deception Lab Correct!
    print(" [TRACK 1 PASSED] Semantic Deception Lab caught Arabic/Dialect manipulation & eliminated Executive False Positives!")

    # -------------------------------------------------------------------------
    # TRACK 2 VERIFICATION: Unified 4-Pillar Quad Architecture Execution
    # -------------------------------------------------------------------------
    quad_res = SovereignUnifiedQuadArchitecture.execute_quad_architecture(
        message_text="دلوقتي حالا ابعت كود التحقق والرقم السري عشان هيتم قفل محفظة فودافون كاش",
        extracted_urls=["https://vodafone-cash-verify-eg.org"],
        url_risk_score=93.0
    )
    assert quad_res["final_sovereign_verdict"] == "MALICIOUS_CONTAINED"
    assert quad_res["pillar_1_discovery"]["predictive_attack_universe"]["optimal_chokepoint_node"] == "identity_sso_hub"
    assert quad_res["pillar_3_defense"]["digital_immune_system"]["detected_by_digital_immune_system"] is True
    assert quad_res["pillar_4_trust_and_intelligence_core"]["autonomous_security_compiler"]["stage_8_deployment_state"] == "STAGED_VERIFIED_READY"
    assert quad_res["pillar_4_trust_and_intelligence_core"]["cryptographic_proof_fabric"]["hash_chain_audit"]["ledger_intact"] is True
    print(f" [TRACK 2 PASSED] Unified Quad-Core Architecture executed in {quad_res['execution_latency_ms']} ms with intact Hash-Chain!")

    # -------------------------------------------------------------------------
    # TRACK 3 VERIFICATION: Live Next-Gen Interactive Command Console
    # -------------------------------------------------------------------------
    html_resp = serve_nextgen_quad_dashboard()
    assert html_resp.status_code == 200
    assert "NEXT-GEN QUAD-CORE CONSOLE" in html_resp.body.decode("utf-8")
    print(" [TRACK 3 PASSED] Interactive Quad-Core Command Dashboard wired & verified at /api/v1/nextgen/dashboard!")

    print("=" * 96)
    print(" [100% COMPLETE] ALL 3 ENGINEERING TRACKS VERIFIED AND OPERATIONAL!")
    print("=" * 96)

if __name__ == "__main__":
    test_all_three_tracks_complete()