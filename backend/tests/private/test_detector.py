import pytest

from app.privacy_gateway.detector import detect, tokenize


def kinds(text, terms=()):
    return [(text[s.start:s.end], s.kind) for s in detect(text, terms)]


def test_email_phone_and_card():
    found = dict(kinds("mail a.b+c@example.co.uk or +20 100 123 4567, card 4111 1111 1111 1111"))
    assert found["a.b+c@example.co.uk"] == "EMAIL"
    assert found["+20 100 123 4567"] == "PHONE"
    assert found["4111 1111 1111 1111"] == "CARD"


def test_complete_url_is_one_span_including_sensitive_components_and_overlaps():
    url = "https://user:credential@secure.example:8443/reset/path?email=alice%40example.invalid&phone=%2B12025550123#fragment-secret"
    found = kinds(f"visit {url} now")
    assert found == [(url, "URL")]


def test_multiple_urls_are_detected_as_separate_complete_spans():
    first = "https://first.example/path?q=one#frag"
    second = "http://user:pass@second.example:8080/reset?token=two"
    assert kinds(f"{first} and {second}") == [(first, "URL"), (second, "URL")]


def test_card_requires_a_valid_luhn_checksum():
    assert ("4111 1111 1111 1112", "CARD") not in kinds("number 4111 1111 1111 1112")


def test_iban_requires_valid_checksum():
    assert ("GB82WEST12345698765432", "IBAN") in kinds("pay GB82WEST12345698765432 now")
    assert all(k != "IBAN" for _, k in kinds("pay GB82WEST12345698765433 now"))


def test_secrets_and_codes():
    text = "api_key = AIzaSyA1234567890abcdefghijklmnopqrstuv and password: hunter2hunter2, code 482913."
    found = kinds(text)
    assert any(k == "SECRET" for _, k in found)
    assert ("hunter2hunter2", "SECRET") in found
    assert ("482913", "CODE") in found


def test_national_id_and_ssn():
    assert ("29001011234567", "NATIONAL_ID") in kinds("id 29001011234567 ok")
    assert ("123-45-6789", "SSN") in kinds("ssn 123-45-6789")


def test_protected_terms_are_case_insensitive_and_ignore_tiny_words():
    found = kinds("Dear MARIAM hassan, hello al", ["Mariam Hassan", "al"])
    assert ("MARIAM hassan", "PROTECTED") in found
    assert all(value != "al" for value, _ in found)


def test_dates_and_plain_numbers_are_not_phones():
    assert kinds("Trained 2026-11-05 08:28 UTC, 20000 rows, version 1.1") == []


def test_overlaps_choose_one_span():
    spans = detect("write to 4111111111111111@example.com")
    assert len(spans) == 1 and spans[0].kind == "EMAIL"


def test_tokenize_replaces_every_occurrence_and_reuses_tokens():
    text = "a@b.co wrote to a@b.co; see http://x.test/?u=a@b.co"
    sanitized, mapping, records = tokenize(text, detect(text))
    assert "a@b.co" not in sanitized
    assert list(mapping.values()) == ["a@b.co", "http://x.test/?u=a@b.co"]
    assert len({r["token"] for r in records}) == 2


def test_tokens_are_unpredictable_per_request():
    text = "a@b.co"
    first = tokenize(text, detect(text))[1]
    seen = {next(iter(tokenize(text, detect(text))[1])) for _ in range(30)} | set(first)
    assert len(seen) > 1


def test_unicode_and_empty_input_do_not_crash():
    assert detect("") == []
    assert detect("مرحبا بالعالم 🌍 test@example.com")[0].kind == "EMAIL"


def test_a_protected_word_that_appears_inside_token_syntax_cannot_corrupt_tokens():
    text = "email mail@x.com from Email_1 team"
    sanitized, mapping, _ = tokenize(text, detect(text, ["mail"]))
    assert all(token in sanitized for token in mapping)  # every token is intact
    assert "mail@x.com" not in sanitized


def test_random_mixtures_never_leave_a_detected_value_behind():
    import random

    rng = random.Random(7)
    pieces = ["hello", "account", "verify", "a@b.co", "john.doe@mail.example.org", "+20 100 123 4567",
              "4111 1111 1111 1111", "password: Hunter22xyz", "code 123456", "http://x.test/p?e=a@b.co",
              "Mariam Hassan", "29001011234567", "مرحبا", "\n", "  "]
    for _ in range(300):
        text = " ".join(rng.choice(pieces) for _ in range(rng.randint(1, 12)))
        sanitized, mapping, records = tokenize(text, detect(text, ["Mariam Hassan"]))
        for value in mapping.values():
            assert value not in sanitized
        assert len(records) >= len(mapping)
