import math
from typing import Dict, Any, List, Tuple, Set

class DigitalWorldModel:
    """
    الأصل الاستراتيجي الأول: Digital World Model & Cross-Reality Threat Correlation.
    يبني تمثيلاً ديناميكياً للعلاقات الطبيعية بين (Users, Browsers, Mobile, Cloud, IdP, APIs)،
    يرصد العلاقات غير المنطقية طوبولوجياً، ويحاكي تأثير اختراق كيان واحد على بقية المنظومة.
    """
    def __init__(self):
        # Baseline normal transition frequencies: (source_entity, target_entity) -> count
        self.baseline_edges: Dict[Tuple[str, str], int] = {}
        self.entity_types: Dict[str, str] = {}
        self.adjacency: Dict[str, Dict[str, float]] = {}

    def learn_normal_environment(self, interactions: List[Tuple[str, str, str, str]]) -> None:
        """يتعلم شكل البيئة الطبيعية من أحداث تاريخية: (src, src_type, dst, dst_type)."""
        for src, s_type, dst, d_type in interactions:
            self.entity_types[src] = s_type
            self.entity_types[dst] = d_type
            pair = (src, dst)
            self.baseline_edges[pair] = self.baseline_edges.get(pair, 0) + 1
            self.adjacency.setdefault(src, {})
            # وزن انتشار الخطر يعتمد على تردد الاتصال
            self.adjacency[src][dst] = min(0.95, 0.25 + 0.15 * self.baseline_edges[pair])

    def correlate_cross_reality_events(self, live_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        يربط إشارات من عوالم مختلفة (Email, Browser, Mobile, IdP, API) ويكتشف:
        1. الحواف غير المنطقية التي لم تظهر في البيئة الطبيعية.
        2. الهجمات المركبة التي تبدو طبيعية منفردة لكنها خطيرة عند جمعها عبر القنوات.
        """
        anomalous_relations = []
        realities_observed: Set[str] = set()
        accumulated_anomaly_score = 0.0

        for ev in live_events:
            src = ev["src"]
            dst = ev["dst"]
            channel = ev.get("reality_channel", "UNKNOWN")
            signal_risk = float(ev.get("signal_risk", 0.2))
            realities_observed.add(channel)

            is_unseen_edge = (src, dst) not in self.baseline_edges
            if is_unseen_edge:
                anomalous_relations.append(f"{src}->{dst} via {channel}")
                accumulated_anomaly_score += signal_risk * 1.4
            else:
                accumulated_anomaly_score += signal_risk * 0.5

        # معامل التضخيم عبر العوالم: ظهور إشارات متزامنة في 3+ قنوات مختلفة يرفع خطورة الحملة
        cross_reality_multiplier = 1.0 + (0.25 * max(0, len(realities_observed) - 1))
        correlated_risk = min(1.0, round((accumulated_anomaly_score / max(len(live_events), 1)) * cross_reality_multiplier, 4))

        return {
            "realities_correlated": sorted(list(realities_observed)),
            "illogical_new_relations": anomalous_relations,
            "cross_reality_amplification": round(cross_reality_multiplier, 2),
            "correlated_campaign_risk": correlated_risk,
            "emergent_threat_detected": correlated_risk >= 0.65
        }

    def simulate_entity_compromise_blast_radius(self, compromised_node: str, infection_threshold: float = 0.25) -> Dict[str, Any]:
        """يحاكي انتشار الاختراق عبر البيئة الرقمية باستخدام انتشار الاحتمالات (Iterative Risk Propagation)."""
        infection_prob: Dict[str, float] = {compromised_node: 1.0}
        frontier = [compromised_node]

        while frontier:
            curr = frontier.pop(0)
            curr_p = infection_prob[curr]
            for neighbor, edge_weight in self.adjacency.get(curr, {}).items():
                propagated_p = round(curr_p * edge_weight, 4)
                if propagated_p >= infection_threshold and propagated_p > infection_prob.get(neighbor, 0.0):
                    infection_prob[neighbor] = propagated_p
                    frontier.append(neighbor)

        vulnerable_zones = [
            {"entity": k, "type": self.entity_types.get(k, "SERVICE"), "compromise_probability": v}
            for k, v in sorted(infection_prob.items(), key=lambda x: -x[1])
            if k != compromised_node
        ]
        return {
            "seed_compromised_entity": compromised_node,
            "affected_entities_count": len(vulnerable_zones),
            "most_vulnerable_zones": vulnerable_zones
        }