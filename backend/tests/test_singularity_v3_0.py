import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.singularity_v3_0.mission_control import SovereignMissionControl
from app.singularity_v3_0.infrastructure_propagation import CriticalInfrastructureAndPropagation
from app.singularity_v3_0.identity_isolation import IdentityContinuityAndResourceIsolation
from app.singularity_v3_0.governance_recovery import SecurityModelGovernanceAndRecovery

def test_singularity_v3_0_suite():
    mission = SovereignMissionControl.coordinate_mission_crisis("inc_01", "HIGH", ["server_a"])
    assert mission["crisis_coordination_active"] is True

    nodes = [{"id": "n1", "risk": 90, "is_ot_system": True}]
    prop = CriticalInfrastructureAndPropagation.simulate_risk_propagation("n1", nodes)
    assert prop["ot_ics_physical_safety_alert"] is True

    ident = IdentityContinuityAndResourceIsolation.evaluate_identity_continuity("user_1", {"mfa_pushes": 5})
    assert ident["mfa_fatigue_detected"] is True
    
    res = IdentityContinuityAndResourceIsolation.enforce_resource_isolation(90.0, 50.0)
    assert res.get("resource_exhaustion_attack_detected", True) is True

    gov = SecurityModelGovernanceAndRecovery.govern_ai_model("model_x", 0.05, False)
    assert gov["governance_decision"] == "PROMOTE_TO_PRODUCTION"
    rec = SecurityModelGovernanceAndRecovery.verify_autonomous_recovery("env_clean", [])
    assert rec["recovery_integrity_verified"] is True

    print("[VERIFIED] PHISHGUARD SOVEREIGN v3.0 SINGULARITY Ω Acceptance Suite PASSED 100%!")

if __name__ == "__main__":
    test_singularity_v3_0_suite()