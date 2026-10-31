from typing import Dict, Any, List

class CriticalInfrastructureAndPropagation:
    """
    Critical Infrastructure Protection & Cyber Risk Propagation Simulator:
    - حماية بيئات OT و ICS ورصد الاتصالات غير الطبيعية.
    - محاكاة انتشار المخاطر وحساب الـ Blast Radius قبل اتخاذ قرار الاحتواء.
    """
    @staticmethod
    def simulate_risk_propagation(initial_compromised_node: str, network_nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
        infected_nodes = [n["id"] for n in network_nodes if n.get("connected_to", "") == initial_compromised_node or n.get("risk", 0) > 75]
        blast_radius_ratio = round(len(infected_nodes) / max(len(network_nodes), 1), 2)

        ot_ics_alert = any(n.get("is_ot_system", False) for n in network_nodes if n["id"] in infected_nodes)

        return {
            "initial_compromised_node": initial_compromised_node,
            "infected_nodes_propagated": infected_nodes,
            "blast_radius_ratio": blast_radius_ratio,
            "ot_ics_physical_safety_alert": ot_ics_alert,
            "recommended_containment_boundary": "AIR_GAP_ISOLATE_SUBNET" if ot_ics_alert else "CONTAIN_NODE"
        }