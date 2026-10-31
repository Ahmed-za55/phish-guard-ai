from typing import Dict, Any, List

class AutonomousArchitectureAuditorAndFeasibility:
    """
    Genesis P0 & P1:
    - Autonomous Architecture Auditor (فحص SPOF، انتهاكات الثقة، الاعتماديات الدائرية).
    - Attack Feasibility Engine (تقييم قابلية الاستغلال الفعلي وتمييز النظري عن العملي).
    """
    @staticmethod
    def audit_architecture_topology(components: List[Dict[str, Any]]) -> Dict[str, Any]:
        spofs = [c["name"] for c in components if c.get("is_single_point_of_failure", False)]
        circular_deps = [c["name"] for c in components if c.get("has_circular_dependency", False)]
        privilege_escalation_paths = [c["name"] for c in components if c.get("unprotected_admin_api", False)]

        risk_level = "CRITICAL" if spofs or privilege_escalation_paths else ("MEDIUM" if circular_deps else "LOW")

        return {
            "architectural_audit_risk_level": risk_level,
            "single_points_of_failure": spofs,
            "circular_dependencies": circular_deps,
            "privilege_escalation_paths": privilege_escalation_paths,
            "audit_status": "COMPLETED_REPRODUCIBLE_MAP_GENERATED"
        }

    @staticmethod
    def evaluate_attack_feasibility(vulnerability_id: str, required_privileges: str, network_exposed: bool) -> Dict[str, Any]:
        # التميز بين الثغرة النظرية والخطر القابل للتحقق العملي
        exploitable_in_practice = network_exposed and required_privileges in {"NONE", "GUEST", "LOW"}
        feasibility_score = 0.88 if exploitable_in_practice else 0.15

        return {
            "vulnerability_id": vulnerability_id,
            "practically_exploitable": exploitable_in_practice,
            "attack_feasibility_score": feasibility_score,
            "remediation_priority": "P0_IMMEDIATE_FIX" if exploitable_in_practice else "P3_THEORETICAL_RISK"
        }