import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.apogee_v6.apogee_1_adversary_cross_platform import AdversaryAndCrossPlatformIntelligence
from app.apogee_v6.apogee_2_interception_contradiction import PreExecutionAndContradictionEngine
from app.apogee_v6.apogee_3_attack_lab_forecasting import AttackPathLabAndFailureIntelligence
from app.apogee_v6.apogee_4_provenance_control_plane import DecisionProvenanceAndControlPlane

def test_apogee_v6_acceptance_suite():
    # 1. Pre-Execution Deterministic Interception: حظر الروابط والملفات التنفيذية حتمياً
    inter = PreExecutionAndContradictionEngine.intercept_pre_execution(
        urls=["javascript:alert(1)", "https://evil.com/payload.exe"],
        filenames=["invoice.scr"],
        requested_permission="SYSTEM_SHELL"
    )
    assert inter["pre_execution_blocked"] is True
    assert inter["gate_action"] == "PRE_EXECUTION_DROP"

    # 2. Intelligence Contradiction Resolution: تغليب السلوك الحديث على القوائم القديمة
    ev_list = [
        {"source": "old_reputation_feed", "verdict": "SAFE", "reliability": 0.7, "age_hours": 100},
        {"source": "live_credential_scanner", "verdict": "MALICIOUS", "reliability": 0.9, "age_hours": 1}
    ]
    res = PreExecutionAndContradictionEngine.resolve_intelligence_contradictions(ev_list)
    assert res["contradiction_found"] is True
    assert res["stale_sources_discounted"] == 1
    assert res["final_resolution"] == "MALICIOUS_CONFIRMED_BY_BEHAVIOR"

    # 3. Adversary Reconstruction & Cross-Platform Hops
    adv = AdversaryAndCrossPlatformIntelligence.reconstruct_adversary_and_path(
        "Urgent Microsoft invoice wire payment", ["https://login-ms.com"], ["EMAIL", "BROWSER", "LOGIN_PROMPT"]
    )
    assert adv["cross_platform_intelligence"]["multi_stage_attack_detected"] is True
    assert adv["adversary_reconstruction"]["semantic_indicators"]["financial_context_manipulation"] is True

    # 4. Attack Path Lab & Replay Verification
    lab = AttackPathLabAndFailureIntelligence.run_isolated_attack_simulation("PhishChain", "redirect_chain", patch_applied=True)
    assert lab["replay_blocked_after_patch"] is True

    # 5. Control Plane & Decision Provenance: منع توسيع الصلاحيات وعزل المحرك المخالف
    ctrl_bad = DecisionProvenanceAndControlPlane.enforce_intelligence_control_plane("rogue_engine", "GRANT_ROOT_ACCESS", 20.0)
    assert ctrl_bad["permitted"] is False
    assert ctrl_bad["self_privilege_escalation_blocked"] is True
    assert ctrl_bad["engine_isolated_automatically"] is True

    prov = DecisionProvenanceAndControlPlane.build_decision_provenance_record("MALICIOUS", 0.95, ev_list)
    assert "tamper_evident_provenance_hash" in prov

    print("[VERIFIED] PHISHGUARD SOVEREIGN v6.0 APOGEE ARCHITECTURE Acceptance Suite PASSED 100%!")

if __name__ == "__main__":
    test_apogee_v6_acceptance_suite()