from typing import Dict, Any, List, Tuple

class PredictiveAttackUniverse:
    """
    التقنية الثانية: Predictive Attack Universe & Counterfactual Security Engine.
    - يبني رسم المسارات الهجومية المستقبلية (Attack Path Graph) بين الهويات والأجهزة والخدمات.
    - يحسب الخسارة المتوقعة عبر جميع المسارات الممكنة نحو الأصول الحرجة (Crown Jewels).
    - يجري محاكاة مضادة للواقع (What-If Node Interdiction) لاكتشاف نقطة التدخل ذات العائد الأعلى
      مقارنةً بالـ Baseline الساذج (الذي يعزل أول عقدة فقط).
    """
    @staticmethod
    def _enumerate_paths(
        graph: Dict[str, List[Tuple[str, float]]],
        current: str,
        targets: set,
        visited: set
    ) -> List[Tuple[List[str], float]]:
        if current in targets:
            return [([current], 1.0)]
        paths = []
        for nxt, prob in graph.get(current, []):
            if nxt not in visited:
                sub_paths = PredictiveAttackUniverse._enumerate_paths(graph, nxt, targets, visited | {nxt})
                for sp, s_prob in sub_paths:
                    paths.append(([current] + sp, prob * s_prob))
        return paths

    @classmethod
    def explore_future_attack_universe(
        cls,
        entry_nodes: List[str],
        adjacency_graph: Dict[str, List[Tuple[str, float]]],
        asset_values_usd: Dict[str, float],
        intervention_costs_usd: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        يحسب:
        1. إجمالي الخطر المستقبلي بدون تدخل.
        2. نتيجة الـ Baseline التقليدي (عزل أول نقطة دخول فقط).
        3. نقطة التدخل المثلى عبر محاكاة ماذا لو (Counterfactual Chokepoint Optimization).
        """
        crown_jewels = set(asset_values_usd.keys())

        def compute_expected_universe_damage(blocked_nodes: set) -> Tuple[float, List[Dict[str, Any]]]:
            active_paths = []
            # حساب احتمالية وصول المهاجم لكل أصل حرج عبر قانون دمج المسارات المستقلة: 1 - prod(1 - p_path)
            jewel_escape_probs = {j: 1.0 for j in crown_jewels}

            for start in entry_nodes:
                if start in blocked_nodes:
                    continue
                raw_paths = cls._enumerate_paths(adjacency_graph, start, crown_jewels, {start} | blocked_nodes)
                for path_nodes, path_prob in raw_paths:
                    jewel = path_nodes[-1]
                    jewel_escape_probs[jewel] *= (1.0 - path_prob)
                    active_paths.append({
                        "trajectory": " -> ".join(path_nodes),
                        "reachability_prob": round(path_prob, 4),
                        "target_asset": jewel,
                        "expected_path_loss_usd": round(path_prob * asset_values_usd[jewel], 2)
                    })

            total_damage = 0.0
            for j, prob_safe in jewel_escape_probs.items():
                compromise_prob = 1.0 - prob_safe
                total_damage += compromise_prob * asset_values_usd[j]

            return round(total_damage, 2), sorted(active_paths, key=lambda x: -x["expected_path_loss_usd"])

        # 1. العالم بدون تدخل (Unmitigated Future Universe)
        unmitigated_loss, all_trajectories = compute_expected_universe_damage(set())

        # 2. أداء الـ Baseline التقليدي (Reactive Entry-Node Block: يحظر أول نقطة دخول فقط)
        naive_node = entry_nodes[0]
        naive_residual_loss, _ = compute_expected_universe_damage({naive_node})
        naive_total_cost = round(naive_residual_loss + intervention_costs_usd.get(naive_node, 500.0), 2)

        # 3. محاكاة ماذا لو (Counterfactual Chokepoint Search) عبر جميع العقد الوسطية والمداخل
        candidate_nodes = set(intervention_costs_usd.keys())
        counterfactual_evaluations = []
        optimal_node = None
        optimal_total_cost = float("inf")

        for node in sorted(candidate_nodes):
            res_loss, _ = compute_expected_universe_damage({node})
            int_cost = intervention_costs_usd[node]
            combined_cost = round(res_loss + int_cost, 2)
            damage_avoided = round(unmitigated_loss - res_loss, 2)

            counterfactual_evaluations.append({
                "what_if_intervene_at": node,
                "intervention_cost_usd": int_cost,
                "residual_attack_loss_usd": res_loss,
                "total_economic_burden_usd": combined_cost,
                "net_damage_prevented_usd": damage_avoided
            })

            if combined_cost < optimal_total_cost:
                optimal_total_cost = combined_cost
                optimal_node = node

        savings_over_baseline = round(naive_total_cost - optimal_total_cost, 2)

        return {
            "total_future_trajectories_mapped": len(all_trajectories),
            "top_predicted_trajectories": all_trajectories[:4],
            "unmitigated_expected_loss_usd": unmitigated_loss,
            "reactive_baseline_interdiction_node": naive_node,
            "reactive_baseline_total_burden_usd": naive_total_cost,
            "optimal_chokepoint_node": optimal_node,
            "optimal_chokepoint_total_burden_usd": optimal_total_cost,
            "net_savings_vs_reactive_baseline_usd": savings_over_baseline,
            "counterfactual_what_if_ledger": counterfactual_evaluations
        }