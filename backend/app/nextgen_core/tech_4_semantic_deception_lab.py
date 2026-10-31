from typing import Dict, Any, List

class SemanticDeceptionLaboratory:
    """
    المسار الأول: Semantic Deception Laboratory (مختبر فهم الخداع البشري والرقمي).
    يدرس كيف يتم التلاعب بقرارات الإنسان عبر اللغتين الإنجليزية والعربية (الفصحى والعامية المصرية):
    1. Authority Impersonation (انتحال السلطة والقيادة).
    2. Coercive Urgency & Fear (التلاعب بالإلحاح والخوف).
    3. Thread Context Hijacking (تغيير سياق المحادثة المفاجئ إلى طلب مالي أو سري).
    4. Cross-Channel Isolation (محاولة نقل الضحية إلى قناة غير خاضعة للرقابة مثل واتساب/تليجرام).
    ويفصل بين "الطلب العاجل المشروع" و"التلاعب الخبيث" عبر معادلة التناقض السياقي (Contextual Dissonance).
    """
    PSYCHOLOGICAL_LEVERS = {
        "authority_coercion": [
            "ceo", "chief executive", "board of directors", "executive office", "legal department",
            "المدير التنفيذي", "رئيس مجلس الإدارة", "مكتب العميد", "الشؤون القانونية", "أمر مباشر من الإدارة"
        ],
        "urgency_and_fear": [
            "immediately", "within 1 hour", "account suspended", "legal action", "penalty", "terminated",
            "فوراً", "خلال ساعة", "إيقاف الحساب", "إجراء قانوني", "غرامة", "دلوقتي حالا", "هيتم قفل", "تحذير نهائي"
        ],
        "secrecy_and_isolation": [
            "keep this confidential", "do not discuss", "in a meeting cannot talk", "text me on whatsapp",
            "الأمر سري للغاية", "لا تبلغ أحداً", "أنا في اجتماع لا تتصل", "ابعتلي على واتساب", "محدش يعرف"
        ],
        "high_stakes_demand": [
            "wire transfer", "iban", "gift cards", "verify password", "otp", "seed phrase", "session token",
            "تحويل بنكي", "فاتورة مستعجلة", "كود التحقق", "الرقم السري", "كروت شحن", "فودافون كاش", "انستا باي"
        ]
    }

    @classmethod
    def analyze_human_deception(
        cls,
        message_text: str,
        prior_thread_topic: str = "GENERAL_OPERATIONS",
        sender_verified_role: str = "EXTERNAL_UNVERIFIED",
        channel_count: int = 1
    ) -> Dict[str, Any]:
        text_l = message_text.lower()

        lever_scores: Dict[str, float] = {}
        matched_cues: Dict[str, List[str]] = {}

        for lever, phrases in cls.PSYCHOLOGICAL_LEVERS.items():
            hits = [p for p in phrases if p in text_l]
            matched_cues[lever] = hits
            lever_scores[lever] = min(1.0, len(hits) * 0.55)

        # Baseline التقليدي: يعتمد فقط على وجود كلمات الإلحاح أو السلطة ( فيقع في False Positives مع رسائل المدير الحقيقية)
        naive_keyword_score = round(
            0.50 * lever_scores["authority_coercion"] + 0.50 * lever_scores["urgency_and_fear"], 4
        )
        baseline_verdict = "MALICIOUS_DECEPTION" if naive_keyword_score >= 0.50 else "BENIGN_REQUEST"

        # 1. حساب اختطاف السياق (Context Drift / Thread Hijacking)
        # إذا كانت المحادثة السابقة عادية ثم تحولت فجأة لطلب مالي أو سري
        context_hijack_score = 0.0
        if prior_thread_topic in {"GENERAL_OPERATIONS", "HR_ROUTINE", "PROJECT_SYNC"} and lever_scores["high_stakes_demand"] > 0:
            context_hijack_score = 0.85

        # 2. حساب التناقض بين الهوية المثبتة والسلطة المدعاة (Authority-Identity Dissonance)
        authority_dissonance = 0.0
        if lever_scores["authority_coercion"] > 0 and sender_verified_role != "VERIFIED_INTERNAL_EXECUTIVE":
            authority_dissonance = 0.90
        elif sender_verified_role == "VERIFIED_INTERNAL_EXECUTIVE" and lever_scores["high_stakes_demand"] == 0 and lever_scores["secrecy_and_isolation"] == 0:
            # مدير حقيقي يرسل تنبيهاً عاجلاً روتينياً بدون طلب تحويل سري أو عزل -> كبح الإنذار الكاذب!
            authority_dissonance = -0.45

        # 3. معامل التلاعب النفسي المركب (Cognitive Manipulation Index)
        multi_channel_boost = 0.15 if channel_count > 1 else 0.0
        cognitive_score = (
            0.25 * lever_scores["urgency_and_fear"]
            + 0.30 * lever_scores["high_stakes_demand"]
            + 0.25 * lever_scores["secrecy_and_isolation"]
            + 0.20 * context_hijack_score
            + authority_dissonance
            + multi_channel_boost
        )
        cognitive_score = max(0.0, min(1.0, round(cognitive_score, 4)))

        deception_verdict = "MALICIOUS_DECEPTION" if cognitive_score >= 0.55 else "LEGITIMATE_COMMUNICATION"

        active_levers = [k for k, v in lever_scores.items() if v > 0]
        if context_hijack_score > 0:
            active_levers.append("thread_context_hijacking")
        if authority_dissonance > 0:
            active_levers.append("unverified_authority_impersonation")

        return {
            "deception_verdict": deception_verdict,
            "cognitive_manipulation_index": cognitive_score,
            "naive_keyword_baseline_verdict": baseline_verdict,
            "naive_keyword_baseline_score": naive_keyword_score,
            "active_psychological_levers": active_levers,
            "matched_linguistic_cues": {k: v for k, v in matched_cues.items() if v},
            "context_hijack_detected": context_hijack_score > 0,
            "sender_role_verified": sender_verified_role
        }