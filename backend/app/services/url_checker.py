import re
from urllib.parse import urlparse
from app.services.brand_detector import detect_brand_impersonation
URL_PATTERN = re.compile(
    r"https?://[^\s<>\"]+",
    re.IGNORECASE,
)


# Common legitimate brands attackers often impersonate.
BRAND_KEYWORDS = {
    "paypal",
    "microsoft",
    "apple",
    "google",
    "amazon",
    "facebook",
    "instagram",
    "whatsapp",
    "netflix",
    "bank",
    "visa",
    "mastercard",
}

# Terms commonly found in credential/payment phishing URLs.
SUSPICIOUS_PATH_TERMS = {
    "login",
    "signin",
    "sign-in",
    "verify",
    "verification",
    "account",
    "secure",
    "security",
    "password",
    "payment",
    "billing",
    "wallet",
    "update",
    "confirm",
    "unlock",
    "suspend",
    "recover",
}

# Shorteners hide the final destination.
URL_SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "is.gd",
    "ow.ly",
    "cutt.ly",
    "rebrand.ly",
}

# TLDs that can appear frequently in abusive registrations.
# This is only a signal, NOT proof of maliciousness.
SUSPICIOUS_TLDS = {
    "xyz",
    "top",
    "click",
    "shop",
    "online",
    "site",
    "icu",
    "buzz",
}


def extract_urls(text: str) -> list[str]:
    """Extract HTTP/HTTPS URLs without visiting them."""

    urls = URL_PATTERN.findall(text)

    # Remove trailing punctuation commonly attached to prose.
    cleaned = []

    for url in urls:
        url = url.rstrip(".,!?;:)]}'\"")
        cleaned.append(url)

    return list(dict.fromkeys(cleaned))


def analyze_url(url: str) -> dict:
    """
    Analyze URL characteristics without making network requests.

    Important:
    This is heuristic analysis. A LOW score does not guarantee safety.
    """

    parsed = urlparse(url)

    hostname = (parsed.hostname or "").lower()
    path = (parsed.path or "").lower()
    query = (parsed.query or "").lower()

    reasons: list[str] = []
    score = 0

    # ---------------------------------------------------------
    # 1. HTTPS
    # ---------------------------------------------------------
    if parsed.scheme.lower() != "https":
        score += 20
        reasons.append("The URL does not use HTTPS.")

    # ---------------------------------------------------------
    # 2. Raw IP address
    # ---------------------------------------------------------
    if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", hostname):
        score += 30
        reasons.append(
            "The URL uses an IP address instead of a domain name."
        )

    # ---------------------------------------------------------
    # 3. URL shortener
    # ---------------------------------------------------------
    if hostname in URL_SHORTENERS:
        score += 25
        reasons.append(
            "The URL uses a URL-shortening service."
        )

    # ---------------------------------------------------------
    # 4. @ symbol
    # ---------------------------------------------------------
    if "@" in url:
        score += 20
        reasons.append(
            "The URL contains an '@' character."
        )

    # ---------------------------------------------------------
    # 5. Punycode
    # ---------------------------------------------------------
    if "xn--" in hostname:
        score += 25
        reasons.append(
            "The domain uses punycode, which can be used for lookalike domains."
        )

    # ---------------------------------------------------------
    # 6. Too many subdomains
    # ---------------------------------------------------------
    if hostname.count(".") >= 3:
        score += 10
        reasons.append(
            "The domain contains many subdomains."
        )

    # ---------------------------------------------------------
    # 7. Suspicious TLD
    # ---------------------------------------------------------
    tld = hostname.rsplit(".", 1)[-1] if "." in hostname else ""

    if tld in SUSPICIOUS_TLDS:
        score += 10
        reasons.append(
            f"The domain uses the '{tld}' top-level domain, which is treated as a risk signal."
        )

    # ---------------------------------------------------------
    # 8. Login / verification / payment path
    # ---------------------------------------------------------
    full_target = f"{path}?{query}"

    matched_path_terms = sorted(
        term
        for term in SUSPICIOUS_PATH_TERMS
        if term in full_target
    )

    if matched_path_terms:
        score += min(20, len(matched_path_terms) * 5)

        reasons.append(
            "The URL contains sensitive-action terms: "
            + ", ".join(matched_path_terms)
            + "."
        )

    # ---------------------------------------------------------
    # 9. Brand keywords in hostname
    # ---------------------------------------------------------
    matched_brands = sorted(
        brand
        for brand in BRAND_KEYWORDS
        if brand in hostname
    )

    if matched_brands:
        score += min(25, len(matched_brands) * 10)

        reasons.append(
            "The hostname contains brand-related terms: "
            + ", ".join(matched_brands)
            + "."
        )

    # ---------------------------------------------------------
    # 10. Suspicious brand-like hostname patterns
    # ---------------------------------------------------------
    brand_like_pattern = (
        r"(secure|login|verify|update|support|account|"
        r"security|service|billing|help|official|confirm)"
    )

    brand_like_matches = re.findall(
        brand_like_pattern,
        hostname,
        re.IGNORECASE,
    )

    if brand_like_matches:
        score += min(
            15,
            len(set(brand_like_matches)) * 5,
        )

        reasons.append(
            "The hostname contains security/account-related branding terms."
        )

    # ---------------------------------------------------------
    # 11. Hyphen-heavy domain
    # ---------------------------------------------------------
    if hostname.count("-") >= 2:
        score += 10
        reasons.append(
            "The hostname contains multiple hyphens."
        )

    # ---------------------------------------------------------
    # 12. Very long URL
    # ---------------------------------------------------------
    if len(url) > 120:
        score += 10
        reasons.append(
            "The URL is unusually long."
        )

    # ---------------------------------------------------------
    # 13. Suspicious path depth
    # ---------------------------------------------------------
    path_parts = [
        part for part in path.split("/")
        if part
    ]

    if len(path_parts) >= 4:
        score += 5
        reasons.append(
            "The URL contains an unusually deep path."
        )
    # ---------------------------------------------------------
    # 14. Brand impersonation
    # ---------------------------------------------------------
    brand_result = detect_brand_impersonation(url)

    if brand_result:
        score = max(score, brand_result["risk_score"])
        reasons.append(brand_result["reason"])
    # ---------------------------------------------------------
    # Final score
    # ---------------------------------------------------------
    score = min(score, 100)

    if score >= 75:
        risk_level = "HIGH"
    elif score >= 45:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "url": url,
        "hostname": hostname,
        "risk_score": score,
        "risk_level": risk_level,
        "reasons": reasons,
    }