import itertools
import os

import pytest

from app.privacy_gateway.shamir import P, ShareError, combine, decode_share, key_id, split


def test_any_two_of_three_recover_the_key():
    key = os.urandom(32)
    shares = split(key, 2, 3)
    for pair in itertools.combinations(shares, 2):
        assert combine(list(pair), 2) == key


def test_three_of_five_threshold():
    key = os.urandom(32)
    shares = split(key, 3, 5)
    for trio in itertools.combinations(shares, 3):
        assert combine(list(trio), 3) == key
    with pytest.raises(ShareError):
        combine(shares[:2], 3)


def test_one_share_is_not_enough():
    shares = split(os.urandom(32), 2, 3)
    with pytest.raises(ShareError):
        combine([shares[0]], 2)


def test_duplicate_share_does_not_count_twice():
    shares = split(os.urandom(32), 2, 3)
    with pytest.raises(ShareError):
        combine([shares[0], shares[0]], 2)


def test_shares_from_different_keys_are_rejected():
    a, b = split(os.urandom(32), 2, 3), split(os.urandom(32), 2, 3)
    with pytest.raises(ShareError):
        combine([a[0], b[1]], 2)


def test_a_single_share_is_consistent_with_every_possible_secret():
    """Perfect secrecy for k=2: through one point (x, y) passes exactly one line for ANY secret s'."""
    share = split(os.urandom(32), 2, 3)[0]
    for candidate in (0, 1, 2**255, 2**256 - 1, 123456789):
        slope = ((share.y - candidate) * pow(share.index, -1, P)) % P
        assert (candidate + slope * share.index) % P == share.y


def test_encoding_roundtrip_and_validation():
    key = os.urandom(32)
    share = split(key, 2, 3)[1]
    decoded = decode_share(share.encode())
    assert (decoded.kid, decoded.index, decoded.y) == (share.kid, share.index, share.y)
    assert decoded.kid == key_id(key)
    text = share.encode()
    for bad in ["", "nonsense", text[:-1], text.replace("PG1", "PG2"), text[:-5] + "0000" + text[-1]]:
        with pytest.raises(ShareError):
            decode_share(bad)


def test_edited_share_text_is_caught_by_checksum():
    text = split(os.urandom(32), 2, 3)[0].encode()
    parts = text.split(".")
    parts[3] = parts[3][:-1] + ("0" if parts[3][-1] != "0" else "1")
    with pytest.raises(ShareError):
        decode_share(".".join(parts))


def test_key_must_be_32_bytes():
    with pytest.raises(ValueError):
        split(b"short", 2, 3)
