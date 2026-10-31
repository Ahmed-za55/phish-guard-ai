import sys
import hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.omega_genesis_v83.omega_genesis_1_meta_control import SovereignMetaControlAndHardwareTrust
from app.omega_genesis_v83.omega_genesis_2_infrastructure_physics import SelfDefendingAndFailurePhysics
from app.omega_genesis_v83.omega_genesis_3_computation import VerifiableSecurityComputation

def test_omega_genesis_v83_suite():
    # 1. Hardware Root of Trust & Attestation
    q = hashlib.sha256(b"secure").hexdigest()
    hw = SovereignMetaControlAndHardwareTrust.verify_hardware_attestation(q, q)
    assert hw["tpm_attestation_valid"] is True

    # 2. Multi-Party Authorization (حاجة لتوقيعين)
    gov = SovereignMetaControlAndHardwareTrust.evaluate_meta_control_governance("Authorization Governor", "action", ["sig1", "sig2"])
    assert gov["multi_party_authorization_achieved"] is True

    # 3. Self-Defending Fabric & Failure Physics
    fab = SelfDefendingAndFailurePhysics.inspect_infrastructure_fabric({"db": "COMPROMISED"})
    assert fab["emergency_mode_active"] is True
    
    phys = SelfDefendingAndFailurePhysics.simulate_failure_physics(["node_1"], {"node_2": ["node_1"]})
    assert phys["total_nodes_affected"] == 2

    # 4. Verifiable Security Computation
    comp = VerifiableSecurityComputation.execute_verifiable_computation("alg_1", "data", {"env": "prod"})
    assert comp["verifiable_proof_generated"] is True

    print("[VERIFIED] PHISHGUARD SOVEREIGN OMEGA GENESIS ∞ (v83) Acceptance Suite PASSED 100%!")

if __name__ == "__main__":
    test_omega_genesis_v83_suite()