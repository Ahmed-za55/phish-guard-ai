import sys
import traceback

sys.path.insert(0, "E:/phish-guard-ai/backend")

from app.services.ai_service import analyze_text

test_text = (
    "URGENT: Your bank account has been suspended. "
    "Verify your identity immediately at "
    "http://secure-bank-login.example.com"
)

print("\n=== DIRECT AI SERVICE DIAGNOSTIC ===")

try:
    result = analyze_text(test_text)
    print("\nANALYSIS RESULT:")
    print(result)

except Exception as exc:
    print("\n=== ORIGINAL EXCEPTION ===")
    print(type(exc).__name__, str(exc))
    traceback.print_exc()

