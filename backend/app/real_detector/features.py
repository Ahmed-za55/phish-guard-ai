"""Feature extraction.

DESIGN DECISION: the model scores the REGISTERED DOMAIN only (e.g. "evil-login.xyz" for
"a.b.evil-login.xyz/path"). Why: the legitimate training domains have almost no subdomains
(0.1%) while phishing hosts do (68%), so a model that sees subdomains just learns
"has a subdomain => phishing" and flags en.wikipedia.org. Path/query are ignored for the same reason.
Subdomain/brand hints are still shown to the user as explanations, but never change the score.
"""
from __future__ import annotations

import ipaddress
import math
import re
from collections import Counter
from typing import Dict, List, Tuple
from urllib.parse import urlsplit

import pandas as pd

# second-level labels that, together with a 2-letter TLD, form a "public suffix" (co.uk, com.eg ...)
_SECOND_LEVEL = {"co", "com", "org", "net", "gov", "edu", "ac", "or", "ne", "go", "gob"}

SUSPICIOUS_KEYWORDS = (
    "login", "signin", "verify", "secure", "account", "update", "confirm", "support",
    "wallet", "bank", "billing", "invoice", "password", "recover", "unlock", "suspend",
    "alert", "auth", "webmail", "service", "helpdesk",
)
BRANDS = (
    "paypal", "microsoft", "office365", "outlook", "google", "apple", "icloud", "amazon",
    "netflix", "facebook", "instagram", "whatsapp", "binance", "coinbase", "metamask",
    "dhl", "fedex", "usps", "chase", "wellsfargo", "bankofamerica", "hsbc", "linkedin",
    "dropbox", "adobe", "docusign", "steam", "telegram", "ebay", "walmart",
)

# features the MODEL uses (all computed on the registered domain)
NUMERIC_COLUMNS: List[str] = [
    "length", "n_labels", "n_hyphens", "n_digits", "digit_ratio", "entropy",
    "longest_label", "is_ip", "has_punycode",
    "kw_count", "brand_variant_in_reg", "max_digit_run", "max_consonant_run",
]

# free / shared hosting platforms: the platform's domain says nothing about one specific site on it
SHARED_HOSTING = {
    "github.io", "netlify.app", "vercel.app", "pages.dev", "webflow.io", "weeblysite.com",
    "weebly.com", "000webhostapp.com", "appspot.com", "duckdns.org", "blogspot.com",
    "wixsite.com", "herokuapp.com", "glitch.me", "web.app", "firebaseapp.com", "workers.dev",
    "repl.co", "godaddysites.com", "myshopify.com",
}
CAT_COLUMNS: List[str] = ["tld"]
FEATURE_COLUMNS: List[str] = ["host"] + NUMERIC_COLUMNS + CAT_COLUMNS

_BAD_SCHEMES = re.compile(r"^(javascript|data|vbscript|file|mailto|blob):", re.I)
_HOST_RE = re.compile(r"^[a-z0-9_-]+(\.[a-z0-9_-]+)*$")


def normalize_host(host: str) -> str:
    h = host.strip().lower().rstrip(".")
    if not h:
        raise ValueError("empty host")
    try:
        h.encode("ascii")
    except UnicodeEncodeError:
        try:
            h = h.encode("idna").decode("ascii")
        except UnicodeError as exc:
            raise ValueError("invalid internationalized host") from exc
    if not _HOST_RE.match(h):
        raise ValueError("invalid host")
    return h


def extract_host(url: str) -> str:
    """URL (with or without scheme) -> normalized hostname. Raises ValueError if unusable."""
    s = (url or "").strip()
    if not s:
        raise ValueError("empty url")
    if _BAD_SCHEMES.match(s):
        raise ValueError("unsupported scheme")
    if "://" not in s:
        s = "http://" + s
    parts = urlsplit(s)
    if parts.scheme.lower() not in {"http", "https", "ftp"}:
        raise ValueError("unsupported scheme")
    if not parts.hostname:
        raise ValueError("no host in url")
    return normalize_host(parts.hostname)


def _is_ip(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def split_host(host: str) -> Tuple[str, str, str]:
    """Return (subdomain, registered_domain, tld). Simple heuristic, no public-suffix list."""
    if _is_ip(host):
        return "", host, "ip"
    labels = host.split(".")
    if len(labels) == 1:
        return "", host, "none"
    tld = labels[-1]
    take = 3 if (len(labels) >= 3 and labels[-2] in _SECOND_LEVEL and len(tld) == 2) else 2
    take = min(take, len(labels))
    reg = ".".join(labels[-take:])
    sub = ".".join(labels[:-take])
    return sub, reg, tld


def registered_domain(host: str) -> str:
    return split_host(host)[1]


def _entropy(s: str) -> float:
    if not s:
        return 0.0
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in Counter(s).values())


def _longest_run(pattern: str, s: str) -> int:
    runs = re.findall(pattern, s)
    return max((len(r) for r in runs), default=0)


def host_features(host: str) -> Dict[str, float]:
    sub, reg, tld = split_host(host)
    labels = host.split(".")
    reg_label = reg.split(".")[0] if reg else ""
    n_digits = sum(ch.isdigit() for ch in host)
    return {
        "host": host,
        "length": len(host),
        "n_labels": len(labels),
        "n_hyphens": host.count("-"),
        "n_digits": n_digits,
        "digit_ratio": n_digits / len(host),
        "entropy": _entropy(host),
        "longest_label": max(len(label) for label in labels),
        "sub_depth": len(sub.split(".")) if sub else 0,
        "reg_len": len(reg),
        "sub_len": len(sub),
        "is_ip": int(_is_ip(host)),
        "has_punycode": int("xn--" in host),
        "kw_count": sum(k in host for k in SUSPICIOUS_KEYWORDS),
        "brand_in_sub": int(any(b in sub for b in BRANDS)),
        "brand_variant_in_reg": int(any(b in reg_label and reg_label != b for b in BRANDS)),
        "max_digit_run": _longest_run(r"\d+", host),
        "max_consonant_run": _longest_run(r"[bcdfghjklmnpqrstvwxz]+", host),
        "tld": tld,
    }


def features_frame(hosts: List[str]) -> pd.DataFrame:
    return pd.DataFrame([host_features(h) for h in hosts], columns=FEATURE_COLUMNS)


def indicators(feats: Dict[str, float]) -> List[str]:
    """Human-readable hints on the FULL host. They EXPLAIN the input; the score comes only from the model."""
    out: List[str] = []
    if registered_domain(str(feats["host"])) in SHARED_HOSTING:
        out.append("Hosted on a free/shared platform: the score cannot judge this specific site")
    if feats["is_ip"]:
        out.append("Host is a raw IP address")
    if feats["has_punycode"]:
        out.append("Internationalized (punycode) host - possible look-alike characters")
    if feats["brand_in_sub"]:
        out.append("Brand name appears in the subdomain, not the registered domain")
    elif feats["brand_variant_in_reg"]:
        out.append("Registered domain contains a brand name plus extra text")
    if feats["kw_count"]:
        out.append(f"{int(feats['kw_count'])} sensitive keyword(s) in host (login, verify, secure...)")
    if feats["n_hyphens"] >= 3:
        out.append(f"{int(feats['n_hyphens'])} hyphens in host")
    if feats["max_digit_run"] >= 5:
        out.append("Long run of digits in host")
    if feats["sub_depth"] >= 3:
        out.append("Deeply nested subdomains")
    if feats["entropy"] >= 3.8 and feats["length"] >= 16:
        out.append("Random-looking host (high character entropy)")
    return out
