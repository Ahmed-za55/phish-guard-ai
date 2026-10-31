from typing import Dict, Any, List
from app.omega_frontier.omega_frontier_1_trust import OmegaSovereignTrust
from app.omega_frontier.omega_frontier_2_intelligence import OmegaSovereignIntelligence
from app.omega_frontier.omega_frontier_3_defense import OmegaSovereignDefense
from app.omega_frontier.omega_frontier_4_control import OmegaSovereignControlPlane
from app.omega_frontier.omega_frontier_5_assurance import OmegaSovereignAssurance

class OmegaFrontierMasterNexus:
    """
    المنسق المركزي لبرنامج OMEGA FRONTIER:
    يربط المنظومات الخمس (Trust, Intelligence, Defense, Control, Assurance) ويحكم إيقاع العمليات.
    """
    @staticmethod
    def run_omega_frontier_pipeline(
        text: str,
        extracted_urls: List[str],
        url_results: List[Dict[str, Any]],
        tenant_id: str = "enterprise_omega_tenant"
    ) -> Dict[str, Any]:
        max_url_risk = max([float(u.get("risk_score", 0.0)) for u in url_results], default=0.0)

        # 1. Trust: SBOM & Vault
        sbom = OmegaSovereignTrust.generate_sbom([{"name": "requests", "version": "2.31.0"}])
        vault = OmegaSovereignTrust.record_cryptographic_vault(tenant_id, text[:60])

        # 2. Intelligence: Long-term compromise & Identity graph
        compromise = OmegaSovereignIntelligence.analyze_long_term_compromise("user_alpha", 1.2, 4.1)
        identity_g = OmegaSovereignIntelligence.query_identity_graph("user_alpha", ["device_01", "session_xyz", "ip_ab"])

        # 3. Defense: Deception Canary & Attack Surface
        canary = OmegaSovereignDefense.monitor_deception_canary(canary_token_accessed=False)
        surface = OmegaSovereignDefense.scan_attack_surface(["portal.internal", "legacy_test_server.internal"])

        # 4. Control Plane Enforcement
        action = "QUARANTINE_SESSION" if max_url_risk >= 70.0 else "WARN_USER"
        control = OmegaSovereignControlPlane.enforce_control_plane_boundary("detector_agent_1", action)

        # 5. Assurance & Decision Intelligence
        decision = OmegaSovereignAssurance.execute_decision_intelligence(max_url_risk / 100.0, 25.0, 100.0)
        assurance = OmegaSovereignAssurance.evaluate_assurance_metrics()

        return {
            "omega_frontier_tier": "PHISHGUARD_SOVEREIGN_OMEGA_FRONTIER",
            "sovereign_trust": {"sbom": sbom, "evidence_vault": vault},
            "sovereign_intelligence": {"long_term_compromise": compromise, "identity_graph": identity_g},
            "sovereign_defense": {"deception_canary": canary, "attack_surface": surface},
            "sovereign_control_plane": control,
            "sovereign_assurance": {"decision_intelligence": decision, "effectiveness": assurance}
        }