from typing import Dict, Any, List

class CrossSignalGraphEngine:
    """
    يربط المؤشرات المنفردة (روابط، سلوك نصي، علامات أمان) في رسم بياني موحد
    مع الاحتفاظ بمصدر كل إشارة ودرجة موثوقيتها لكشف حملات التصيد المترابطة.
    """
    SOURCE_RELIABILITY = {
        "url_lexical_scanner": 0.85,
        "ast_deobfuscator": 0.95,
        "homograph_detector": 0.98,
        "linguistic_heuristic": 0.70,
        "external_security_flag": 0.90
    }

    @classmethod
    def correlate_signals(cls, urls: List[Dict[str, Any]], ast_res: Dict[str, Any], homograph_res: Dict[str, Any], urgency_detected: bool, flags: List[str]) -> Dict[str, Any]:
        nodes = []
        edges = []
        weighted_score = 0.0

        for idx, u in enumerate(urls):
            node_id = f"url_node_{idx}"
            rel = cls.SOURCE_RELIABILITY["url_lexical_scanner"]
            risk = float(u.get("risk_score", 0.0))
            nodes.append({"id": node_id, "type": "url", "raw_risk": risk, "source": "url_lexical_scanner", "reliability": rel})
            weighted_score += (risk * rel * 0.4)

        if ast_res.get("deep_inspection_triggered"):
            rel = cls.SOURCE_RELIABILITY["ast_deobfuscator"]
            nodes.append({"id": "signal_ast", "type": "script_payload", "raw_risk": 85.0, "source": "ast_deobfuscator", "reliability": rel})
            weighted_score += (85.0 * rel * 0.35)
            if urls:
                edges.append({"from": "url_node_0", "to": "signal_ast", "relation": "delivers_obfuscated_code"})

        if homograph_res.get("idn_homograph_attack_detected"):
            rel = cls.SOURCE_RELIABILITY["homograph_detector"]
            nodes.append({"id": "signal_homograph", "type": "visual_spoof", "raw_risk": 95.0, "source": "homograph_detector", "reliability": rel})
            weighted_score += (95.0 * rel * 0.45)
            if urls:
                edges.append({"from": "url_node_0", "to": "signal_homograph", "relation": "impersonates_brand_domain"})

        if urgency_detected:
            rel = cls.SOURCE_RELIABILITY["linguistic_heuristic"]
            nodes.append({"id": "signal_urgency", "type": "social_engineering", "raw_risk": 45.0, "source": "linguistic_heuristic", "reliability": rel})
            weighted_score += (45.0 * rel * 0.20)
            if urls:
                edges.append({"from": "signal_urgency", "to": "url_node_0", "relation": "coerces_click_action"})

        # تضخيم الخطر في حال تلاقي أكثر من إشارة ضعيفة (Campaign Correlation)
        multi_signal_multiplier = 1.25 if len(nodes) >= 3 else (1.10 if len(nodes) == 2 else 1.0)
        correlated_risk = min(100.0, round(weighted_score * multi_signal_multiplier, 2))

        return {
            "correlated_risk_score": correlated_risk,
            "signal_nodes_count": len(nodes),
            "campaign_correlation_detected": len(edges) >= 2,
            "signal_graph": {"nodes": nodes, "edges": edges}
        }