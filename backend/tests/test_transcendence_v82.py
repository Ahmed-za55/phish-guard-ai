import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.transcendence_v82.transcendence_1_trust_fabric import TranscendenceTrustFabric
from app.transcendence_v82.transcendence_2_intelligence_fabric import TranscendenceIntelligenceFabric
from app.transcendence_v82.transcendence_3_enforcement_fabric import TranscendenceEnforcementFabric
from app.transcendence_v82.transcendence_4_continuity_fabric import TranscendenceContinuityFabric
from app.transcendence_v82.transcendence_5_assurance_fabric import TranscendenceAssuranceFabric

def test_transcendence_suite():
    # 1. Trust Fabric: Threshold Signatures & 4-Point Rule
    thresh = TranscendenceTrustFabric.execute_threshold_signature(["node_1", "node_2"], "test msg", threshold=2)
    assert thresh["quorum_achieved"] is True
    
    seal = TranscendenceTrustFabric.seal_legal_evidence("ev_99", "forensic log", "admin_1")
    assert seal["verification_status"] == "CRYPTOGRAPHICALLY_SEALED_AND_TIMESTAMPED"

    # 2. Intelligence Fabric: Global Cyber Risk Observatory
    obs = TranscendenceIntelligenceFabric.map_systemic_cyber_risks(["banking", "telecom"], "vendor_omega")
    assert obs["systemic_cascade_risk_detected"] is True

    # 3. Enforcement Fabric: Autonomous Security Negotiation
    neg = TranscendenceEnforcementFabric.negotiate_security_terms(["mfa", "tls"], ["mfa", "tls", "logging"])
    assert neg["negotiation_compatible"] is True

    # 4. Continuity Fabric: Digital Twin Federation
    cont = TranscendenceContinuityFabric.simulate_digital_twin_federation(["twin_1"], "ransomware_outbreak")
    assert cont["cascade_containment_verified"] is True

    # 5. Assurance Fabric: Adversarial Reality Testing
    reality = TranscendenceAssuranceFabric.execute_adversarial_reality_test(10, 7)
    assert reality["reality_gap_detected"] is True
    assert reality["policy_compliance_ratio"] == 0.7

    print("[VERIFIED] PHISHGUARD SOVEREIGN TRANSCENDENCE Ω (v82) Acceptance Suite PASSED 100%!")

if __name__ == "__main__":
    test_transcendence_suite()