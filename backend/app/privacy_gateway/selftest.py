"""Runs the security properties on synthetic data, with an offline spy provider (no API call).
Used by GET /api/v1/private/selftest so the demo can show the checks passing live."""
from __future__ import annotations

import itertools
from typing import Any, Callable, Dict, List

from . import service, vault
from .provider import MockProvider, ProviderPayload
from .shamir import ShareError, combine, decode_share, split
from .validation import validate

SENTINEL_TEXT = (
    "Hi Mariam Hassan, your account is locked. Verify within 24 hours at http://secure-login-48213.xyz/verify "
    "Contact mariam.hassan@example.org or +20 100 123 4567. Card 4111 1111 1111 1111, "
    "password: Tr0ub4dor&3xx, code 482913."
)
SENTINELS = ["Mariam Hassan", "mariam.hassan@example.org", "+20 100 123 4567",
             "4111 1111 1111 1111", "Tr0ub4dor&3xx", "482913"]


def _check(name: str, fn: Callable[[], str]) -> Dict[str, Any]:
    try:
        return {"name": name, "passed": True, "detail": fn()}
    except AssertionError as exc:
        return {"name": name, "passed": False, "detail": str(exc) or "assertion failed"}
    except Exception as exc:  # noqa: BLE001
        return {"name": name, "passed": False, "detail": f"{type(exc).__name__}: {exc}"}


def run() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    extra_ids: List[str] = []
    spy = MockProvider()
    result = service.analyze(SENTINEL_TEXT, spy, protected_terms=["Mariam Hassan"])
    shares = [s["share"] for s in result["custody"]["shares"]]
    rid = result["request_id"]
    sent = spy.received[0].as_text()

    def no_sentinels() -> str:
        leaked = [s for s in SENTINELS if s in sent]
        assert not leaked, f"{len(leaked)} sensitive value(s) reached the provider"
        return f"{len(SENTINELS)} sensitive values, 0 found in the {len(sent)}-byte payload"

    def no_keys() -> str:
        assert not any(s in sent for s in shares), "a share reached the provider"
        assert not any(f"{decode_share(s).y:x}" in sent for s in shares), "share value reached the provider"
        return "no key shares or key material in the payload"

    def roundtrip() -> str:
        restored = service.restore(rid, shares[:2])
        assert restored["values_restored"] >= len(SENTINELS) - 1
        return f"{restored['values_restored']} values restored with two shares"

    def one_share_fails() -> str:
        for s in shares:
            try:
                service.restore(rid, [s])
            except service.RestoreDenied:
                continue
            raise AssertionError("one share opened the vault")
        return "each single share was refused"

    def any_two() -> str:
        for pair in itertools.combinations(shares, 2):
            service.restore(rid, list(pair))
        return "A+B, A+C and B+C all open the vault"

    def tamper() -> str:
        key = vault.new_key()
        nonce, ct, kid = vault.seal(key, {"[[X_1_abcd]]": "secret"}, "req1")
        flipped = bytes([ct[0] ^ 1]) + ct[1:]
        try:
            vault.open_vault(key, nonce, flipped, "req1", kid)
        except vault.VaultError:
            try:
                vault.open_vault(key, nonce, ct, "other-request", kid)
            except vault.VaultError:
                return "a flipped bit and a moved vault are both rejected"
        raise AssertionError("tampered vault was accepted")

    def mixed() -> str:
        other = split(vault.new_key(), 2, 3)
        try:
            combine([decode_share(shares[0]), other[1]], 2)
        except ShareError:
            return "shares from two different keys are rejected"
        raise AssertionError("mixed shares were accepted")

    def untrusted_output() -> str:
        raw = ('{"verdict":"PHISHING","risk_score":90,"reasons":["Sent by guess@leak.example and [[EMAIL_9_zzzz]]"],'
               '"recommendations":[]}')
        v = validate(raw, set())
        text = v.reasons[0]
        assert "guess@leak.example" not in text and "[[EMAIL_9_zzzz]]" not in text
        return f"{len(v.violations)} violations flagged; invented token and email were removed"

    def fail_closed() -> str:
        try:
            service.assert_clean(ProviderPayload(system="s", sanitized_text="mail me at a@b.co"), ["a@b.co"])
        except service.GatewayBlocked:
            return "a payload containing an original value is blocked before any provider call"
        raise AssertionError("leaky payload was not blocked")

    def degraded() -> str:
        down = MockProvider(fail=True)
        r = service.analyze("Click http://secure-login-48213.xyz/verify now", down)
        extra_ids.append(r["request_id"])
        assert r["provider"]["status"] == "unavailable"
        assert r["analysis"] is None and r["overall"]["source"] == "local detector"
        return "provider down: local detector still returns a result, status is reported"

    for name, fn in [
        ("Sensitive values never reach the provider", no_sentinels),
        ("No key shares or key material reach the provider", no_keys),
        ("Two shares restore the original values", roundtrip),
        ("One share alone is refused", one_share_fails),
        ("Any two of the three shares work", any_two),
        ("Tampered or moved vaults are rejected (AES-GCM tag)", tamper),
        ("Shares from different keys are rejected", mixed),
        ("Provider output is treated as untrusted", untrusted_output),
        ("Gateway fails closed on a leak", fail_closed),
        ("Provider outage leaves local analysis available", degraded),
    ]:
        checks.append(_check(name, fn))

    for request_id in [rid, *extra_ids]:  # remove only the sessions this self-test created
        service.drop_session(request_id)
    passed = sum(1 for c in checks if c["passed"])
    return {"passed": passed, "total": len(checks), "checks": checks}
