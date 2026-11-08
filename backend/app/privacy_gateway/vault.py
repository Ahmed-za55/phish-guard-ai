"""Authenticated encryption of the token -> original-value mapping.

AES-256-GCM via the `cryptography` package (OpenSSL's C implementation does the math).
A fresh random 256-bit key is generated for every request, so a random 96-bit nonce is safe.
The associated data binds the ciphertext to its request id and key id, so a vault cannot be
moved to another request, and a wrong or tampered key/ciphertext fails closed.
"""
from __future__ import annotations

import json
import os
from typing import Dict, Tuple

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .shamir import KEY_BYTES, key_id


class VaultError(Exception):
    """The vault could not be opened (wrong key, tampering, or wrong request)."""


def new_key() -> bytes:
    return os.urandom(KEY_BYTES)


def make_aad(request_id: str, kid: str) -> bytes:
    return f"pg-vault|v1|{request_id}|{kid}".encode("ascii")


def seal(key: bytes, mapping: Dict[str, str], request_id: str) -> Tuple[bytes, bytes, str]:
    """Return (nonce, ciphertext, kid)."""
    kid = key_id(key)
    nonce = os.urandom(12)
    plaintext = json.dumps(mapping, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, make_aad(request_id, kid))
    return nonce, ciphertext, kid


def open_vault(key: bytes, nonce: bytes, ciphertext: bytes, request_id: str, kid: str) -> Dict[str, str]:
    if len(key) != KEY_BYTES:
        raise VaultError("Invalid key.")
    try:
        plaintext = AESGCM(key).decrypt(nonce, ciphertext, make_aad(request_id, kid))
        data = json.loads(plaintext.decode("utf-8"))
    except (InvalidTag, ValueError):
        raise VaultError("The key does not open this vault, or the vault was altered.") from None
    if not isinstance(data, dict):
        raise VaultError("Vault content is malformed.")
    return {str(k): str(v) for k, v in data.items()}
