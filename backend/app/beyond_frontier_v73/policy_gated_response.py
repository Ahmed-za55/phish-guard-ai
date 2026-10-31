import hashlib
from typing import Dict, Any, List

class PolicyGatedResponseAndExchangePlane:
    """
    الطبقة السابعة: تبادل استخبارات التهديدات مع احترام الخصوصية وسياسات الاحتفاظ،
    وتنفيذ الاستجابة المحكومة بالسياسات مع دعم التراجع الآمن.
    """
    @staticmethod
    def prepare_privacy_preserving_threat_exchange(urls: List[Dict[str, Any]], is_confirmed_threat: bool) -> Dict[str, Any]:
        # 10: Privacy-Preserving Threat Exchange — مشاركة مؤشرات مجزأة ومنقحة فقط مع سياسة انتهاء صلاحية
        shared_indicators = []
        if is_confirmed_threat:
            for u in urls:
                domain = u.get("url", "").split("//")[-1].split("/")[0].lower()
                if domain:
                    domain_hash = hashlib.sha256(domain.encode("utf-8")).hexdigest()
                    shared_indicators.append({"indicator_type": "domain_sha256", "value": domain_hash})

        return {
            "raw_payload_shared": False,
            "minimized_indicators_count": len(shared_indicators),
            "shared_indicators": shared_indicators,
            "retention_policy_days": 30,
            "anti_poisoning_quorum_required": True
        }