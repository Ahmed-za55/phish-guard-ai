"""Provider output is untrusted: parse strictly, bound sizes, allow only issued tokens."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set

from .detector import detect

_TOKEN = re.compile(r"\[\[[A-Za-z_]+_\d+_[a-z0-9]{4}\]\]")
_ANY_BRACKET_TOKEN = re.compile(r"\[\[[^\[\]\n]{1,60}\]\]")
VERDICTS = {"PHISHING", "SUSPICIOUS", "LIKELY_SAFE"}
MAX_REASONS, MAX_RECS, MAX_LEN = 6, 4, 400


class ProviderOutputError(ValueError):
    """The provider answer does not match the expected schema."""


@dataclass
class ValidatedAnalysis:
    verdict: str
    risk_score: int
    reasons: List[str]
    recommendations: List[str]
    violations: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return {"verdict": self.verdict, "risk_score": self.risk_score, "reasons": self.reasons,
                "recommendations": self.recommendations, "violations": self.violations}


def _extract_json(raw: str) -> Any:
    text = (raw or "").strip()
    if len(text) > 20_000:
        raise ProviderOutputError("Provider answer is too long.")
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            raise ProviderOutputError("Provider answer is not JSON.") from None
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            raise ProviderOutputError("Provider answer is not valid JSON.") from None


def _clean_text(value: Any, issued: Set[str], violations: List[str]) -> str:
    if not isinstance(value, str):
        raise ProviderOutputError("Expected a string in the provider answer.")
    text = value.strip()[:MAX_LEN]

    def fix_token(match: "re.Match[str]") -> str:
        token = match.group(0)
        if token in issued:
            return token
        violations.append(f"unknown token removed: {token[:24]}")
        return "[[UNKNOWN]]"

    text = _ANY_BRACKET_TOKEN.sub(fix_token, text)

    # The provider must not emit sensitive-looking values of its own (for example a guessed email).
    spans = [s for s in detect(text) if "[[" not in text[max(0, s.start - 2):s.start + 2]]
    for span in reversed(spans):
        violations.append(f"sensitive-looking value from provider redacted ({span.kind.lower()})")
        text = text[:span.start] + "[[REDACTED]]" + text[span.end:]
    return text


def validate(raw: str, issued_tokens: Set[str]) -> ValidatedAnalysis:
    data = _extract_json(raw)
    if not isinstance(data, dict):
        raise ProviderOutputError("Provider answer must be a JSON object.")

    verdict = data.get("verdict")
    if verdict not in VERDICTS:
        raise ProviderOutputError("Unknown verdict.")
    score = data.get("risk_score")
    if isinstance(score, bool) or not isinstance(score, (int, float)) or not (0 <= score <= 100):
        raise ProviderOutputError("risk_score must be a number from 0 to 100.")

    reasons_raw, recs_raw = data.get("reasons", []), data.get("recommendations", [])
    if not isinstance(reasons_raw, list) or not isinstance(recs_raw, list):
        raise ProviderOutputError("reasons and recommendations must be lists.")

    violations: List[str] = []
    if len(reasons_raw) > MAX_REASONS or len(recs_raw) > MAX_RECS:
        violations.append("answer had more items than allowed; extra items dropped")
    reasons = [_clean_text(r, issued_tokens, violations) for r in reasons_raw[:MAX_REASONS]]
    recs = [_clean_text(r, issued_tokens, violations) for r in recs_raw[:MAX_RECS]]
    return ValidatedAnalysis(verdict=verdict, risk_score=int(round(score)), reasons=reasons,
                             recommendations=recs, violations=violations)
