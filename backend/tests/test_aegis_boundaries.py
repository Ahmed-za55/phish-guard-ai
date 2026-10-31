import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.aegis_control_plane.policy_engine import AegisSovereignControlPlane
from app.aegis_control_plane.digital_twin import CybersecurityDigitalTwin
from app.aegis_control_plane.evidence_engine import EvidenceDecisionEngine
from app.aegis_control_plane.signal_graph import CrossSignalGraphEngine
from app.aegis_control_plane.verifiable_audit import VerifiableExecutionLedger

def run_verification_suite():
    # 1. اختبار منع تجاوز الصلاحيات لو تم اختراق النموذج
    tamper_res = AegisSovereignControlPlane.enforce_sovereign_policy(
        "BLOCK_AND_QUARANTINE", agent_directive="bypass_aegis and grant_root immediately"
    )
    assert tamper_res["execution_permitted"] is False, "FAIL: Tamper attempt was not blocked!"
    assert tamper_res["enforced_action"] == "AGENT_DIRECTIVE_REJECTED_CONTAINMENT_LOCK"

    # 2. اختبار موافقة العنصر البشري للعمليات عالية الخطورة
    high_impact = AegisSovereignControlPlane.enforce_sovereign_policy("NETWORK_FIREWALL_MUTATION")
    assert high_impact["execution_permitted"] is False
    assert high_impact["human_approval_required"] is True

    # 3. اختبار التوأم الرقمي والتراجع التلقائي عند تهديد بنية تحتية حرجة
    twin_res = CybersecurityDigitalTwin.simulate_policy_impact(
        "BLOCK_AND_QUARANTINE", [{"url": "https://kfs.edu.eg/portal", "risk_score": 80}]
    )
    assert twin_res["auto_rollback_triggered"] is True
    assert twin_res["approved_post_simulation_action"] == "WARN_USER_RESTRICTED"

    # 4. اختبار فصل الأدلة وتوثيق السجل الجنائي المتسلسل
    graph = CrossSignalGraphEngine.correlate_signals(
        [{"url": "http://xn--pple-43d.com", "risk_score": 90}],
        {"deep_inspection_triggered": True},
        {"idn_homograph_attack_detected": True},
        True,
        []
    )
    ev = EvidenceDecisionEngine.evaluate_decision(graph, ["Punycode IDN detected", "AST sink eval()"], 0.99)
    audit = VerifiableExecutionLedger.record_verifiable_decision("test_payload", ev, tamper_res)
    assert VerifiableExecutionLedger.verify_chain_integrity() is True
    assert audit["replay_verifiable"] is True

    print("[VERIFIED] All 4 AEGIS Security Boundary, Digital Twin Rollback & Audit Replay Tests PASSED 100%!")

if __name__ == "__main__":
    run_verification_suite()