import math
from typing import Dict, Any, List

class ProjectGenesisDiscovery:
    """
    PROJECT GENESIS:
    اكتشاف التهديدات المجهولة (Zero-Day & Open-Set Anomaly Discovery) عبر تحليل المسافة الإحصائية
    والإنتروبيا بدون الاعتماد على توقيعات مسبقة.
    """
    @staticmethod
    def discover_unknown_threats(feature_vector: List[float], text_entropy: float) -> Dict[str, Any]:
        # حساب الانحراف المعياري والمسافة عن النواة الطبيعية
        mean_val = sum(feature_vector) / max(len(feature_vector), 1)
        variance = sum((x - mean_val) ** 2 for x in feature_vector) / max(len(feature_vector), 1)
        std_dev = math.sqrt(variance)

        is_novel = std_dev > 2.8 or text_entropy > 4.85
        discovery_confidence = min(1.0, round((std_dev / 4.0) * 0.5 + (text_entropy / 6.0) * 0.5, 3))

        return {
            "genesis_unknown_threat_discovered": is_novel,
            "anomaly_deviation_score": round(std_dev, 3),
            "text_entropy_metric": text_entropy,
            "discovery_confidence": discovery_confidence,
            "hypothesis_generated": "NOVEL_BEHAVIORAL_EVASION_PATTERN" if is_novel else "KNOWN_DISTRIBUTION"
        }