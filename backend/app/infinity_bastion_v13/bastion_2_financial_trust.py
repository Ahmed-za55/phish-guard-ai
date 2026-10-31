import hmac
import hashlib
from typing import Dict, Any, List

class FinancialIntentSecurityEngine:
    """
    2. Financial Intent Security & Independent Trust Confirmation Protocol (IOTP):
    - يقارن بيانات المستفيد في الفواتير بالمستفيدين المعتمدين مسبقاً.
    - يكتشف تغيير الحسابات البنكية وبيانات التحويل (BEC Wire Fraud).
    - يفرض بروتوكول تأكيد مستقل عبر قناة منفصلة (Independent Trust Confirmation).
    """
    _KNOWN_APPROVED_BENEFICIARIES: Dict[str, str] = {
        "acme corp": "US1234567890SWIFT",
        "global logistics ltd": "GB9876543210IBAN"
    }

    @classmethod
    def evaluate_financial_transaction_intent(
        cls,
        vendor_name: str,
        invoiced_iban_or_swift: str,
        amount_usd: float,
        out_of_band_confirmed: bool
    ) -> Dict[str, Any]:
        vendor_key = vendor_name.lower().strip()
        approved_account = cls._KNOWN_APPROVED_BENEFICIARIES.get(vendor_key)

        account_mismatch = False
        if approved_account:
            account_mismatch = (approved_account.lower() != invoiced_iban_or_swift.lower())
        else:
            # مورد جديد غير مسجل مسبقاً بمبلغ عالٍ يعتبر خطراً داهمًا
            account_mismatch = amount_usd >= 5000.0

        requires_iotp = account_mismatch or (amount_usd >= 10000.0)
        transaction_permitted = (not requires_iotp) or out_of_band_confirmed

        return {
            "financial_security_tier": "BEC_WIRE_FRAUD_PREVENTER",
            "vendor_recognized": vendor_key in cls._KNOWN_APPROVED_BENEFICIARIES,
            "beneficiary_account_mismatch": account_mismatch,
            "independent_trust_confirmation_required": requires_iotp,
            "out_of_band_confirmed": out_of_band_confirmed,
            "transaction_execution_permitted": transaction_permitted,
            "enforced_action": "PERMIT_TRANSACTION" if transaction_permitted else "BLOCK_AND_REQUIRE_OUT_OF_BAND_VERIFICATION"
        }