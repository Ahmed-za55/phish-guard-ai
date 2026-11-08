"""Shamir secret sharing over the prime field GF(P), P = 2^521 - 1 (a Mersenne prime).

A secret s (an integer below P) is the constant term of a random polynomial of degree k-1:

    f(x) = s + a_1 x + ... + a_{k-1} x^{k-1}   (mod P),   a_i uniform in [0, P)

Share i is the point (i, f(i)). Any k shares recover s by Lagrange interpolation at x = 0;
any k-1 shares are statistically independent of s (perfect secrecy): for a fixed set of k-1
points and ANY candidate secret s' there is exactly one polynomial through them, and every
polynomial is equally likely.

Share text format:  PG1.<kid>.<index>.<y as 132 hex digits>.<check>
  kid    8 hex digits, identifies which key the share belongs to (rejects mixed shares early)
  check  4 hex digits of SHA-256 over the fields before it (catches typing mistakes only;
         it is NOT a security feature - the AES-GCM tag is what authenticates a reconstructed key)
"""
from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from typing import List, Sequence

P = (1 << 521) - 1
KEY_BYTES = 32
_Y_HEX_LEN = 132  # 66 bytes = 528 bits >= 521 bits
VERSION = "PG1"


class ShareError(ValueError):
    """A share is malformed, inconsistent, or not enough shares were given."""


@dataclass(frozen=True)
class Share:
    kid: str
    index: int
    y: int

    def encode(self) -> str:
        body = f"{VERSION}.{self.kid}.{self.index}.{self.y:0{_Y_HEX_LEN}x}"
        return f"{body}.{_check(body)}"


def key_id(key: bytes) -> str:
    """Public, non-reversible label for a 256-bit random key."""
    return hashlib.sha256(b"pg-kid-v1" + key).hexdigest()[:8]


def _check(body: str) -> str:
    return hashlib.sha256(body.encode("ascii")).hexdigest()[:4]


def decode_share(text: str) -> Share:
    parts = (text or "").strip().split(".")
    if len(parts) != 5 or parts[0] != VERSION:
        raise ShareError("Share has the wrong format.")
    _, kid, index_s, y_hex, check = parts
    if len(kid) != 8 or len(y_hex) != _Y_HEX_LEN:
        raise ShareError("Share has the wrong length.")
    if _check(".".join(parts[:4])) != check:
        raise ShareError("Share has a typing error (checksum mismatch).")
    try:
        index = int(index_s)
        y = int(y_hex, 16)
        int(kid, 16)
    except ValueError as exc:
        raise ShareError("Share contains invalid characters.") from exc
    if not (1 <= index <= 255) or not (0 <= y < P):
        raise ShareError("Share is out of range.")
    return Share(kid=kid, index=index, y=y)


def split(key: bytes, threshold: int = 2, total: int = 3) -> List[Share]:
    if len(key) != KEY_BYTES:
        raise ValueError("key must be exactly 32 bytes")
    if not (2 <= threshold <= total <= 255):
        raise ValueError("need 2 <= threshold <= total <= 255")
    secret = int.from_bytes(key, "big")
    coeffs = [secret] + [secrets.randbelow(P) for _ in range(threshold - 1)]
    kid = key_id(key)
    shares = []
    for x in range(1, total + 1):
        y = 0
        for c in reversed(coeffs):  # Horner's rule, all arithmetic mod P
            y = (y * x + c) % P
        shares.append(Share(kid=kid, index=x, y=y))
    return shares


def combine(shares: Sequence[Share], threshold: int = 2) -> bytes:
    """Lagrange interpolation at 0 using the first `threshold` distinct shares."""
    if len({s.kid for s in shares}) > 1:
        raise ShareError("Shares belong to different keys.")
    unique = {}
    for s in shares:
        if s.index in unique and unique[s.index].y != s.y:
            raise ShareError("Two different shares claim the same index.")
        unique[s.index] = s
    if len(unique) < threshold:
        raise ShareError(f"At least {threshold} different shares are required.")
    points = list(unique.values())[:threshold]

    total = 0
    for i, si in enumerate(points):
        num, den = 1, 1
        for j, sj in enumerate(points):
            if i == j:
                continue
            num = (num * (-sj.index)) % P
            den = (den * (si.index - sj.index)) % P
        total = (total + si.y * num * pow(den, -1, P)) % P

    if total >> (KEY_BYTES * 8):
        raise ShareError("Shares are inconsistent (reconstructed value is not a 256-bit key).")
    return total.to_bytes(KEY_BYTES, "big")
