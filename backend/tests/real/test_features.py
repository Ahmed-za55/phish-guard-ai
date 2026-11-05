import pytest

from app.real_detector.features import (
    extract_host, host_features, indicators, normalize_host, registered_domain, split_host,
)


@pytest.mark.parametrize("url,host", [
    ("https://www.Example.com/path?x=1", "www.example.com"),
    ("example.com", "example.com"),
    ("http://user:pw@example.com:8080/a", "example.com"),
    ("https://example.com.", "example.com"),
    ("HTTP://EXAMPLE.ORG", "example.org"),
])
def test_extract_host(url, host):
    assert extract_host(url) == host


@pytest.mark.parametrize("bad", ["", "   ", "javascript:alert(1)", "data:text/html,hi", "file:///etc/passwd", "mailto:a@b.com"])
def test_extract_host_rejects_unusable_input(bad):
    with pytest.raises(ValueError):
        extract_host(bad)


def test_idn_host_becomes_punycode():
    assert normalize_host("münchen.de") == "xn--mnchen-3ya.de"
    assert host_features("xn--mnchen-3ya.de")["has_punycode"] == 1


def test_split_host():
    assert split_host("en.wikipedia.org") == ("en", "wikipedia.org", "org")
    assert split_host("www.bbc.co.uk") == ("www", "bbc.co.uk", "uk")
    assert split_host("evil.com") == ("", "evil.com", "com")
    assert split_host("10.0.0.1") == ("", "10.0.0.1", "ip")
    assert registered_domain("a.b.c.example.com") == "example.com"


def test_features_basic_values():
    f = host_features("aaaa.com")
    assert f["is_ip"] == 0 and f["n_hyphens"] == 0
    assert host_features("x7k9q2zv4mw8.com")["entropy"] > f["entropy"]
    f = host_features("secure-login-1234567.xyz")
    assert f["n_hyphens"] == 2 and f["kw_count"] >= 2 and f["max_digit_run"] == 7
    assert host_features("192.168.1.1")["is_ip"] == 1


def test_brand_in_subdomain_indicator():
    hints = indicators(host_features("paypal.com.account-verify.top"))
    assert any("Brand name appears in the subdomain" in h for h in hints)
    assert not any("Brand name appears" in h for h in indicators(host_features("paypal.com")))


def test_shared_hosting_is_flagged_as_unscorable():
    hints = indicators(host_features("my-site.netlify.app"))
    assert any("shared platform" in h for h in hints)
