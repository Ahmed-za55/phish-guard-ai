import pytest

from app.privacy_gateway import vault


def test_roundtrip():
    key = vault.new_key()
    nonce, ct, kid = vault.seal(key, {"[[EMAIL_1_abcd]]": "a@b.co"}, "req")
    assert vault.open_vault(key, nonce, ct, "req", kid) == {"[[EMAIL_1_abcd]]": "a@b.co"}


def test_plaintext_is_not_in_the_ciphertext():
    key = vault.new_key()
    _, ct, _ = vault.seal(key, {"t": "very-secret-value"}, "req")
    assert b"very-secret-value" not in ct


def test_wrong_key_fails():
    nonce, ct, kid = vault.seal(vault.new_key(), {"t": "v"}, "req")
    with pytest.raises(vault.VaultError):
        vault.open_vault(vault.new_key(), nonce, ct, "req", kid)


def test_tampered_ciphertext_fails():
    key = vault.new_key()
    nonce, ct, kid = vault.seal(key, {"t": "v"}, "req")
    with pytest.raises(vault.VaultError):
        vault.open_vault(key, nonce, bytes([ct[0] ^ 1]) + ct[1:], "req", kid)


def test_vault_is_bound_to_its_request():
    key = vault.new_key()
    nonce, ct, kid = vault.seal(key, {"t": "v"}, "req-1")
    with pytest.raises(vault.VaultError):
        vault.open_vault(key, nonce, ct, "req-2", kid)


def test_nonces_are_unique_across_seals():
    key = vault.new_key()
    nonces = {vault.seal(key, {"t": "v"}, "req")[0] for _ in range(200)}
    assert len(nonces) == 200
