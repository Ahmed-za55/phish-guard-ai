# 🛡️ Phish Guard AI

> **Next-Generation Zero-Trust Cyber Defense Engine** combining Multimodal Large Language Models (LLMs), Deterministic Security Heuristics, and Real-Time Threat Intelligence.

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/AI-Google%20Gemini%202.5%20Flash-4285F4?style=flat-square&logo=google)](https://ai.google.dev/)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%20%2F%20React-000000?style=flat-square&logo=next.js)](https://nextjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Security: Hardened](https://img.shields.io/badge/Security-Hardened%20%26%20Rate--Limited-red?style=flat-square&logo=shield)](https://github.com/)

---

## 📌 Executive Summary

Phishing and social engineering attacks account for over **90% of all organizational security breaches**, resulting in billions of dollars in annual losses. Traditional email filters rely primarily on static, retroactive blacklists, while naive LLM wrappers suffer from hallucinations, high latency, and frequent rate-limit failures.

**Phish Guard AI** bridges this critical gap through a **Hybrid Defense Architecture**. It pairs Gemini's deep cognitive understanding with deterministic header forensics, heuristic URL risk profiling, and an offline **Zero-Downtime Fallback Engine**.

---

## 🚀 Key Features

### 1. 📧 Deep Header & Metadata Forensics (`.eml`)
- **Display Name Spoofing Detection:** Catches sophisticated impersonation where the display name mimicks trusted institutions (e.g., `PayPal Support`) while originating from unrelated sender domains.
- **Reply-To Mismatch Analysis:** Flags hidden reply routing discrepancies where attacker addresses diverge from official `From` headers.
- **Attachment Risk Analyzer:** Inspects filename patterns, high-risk extensions, double extensions (`.pdf.exe`), script payloads, and macro-enabled documents.

### 2. 🔗 Heuristic & Threat Intelligence URL Profiling
- **Zero-Click Inspection:** Analyzes suspicious URLs safely without resolving or visiting attacker endpoints.
- **Algorithmic Indicators:** Identifies typosquatting, excessive subdomain nesting, high-risk TLDs (`.xyz`, `.work`, `.click`), non-HTTPS transport, and sensitive credential-harvesting endpoints (`/login`, `/verify`).

### 3. 📷 Multimodal Screenshot OCR (`Vision Mode`)
- Direct visual analysis for phishing screenshots, SMS/WhatsApp smishing captures, and QR code traps using Gemini Vision models.

### 4. ⚖️ Risk Engine v2 (Calibrated Weighted Matrix)
- Transparent, explainable risk scoring (`0–100`) mapped to distinct severity tiers: `LOW`, `MEDIUM`, `HIGH`, and `CRITICAL`.
- Prevents artificial inflation (score capping) while deduplicating multi-source evidence.

### 5. 🛡️ Production-Grade Hardening & Fallback Resilience
- **Zero-Downtime Heuristic Fallback:** Seamlessly shifts to local heuristic evaluation during network cuts, upstream quota exhaustion, or API unavailability.
- **Thread-Safe Rate Limiting:** Built-in sliding-window IP rate limiting (`10 req/min`) with strict `HTTP 429` enforcement and `Retry-After` response headers.

---

## 🏗️ System Architecture

```
                                 [ Incoming Request ]
                     (Raw Text, Screenshot Image, or .EML File)
                                          │
                                          ▼
                         ┌─────────────────────────────────┐
                         │   Security & Hygiene Gateway    │
                         │  • Sliding-Window Rate Limiter  │
                         │  • File Size & MIME Validation  │
                         └────────────────┬────────────────┘
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
    ┌───────────────────────────┐                   ┌───────────────────────────┐
    │ Deterministic Forensics   │                   │ Multimodal AI Reasoning   │
    │ • Header Parser (RFC 822) │                   │ • Google Gemini Engine    │
    │ • Display Name Spoofing   │                   │ • Intent Extraction       │
    │ • URL Heuristics & TLDs   │                   │ • Vision OCR (Screenshots)│
    │ • Attachment Analysis     │                   │ • Zero-Downtime Fallback  │
    └─────────────┬─────────────┘                   └─────────────┬─────────────┘
                  │                                               │
                  └───────────────────────┬───────────────────────┘
                                          ▼
                         ┌─────────────────────────────────┐
                         │         Risk Engine v2          │
                         │  • Deduplication & Normalization│
                         │  • Severity Weight Calculation  │
                         │  • Score Calibration (0 - 100)  │
                         └────────────────┬────────────────┘
                                          │
                                          ▼
                       [ Unified Security Verdict Output ]
                  (Risk Score, Evidence, Threats & Mitigations)
```

---

## 🛠️ Technology Stack

- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **AI / LLM:** Google GenAI SDK (`gemini-2.5-flash`)
- **Security & Networking:** Heuristic Regex Engines, Sliding-Window Token Bucket, SlowAPI-compatible Rate Limiting
- **Frontend:** Next.js / React, TailwindCSS, Lucide Icons
- **Data Protocols:** Standard RFC 822 / MIME email parsing, Safe URL inspection

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ (for Frontend)
- Google Gemini API Key

### 1. Backend Setup

```bash
# Clone the repository
git clone https://github.com/your-username/phish-guard-ai.git
cd phish-guard-ai/backend

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.\.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
```

Edit `.env` with your credentials:
```env
GEMINI_API_KEY="your-gemini-api-key-here"
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60
MAX_TEXT_LENGTH=20000
FRONTEND_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

Start the backend server:
```bash
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd ../frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to access the dashboard.

---

## 🧪 API Reference & Endpoints

| Method | Endpoint | Description | Rate Limit |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Service health status check | Unlimited |
| `POST` | `/analyze` | Analyzes raw text or URLs | 10 req / min |
| `POST` | `/analyze-image` | Evaluates screenshot files (JPEG/PNG/WEBP) | 10 req / min |
| `POST` | `/analyze-email` | Deep header forensics on uploaded `.eml` | 10 req / min |

### Sample Response (`POST /analyze-email`)

```json
{
  "is_phishing": true,
  "confidence": 0.99,
  "risk_level": "CRITICAL",
  "risk_score": 92,
  "threats": [
    "Brand Impersonation",
    "Credential Theft",
    "Reply-To Mismatch",
    "Malicious Links"
  ],
  "evidence": [
    "Display Name Spoofing: Claims to be 'PayPal Support' but originates from 'evil-domain.com'.",
    "Reply-To header mismatches the envelope sender.",
    "Contains unencrypted HTTP authentication link: 'http://paypal-security-update.xyz/login'",
    "Domain uses high-risk suspicious TLD (.xyz)."
  ],
  "recommendations": [
    "Do not click links or provide credentials.",
    "Verify security notices directly via official banking/payment portals.",
    "Report this message to internal security operations."
  ],
  "risk_breakdown": {
    "raw_score": 94.2,
    "risk_score": 92,
    "risk_level": "CRITICAL",
    "capped": false
  }
}
```

---

## 🏆 Hackathon Demo Showcase

During evaluation pitches, Phish Guard AI demonstrates resilience across edge cases:
1. **The Subtle Spoof:** An email that reads cleanly but routes replies to a burner inbox while spoofing trusted executive names.
2. **The Offline Survival:** Cutting upstream network connectivity during live inference triggers instant heuristic fallback scoring without service degradation (`0% downtime`).
3. **DoS Defense Demonstration:** Automated high-frequency request bursts immediately encounter RFC-compliant `HTTP 429 Too Many Requests`.

---

## 📄 License
This project is open-source and licensed under the [MIT License](LICENSE).