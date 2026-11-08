import json
from urllib.parse import urlsplit

from app.storage import vector_cache
from app.storage.vector_cache import ThreatMemoryCache


def test_cache_redacts_sensitive_values_and_preserves_detection_fields(monkeypatch, tmp_path):
    cache_path = tmp_path / "threat_cache.json"
    monkeypatch.setattr(vector_cache, "CACHE_FILE", cache_path)

    sentinel = "CACHE_SENTINEL_ACCOUNT_7F3A"
    email = "private-cache-sentinel@example.invalid"
    phone = "+1 (202) 555-0198"
    url = f"https://secure.example.invalid/reset?token={sentinel}"
    text = f"Urgent: contact {email}, call {phone}, then visit {url}"
    result = {
        "is_phishing": True,
        "confidence": 0.99,
        "threats": ["Malicious Links", "Social Engineering"],
        "evidence": [f"Matched URL {url}", f"Contact marker {email}"],
        "urls": [
            {
                "url": url,
                "hostname": urlsplit(url).hostname,
                "risk_score": 92,
                "risk_level": "HIGH",
                "reasons": ["The URL contains sensitive-action terms."],
            }
        ],
        "local_llm_consult": {
            "assistant_mode": "offline_sovereign_neural",
            "analysis_commentary": f"Analyzed threat vector: {text[:60]}...",
        },
        "ast_payload_deobfuscation": {
            "deep_inspection_triggered": True,
            "decoded_hidden_artifacts": [sentinel],
        },
        "frontier_architecture_v72": {
            "2_detection_intelligence": {
                "privacy_preserving_inference": {
                    "sanitized_text": text,
                    "pii_redacted": True,
                }
            }
        },
    }

    ThreatMemoryCache.set(text, result)

    serialized_cache = cache_path.read_text(encoding="utf-8")
    for sensitive_value in (sentinel, email, phone, url, text[:60]):
        assert sensitive_value not in serialized_cache
    assert '"_cache_privacy_schema": 3' in serialized_cache

    cached = ThreatMemoryCache.get(text)
    assert cached is not None
    assert cached["is_phishing"] is True
    assert cached["threats"] == result["threats"]
    assert cached["urls"][0]["url"] == url
    assert cached["urls"][0]["risk_score"] == 92
    assert cached["evidence"][0] == f"Matched URL {url}"
    assert cached["local_llm_consult"]["analysis_commentary"] == ""
    assert cached["ast_payload_deobfuscation"]["decoded_hidden_artifacts"] == []
    assert (
        cached["frontier_architecture_v72"]["2_detection_intelligence"]
        ["privacy_preserving_inference"]["sanitized_text"]
        is None
    )


def test_cache_round_trip_preserves_non_sensitive_results(monkeypatch, tmp_path):
    monkeypatch.setattr(vector_cache, "CACHE_FILE", tmp_path / "threat_cache.json")
    text = "Urgent message with no sensitive identifiers"
    result = {
        "is_phishing": True,
        "threats": ["Social Engineering"],
        "urls": [],
        "risk_score": 73,
    }

    ThreatMemoryCache.set(text, result)

    assert ThreatMemoryCache.get(text) == result


def test_legacy_entries_are_cache_misses_without_changing_runtime_cache(monkeypatch, tmp_path):
    cache_path = tmp_path / "threat_cache.json"
    monkeypatch.setattr(vector_cache, "CACHE_FILE", cache_path)
    content = "legacy synthetic fixture"
    legacy = {ThreatMemoryCache._hash_payload(content): {"is_phishing": True}}
    cache_path.write_text(json.dumps(legacy), encoding="utf-8")

    assert ThreatMemoryCache.get(content) is None
    assert json.loads(cache_path.read_text(encoding="utf-8")) == legacy


def test_orchestrator_rebuilds_omitted_fields_from_current_input(monkeypatch):
    from app.agents import orchestrator

    text = "Please verify CACHE_SENTINEL_REHYDRATE_91AC"
    cached = {
        "local_llm_consult": {
            "assistant_mode": "offline_sovereign_neural",
            "analysis_commentary": "",
        },
        "architecture_grade": "uncached-grade",
        "ast_payload_deobfuscation": {
            "deep_inspection_triggered": False,
            "decoded_hidden_artifacts": [],
        },
        "frontier_architecture_v72": {
            "2_detection_intelligence": {
                "privacy_preserving_inference": {
                    "sanitized_text": None,
                    "pii_redacted": False,
                }
            }
        },
    }

    rebuilt_apocalypse = {"rebuilt": True}
    monkeypatch.setattr(orchestrator.SovereignLocalLLMAssistant, "consult_assistant", lambda value: {"analysis_commentary": value[:60]})
    monkeypatch.setattr(orchestrator.ASTPayloadDeobfuscator, "deobfuscate_and_inspect", lambda value: {"input": value})
    monkeypatch.setattr(orchestrator.FrontierDetectionIntelligence, "sanitize_privacy_preserving_input", lambda value: {"sanitized_text": value})
    monkeypatch.setattr(orchestrator, "extract_urls", lambda value: [])
    apoc_calls = []
    monkeypatch.setattr(
        orchestrator.ApocalypseTierMasterNexusV2,
        "run_apocalypse_enterprise_pipeline",
        lambda **kwargs: apoc_calls.append(kwargs) or rebuilt_apocalypse,
    )
    restored = orchestrator._restore_cached_input_dependent_fields(cached, text)

    assert text[:60] in restored["local_llm_consult"]["analysis_commentary"]
    assert (
        restored["frontier_architecture_v72"]["2_detection_intelligence"]
        ["privacy_preserving_inference"]["sanitized_text"]
        == text
    )
    assert restored["apocalypse_tier_v2_0"] == rebuilt_apocalypse
    assert restored["architecture_grade"] == "uncached-grade"
    assert apoc_calls == [{
        "text": text,
        "extracted_urls": [],
        "url_results": [],
        "tenant_id": "enterprise_client_001",
    }]


def test_no_url_apocalypse_prefix_is_never_serialized(monkeypatch, tmp_path):
    cache_path = tmp_path / "threat_cache.json"
    monkeypatch.setattr(vector_cache, "CACHE_FILE", cache_path)
    text = "NOURL_PREFIX_SENTINEL_83CD followed by synthetic message text"
    result = {
        "is_phishing": True,
        "apocalypse_tier_v2_0": {
            "enterprise_integration_fabric": {
                "sigma_rule": f"selection: {text[:20]}",
                "yara_rule": f"$a = \"{text[:20]}\"",
            }
        },
    }

    ThreatMemoryCache.set(text, result)

    serialized = cache_path.read_text(encoding="utf-8")
    assert text[:20] not in serialized
    assert "apocalypse_tier_v2_0" not in serialized
    cached = ThreatMemoryCache.get(text)
    assert cached is not None
    assert cached["is_phishing"] is True
    assert "apocalypse_tier_v2_0" not in cached


def test_structured_restoration_handles_placeholder_like_input_and_unrelated_markers(monkeypatch, tmp_path):
    monkeypatch.setattr(vector_cache, "CACHE_FILE", tmp_path / "cache.json")
    marker = "__PHISHGUARD_CACHE_VALUE_0000__"
    content = marker
    unrelated_marker = "__PHISHGUARD_CACHE_VALUE_9999__"
    result = {
        "source_defined": unrelated_marker,
        "nested": {"ordinary_key": [f"prefix {marker} suffix", ("another", marker)]},
    }

    ThreatMemoryCache.set(content, result)
    serialized = vector_cache.CACHE_FILE.read_text(encoding="utf-8")
    assert marker not in serialized
    restored = ThreatMemoryCache.get(content)

    assert restored == {
        "source_defined": unrelated_marker,
        "nested": {"ordinary_key": [f"prefix {marker} suffix", ["another", marker]]},
    }


def test_multiple_sensitive_values_and_nested_dictionary_keys_are_sanitized(monkeypatch, tmp_path):
    cache_path = tmp_path / "cache.json"
    monkeypatch.setattr(vector_cache, "CACHE_FILE", cache_path)
    first = "NESTED_KEY_SENTINEL_A19F"
    second = "SECOND_VALUE_SENTINEL_D4B2"
    content = f"contact {first}; backup {second}"
    result = {"outer": {f"dynamic-{first}": [f"{first}/{second}", {second: "safe verdict"}]}}

    ThreatMemoryCache.set(content, result)
    serialized = cache_path.read_text(encoding="utf-8")
    assert first not in serialized
    assert second not in serialized
    assert "dynamic-" + first not in serialized
    restored = ThreatMemoryCache.get(content)

    assert restored == result


def test_non_string_dynamic_dictionary_keys_fail_closed(monkeypatch, tmp_path):
    cache_path = tmp_path / "cache.json"
    monkeypatch.setattr(vector_cache, "CACHE_FILE", cache_path)
    ThreatMemoryCache.set("synthetic", {"safe": {42: "unsupported"}})
    assert not cache_path.exists()


def test_security_flags_bypass_cache_reads_and_writes(monkeypatch):
    from app.agents import orchestrator

    calls = []
    monkeypatch.setattr(orchestrator.ThreatMemoryCache, "get", lambda text: calls.append(("get", text)))
    monkeypatch.setattr(orchestrator.ThreatMemoryCache, "set", lambda text, result: calls.append(("set", text)))

    assert orchestrator._get_cache_entry("synthetic", ["attachment: private-name.txt"]) is None
    orchestrator._store_cache_entry("synthetic", {}, ["attachment: private-name.txt"])
    assert calls == []


def test_empty_security_flags_preserve_cache_reads_and_writes(monkeypatch):
    from app.agents import orchestrator

    calls = []
    cached_value = {"is_phishing": False}
    monkeypatch.setattr(orchestrator.ThreatMemoryCache, "get", lambda text: calls.append(("get", text)) or cached_value)
    monkeypatch.setattr(orchestrator.ThreatMemoryCache, "set", lambda text, result: calls.append(("set", text, result)))

    assert orchestrator._get_cache_entry("synthetic", []) is cached_value
    orchestrator._store_cache_entry("synthetic", cached_value, [])
    assert calls == [("get", "synthetic"), ("set", "synthetic", cached_value)]
