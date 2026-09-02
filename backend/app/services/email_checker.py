from email import policy
from email.message import Message
from email.parser import BytesParser
from email.utils import parseaddr


OFFICIAL_DOMAINS = {
    "paypal": ["paypal.com"],
    "microsoft": ["microsoft.com"],
    "apple": ["apple.com"],
    "google": ["google.com"],
    "amazon": ["amazon.com"],
    "facebook": ["facebook.com"],
    "instagram": ["instagram.com"],
    "whatsapp": ["whatsapp.com"],
    "netflix": ["netflix.com"],
    "visa": ["visa.com"],
    "mastercard": ["mastercard.com"],
}


HIGH_RISK_EXTENSIONS = {
    ".exe",
    ".scr",
    ".bat",
    ".cmd",
    ".com",
    ".msi",
    ".dll",
    ".jar",
    ".vbs",
    ".vbe",
    ".js",
    ".jse",
    ".wsf",
    ".wsh",
    ".ps1",
    ".hta",
}


MACRO_DOCUMENT_EXTENSIONS = {
    ".docm",
    ".xlsm",
    ".pptm",
}


ARCHIVE_EXTENSIONS = {
    ".zip",
    ".rar",
    ".7z",
    ".iso",
    ".img",
}


DOUBLE_EXTENSION_PATTERN = (
    ".pdf.exe",
    ".doc.exe",
    ".docx.exe",
    ".xls.exe",
    ".xlsx.exe",
    ".jpg.exe",
    ".jpeg.exe",
    ".png.exe",
    ".pdf.scr",
    ".doc.scr",
    ".docx.scr",
    ".jpg.scr",
    ".png.scr",
)


def get_domain(email_address: str) -> str:
    """Extract the domain from an email address."""

    if "@" not in email_address:
        return ""

    return email_address.rsplit(
        "@",
        1,
    )[1].lower().strip()


def detect_display_name_spoofing(
    sender_name: str,
    sender_email: str,
) -> str | None:
    """
    Detect when the display name appears to represent a trusted brand
    but the actual sender domain is not an official domain.
    """

    if not sender_name or not sender_email:
        return None

    name = sender_name.lower().strip()
    sender_domain = get_domain(sender_email)

    if not sender_domain:
        return None

    for brand, official_domains in OFFICIAL_DOMAINS.items():

        if brand not in name:
            continue

        is_official = any(
            sender_domain == domain
            or sender_domain.endswith("." + domain)
            for domain in official_domains
        )

        if not is_official:
            return (
                f"The display name appears to impersonate {brand}, "
                f"but the actual sender domain is "
                f"'{sender_domain}'."
            )

    return None


def analyze_attachment(filename: str) -> dict:
    """
    Analyze an attachment name without opening the file.

    This is heuristic analysis only.
    """

    original_name = filename or "unnamed_attachment"
    name = original_name.lower().strip()

    reasons: list[str] = []
    risk_score = 0

    # Double-extension detection.
    if any(
        name.endswith(pattern)
        for pattern in DOUBLE_EXTENSION_PATTERN
    ):
        risk_score += 60
        reasons.append(
            "The filename uses a suspicious double extension."
        )

    # High-risk executable/script extensions.
    for extension in HIGH_RISK_EXTENSIONS:
        if name.endswith(extension):
            risk_score += 50
            reasons.append(
                f"The attachment uses a high-risk file type: {extension}"
            )
            break

    # Macro-enabled Office documents.
    for extension in MACRO_DOCUMENT_EXTENSIONS:
        if name.endswith(extension):
            risk_score += 30
            reasons.append(
                f"The attachment is a macro-enabled document: {extension}"
            )
            break

    # Archive/container files.
    for extension in ARCHIVE_EXTENSIONS:
        if name.endswith(extension):
            risk_score += 15
            reasons.append(
                f"The attachment is an archive/container file: {extension}"
            )
            break

    # Suspicious words in filename.
    suspicious_words = {
        "invoice",
        "payment",
        "refund",
        "receipt",
        "urgent",
        "update",
        "security",
        "verification",
        "password",
        "account",
        "document",
    }

    matched_words = [
        word
        for word in suspicious_words
        if word in name
    ]

    if matched_words:
        risk_score += min(
            15,
            len(matched_words) * 5,
        )
        reasons.append(
            "The filename contains sensitive or urgency-related terms: "
            + ", ".join(sorted(matched_words))
            + "."
        )

    risk_score = min(risk_score, 100)

    if risk_score >= 75:
        risk_level = "CRITICAL"
    elif risk_score >= 50:
        risk_level = "HIGH"
    elif risk_score >= 25:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "filename": original_name,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reasons": reasons,
    }


def extract_email_content(email_bytes: bytes) -> dict:
    """
    Parse an .eml file and extract security-relevant information.

    No links are opened and no attachments are executed.
    """

    message: Message = BytesParser(
        policy=policy.default
    ).parsebytes(email_bytes)

    from_header = message.get("From", "")
    to_header = message.get("To", "")
    subject = message.get("Subject", "")
    reply_to_header = message.get("Reply-To", "")

    sender_name, sender_email = parseaddr(
        from_header
    )

    _, reply_to_email = parseaddr(
        reply_to_header
    )

    sender_domain = get_domain(
        sender_email
    )

    reply_to_domain = get_domain(
        reply_to_email
    )

    body_parts: list[str] = []
    attachments: list[str] = []

    if message.is_multipart():

        for part in message.walk():

            disposition = part.get_content_disposition()

            if disposition == "attachment":

                filename = part.get_filename()

                attachments.append(
                    filename or "unnamed_attachment"
                )

                continue

            if part.get_content_type() == "text/plain":

                try:
                    content = part.get_content()

                    if content:
                        body_parts.append(
                            content
                        )

                except Exception:
                    pass

    else:

        try:
            content = message.get_content()

            if content:
                body_parts.append(
                    content
                )

        except Exception:
            pass

    body = "\n".join(
        body_parts
    ).strip()

    security_flags: list[str] = []

    # ---------------------------------------------------------
    # Display Name spoofing
    # ---------------------------------------------------------

    display_name_flag = detect_display_name_spoofing(
        sender_name,
        sender_email,
    )

    if display_name_flag:
        security_flags.append(
            display_name_flag
        )

    # ---------------------------------------------------------
    # Reply-To mismatch
    # ---------------------------------------------------------

    if (
        sender_email
        and reply_to_email
        and sender_email.lower()
        != reply_to_email.lower()
    ):
        security_flags.append(
            "Reply-To address does not match the From address."
        )

    # ---------------------------------------------------------
    # Reply-To domain mismatch
    # ---------------------------------------------------------

    if (
        sender_domain
        and reply_to_domain
        and sender_domain
        != reply_to_domain
    ):
        security_flags.append(
            "Reply-To domain does not match the sender domain."
        )

    # ---------------------------------------------------------
    # Attachment analysis
    # ---------------------------------------------------------

    attachment_analysis = [
        analyze_attachment(filename)
        for filename in attachments
    ]

    for attachment in attachment_analysis:

        if attachment["risk_score"] >= 75:
            security_flags.append(
                f"High-risk attachment detected: "
                f"{attachment['filename']}."
            )

        elif attachment["risk_score"] >= 50:
            security_flags.append(
                f"Suspicious attachment detected: "
                f"{attachment['filename']}."
            )

    return {
        "from": from_header,
        "sender_name": sender_name,
        "sender_email": sender_email,
        "sender_domain": sender_domain,
        "to": to_header,
        "subject": subject,
        "reply_to": reply_to_header,
        "reply_email": reply_to_email,
        "reply_to_domain": reply_to_domain,
        "body": body,
        "attachments": attachments,
        "attachment_analysis": attachment_analysis,
        "security_flags": security_flags,
    }