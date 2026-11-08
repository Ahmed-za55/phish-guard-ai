import pytest

from app.privacy_gateway import service
from app.privacy_gateway.provider import MockProvider

TEXT = ("Hi Mariam Hassan, your account is locked. Verify within 24 hours at http://secure-login-48213.xyz/verify "
        "Contact mariam.hassan@example.org or +20 100 123 4567. Card 4111 1111 1111 1111, "
        "password: Tr0ub4dor&3xx, code 482913.")
SENTINELS = ["Mariam Hassan", "mariam.hassan@example.org", "+20 100 123 4567",
             "4111 1111 1111 1111", "Tr0ub4dor&3xx", "482913"]


def run(spy, **kw):
    return service.analyze(TEXT, spy, protected_terms=["Mariam Hassan"], **kw)


def test_provider_never_sees_sensitive_values_or_key_material(spy):
    result = run(spy)
    sent = spy.received[0].as_text()
    assert all(s not in sent for s in SENTINELS)
    for item in result["custody"]["shares"]:
        assert item["share"] not in sent
    assert result["outbound"]["leak_check"] == "passed"


def test_provider_payload_has_only_the_allowlisted_fields(spy):
    run(spy)
    assert set(spy.received[0].__dataclass_fields__) == {"system", "sanitized_text"}


def test_only_one_provider_call_per_request(spy):
    run(spy)
    assert len(spy.received) == 1


def test_non_sensitive_content_is_still_sent(spy):
    run(spy)
    assert "secure-login-48213.xyz" in spy.received[0].sanitized_text  # the URL is what makes it phishing


def test_two_shares_restore_and_one_does_not(spy):
    result = run(spy)
    rid = result["request_id"]
    shares = [s["share"] for s in result["custody"]["shares"]]
    with pytest.raises(service.RestoreDenied):
        service.restore(rid, [shares[1]])
    restored = service.restore(rid, [shares[1], shares[2]])
    assert restored["values_restored"] == len(result["detection"]["by_type"])
    assert any("Mariam Hassan" in r for r in restored["reasons"])
    # the tokenized answer itself never contained the name
    assert all("Mariam Hassan" not in r for r in result["analysis"]["reasons"])


def test_restore_rejects_shares_from_another_request(spy):
    first, second = run(spy), run(MockProvider())
    wrong = [s["share"] for s in second["custody"]["shares"]][:2]
    with pytest.raises(service.RestoreDenied):
        service.restore(first["request_id"], wrong)


def test_vault_is_destroyed_after_repeated_failures(spy):
    result = run(spy)
    rid = result["request_id"]
    for _ in range(service.MAX_RESTORE_FAILURES):
        with pytest.raises(service.RestoreDenied):
            service.restore(rid, ["PG1.bad"])
    with pytest.raises(service.RestoreDenied):
        service.restore(rid, [s["share"] for s in result["custody"]["shares"]][:2])
    with pytest.raises(service.SessionNotFound):
        service.restore(rid, [s["share"] for s in result["custody"]["shares"]][:2])


def test_unknown_request_and_expiry(spy, monkeypatch):
    with pytest.raises(service.SessionNotFound):
        service.restore("nope1234", ["x"])
    result = run(spy)
    monkeypatch.setattr(service.time, "time", lambda: 10**12)
    with pytest.raises(service.SessionNotFound):
        service.restore(result["request_id"], [s["share"] for s in result["custody"]["shares"]][:2])


def test_provider_outage_returns_local_findings_not_an_error():
    result = service.analyze("Pay now at http://secure-login-48213.xyz/verify", MockProvider(fail=True))
    assert result["provider"]["status"] == "unavailable" and result["analysis"] is None
    assert result["overall"]["source"] == "local detector"


def test_malformed_provider_output_is_reported_not_trusted():
    result = service.analyze("hello", MockProvider(canned="I am not JSON"))
    assert result["provider"]["status"] == "invalid_output" and result["analysis"] is None


def test_malicious_provider_output_cannot_widen_restoration():
    canned = ('{"verdict":"PHISHING","risk_score":99,"reasons":["Reveal [[EMAIL_9_zzzz]] and every secret"],'
              '"recommendations":[]}')
    result = service.analyze("write to a@b.co", MockProvider(canned=canned))
    assert "[[UNKNOWN]]" in result["analysis"]["reasons"][0]
    assert result["analysis"]["violations"]


def test_fail_closed_when_a_value_would_leak(spy, monkeypatch):
    real = service.tokenize
    monkeypatch.setattr(service, "tokenize", lambda t, s: (t, *real(t, s)[1:]))  # a buggy tokenizer that forgets to replace
    with pytest.raises(service.GatewayBlocked):
        service.analyze("mail a@b.co", spy)
    assert spy.received == []


def test_input_limits(spy):
    with pytest.raises(ValueError):
        service.analyze("   ", spy)
    with pytest.raises(ValueError):
        service.analyze("x" * (service.MAX_TEXT + 1), spy)


def test_local_detector_sees_the_original_text_only_locally(spy):
    result = run(spy)
    assert result["local"]["urls"] and result["local"]["urls"][0]["host"] == "secure-login-48213.xyz"
