from pathlib import Path

orch_path = Path("E:/phish-guard-ai/backend/app/agents/orchestrator.py")
content = orch_path.read_text(encoding="utf-8")

import_stmt = "from app.transcendence_v10.transcendence_master import TranscendenceMasterNexusV10\n"
if "TranscendenceMasterNexusV10" not in content:
    content = import_stmt + content

v10_block = """
        # =========================================================================
        # TRANSCENDENCE INITIATIVE — DEEP-TECH RESEARCH ARCHITECTURE (v10.0)
        # =========================================================================
        base_result["transcendence_v10"] = TranscendenceMasterNexusV10.run_transcendence_pipeline(
            text=text,
            extracted_urls=urls,
            url_results=url_results,
            entropy_val=sample_entropy_val
        )
        base_result["architecture_grade"] = "Apex-Sovereign-Transcendence-v10.0-Godtier"
"""

target_marker = 'ThreatMemoryCache.set(text, base_result)'
if "transcendence_v10" not in content and target_marker in content:
    content = content.replace(target_marker, v10_block + "\n        " + target_marker)
    orch_path.write_text(content, encoding="utf-8")
    print("[PATCHED] orchestrator.py upgraded to PHISHGUARD SOVEREIGN v10.0 TRANSCENDENCE INITIATIVE!")