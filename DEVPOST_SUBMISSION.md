# PhishGuard AI: Mathematical & Hybrid Agentic Threat Detection

## Inspiration
Modern phishing campaigns bypass traditional blocklists within minutes by using algorithmically generated domains (DGA), homoglyph typosquatting (e.g., `paypa1-secure.xyz`), and context-aware social engineering. Relying solely on Large Language Models (LLMs) introduces latency and availability risks, while purely rule-based systems fail against semantic manipulation. We built **PhishGuard AI** to bridge **Mathematical Systems Security** (Information Theory, Metric Space String Distance, and Calibrated Risk Modeling) with **Multi-Modal Generative AI**.

## What it does
PhishGuard AI is an explainable cybersecurity defense platform that analyzes **raw text messages/SMS**, **screenshots (vision)**, and **raw `.eml` email files** without executing attachments or visiting malicious links:
1. **Information-Theoretic URL Telemetry:** Computes Shannon Entropy $H(X)$ across URLs and hostnames to detect cryptographic obfuscation and DGA domains.
2. **Metric Space Brand Protection:** Uses homoglyph normalization $\phi(t)$ combined with Levenshtein Edit Distance $d_L$ and normalized string similarity $S_L$ to catch lookalike domains.
3. **Forensic `.eml` & Attachment Inspection:** Parses MIME structures to uncover `From` vs. `Reply-To` domain mismatches, display-name spoofing, double extensions (`.pdf.exe`), and macro-enabled payloads.
4. **Calibrated Mathematical Risk Engine:** Aggregates probabilistic AI confidence with deterministic and mathematical signals using set-theoretic deduplication so no threat category is double-counted.
5. **Resilient Multi-Model & Heuristic Fallback:** Implements exponential backoff ($2^k$ seconds) across fallback LLM chains and seamlessly switches to our deterministic mathematical engine during API outages.

## Mathematical Foundations in Systems Security

### 1. Shannon Information Entropy $H(X)$
For any extracted URL or hostname string $X$ of length $|X|$ over character alphabet $\Sigma$, we compute the empirical Shannon entropy in bits per character:
$$H(X) = -\sum_{x_i \in \Sigma} P(x_i) \log_2 P(x_i), \quad P(x_i) = \frac{\text{count}(x_i)}{|X|}$$
When $H(\text{URL}) \ge 4.35$ or $H(\text{Hostname}) \ge 3.85$, the engine flags high-entropy lexical obfuscation.

### 2. Homoglyph-Normalized Levenshtein Similarity $S_L(t, b)$
Given a domain lexical token $t$ and a protected brand $b$, we apply a homoglyph de-obfuscation morphism $\phi$ (mapping visually deceptive numerals/symbols to canonical ASCII characters) and compute the normalized Levenshtein metric:
$$S_L(t, b) = 1 - \frac{\min(d_L(t, b), d_L(\phi(t), b))}{\max(|t|, |b|)}$$
A domain is flagged for mathematical typosquatting when $0 < d_L \le 2$ and $S_L(t, b) \ge 0.72$.

### 3. Set-Deduplicated Threat Scoring Model
To produce a bounded, explainable score $R_{\text{final}} \in [0, 100]$, we define disjoint threat sets $\mathcal{T}$ (AI-classified threats) and $\mathcal{D}$ (deterministic forensic flags):
$$R_{\text{raw}} = 12 C_{\text{AI}} + 22 \mathbb{I}_{\text{phish}} + \sum_{k \in \mathcal{T}} w_k + \sum_{m \in \mathcal{D} \setminus \mathcal{T}} d_m + \min(0.25 U_{\max}, 20) + \Delta_{\text{math}}$$
$$R_{\text{final}} = \min(100, \max(0, \text{round}(R_{\text{raw}})))$$

## How we built it
- **Backend:** Python, FastAPI, Pydantic, deterministic `.eml` MIME parser, and custom mathematical security modules (`risk_engine.py`, `url_checker.py`, `brand_detector.py`).
- **AI & Resilience Layer:** Google Gemini (`google-genai` SDK) for text and vision threat analysis, protected by a sliding-window IP rate limiter and an offline deterministic fallback engine.
- **Frontend:** Next.js, TypeScript, and Tailwind CSS providing an interactive security breakdown dashboard.

## Challenges we ran into
- **Preventing Score Inflation (Double-Counting):** When both the LLM and the deterministic parser flagged attachment abuse or brand spoofing, naive additive scoring inflated low-risk alerts. We solved this using canonical threat mapping and set difference $\mathcal{D} \setminus \mathcal{T}$ in `risk_engine.py`.
- **Catching Obfuscated Lookalike Domains:** Simple substring checks missed `paypa1` or `micr0soft`. Combining a homoglyph translation matrix with dynamic-programming Levenshtein distance solved this with zero external network calls.

## Accomplishments that we're proud of
- Zero-trust static inspection: URLs are never fetched and attachments are never executed.
- Complete mathematical explainability: Every single point in the 0-100 risk score is itemized by signal, source, and weight.
- 100% uptime guarantee via automatic heuristic/mathematical fallback when LLM endpoints experience 429/503 errors.

## What's next for PhishGuard AI
- Integrating Markov-chain transition probability matrices for n-gram domain naturalness scoring.
- Browser extension and MCP server integration for real-time inbox protection.