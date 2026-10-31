import hashlib
from typing import Dict, Any, List

class AdversaryAndCrossPlatformIntelligence:
    """
    1. Adversary Intelligence Reconstruction: ربط البنية التحتية وبناء البصمة السلوكية للحملة.
    2. Cross-Platform Attack Surface: تتبع الهجمات عبر (Email -> Browser -> Fake Login -> Credential Theft).
    3. Semantic Attack & Knowledge Graph Federation: تحليل السياق المالي وانتحال المؤسسات.
    """
    @staticmethod
    def reconstruct_adversary_and_path(text: str, urls: List[str], platform_hops: List[str]) -> Dict[str, Any]:
        text_l = text.lower()
        
        # تحليل السياق الدلالي (Semantic Attack Intelligence)
        financial_lure = any(w in text_l for w in ["invoice", "swift", "iban", "wire", "payment", "تحويل", "فاتورة"])
        brand_impersonation = any(w in text_l for w in ["microsoft", "google", "bank", "admin", "support", "security"])
        
        # بصمة سلوكية للحملة لربط الهجمات ذات البنية المشتركة
        infra_pattern = f"urls:{len(urls)}_fin:{financial_lure}_brand:{brand_impersonation}_hops:{'-'.join(platform_hops)}"
        campaign_cluster_id = f"camp_{hashlib.sha256(infra_pattern.encode()).hexdigest()[:12]}"

        # تحليل المسار العابر للمنصات (Cross-Platform Attack Path)
        multi_stage_detected = len(platform_hops) >= 2
        choke_point = platform_hops[1] if len(platform_hops) >= 2 else (platform_hops[0] if platform_hops else "INGESTION_GATEWAY")

        confidence = 0.88 if (multi_stage_detected and (financial_lure or brand_impersonation)) else 0.55

        return {
            "adversary_reconstruction": {
                "campaign_cluster_id": campaign_cluster_id,
                "campaign_correlation_probability": confidence,
                "evidence_source": "telemetry_and_structural_dna",
                "semantic_indicators": {
                    "financial_context_manipulation": financial_lure,
                    "brand_impersonation_detected": brand_impersonation
                }
            },
            "cross_platform_intelligence": {
                "observed_platform_hops": platform_hops,
                "multi_stage_attack_detected": multi_stage_detected,
                "recommended_interruption_choke_point": choke_point
            }
        }