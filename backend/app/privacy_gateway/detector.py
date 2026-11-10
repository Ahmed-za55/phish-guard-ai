"""Find sensitive values in text and replace them with opaque, request-scoped tokens.

Honest scope: this is pattern matching (URLs, emails, phone numbers, card numbers with a Luhn check,
IBANs with a mod-97 check, national IDs, SSNs, API keys / passwords / JWTs, one-time codes) plus
words the user marks as protected (for example their own name). It cannot find every secret:
anything it does not recognise stays in the text that is sent to the provider.
"""
from __future__ import annotations

import re
import secrets
import string
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple


@dataclass(frozen=True)
class Span:
    start: int
    end: int
    kind: str


# priority: lower number wins when two matches overlap
_PRIORITY = {
    "URL": -1, "SECRET": 0, "PROTECTED": 1, "CARD": 2, "IBAN": 3, "NATIONAL_ID": 4,
    "SSN": 5, "EMAIL": 6, "CODE": 7, "PHONE": 8,
}

_EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
# Consume the complete URL, including userinfo, host, port, path, query, and fragment.
# Deliberately include trailing URL punctuation rather than risk leaving a sensitive suffix.
_URL = re.compile(r"https?://[^\s<>]+", re.IGNORECASE)
_CARD = re.compile(r"(?<![\d])(?:\d[ \-]?){12,18}\d(?![\d])")
_IBAN = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")
_NATIONAL_ID = re.compile(r"(?<!\d)[23]\d{13}(?!\d)")
_SSN = re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)")
_PHONE_INTL = re.compile(r"(?<![\w.\-])(?:\+|00|0)\d[\d ()\-.]{6,16}\d(?![\w])")
_PHONE_US = re.compile(r"(?<![\w\-])\(?\d{3}\)?[ \-.]\d{3}[\-.]\d{4}(?![\w\-])")
_CODE = re.compile(r"(?i)\b(?:code|otp|pin|passcode|verification)\b[^\d\n]{0,20}(\d{4,8})(?!\d)")
_SECRET_LITERALS = [
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\b"),
]
_SECRET_ASSIGN = re.compile(r"(?i)\b(?:password|passwd|pwd|secret|api[_\-]?key|token)\b\s*[:=]\s*(\S{4,})")


def _luhn_ok(digits: str) -> bool:
    total, flip = 0, False
    for ch in reversed(digits):
        d = int(ch)
        if flip:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        flip = not flip
    return total % 10 == 0


def _iban_ok(candidate: str) -> bool:
    rearranged = candidate[4:] + candidate[:4]
    numeric = "".join(str(int(ch, 36)) for ch in rearranged)
    return int(numeric) % 97 == 1


def _digits(s: str) -> str:
    return "".join(ch for ch in s if ch.isdigit())


def _find(text: str, protected_terms: Sequence[str]) -> List[Span]:
    spans: List[Span] = []

    # URLs must be considered as whole spans so email/phone/credential matches inside them
    # cannot leave URL components in the provider-bound text.
    spans += [Span(m.start(), m.end(), "URL") for m in _URL.finditer(text)]

    for pattern in _SECRET_LITERALS:
        spans += [Span(m.start(), m.end(), "SECRET") for m in pattern.finditer(text)]
    for m in _SECRET_ASSIGN.finditer(text):
        value = m.group(1).rstrip(".,;:!?)\"'")  # trailing punctuation belongs to the sentence, not the secret
        if len(value) >= 4:
            spans.append(Span(m.start(1), m.start(1) + len(value), "SECRET"))

    for term in protected_terms:
        term = term.strip()
        if len(term) < 3:
            continue
        spans += [Span(m.start(), m.end(), "PROTECTED")
                  for m in re.finditer(re.escape(term), text, flags=re.IGNORECASE)]

    for m in _CARD.finditer(text):
        d = _digits(m.group())
        if 13 <= len(d) <= 19 and _luhn_ok(d):
            spans.append(Span(m.start(), m.end(), "CARD"))
    for m in _IBAN.finditer(text):
        if _iban_ok(m.group()):
            spans.append(Span(m.start(), m.end(), "IBAN"))
    spans += [Span(m.start(), m.end(), "NATIONAL_ID") for m in _NATIONAL_ID.finditer(text)]
    spans += [Span(m.start(), m.end(), "SSN") for m in _SSN.finditer(text)]
    spans += [Span(m.start(), m.end(), "EMAIL") for m in _EMAIL.finditer(text)]
    spans += [Span(m.start(1), m.end(1), "CODE") for m in _CODE.finditer(text)]
    for m in _PHONE_INTL.finditer(text):
        if 9 <= len(_digits(m.group())) <= 15:
            spans.append(Span(m.start(), m.end(), "PHONE"))
    spans += [Span(m.start(), m.end(), "PHONE") for m in _PHONE_US.finditer(text)]
    return spans


def detect(text: str, protected_terms: Iterable[str] = ()) -> List[Span]:
    """Non-overlapping spans, sorted by position. Overlaps: the longest span wins, then priority.
    (Longest first matters: it tokenizes a whole email instead of only the card-like digits inside it.)"""
    candidates = sorted(
        _find(text, list(protected_terms)),
        key=lambda s: (-(s.end - s.start), _PRIORITY[s.kind], s.start),
    )
    chosen: List[Span] = []
    for span in candidates:
        if all(span.end <= c.start or span.start >= c.end for c in chosen):
            chosen.append(span)
    return sorted(chosen, key=lambda s: s.start)


def _suffix() -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(4))


def tokenize(text: str, spans: Sequence[Span]) -> Tuple[str, Dict[str, str], List[dict]]:
    """Return (sanitized_text, token -> original value, occurrence records for the UI).

    One regex pass replaces EVERY occurrence of every detected value, longest value first. Doing it in a
    single pass over the original text means a value can never be replaced inside a token we just wrote.
    """
    suffix = _suffix()  # makes tokens unpredictable and avoids clashing with text the sender wrote
    value_kind: Dict[str, str] = {}
    for span in sorted(spans, key=lambda s: s.start):
        value_kind.setdefault(text[span.start:span.end], span.kind)
    if not value_kind:
        return text, {}, []

    counters: Dict[str, int] = {}
    value_to_token: Dict[str, str] = {}
    for value, kind in value_kind.items():
        counters[kind] = counters.get(kind, 0) + 1
        value_to_token[value] = f"[[{kind}_{counters[kind]}_{suffix}]]"

    pattern = re.compile("|".join(re.escape(v) for v in sorted(value_kind, key=len, reverse=True)))
    out: List[str] = []
    records: List[dict] = []
    cursor = 0
    for m in pattern.finditer(text):
        token = value_to_token[m.group(0)]
        out.append(text[cursor:m.start()])
        out.append(token)
        records.append({"start": m.start(), "end": m.end(), "type": value_kind[m.group(0)], "token": token})
        cursor = m.end()
    out.append(text[cursor:])
    return "".join(out), {t: v for v, t in value_to_token.items()}, records
