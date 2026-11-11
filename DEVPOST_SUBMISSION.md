# PhishGuard AI: Explainable Phishing Detection with a Trained Domain Model

## Inspiration
Phishing campaigns get around blocklists within minutes by using algorithmically generated domains (DGA), look-alike domains such as `paypa1-secure.xyz`, and social-engineering text. Relying only on an LLM adds latency and availability risk, and purely rule-based systems miss new domains. We built **PhishGuard AI** to combine three layers that cover each other's weaknesses: transparent mathematical rules, a **trained machine-learning domain classifier**, and a **privacy-preserving Gemini AI gateway** with AES-256-GCM vaulting and Shamir 2-of-3 secret sharing.

## Live Demo
- **Deployment:** https://phish-guard-app-beta.vercel.app
- **Repository:** https://github.com/Ahmed-za55/phish-guard-ai

## What it does
PhishGuard AI analyzes **text messages**, **screenshots**, and **raw `.eml` emails** without executing attachments or visiting links, and returns a 0-100 risk score in which every point is itemized.

1. **Trained domain classifier (new):** a logistic-regression model on character n-grams and domain features, evaluated on domains it never saw during training (results below). Exposed as `POST /api/v1/detect` with a small web UI.
2. **Information-theoretic URL telemetry:** Shannon entropy of URLs and hostnames to flag obfuscated or DGA-style hosts.
3. **Homoglyph-aware brand protection:** Levenshtein distance after homoglyph normalization to catch look-alike domains.
4. **Forensic `.eml` inspection:** `From` vs `Reply-To` mismatches, display-name spoofing, double extensions (`.pdf.exe`), macro-enabled attachments.
5. **Transparent risk engine:** combines AI confidence with deterministic signals using set-based de-duplication, so one threat is never counted twice. Every contribution is listed by signal, source and points.
6. **Graceful degradation:** in private mode (/api/v1/private/analyze), if Gemini is rate-limited or unavailable, the gateway still returns the local trained domain classifier verdict; legacy routes use deterministic lexical and .eml analysis.

## Measured results of the trained model
All numbers come from `backend/scripts/train.py` and are reproducible from public data.

- **Data:** 20,000 registered domains (10,000 phishing from the Phishing.Database feed, 10,000 legitimate from OpenDNS top and random domain lists).
- **Evaluation:** train / validation / test split grouped by domain; the 4,000 test domains never appear in training. Thresholds were chosen on validation data only.

| Verdict used by the API | Precision | Recall | False-positive rate |
|---|---|---|---|
| `PHISHING` (tuned for false positives of at most 5%) | 91.8% | 56.5% | 4.9% |
| `SUSPICIOUS` or worse (best F1) | 74.8% | 78.4% | 25.4% |

For comparison, a hand-written rule baseline on the same test set catches only 20.3% of phishing domains (F1 33.1% vs 76.6% for the trained model).

**Limitations, stated plainly:** the model judges the registered domain name only (not page content, path or domain age); it cannot judge individual sites hosted on shared platforms such as `github.io` or `netlify.app` (the API returns `NOT_SCORED`); and real traffic contains more kinds of legitimate sites than our data, so real-world false positives are likely higher than shown. We did not benchmark the LLM component.

## Mathematical foundations

### 1. Shannon information entropy
For a URL or hostname string $X$ over alphabet $\Sigma$:
$$H(X) = -\sum_{x_i \in \Sigma} P(x_i) \log_2 P(x_i), \quad P(x_i) = \frac{\text{count}(x_i)}{|X|}$$
When $H(\text{URL}) \ge 4.35$ or $H(\text{Hostname}) \ge 3.85$, the engine flags lexical obfuscation.

### 2. Homoglyph-normalized Levenshtein similarity
For a domain token $t$, a protected brand $b$ and a homoglyph normalization map $\phi$:
$$S_L(t, b) = 1 - \frac{\min(d_L(t, b), d_L(\phi(t), b))}{\max(|t|, |b|)}$$
A domain is flagged as a look-alike when $0 < d_L \le 2$ and $S_L(t, b) \ge 0.72$.

### 3. Set-deduplicated, itemized scoring
With disjoint sets of AI-classified threats $\mathcal{T}$ and deterministic flags $\mathcal{D}$:
$$R_{\text{raw}} = 12 C_{\text{AI}} + 22 \mathbb{I}_{\text{phish}} + \sum_{k \in \mathcal{T}} w_k + \sum_{m \in \mathcal{D} \setminus \mathcal{T}} d_m + \min(0.25 U_{\max}, 20) + \Delta_{\text{math}}$$
$$R_{\text{final}} = \min(100, \max(0, \text{round}(R_{\text{raw}})))$$
The weights are set by hand and explained in the output; they are not fitted probabilities. The trained domain model feeds the URL term $U_{\max}$: a `PHISHING` verdict raises the URL score to at least the model score, a `SUSPICIOUS` verdict adds 10 points, and the model never lowers a score.

### 4. Privacy-preserving vault & Shamir $(2, 3)$ key custody over $\mathbb{F}_{2^{521}-1}$
Sensitive entities (names, emails, phones, cards, credentials, URLs) are replaced with random opaque tokens before any external LLM call. The token mapping is sealed with **AES-256-GCM** using a 256-bit ephemeral key $K$ and request-bound AAD (`pg-vault|v1|{request_id}|{kid}`). The key $K$ is split into 3 shares over the Mersenne prime field $p = 2^{521} - 1$ via a random degree-1 polynomial:
$$f(x) = (K + a_1 x) \bmod p, \quad S_i = (x_i, f(x_i)) \text{ for } x_i \in \{1, 2, 3\}$$
Any 2 shares reconstruct $K$ at $x = 0$ via Lagrange interpolation, while a single share leaves every 256-bit key equally probable:
$$K = \left( y_0 \frac{-x_1}{x_0 - x_1} + y_1 \frac{-x_0}{x_1 - x_0} \right) \bmod p$$

## How we built it
- **Backend:** Python, FastAPI, Pydantic, a deterministic `.eml` MIME parser, scikit-learn for the domain model.
- **AI layer:** Google Gemini (`google-genai`) for text and vision analysis, with a sliding-window rate limiter and a deterministic fallback.
- **Frontend:** Next.js, TypeScript, Tailwind CSS.
- **Quality:** 125 automated tests (75 for the privacy gateway & cryptography, 50 for the trained detector & API integration) and a GitHub Actions CI pipeline.

## Challenges we ran into
- **A data shortcut that fooled our own evaluation.** Our first model scored 93% F1, but it flagged `en.wikipedia.org` as phishing. The cause: legitimate training domains almost never have subdomains (0.1%) while phishing hosts often do (68%), so the model had learned "has a subdomain means phishing". We fixed it by scoring the registered domain only, removing shared-hosting platforms from the training data, and adding everyday (non-famous) legitimate domains. Honest accuracy dropped to the numbers above, and we report those.
- **Score inflation.** When both the LLM and the parser flagged the same threat, naive addition inflated low-risk alerts. Canonical threat mapping and the set difference $\mathcal{D} \setminus \mathcal{T}$ fixed it.
- **Look-alike domains.** Substring checks missed `paypa1` and `micr0soft`; homoglyph normalization plus dynamic-programming Levenshtein distance solved this with no external network calls.

## Accomplishments that we're proud of
- Static inspection only: URLs are never fetched and attachments are never executed.
- Every point of the risk score is itemized by signal, source and weight.
- An evaluation we can defend: domain-grouped splits, a baseline to beat, and limitations published next to the numbers.

## What's next
- Add page, path and domain-age features, and evaluate on a time-based split (train on older feeds, test on newer ones).
- More diverse legitimate data (regional and institutional domains are over-flagged today).
- Browser extension and MCP server for real-time inbox protection.