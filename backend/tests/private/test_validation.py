import json

import pytest

from app.privacy_gateway.validation import ProviderOutputError, validate

OK = {"verdict": "SUSPICIOUS", "risk_score": 55, "reasons": ["r"], "recommendations": ["x"]}


def raw(**changes):
    return json.dumps({**OK, **changes})


def test_valid_answer_passes():
    v = validate(raw(), set())
    assert (v.verdict, v.risk_score, v.violations) == ("SUSPICIOUS", 55, [])


def test_code_fences_are_accepted():
    assert validate("```json\n" + raw() + "\n```", set()).risk_score == 55


@pytest.mark.parametrize("bad", [
    "not json", "[]", raw(verdict="MAYBE"), raw(risk_score=101), raw(risk_score=-1),
    raw(risk_score="high"), raw(risk_score=True), raw(reasons="a string"), raw(reasons=[1]),
    "x" * 30_000,
])
def test_invalid_answers_are_rejected(bad):
    with pytest.raises(ProviderOutputError):
        validate(bad, set())


def test_unknown_tokens_are_removed_and_known_tokens_kept():
    v = validate(raw(reasons=["[[EMAIL_1_abcd]] and [[EMAIL_2_abcd]]"]), {"[[EMAIL_1_abcd]]"})
    assert v.reasons[0] == "[[EMAIL_1_abcd]] and [[UNKNOWN]]"
    assert any("unknown token" in x for x in v.violations)


def test_sensitive_looking_values_from_the_provider_are_redacted():
    v = validate(raw(reasons=["Contact guess@leak.example or +20 100 123 4567"]), set())
    assert "guess@leak.example" not in v.reasons[0] and "123 4567" not in v.reasons[0]
    assert v.violations


def test_lengths_and_counts_are_bounded():
    v = validate(raw(reasons=["a" * 1000] * 12, recommendations=["b"] * 20), set())
    assert len(v.reasons) == 6 and len(v.recommendations) == 4
    assert all(len(r) <= 400 for r in v.reasons) and v.violations
