import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.genesis_v81.genesis_1_constitution_contracts import SecurityConstitution2AndContracts
from app.genesis_v81.genesis_2_auditor_feasibility import AutonomousArchitectureAuditorAndFeasibility
from app.genesis_v81.genesis_3_adversarial_versioning import AdversarialSystemIdentificationAndVersioning

def test_genesis_v81_suite():
    # 1. Runtime Security Contracts & Constitution 2.0
    contract_test = SecurityConstitution2AndContracts.enforce_runtime_contract("worker_1", "BYPASS_CONSTITUTION", 50.0)
    assert contract_test["contract_breached"] is True
    assert contract_test["enforced_behavior"] == "HALT_AND_ISOLATE_COMPONENT"

    # 2. Autonomous Architecture Auditor
    topo = [{"name": "db_node", "is_single_point_of_failure": True, "has_circular_dependency": False, "unprotected_admin_api": True}]
    audit_test = AutonomousArchitectureAuditorAndFeasibility.audit_architecture_topology(topo)
    assert "db_node" in audit_test["single_points_of_failure"]
    assert audit_test["architectural_audit_risk_level"] == "CRITICAL"

    # 3. Attack Feasibility Engine
    feas_test = AutonomousArchitectureAuditorAndFeasibility.evaluate_attack_feasibility("VULN-01", "LOW", True)
    assert feas_test["practically_exploitable"] is True

    # 4. Cross-Version Intelligence (Regression Prevention)
    ver_test = AdversarialSystemIdentificationAndVersioning.compare_cross_version_security({"recall": 0.99}, {"recall": 0.92})
    assert ver_test["security_regression_detected"] is True
    assert ver_test["promotion_gate"] == "BLOCKED_SECURITY_DEGRADATION"

    print("[VERIFIED] PHISHGUARD SOVEREIGN GENESIS Ω (v81) Acceptance Suite PASSED 100%!")

if __name__ == "__main__":
    test_genesis_v81_suite()