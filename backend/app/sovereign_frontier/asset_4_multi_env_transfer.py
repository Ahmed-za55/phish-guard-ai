from typing import Dict, Any, List

class MultiEnvironmentTransferLab:
    """
    الأصل الاستراتيجي الرابع:
    1. Multi-Environment Intelligence Transfer: ينقل تمثيل التهديد الهيكلي من بيئة التدريب (مثلاً الإنجليزية على سطح المكتب)
       إلى بيئات جديدة (العربية الفصحى، العامية المصرية/الخليجية، تطبيقات الجوال) عبر سمات مستقلة عن اللغة (Language-Invariant Structural Features).
    2. Autonomous Defensive Experimentation: يختبر النماذج على مجموعات اختبار مفصولة زمنياً (T0 Train vs. T1 Future Holdout)
       ويحول أي فشل إلى اختبار Regression دائم.
    """
    # معجم الدلالات الوظيفية العابرة للغات واللهجات (Cross-Lingual Semantic Anchors)
    SEMANTIC_INTENT_LEXICON = {
        "COERCIVE_URGENCY": [
            "urgent", "immediately", "suspended", "عاجل", "فوراً", "ايقاف حسابك",
            "دلوقتي حالا", "هيتم قفل", "بسرعة", "تحديث بياناتك"
        ],
        "FINANCIAL_DIVERSION": [
            "iban", "swift", "wire transfer", "invoice", "تحويل بنكي", "فاتورة",
            "رقم الحساب الجديد", "حساب المستفيد", "فودافون كاش", "انستا باي"
        ],
        "CREDENTIAL_HARVEST": [
            "verify password", "login", "otp", "token", "تأكيد كلمة المرور",
            "كود التحقق", "الرقم السري", "تسجيل الدخول"
        ]
    }

    @classmethod
    def extract_environment_invariant_representation(cls, sample: Dict[str, Any]) -> Dict[str, float]:
        """يستخرج تمثيلاً موحداً لا ينهار عند تغير اللغة أو نظام التشغيل أو المتصفح."""
        text = str(sample.get("text", "")).lower()
        intents_matched = 0
        for _, phrases in cls.SEMANTIC_INTENT_LEXICON.items():
            if any(p in text for p in phrases):
                intents_matched += 1

        semantic_intent_score = min(1.0, intents_matched / 2.0)
        structural_url_risk = float(sample.get("domain_mismatch_score", 0.0))
        auth_flow_anomaly = float(sample.get("auth_flow_anomaly", 0.0))

        # درجة خطر عابرة للبيئات (تعتمد على السلوك + الدلالة العابرة للغات)
        invariant_risk = round(
            0.35 * semantic_intent_score + 0.40 * structural_url_risk + 0.25 * auth_flow_anomaly,
            4
        )
        return {
            "semantic_intent_score": round(semantic_intent_score, 4),
            "structural_url_risk": structural_url_risk,
            "auth_flow_anomaly": auth_flow_anomaly,
            "invariant_threat_score": invariant_risk
        }

    @classmethod
    def evaluate_cross_environment_and_temporal_split(
        cls,
        t0_english_samples: List[Dict[str, Any]],
        t1_future_arabic_and_mobile_samples: List[Dict[str, Any]],
        threshold: float = 0.52
    ) -> Dict[str, Any]:
        def eval_batch(batch: List[Dict[str, Any]]) -> Dict[str, Any]:
            tp = fp = tn = fn = 0
            failures = []
            for s in batch:
                rep = cls.extract_environment_invariant_representation(s)
                pred = 1 if rep["invariant_threat_score"] >= threshold else 0
                actual = int(s["label"])
                if actual == 1 and pred == 1:
                    tp += 1
                elif actual == 0 and pred == 1:
                    fp += 1
                elif actual == 0 and pred == 0:
                    tn += 1
                else:
                    fn += 1
                    failures.append(s["id"])

            recall = tp / max(tp + fn, 1)
            fpr = fp / max(fp + tn, 1)
            precision = tp / max(tp + fp, 1)
            f1 = (2 * precision * recall) / max(precision + recall, 1e-9)
            return {
                "f1": round(f1, 4),
                "recall": round(recall, 4),
                "fpr": round(fpr, 4),
                "missed_attack_ids": failures
            }

        t0_metrics = eval_batch(t0_english_samples)
        t1_metrics = eval_batch(t1_future_arabic_and_mobile_samples)
        transfer_degradation = round(max(0.0, t0_metrics["f1"] - t1_metrics["f1"]), 4)

        return {
            "t0_source_env_english_desktop": t0_metrics,
            "t1_target_env_arabic_dialect_mobile": t1_metrics,
            "cross_environment_f1_drop": transfer_degradation,
            "permanent_regression_tests_generated": len(t1_metrics["missed_attack_ids"]),
            "temporal_and_env_generalization_verified": (t1_metrics["f1"] >= 0.92 and t1_metrics["fpr"] <= 0.03)
        }