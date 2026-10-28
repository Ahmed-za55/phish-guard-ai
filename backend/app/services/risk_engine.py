from typing import Any


CATEGORY_WEIGHTS = {
    "phishing": 22,
    "credential theft": 18,
    "brand impersonation": 16,
    "reply-to mismatch": 10,
    "social engineering": 10,
    "malicious link": 14,
    "attachment risk": 14,
    "financial fraud": 12,
    "account takeover": 18,
    "malware": 20,
    "smishing": 10,
}


def normalize_text(value: str) -> str:
    return " ".join(value.lower().strip().split())


def classify_threat(threat: str) -> str:
    normalized = normalize_text(threat)

    if normalized in {
        "phishing",
        "smishing",
        "smishing (sms phishing)",
        "sms phishing",
    }:
        return "phishing"

    if normalized in {
        "credential theft",
        "credential harvesting",
    }:
        return "credential theft"

    if normalized in {
        "brand impersonation",
        "display-name impersonation",
        "display name impersonation",
        "impersonation",
    }:
        return "brand impersonation"

    if normalized in {
        "reply-to mismatch",
        "reply to mismatch",
    }:
        return "reply-to mismatch"

    if normalized in {
        "malicious link",
        "malicious links",
    }:
        return "malicious link"

    if any(
        keyword in normalized
        for keyword in {
            "malicious attachment",
            "malicious attachments",
            "suspicious attachment",
            "suspicious attachments",
            "double-extension attachment",
            "double extension attachment",
            "double-extension attachments",
            "double extension attachments",
            "executable attachment",
            "executable attachments",
            "attachment risk",
            "attachment detected",
        }
    ):
        return "attachment risk"

    if normalized == "social engineering":
        return "social engineering"

    if normalized == "financial fraud":
        return "financial fraud"

    if normalized == "account takeover":
        return "account takeover"

    if normalized == "malware":
        return "malware"

    return normalized


def _flag_category(flag: str) -> str | None:
    normalized = normalize_text(flag)

    if (
        "display name" in normalized
        or "display-name" in normalized
        or "impersonate" in normalized
        or "impersonat" in normalized
        or "levenshtein" in normalized
    ):
        return "brand impersonation"

    if (
        "reply-to address" in normalized
        or "reply-to domain" in normalized
        or "reply-to" in normalized
    ):
        return "reply-to mismatch"

    if (
        "high-risk attachment" in normalized
        or "suspicious attachment" in normalized
        or "attachment detected" in normalized
        or "executable attachment" in normalized
        or "double-extension" in normalized
        or "double extension" in normalized
    ):
        return "attachment risk"

    return None


def calculate_risk_breakdown(
    is_phishing: bool,
    confidence: float,
    threats: list[str],
    url_results: list[dict],
    security_flags: list[str] | None = None,
) -> dict[str, Any]:
    """
    Calculate a calibrated and mathematically explainable risk score.
    """
    security_flags = security_flags or []

    contributions: list[dict[str, Any]] = []
    raw_score = 0.0

    # 1. AI CONFIDENCE
    confidence_points = round(
        max(0.0, min(confidence, 1.0)) * 12,
        2,
    )

    if confidence_points > 0:
        raw_score += confidence_points
        contributions.append(
            {
                "signal": "AI confidence",
                "source": "AI",
                "points": confidence_points,
            }
        )

    # 2. PHISHING VERDICT
    if is_phishing:
        phishing_points = CATEGORY_WEIGHTS["phishing"]
        raw_score += phishing_points
        contributions.append(
            {
                "signal": "Phishing verdict",
                "source": "AI",
                "points": phishing_points,
            }
        )

    # 3. AI THREAT CATEGORIES
    scored_categories: set[str] = set()

    for threat in threats:
        category = classify_threat(threat)
        if not category or category in scored_categories:
            continue

        if category == "phishing":
            scored_categories.add(category)
            continue

        points = CATEGORY_WEIGHTS.get(category, 6)
        scored_categories.add(category)
        raw_score += points

        contributions.append(
            {
                "signal": category.title(),
                "source": "Threat classification",
                "points": points,
            }
        )

    # 4. DETERMINISTIC SECURITY FLAGS
    deterministic_categories: set[str] = set()

    for flag in security_flags:
        category = _flag_category(flag)
        if not category or category in scored_categories or category in deterministic_categories:
            continue

        deterministic_categories.add(category)

        if category == "brand impersonation":
            points = 8
            signal_name = "Display-name / brand mismatch"
        elif category == "reply-to mismatch":
            points = 6
            signal_name = "Reply-To mismatch"
        elif category == "attachment risk":
            points = 8
            signal_name = "Attachment risk"
        else:
            points = 5
            signal_name = "Email security signal"

        raw_score += points
        contributions.append(
            {
                "signal": signal_name,
                "source": "Deterministic security check",
                "points": points,
            }
        )

    # 5. URL & MATHEMATICAL TELEMETRY RISK
    highest_url_score = 0

    if url_results:
        highest_url_score = max(
            int(url.get("risk_score", 0))
            for url in url_results
        )

        url_points = round(
            min(highest_url_score * 0.25, 20),
            2,
        )

        if url_points > 0:
            raw_score += url_points
            contributions.append(
                {
                    "signal": "Highest URL risk",
                    "source": "URL analysis",
                    "points": url_points,
                }
            )

        has_entropy_anomaly = any(
            "Shannon Information Entropy" in reason
            for url in url_results
            for reason in url.get("reasons", [])
        )
        if has_entropy_anomaly:
            raw_score += 6
            contributions.append(
                {
                    "signal": "Shannon Entropy Anomaly H(X)",
                    "source": "Mathematical Security Model",
                    "points": 6,
                }
            )

        has_levenshtein_spoof = any(
            "Levenshtein similarity" in reason
            for url in url_results
            for reason in url.get("reasons", [])
        )
        if has_levenshtein_spoof:
            raw_score += 8
            contributions.append(
                {
                    "signal": "Levenshtein Distance Spoofing d_L",
                    "source": "Mathematical Security Model",
                    "points": 8,
                }
            )

        suspicious_urls = sum(
            1
            for url in url_results
            if int(url.get("risk_score", 0)) >= 45
        )

        if suspicious_urls >= 2:
            multiple_url_points = min(5, suspicious_urls)
            raw_score += multiple_url_points
            contributions.append(
                {
                    "signal": f"{suspicious_urls} suspicious URLs",
                    "source": "URL analysis",
                    "points": multiple_url_points,
                }
            )

    # 6. FINAL SCORE
    raw_score = round(raw_score, 2)
    final_score = round(max(0, min(raw_score, 100)))

    # 7. RISK LEVEL
    if final_score >= 75:
        risk_level = "CRITICAL"
    elif final_score >= 50:
        risk_level = "HIGH"
    elif final_score >= 25:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "raw_score": raw_score,
        "risk_score": final_score,
        "risk_level": risk_level,
        "capped": raw_score > 100,
        "highest_url_score": highest_url_score,
        "contributions": contributions,
    }


def calculate_risk_score(
    is_phishing: bool,
    confidence: float,
    threats: list[str],
    url_results: list[dict],
    security_flags: list[str] | None = None,
) -> tuple[int, str]:
    """
    Backward-compatible risk score function.
    """
    breakdown = calculate_risk_breakdown(
        is_phishing=is_phishing,
        confidence=confidence,
        threats=threats,
        url_results=url_results,
        security_flags=security_flags,
    )

    return (
        breakdown["risk_score"],
        breakdown["risk_level"],
    )