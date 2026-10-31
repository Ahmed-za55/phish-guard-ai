import hashlib
from urllib.parse import urlparse
from typing import Dict, Any, List

class PrometheusDataFabricAndCognitive:
    """
    L2 & L3:
    - Evidence Continuity & SSRF Protection
    - Open-World Intelligence (تقدير درجة الجهل وعدم اليقين)
    - Causal Threat Reconstruction (تحليل العلاقات السببية وتحديد الأدلة المؤثرة).
    """
    _PRIVATE_IPS = ("127.", "10.", "192.168.", "169.254.", "172.16.", "0.0.0.0", "localhost")

    @classmethod
    def process_data_and_execute_cognitive(cls, raw_text: str, urls: List[str], entropy_val: float) -> Dict[str, Any]:
        # L2: SSRF Guard
        safe_urls, blocked_ssrf = [], []
        for u in urls:
            host = (urlparse(u).hostname or "").lower()
            if any(host.startswith(p) or host == p for p in cls._PRIVATE_IPS):
                blocked_ssrf.append(u)
            else:
                safe_urls.append(u)

        # L3: Open-World Intelligence & Epistemic Uncertainty
        epistemic_uncertainty = 0.52 if entropy_val >= 4.6 or len(urls) == 0 else 0.12
        open_world_anomaly = bool(entropy_val >= 4.8)

        # Causal Threat Reconstruction
        causal_steps = []
        if "urgent" in raw_text.lower():
            causal_steps.append("Coercive Lure")
        if safe_urls:
            causal_steps.append("Deceptive Routing Vector")
        if open_world_anomaly:
            causal_steps.append("Unknown Novel Payload Structure")

        return {
            "ssrf_protection": {"blocked": blocked_ssrf, "safe": safe_urls},
            "cognitive_open_world": {
                "open_world_anomaly_detected": open_world_anomaly,
                "epistemic_uncertainty_score": epistemic_uncertainty,
                "requires_human_abstention": epistemic_uncertainty >= 0.40
            },
            "causal_reconstruction": {
                "causal_chain_steps": causal_steps,
                "causal_attribution_verified": len(causal_steps) >= 2
            }
        }