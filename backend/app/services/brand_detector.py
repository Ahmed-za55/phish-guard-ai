import re
from urllib.parse import urlparse


OFFICIAL_DOMAINS = {
    "paypal": ["paypal.com"],
    "microsoft": ["microsoft.com", "live.com", "office.com"],
    "apple": ["apple.com", "icloud.com"],
    "google": ["google.com", "gmail.com"],
    "amazon": ["amazon.com", "aws.amazon.com"],
    "facebook": ["facebook.com", "fb.com"],
    "instagram": ["instagram.com"],
    "whatsapp": ["whatsapp.com"],
    "netflix": ["netflix.com"],
    "visa": ["visa.com"],
    "mastercard": ["mastercard.com"],
}

HOMOGLYPH_MAP = str.maketrans({
    "0": "o",
    "1": "l",
    "3": "e",
    "4": "a",
    "5": "s",
    "7": "t",
    "8": "b",
    "@": "a",
    "$": "s",
})


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate mathematical Levenshtein edit distance d_L(s1, s2)."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def normalized_similarity(s1: str, s2: str) -> float:
    """Compute S(s1, s2) = 1 - d_L(s1, s2) / max(|s1|, |s2|)."""
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    dist = levenshtein_distance(s1, s2)
    return round(1.0 - (dist / max_len), 4)


def _extract_domain_tokens(hostname: str) -> list[str]:
    """Split hostname into testable lexical tokens (excluding TLD)."""
    parts = hostname.split(".")
    core_parts = parts[:-1] if len(parts) > 1 else parts
    tokens: list[str] = []
    for part in core_parts:
        tokens.extend(t for t in re.split(r"[-_]", part) if len(t) >= 4)
    return tokens


def detect_brand_impersonation(url: str) -> dict | None:
    """
    Detect possible brand impersonation from the hostname using
    exact matching, homoglyph normalization, and Levenshtein metrics.
    """
    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower()
    if not hostname:
        return None

    for official_domains in OFFICIAL_DOMAINS.values():
        if any(
            hostname == domain or hostname.endswith("." + domain)
            for domain in official_domains
        ):
            return None

    for brand in OFFICIAL_DOMAINS:
        if brand in hostname:
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

    tokens = _extract_domain_tokens(hostname)
    for token in tokens:
        deobfuscated = token.translate(HOMOGLYPH_MAP)
        for brand in OFFICIAL_DOMAINS:
            dist_raw = levenshtein_distance(token, brand)
            dist_norm = levenshtein_distance(deobfuscated, brand)
            sim = max(
                normalized_similarity(token, brand),
                normalized_similarity(deobfuscated, brand),
            )

            if (0 < dist_raw <= 2 or dist_norm <= 1) and sim >= 0.72:
                return {
                    "brand": brand,
                    "is_impersonation": True,
                    "risk_level": "HIGH",
                    "risk_score": 85,
                    "reason": (
                        f"Mathematical Typosquatting Detection: Token '{token}' "
                        f"exhibits {int(sim * 100)}% Levenshtein similarity "
                        f"(edit distance d_L = {min(dist_raw, max(1, dist_norm))}) "
                        f"to protected brand '{brand}'."
                    ),
                }

    return None