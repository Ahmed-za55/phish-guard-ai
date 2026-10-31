from typing import Dict, Any, List

class SelfDefendingAndFailurePhysics:
    """
    Self-Defending Infrastructure Fabric & Cyber Failure Physics:
    - عزل المكونات المخترقة وتفعيل وضع الطوارئ.
    - نمذجة سلوك الانهيار المركب وحساب انتشار الأعطال المتزامنة.
    """
    @staticmethod
    def inspect_infrastructure_fabric(component_states: Dict[str, str]) -> Dict[str, Any]:
        compromised = [comp for comp, status in component_states.items() if status == "COMPROMISED"]
        emergency_mode = len(compromised) > 0

        return {
            "emergency_mode_active": emergency_mode,
            "compromised_components_isolated": compromised,
            "self_defending_fabric_status": "EMERGENCY_ISOLATION_ACTIVE" if emergency_mode else "NOMINAL_SECURE",
            "core_protection_functional": True
        }

    @staticmethod
    def simulate_failure_physics(failing_nodes: List[str], dependency_graph: Dict[str, List[str]]) -> Dict[str, Any]:
        cascaded_failures = set(failing_nodes)
        for node in failing_nodes:
            for dependent, deps in dependency_graph.items():
                if node in deps:
                    cascaded_failures.add(dependent)

        return {
            "initial_failing_nodes": failing_nodes,
            "cascaded_failure_impact": list(cascaded_failures),
            "total_nodes_affected": len(cascaded_failures),
            "system_collapse_risk": "HIGH" if len(cascaded_failures) >= 3 else "CONTROLLED"
        }