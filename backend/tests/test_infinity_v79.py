import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.infinity_frontier_v79.security_constitution import SovereignSecurityConstitution
from app.infinity_frontier_v79.data_provenance_pqc import DataProvenanceAndPostQuantumEngine
from app.infinity_frontier_v79.protection_remediation import ProtectionAndVerifiedRemediationEngine

def test_infinity_frontier_suite():
    # 1. Sovereign Security Constitution: منع أي محاولة لتجاوز الدستور الأمني
    const_test = SovereignSecurityConstitution.enforce_constitution("BYPASS_SECURITY_CONSTITUTION", agent_authenticated=True)
    assert const_test["execution_permitted"] is False
    assert const_test["violation_blocked"] is True

    # 2. Data Provenance & Intelligence Lineage
    prov_test = DataProvenanceAndPostQuantumEngine.record_data_provenance("test payload", ["parser"], "ALLOW")
    assert "provenance_digest" in prov_test

    # 3. Post-Quantum Cryptography Agility
    pqc_test = DataProvenanceAndPostQuantumEngine.evaluate_post_quantum_agility("ML-KEM-768")
    assert pqc_test["post_quantum_compliant"] is True

    # 4. Cognitive Attack Surface Defense (BEC & Social Engineering)
    cog_test = ProtectionAndVerifiedRemediationEngine.analyze_cognitive_attack_surface("Urgent CEO wire transfer request immediately")
    assert cog_test["business_email_compromise_bec"] is True
    assert cog_test["human_social_engineering_protected"] is True

    # 5. Verified Autonomous Remediation
    rem_test = ProtectionAndVerifiedRemediationEngine.execute_verified_remediation("ISSUE_001", "PATCH_SANDBOX")
    assert rem_test["independent_verification_passed"] is True
    assert rem_test["remediation_executed"] is True

    print("[VERIFIED] PHISHGUARD SOVEREIGN INFINITY FRONTIER (v79) Acceptance Suite PASSED 100%!")

if __name__ == "__main__":
    test_infinity_frontier_suite()