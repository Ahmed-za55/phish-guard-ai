import pytest

from app.privacy_gateway import service
from app.privacy_gateway.provider import MockProvider

TEXT = ("Hi Mariam Hassan, your account is locked. Verify within 24 hours at http://secure-login-48213.xyz/verify "
        "Contact mariam.hassan@example.org or +20 100 123 4567. Card 4111 1111 1111 1111, "
        "password: Tr0ub4dor&3xx, code 482913.")
SENTINELS = ["Mariam Hassan", "mariam.hassan@example.org", "+20 100 123 4567",
             "4111 1111 1111 1111", "Tr0ub4dor&3xx", "482913"]
URL = "https://user:route-secret@secure-login-48213.xyz:8443/verify/path?email=mariam.hassan%40example.org&phone=%2B201001234567#fragment-sentinel"


def run(spy, **kw):
    return service.analyze(TEXT, spy, protected_terms=["Mariam Hassan"], **kw)


def test_provider_never_sees_sensitive_values_or_key_material(spy):
    result = run(spy)
    sent = spy.received[0].as_text()
    assert all(s not in sent for s in SENTINELS)
    for item in result["custody"]["shares"]:
        assert item["share"] not in sent
    assert result["outbound"]["leak_check"] == "passed_literal_checks"
    assert "arbitrary unknown text is not covered" in result["outbound"]["leak_check_scope"]


def test_provider_payload_has_only_the_allowlisted_fields(spy):
    run(spy)
    assert set(spy.received[0].__dataclass_fields__) == {"system", "sanitized_text"}


def test_only_one_provider_call_per_request(spy):
    run(spy)
    assert len(spy.received) == 1


def test_full_url_and_all_components_never_reach_provider(spy):
    text = f"Check this link {URL}"
    result = service.analyze(text, spy)
    payload = spy.received[0]
    sent = payload.as_text()
    components = [URL, "https", "secure-login-48213.xyz", "route-secret", "/verify/path",
                  "email=mariam.hassan%40example.org", "mariam.hassan%40example.org",
                  "phone=%2B201001234567", "%2B201001234567", "fragment-sentinel"]
    assert all(value not in sent for value in components)
    assert "[[URL_" in payload.sanitized_text


def test_url_token_restores_only_after_local_share_authorization(spy):
    result = service.analyze(URL, spy)
    assert URL not in spy.received[0].as_text()
    assert URL not in " ".join(result["analysis"]["reasons"])
    shares = [item["share"] for item in result["custody"]["shares"]]
    restored = service.restore(result["request_id"], shares[:2])
    assert any(URL in reason for reason in restored["reasons"])


def test_payload_excludes_standalone_protected_value_classes(spy):
    text = "mail alice.sentinel@example.invalid call +1 202-555-0198 password: CredentialSentinel91"
    service.analyze(text, spy)
    sent = spy.received[0].as_text()
    assert all(value not in sent for value in ["alice.sentinel@example.invalid", "+1 202-555-0198",
                                               "CredentialSentinel91"])


def test_unknown_identifier_is_outside_detector_guarantee(spy):
    unknown = "CaseRef-QZ-9482017"
    service.analyze(f"Review case {unknown}", spy)
    assert unknown in spy.received[0].as_text()


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


def test_fail_closed_when_url_tokenization_fails(spy, monkeypatch):
    real = service.tokenize
    monkeypatch.setattr(service, "tokenize", lambda t, s: (t, *real(t, s)[1:]))
    with pytest.raises(service.GatewayBlocked):
        service.analyze(URL, spy)
    assert spy.received == []


def test_input_limits(spy):
    with pytest.raises(ValueError):
        service.analyze("   ", spy)
    with pytest.raises(ValueError):
        service.analyze("x" * (service.MAX_TEXT + 1), spy)


def test_local_detector_sees_the_original_text_only_locally(spy):
    result = run(spy)
    assert result["local"]["urls"] and result["local"]["urls"][0]["host"] == "secure-login-48213.xyz"


def test_local_analysis_receives_original_url_and_findings_remain_useful(spy, monkeypatch):
    observed = {}
    def local_findings(text):
        observed["text"] = text
        return {"status": "ok", "risk_score": 73, "urls": [{"url": URL,
                "host": "secure-login-48213.xyz", "scored_domain": "48213.xyz",
                "verdict": "PHISHING", "risk_score": 73}]}
    monkeypatch.setattr(service, "_local_findings", local_findings)
    result = service.analyze(f"Check {URL}", spy)
    assert observed["text"] == f"Check {URL}"
    assert result["local"]["urls"][0]["url"] == URL
    assert result["local"]["risk_score"] == 73
    assert URL not in spy.received[0].as_text()
