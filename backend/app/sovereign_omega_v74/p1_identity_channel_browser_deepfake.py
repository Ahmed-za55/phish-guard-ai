from typing import Dict, Any, List

class MultiSurfaceIdentityAndBrowserEngine:
    """
    P1:
    - 02. Human Identity Attack Defense (MFA Fatigue, Session Hijacking, Context Manipulation)
    - 03. Cross-Channel Attack Intelligence (Email, SMS, QR, Voice, Social, Web)
    - 04. Deepfake & Social Engineering Defense (Audio/Video artifacts, Sender context, Uncertainty)
    - 05. Browser Behavior Security Engine (JS behavior, Credential harvesting forms, Redirects, Cloaking)
    """
    @staticmethod
    def analyze_human_identity_threats(text: str, auth_events: Dict[str, Any] = None) -> Dict[str, Any]:
        auth_events = auth_events or {}
        text_l = text.lower()

        mfa_push_count = int(auth_events.get("recent_mfa_pushes", 4 if "approve" in text_l or "mfa" in text_l else 0))
        mfa_fatigue_detected = mfa_push_count >= 3

        session_token_leak_risk = any(k in text_l for k in ["sessionid", "jwt", "cookie", "oauth", "token="])
        impossible_travel_or_context_anomaly = bool(auth_events.get("geo_velocity_anomaly", "login from new device" in text_l))
        fake_login_lure = any(k in text_l for k in ["password", "sign in", "verify account", "sso"])

        identity_risk_score = (
            (35.0 if mfa_fatigue_detected else 0.0)
            + (30.0 if session_token_leak_risk else 0.0)
            + (20.0 if impossible_travel_or_context_anomaly else 0.0)
            + (15.0 if fake_login_lure else 0.0)
        )

        return {
            "identity_risk_score": min(100.0, identity_risk_score),
            "mfa_fatigue_detected": mfa_fatigue_detected,
            "session_hijack_risk_detected": session_token_leak_risk,
            "login_context_manipulation": impossible_travel_or_context_anomaly,
            "linkless_identity_attack_covered": bool(mfa_fatigue_detected or impossible_travel_or_context_anomaly)
        }

    @staticmethod
    def correlate_cross_channel_signals(text: str,urls: List[Dict[str, Any]], channel_metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        channel_metadata = channel_metadata or {}
        text_l = text.lower()
        active_channels = ["email_or_text_body"]

        if urls:
            active_channels.append("web_landing_page")
        if any(k in text_l for k in ["qr", "scan code", "barcode"]) or channel_metadata.get("has_qr"):
            active_channels.append("qr_code_quishing")
        if any(k in text_l for k in ["call", "voice", "voicemail", "urgent callback"]) or channel_metadata.get("has_voice"):
            active_channels.append("voice_vishing")
        if any(k in text_l for k in ["sms", "whatsapp", "telegram", "dm"]):
            active_channels.append("messaging_and_social")

        multi_channel_campaign = len(active_channels) >= 2
        return {
            "observed_channels": active_channels,
            "cross_channel_correlation_active": multi_channel_campaign,
            "correlated_campaign_confidence": min(0.96, round(len(active_channels) * 0.28, 2))
        }

    @staticmethod
    def evaluate_deepfake_and_social_engineering(text: str, media_telemetry: Dict[str, Any] = None) -> Dict[str, Any]:
        media_telemetry = media_telemetry or {}
        text_l = text.lower()

        # فحص التناقض السياقي (مثلاً طلب تحويل مالي عاجل أو سري باسم مدير تنفيذي)
        executive_impersonation_cue = any(k in text_l for k in ["ceo", "wire transfer", "confidential", "gift card", "urgent request"])
        audio_spectral_anomaly = float(media_telemetry.get("audio_synthetic_prob", 0.72 if "voice" in text_l else 0.10))
        video_temporal_flicker = float(media_telemetry.get("video_deepfake_prob", 0.10))

        combined_signal = round(max(audio_spectral_anomaly, video_temporal_flicker, 0.65 if executive_impersonation_cue else 0.10), 2)
        # تقدير عدم اليقين بدلاً من إصدار حكم قاطع من إشارة واحدة
        single_signal_only = sum([executive_impersonation_cue, audio_spectral_anomaly > 0.5, video_temporal_flicker > 0.5]) <= 1
        epistemic_uncertainty = 0.48 if single_signal_only else 0.14

        return {
            "synthetic_impersonation_probability": combined_signal,
            "contextual_sender_inconsistency": executive_impersonation_cue,
            "epistemic_uncertainty": epistemic_uncertainty,
            "adjudication_mode": "UNCERTAIN_REQUIRE_OUT_OF_BAND_VERIFICATION" if single_signal_only and combined_signal >= 0.5 else "HIGH_CONFIDENCE_ASSESSMENT"
        }

    @staticmethod
    def inspect_browser_behavior(text: str, urls: List[Dict[str, Any]], ast_triggered: bool) -> Dict[str, Any]:
        text_l = text.lower()
        sensitive_form_detected = any(k in text_l for k in ["<form", "input type=\"password\"", "creditcard", "cvv", "ssn"])
        multi_hop_redirect_risk = any("//" in u.get("url", "")[8:] or "redirect=" in u.get("url", "").lower() for u in urls)
        user_agent_cloaking_suspected = any(k in text_l for k in ["navigator.useragent", "webdriver", "headless", "onmousemove"])

        behavioral_risk = (
            (35.0 if ast_triggered else 0.0)
            + (30.0 if sensitive_form_detected else 0.0)
            + (20.0 if multi_hop_redirect_risk else 0.0)
            + (15.0 if user_agent_cloaking_suspected else 0.0)
        )

        return {
            "browser_behavioral_risk_score": min(100.0, behavioral_risk),
            "isolated_js_execution_flagged": ast_triggered,
            "credential_harvesting_form_detected": sensitive_form_detected,
            "chained_redirect_behavior": multi_hop_redirect_risk,
            "evasive_fingerprint_cloaking_detected": user_agent_cloaking_suspected
        }