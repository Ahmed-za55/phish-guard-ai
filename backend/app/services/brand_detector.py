from urllib.parse import urlparse


OFFICIAL_DOMAINS = {
    "paypal": ["paypal.com"],
    "microsoft": ["microsoft.com"],
    "apple": ["apple.com"],
    "google": ["google.com"],
    "amazon": ["amazon.com"],
    "facebook": ["facebook.com"],
    "instagram": ["instagram.com"],
    "whatsapp": ["whatsapp.com"],
    "netflix": ["netflix.com"],
    "visa": ["visa.com"],
    "mastercard": ["mastercard.com"],
}


def detect_brand_impersonation(url: str) -> dict | None:
    """
    Detect possible brand impersonation from the hostname.

    This is heuristic analysis only. It does not visit the URL.
    """

    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower()

    for brand, official_domains in OFFICIAL_DOMAINS.items():
        # Brand name appears in hostname.
        if brand not in hostname:
            continue

        # Exact official domain or a legitimate subdomain.
        is_official = any(
            hostname == domain or hostname.endswith("." + domain)
            for domain in official_domains
        )

        if is_official:
            return None

        return {
            "brand": brand,
            "is_impersonation": True,
            "risk_level": "HIGH",
            "risk_score": 80,
            "reason": (
                f"The hostname appears to imitate {brand}, "
                f"but it is not an official {brand} domain."
            ),
        }

    return None