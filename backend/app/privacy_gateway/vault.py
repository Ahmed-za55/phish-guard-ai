"""Authenticated encryption of the token -> original-value mapping."""
from __future__ import annotations

import hmac
import json
import os
import struct
from typing import Dict, Tuple

try:
    from cryptography.exceptions import InvalidTag
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    _HAS_CRYPTO = True
except Exception:
    InvalidTag = ValueError  # type: ignore
    AESGCM = None  # type: ignore
    _HAS_CRYPTO = False

from .shamir import KEY_BYTES, key_id


class VaultError(Exception):
    """The vault could not be opened (wrong key, tampering, or wrong request)."""


_SBOX = (
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16,
)
_RCON = (0x00,0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36,0x6C,0xD8,0xAB,0x4D)
_ZERO_BLOCK = bytes(16)
_J0_SUFFIX = bytes([0, 0, 0, 1])

def _xtime(a: int) -> int:
    return ((a << 1) ^ 0x1B) & 0xFF if (a & 0x80) else (a << 1)

def _aes_expand_key(key: bytes) -> list[list[int]]:
    w = [list(key[i:i+4]) for i in range(0, 32, 4)]
    for i in range(8, 60):
        temp = list(w[i - 1])
        if i % 8 == 0:
            temp = [_SBOX[temp[1]] ^ _RCON[i // 8], _SBOX[temp[2]], _SBOX[temp[3]], _SBOX[temp[0]]]
        elif i % 8 == 4:
            temp = [_SBOX[b] for b in temp]
        w.append([w[i - 8][j] ^ temp[j] for j in range(4)])
    return [[w[r*4 + c][j] for c in range(4) for j in range(4)] for r in range(15)]

def _aes_encrypt_block(block: bytes, rkeys: list[list[int]]) -> bytes:
    s = [block[i] ^ rkeys[0][i] for i in range(16)]
    for rnd in range(1, 14):
        s = [_SBOX[b] for b in s]
        s = [s[0], s[5], s[10], s[15], s[4], s[9], s[14], s[3], s[8], s[13], s[2], s[7], s[12], s[1], s[6], s[11]]
        ns = [0] * 16
        for c in range(4):
            i = c * 4
            a0, a1, a2, a3 = s[i], s[i+1], s[i+2], s[i+3]
            t = a0 ^ a1 ^ a2 ^ a3
            ns[i] = a0 ^ t ^ _xtime(a0 ^ a1)
            ns[i+1] = a1 ^ t ^ _xtime(a1 ^ a2)
            ns[i+2] = a2 ^ t ^ _xtime(a2 ^ a3)
            ns[i+3] = a3 ^ t ^ _xtime(a3 ^ a0)
        s = [ns[i] ^ rkeys[rnd][i] for i in range(16)]
    s = [_SBOX[b] for b in s]
    s = [s[0], s[5], s[10], s[15], s[4], s[9], s[14], s[3], s[8], s[13], s[2], s[7], s[12], s[1], s[6], s[11]]
    return bytes(s[i] ^ rkeys[14][i] for i in range(16))

def _gf_mult(x: int, y: int) -> int:
    z = 0
    v = y
    for i in range(127, -1, -1):
        if (x >> i) & 1:
            z ^= v
        v = (v >> 1) ^ (0xE1 << 120) if (v & 1) else (v >> 1)
    return z

def _ghash(h: int, aad: bytes, ct: bytes) -> int:
    pad_aad = aad + bytes((16 - (len(aad) % 16)) % 16)
    pad_ct = ct + bytes((16 - (len(ct) % 16)) % 16)
    data = pad_aad + pad_ct + struct.pack(">QQ", len(aad) * 8, len(ct) * 8)
    y = 0
    for i in range(0, len(data), 16):
        blk = int.from_bytes(data[i:i+16], "big")
        y = _gf_mult(y ^ blk, h)
    return y

def _ctr_crypt(rkeys: list[list[int]], j0: bytes, data: bytes) -> bytes:
    out = bytearray()
    prefix = j0[:12]
    cnt = int.from_bytes(j0[12:], "big")
    for i in range(0, len(data), 16):
        cnt = (cnt + 1) & 0xFFFFFFFF
        ks = _aes_encrypt_block(prefix + cnt.to_bytes(4, "big"), rkeys)
        chunk = data[i:i+16]
        out.extend(b ^ k for b, k in zip(chunk, ks))
    return bytes(out)

def _py_aesgcm_encrypt(key: bytes, nonce: bytes, plaintext: bytes, aad: bytes) -> bytes:
    rkeys = _aes_expand_key(key)
    h = int.from_bytes(_aes_encrypt_block(_ZERO_BLOCK, rkeys), "big")
    j0 = nonce + _J0_SUFFIX
    ct = _ctr_crypt(rkeys, j0, plaintext)
    s = _ghash(h, aad, ct) ^ int.from_bytes(_aes_encrypt_block(j0, rkeys), "big")
    return ct + s.to_bytes(16, "big")

def _py_aesgcm_decrypt(key: bytes, nonce: bytes, data: bytes, aad: bytes) -> bytes:
    if len(data) < 16:
        raise ValueError("Ciphertext too short")
    ct, tag = data[:-16], data[-16:]
    rkeys = _aes_expand_key(key)
    h = int.from_bytes(_aes_encrypt_block(_ZERO_BLOCK, rkeys), "big")
    j0 = nonce + _J0_SUFFIX
    expected = (_ghash(h, aad, ct) ^ int.from_bytes(_aes_encrypt_block(j0, rkeys), "big")).to_bytes(16, "big")
    if not hmac.compare_digest(tag, expected):
        raise ValueError("Invalid authentication tag")
    return _ctr_crypt(rkeys, j0, ct)

def new_key() -> bytes:
    return os.urandom(KEY_BYTES)

def make_aad(request_id: str, kid: str) -> bytes:
    return f"pg-vault|v1|{request_id}|{kid}".encode("ascii")

def seal(key: bytes, mapping: Dict[str, str], request_id: str) -> Tuple[bytes, bytes, str]:
    kid = key_id(key)
    nonce = os.urandom(12)
    plaintext = json.dumps(mapping, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    aad = make_aad(request_id, kid)
    if _HAS_CRYPTO:
        ciphertext = AESGCM(key).encrypt(nonce, plaintext, aad)
    else:
        ciphertext = _py_aesgcm_encrypt(key, nonce, plaintext, aad)
    return nonce, ciphertext, kid

def open_vault(key: bytes, nonce: bytes, ciphertext: bytes, request_id: str, kid: str) -> Dict[str, str]:
    if len(key) != KEY_BYTES:
        raise VaultError("Invalid key.")
    aad = make_aad(request_id, kid)
    try:
        if _HAS_CRYPTO:
            plaintext = AESGCM(key).decrypt(nonce, ciphertext, aad)
        else:
            plaintext = _py_aesgcm_decrypt(key, nonce, ciphertext, aad)
        data = json.loads(plaintext.decode("utf-8"))
    except (InvalidTag, ValueError):
        raise VaultError("The key does not open this vault, or the vault was altered.") from None
    if not isinstance(data, dict):
        raise VaultError("Vault content is malformed.")
    return {str(k): str(v) for k, v in data.items()}
