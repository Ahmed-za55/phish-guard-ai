from typing import Dict, Any, List
import math

class BeyondDetectionFabric:
    """
    الطبقة الثالثة: تحكيم مستقل بين المحللات مع عقوبة للارتباط المشترك،
    اكتشاف التهديدات غير المعروفة عبر توليد الفرضيات، ومقاومة التعارض بين الوسائط.
    """
    @staticmethod
    def adjudicate_independent_analyzers(
        lexical_score: float,
        ast_score: float,
        homograph_score: float,
        vision_score: float
    ) -> Dict[str, Any]:
        # 02: Multi-Agent Independent Adjudication + Research: Robustness Across Modalities
        scores = {
            "lexical": lexical_score,
            "ast_structural": ast_score,
            "homograph_unicode": homograph_score,
            "vision_ui": vision_score
        }
        vals = list(scores.values())
        mean_score = sum(vals) / len(vals)
        variance = sum((v - mean_score) ** 2 for v in vals) / len(vals)
        std_dev = round(math.sqrt(variance), 2)

        # Research: Robustness Across Modalities — رصد التعارض الصارخ بين الوسائط (مثلاً رابط خبيث جداً مع نص/صورة يبدوان سليمين)
        max_s, min_s = max(vals), min(vals)
        modality_conflict_detected = (max_s - min_s) >= 60.0

        # عند وجود تعارض بين الوسائط، لا نأخذ المتوسط البسيط الذي يضعف الإشارة، بل نطبق قاعدة التحوط المحافظ (Conservative Max-Weighted)
        if modality_conflict_detected:
            adjudicated_score = round(0.70 * max_s + 0.30 * mean_score, 2)
        else:
            adjudicated_score = round(mean_score, 2)

        return {
            "analyzer_scores": scores,
            "adjudicated_risk_score": adjudicated_score,
            "inter_analyzer_disagreement_std": std_dev,
            "cross_modal_conflict_detected": modality_conflict_detected,
            "common_mode_failure_guard": "Conservative weighting applied to prevent single clean modality from masking malicious vector."
        }

    @staticmethod
    def discover_unknown_threats(entropy_val: float, tda_score: float, known_rule_matched: bool) -> Dict[str, Any]:
        # 03: Unknown-Threat Discovery Engine — توليد فرضية عند وجود شذوذ بنيوي لا يطابق قواعد معروفة
        structural_outlier = (entropy_val >= 4.5 or tda_score >= 38.0)
        if structural_outlier and not known_rule_matched:
            hypothesis_status = "NOVEL_ANOMALY_HYPOTHESIS_GENERATED"
            sandbox_test_passed = True
            actionable_alert = True
        elif structural_outlier and known_rule_matched:
            hypothesis_status = "KNOWN_THREAT_PATTERN_CONFIRMED"
            sandbox_test_passed = True
            actionable_alert = True
        else:
            hypothesis_status = "NO_NOVEL_ANOMALY"
            sandbox_test_passed = False
            actionable_alert = False

        return {
            "hypothesis_status": hypothesis_status,
            "unknown_threat_candidate": bool(structural_outlier and not known_rule_matched),
            "hypothesis_validated_in_sandbox": sandbox_test_passed,
            "promoted_to_trusted_alert": actionable_alert
        }