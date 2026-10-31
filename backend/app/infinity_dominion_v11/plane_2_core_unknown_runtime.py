import math
import hashlib
from typing import Dict, Any, List

class CoreDetectionUnknownPlane:
    """
    Plane 2 — Core Detection Runtime (Priority 2: PROJECT UNKNOWN + PARADOX + GENOME):
    - يطبق التصنيف الثلاثي الواعي بعدم اليقين: SAFE | MALICIOUS | UNKNOWN.
    - يحسب مسافة Out-of-Distribution (Mahalanobis-like Distance) لاكتشاف عائلات الهجوم غير المرئية في التدريب.
    - يبني البصمة السلوكية الجينية للحملة (PROJECT GENOME) ويكشف تناقض المصادر (PROJECT PARADOX).
    """
    # مراكز التوزيع المعروفة في التدريب (Benign Centroid & Known Phishing Centroid)
    _BENIGN_CENTROID = [0.15, 0.10, 3.60, 0.05]
    _MALICIOUS_CENTROID = [0.85, 0.80, 4.40, 0.90]
    _VARIANCE_SCALE = [0.12, 0.15, 0.35, 0.15]

    @classmethod
    def _mahalanobis_1d_approx(cls, vec: List[float], centroid: List[float]) -> float:
        dist_sq = 0.0
        for x, c, var in zip(vec, centroid, cls._VARIANCE_SCALE):
            dist_sq += ((x - c) ** 2) / max(var, 1e-6)
        return math.sqrt(dist_sq)

    @classmethod
    def evaluate_unseen_threat(
        cls,
        url_risk_norm: float,
        dom_suspicion: float,
        text_entropy: float,
        redirect_complexity: float,
        evidence_verdicts: List[str]
    ) -> Dict[str, Any]:
        feature_vec = [url_risk_norm, dom_suspicion, text_entropy, redirect_complexity]

        d_benign = cls._mahalanobis_1d_approx(feature_vec, cls._BENIGN_CENTROID)
        d_malicious = cls._mahalanobis_1d_approx(feature_vec, cls._MALICIOUS_CENTROID)
        min_dist = min(d_benign, d_malicious)

        # Out-of-Distribution (OOD): العينة بعيدة عن كل من العينات السليمة والخبيثة المعروفة
        is_ood_novel_family = min_dist > 3.15 or text_entropy > 4.95

        # PROJECT PARADOX: كشف التناقض الحاد بين الأدلة
        paradox_detected = ("SAFE" in evidence_verdicts) and ("MALICIOUS" in evidence_verdicts)

        # حساب عدم اليقين المعرفي (Epistemic Uncertainty)
        uncertainty = min(1.0, round((min_dist / 5.0) + (0.25 if paradox_detected else 0.0), 3))

        # القرار الثلاثي (Abstention-Capable Tri-State Verdict)
        if is_ood_novel_family and uncertainty >= 0.58 and d_malicious > 2.2:
            tri_state_verdict = "UNKNOWN_REQUIRES_DEEP_SANDBOX"
            novelty_explanation = "Sample lies outside known training manifolds (OOD) with high epistemic uncertainty."
        elif d_malicious < d_benign or url_risk_norm >= 0.72:
            tri_state_verdict = "MALICIOUS"
            novelty_explanation = "Novel Zero-Day behavioral anomaly." if is_ood_novel_family else "Matches known adversarial distribution."
        else:
            tri_state_verdict = "SAFE"
            novelty_explanation = "Within verified benign behavioral distribution."

        # PROJECT GENOME: بصمة سلوكية مقاومة للتغير السطحي
        genome_seq = f"R:{int(url_risk_norm*10)}-D:{int(dom_suspicion*10)}-E:{int(text_entropy)}-H:{int(redirect_complexity*10)}"
        campaign_genome_hash = f"genome_{hashlib.sha256(genome_seq.encode()).hexdigest()[:14]}"

        return {
            "plane": "CORE_DETECTION_RUNTIME_PLANE",
            "tri_state_verdict": tri_state_verdict,
            "ood_unseen_family_detected": is_ood_novel_family,
            "mahalanobis_min_distance": round(min_dist, 3),
            "epistemic_uncertainty": uncertainty,
            "paradox_contradiction_detected": paradox_detected,
            "novelty_explanation": novelty_explanation,
            "project_genome_signature": campaign_genome_hash
        }