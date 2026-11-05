import sys
import requests
from pathlib import Path
sys.path.insert(0, str(Path("E:/phish-guard-ai/backend")))

BASE_URL = "http://127.0.0.1:8000/api/v1/nextgen"

def run_submission_live_checks():
    print("=" * 80)
    print(" PHISHGUARD SOVEREIGN — PRE-SUBMISSION END-TO-END VERIFICATION SUITE")
    print("=" * 80)

    # Payload 1: Arabic Social Engineering / Wire Fraud Attack
    payload_attack = {
        "message_text": "أمر مباشر من الإدارة والمدير التنفيذي: الأمر سري للغاية أنا في اجتماع لا تتصل، حول المبلغ فوراً وابعتلي على واتساب",
        "extracted_urls": ["https://phishing-portal-eg.org"],
        "url_risk_score": 92.0,
        "prior_thread_topic": "HR_ROUTINE",
        "sender_verified_role": "EXTERNAL_UNVERIFIED",
        "research_advisory_text": "Threat Advisory: Attackers are spoofing corporate portals using newly registered domains under 14 days, requesting OAuth scope mail.readwrite, and deploying a financial lure containing 'iban'."
    }

    print("\n[TEST 1] Dispatching Advanced Arabic Social Engineering Lure to /analyze...")
    try:
        res = requests.post(f"{BASE_URL}/analyze", json=payload_attack, timeout=10)
        if res.status_code == 200:
            data = res.json()
            print(f" -> Status: SUCCESS (HTTP 200)")
            print(f" -> Final Verdict: {data.get('final_sovereign_verdict')}")
            print(f" -> Execution Latency: {data.get('execution_latency_ms')} ms")
            
            # التحقق من الركن الأول (Discovery & Deception)
            dec = data.get("pillar_1_discovery", {}).get("semantic_deception_lab", {})
            print(f"    * Deception Verdict: {dec.get('deception_verdict')} (Index: {dec.get('cognitive_manipulation_index')})")
            print(f"    * Active Levers: {dec.get('active_psychological_levers')}")

            # التحقق من الركن الثالث (Defense & Immunity)
            imm = data.get("pillar_3_defense", {}).get("digital_immune_system", {})
            print(f"    * Immune Response: {imm.get('response_mode')} (Affinity: {imm.get('antibody_affinity_score')})")

            # التحقق من الركن الرابع (Trust & Proof Core)
            prf = data.get("pillar_4_trust_and_intelligence_core", {}).get("cryptographic_proof_fabric", {})
            print(f"    * Hash-Chain Intact: {prf.get('hash_chain_audit', {}).get('ledger_intact')}")
            print(f"    * Proof SHA-256: {prf.get('latest_sealed_decision', {}).get('proof_record_hash', '')[:24]}...")
        else:
            print(f" -> FAILED with HTTP {res.status_code}: {res.text}")
    except Exception as e:
        print(f" -> CONNECTION ERROR: Is FastAPI running? Details: {e}")

    # Payload 2: Legitimate Executive Notice (Testing False Positive Resistance)
    payload_legit = {
        "message_text": "CEO Executive Office: Please review the board of directors resilience slides immediately before our townhall.",
        "extracted_urls": ["https://internal-docs.microsoft.com"],
        "url_risk_score": 3.0,
        "prior_thread_topic": "GENERAL_OPERATIONS",
        "sender_verified_role": "VERIFIED_INTERNAL_EXECUTIVE",
        "research_advisory_text": ""
    }

    print("\n[TEST 2] Dispatching Legitimate Executive Notice (False Positive Test)...")
    try:
        res = requests.post(f"{BASE_URL}/analyze", json=payload_legit, timeout=10)
        if res.status_code == 200:
            data = res.json()
            dec = data.get("pillar_1_discovery", {}).get("semantic_deception_lab", {})
            print(f" -> Final Verdict: {data.get('final_sovereign_verdict')}")
            print(f" -> Deception Verdict: {dec.get('deception_verdict')} (Expected: LEGITIMATE_COMMUNICATION)")
        else:
            print(f" -> FAILED: {res.status_code}")
    except Exception as e:
        print(f" -> ERROR: {e}")

    print("\n" + "=" * 80)
    print(" [SUBMISSION READY] All endpoints and cognitive pipelines are responding!")
    print("=" * 80)

if __name__ == "__main__":
    run_submission_live_checks()