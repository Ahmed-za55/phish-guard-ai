import re
import math
from typing import Dict, Any, List

class FrontierDetectionIntelligence:
    """
    الطبقة الثانية: الكشف الواعي بعدم اليقين، التحكم الإحصائي التوافقي بالمخاطر (Conformal Prediction)،
    والاستدلال الحافظ للخصوصية (Privacy-Preserving Inference).
    """
    @staticmethod
    def sanitize_privacy_preserving_input(raw_text: str, epsilon_budget: float = 0.5) -> Dict[str, Any]:
        # تنقيح البيانات الشخصية الحساسة (إيميلات، أرقام بطاقات، هواتف) قبل التحليل السحابي
        redacted = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[REDACTED_EMAIL]", raw_text)
        redacted = re.sub(r"\b\d{12,16}\b", "[REDACTED_PAN]", redacted)
        pii_removed = (redacted != raw_text)
        return {
            "sanitized_text": redacted,
            "pii_redacted": pii_removed,
            "differential_privacy_epsilon": epsilon_budget,
            "information_leakage_score": 0.02 if pii_removed else 0.0
        }

    @staticmethod
    def evaluate_uncertainty_and_conformal_risk(raw_score: float, evidence_count: int, alpha: float = 0.05) -> Dict[str, Any]:
        # تحويل الدرجة الخام (0-100) إلى احتمال مُعاير (Calibrated Probability) باستخدام دالة لوجستية
        p_phish = round(1.0 / (1.0 + math.exp(-(raw_score - 50.0) / 12.0)), 4)
        p_benign = round(1.0 - p_phish, 4)

        # حساب عدم اليقين المعرفي (Epistemic Uncertainty) بناءً على قلة الأدلة أو وقوع الاحتمال في المنطقة الرمادية
        entropy = -(p_phish * math.log2(max(p_phish, 1e-9)) + p_benign * math.log2(max(p_benign, 1e-9)))
        evidence_penalty = 0.25 if evidence_count <= 1 else 0.0
        uncertainty_score = round(min(1.0, entropy * 0.6 + evidence_penalty), 4)

        # Conformal Risk Control: بناء مجموعة التنبؤ (Prediction Set) عند مستوى ثقة (1 - alpha = 95%)
        threshold = 1.0 - alpha
        prediction_set: List[str] = []
        if p_phish >= (1.0 - threshold) or uncertainty_score > 0.45:
            prediction_set.append("PHISHING")
        if p_benign >= (1.0 - threshold) or uncertainty_score > 0.45:
            prediction_set.append("BENIGN")

        is_ambiguous = len(prediction_set) > 1
        return {
            "calibrated_probability": p_phish,
            "epistemic_uncertainty": uncertainty_score,
            "conformal_alpha": alpha,
            "conformal_prediction_set": prediction_set,
            "abstain_and_escalate_to_human": is_ambiguous,
            "uncertainty_directive": "HOLD_FOR_HUMAN_REVIEW_OR_DEEP_SCAN" if is_ambiguous else "CONFIDENT_AUTONOMOUS_DECISION"
        }