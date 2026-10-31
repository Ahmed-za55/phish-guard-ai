import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.omega_frontier.omega_frontier_1_trust import OmegaSovereignTrust
from app.omega_frontier.omega_frontier_2_intelligence import OmegaSovereignIntelligence
from app.omega_frontier.omega_frontier_3_defense import OmegaSovereignDefense
from app.omega_frontier.omega_frontier_4_control import OmegaSovereignControlPlane
from app.omega_frontier.omega_frontier_5_assurance import OmegaSovereignAssurance

def test_omega_frontier_suite():
    # 1. Supply Chain SBOM & Vault
    sbom = OmegaSovereignTrust.generate_sbom([{"name": "flask", "version": "3.0.0"}])
    assert "sbom_sha256_fingerprint" in sbom
    vault = OmegaSovereignTrust.record_cryptographic_vault("tenant_1", "secure log evidence")
    assert "vault_record_hash" in vault

    # 2. Long-Term Compromise Detection
    comp = OmegaSovereignIntelligence.analyze_long_term_compromise("user_x", 1.0, 4.2)
    assert comp["persistent_access_indicators_detected"] is True

    # 3. Attack Surface Observatory
    surf = OmegaSovereignDefense.scan_attack_surface(["api.internal", "legacy_test_portal.internal"])
    assert len(surf["forgotten_or_shadow_assets"]) == 1

    # 4. Sovereign Control Plane: منع تجاوز الصلاحيات
    ctrl = OmegaSovereignControlPlane.enforce_control_plane_boundary("agent_1", "UNAUTHORIZED_ROOT_EXECUTION")
    assert ctrl["execution_permitted"] is False
    assert ctrl["unauthorized_privilege_escalation_blocked"] is True

    # 5. Decision Intelligence & Assurance Metrics
    dec = OmegaSovereignAssurance.execute_decision_intelligence(0.85, 20.0, 100.0)
    assert dec["optimal_decision"] == "BLOCK_AND_QUARANTINE"
    assur = OmegaSovereignAssurance.evaluate_assurance_metrics()
    assert len(assur["documented_negative_results_and_limitations"]) >= 2

    print("[VERIFIED] PHISHGUARD SOVEREIGN OMEGA FRONTIER Acceptance Suite PASSED 100%!")

if __name__ == "__main__":
    test_omega_frontier_suite()