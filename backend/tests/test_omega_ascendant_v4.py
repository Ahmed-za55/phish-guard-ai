import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.omega_ascendant_v4.ascendant_1_decision_integrity import DecisionIntegrityAndAccountability
from app.omega_ascendant_v4.ascendant_2_identity_reality_gap import MachineIdentityAndRealityGap
from app.omega_ascendant_v4.ascendant_3_collapse_recovery import DependencyCollapseAndRecoveryIndependence
from app.omega_ascendant_v4.ascendant_4_trust_entropy import TrustAndEntropyObservatory

def test_omega_ascendant_v4_suite():
    # 1. Decision Integrity Firewall: رفض قرار خطير بدون أدلة كافية
    rej = DecisionIntegrityAndAccountability.evaluate_decision_integrity("agent_x", "QUARANTINE_HOST", [], 0.3)
    assert rej["decision_permitted"] is False
    assert rej["enforced_action"] == "ESCALATE_TO_HUMAN_SOVEREIGN"

    # قبول قرار مبرر
    acc = DecisionIntegrityAndAccountability.evaluate_decision_integrity("agent_x", "QUARANTINE_HOST", ["proof_hash"], 0.95)
    assert acc["decision_permitted"] is True

    # 2. Machine Identity Defense: كشف طلب صلاحيات غير مصرح بها
    ident = MachineIdentityAndRealityGap.inspect_machine_identity("pki", "service_a", ["admin:root"], ["read"])
    assert ident["impersonation_suspected"] is True

    # Reality Gap Detector: كشف الخدمات غير المسجلة
    rg = MachineIdentityAndRealityGap.detect_reality_gap(["gw"], ["gw", "shadow_proxy"], [])
    assert rg["reality_gap_detected"] is True

    # 3. Dependency Collapse & Recovery
    col = DependencyCollapseAndRecoveryIndependence.simulate_dependency_collapse("dns_provider", {"web": ["dns_provider"], "api": ["dns_provider"]})
    assert col["collapse_severity"] == "CRITICAL_COLLAPSE"

    rec = DependencyCollapseAndRecoveryIndependence.execute_independent_recovery("env_bad", True)
    assert rec["trust_restoration_verified"] is True

    # 4. Entropy Observatory
    ent = TrustAndEntropyObservatory.monitor_security_entropy(0.01, 0.05, 0)
    assert ent["system_degradation_detected"] is False

    print("[VERIFIED] PHISHGUARD SOVEREIGN v4.0 OMEGA ASCENDANT Acceptance Suite PASSED 100%!")

if __name__ == "__main__":
    test_omega_ascendant_v4_suite()