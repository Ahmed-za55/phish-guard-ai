# PhishGuard AI

A phishing-domain detector: a **trained machine-learning model** behind a FastAPI service, with a small web UI.
Every number below is produced by code in this repo (`backend/scripts/train.py`) on a public dataset - nothing is hardcoded.

## What is real here

| Part | Status |
|---|---|
| URL/domain classifier (`backend/app/real_detector/`) | Trained model, measured on held-out domains |
| REST API `POST /api/v1/detect` + web UI `/api/v1/detect/ui` | Working |
| Tests (`backend/tests/real/`) + GitHub Actions CI | Working |
| Other folders under `backend/app/` (`apex_math_core`, `nextgen_core`, ...) | **Research prototypes / simulations.** Their outputs are illustrative and are *not* measured; the detector does not depend on them. |

## Quick start

```bash
cd backend
python -m venv venv                 # Windows: venv\Scripts\activate   |   Linux/macOS: source venv/bin/activate
pip install -r requirements-real.txt
python scripts/fetch_data.py        # downloads a public dataset (no account needed)
python scripts/train.py             # trains, evaluates, writes models/ and the Results table below
python -m pytest                    # runs the tests
uvicorn app.main:app --reload       # open http://127.0.0.1:8000/api/v1/detect/ui
```

```bash
curl -X POST http://127.0.0.1:8000/api/v1/detect -H "Content-Type: application/json" \
     -d '{"url": "http://secure-paypal-login-48213.xyz/verify"}'
```

Response (shortened): `{"verdict": "PHISHING", "risk_score": 100.0, "scored_domain": "secure-paypal-login-48213.xyz", "indicators": [...]}`

## Results

<!-- RESULTS:START -->
_Trained 2026-11-05 08:28 UTC - scikit-learn 1.8.0 - 20,000 hosts (10,000 phishing / 10,000 legitimate). Test set: 4,000 hosts from 4,000 registered domains that never appear in training._

| Model (held-out domains) | Precision | Recall | F1 | False-positive rate | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression (char n-grams + features) **(shipped)** | 74.84% | 78.43% | 76.59% | 25.36% | 0.8575 |
| Random Forest (features only) | 65.24% | 80.57% | 72.10% | 41.29% | 0.8086 |
| Hand-written rules (baseline) | 89.84% | 20.30% | 33.11% | 2.21% | 0.5904 |

How the shipped model is used (two thresholds chosen on validation data, measured on the test set):

| Verdict | Rule | Precision | Recall | False-positive rate |
|---|---|---|---|---|
| PHISHING | score >= 0.71 (tuned for FPR <= 5%) | 91.80% | 56.50% | 4.86% |
| SUSPICIOUS or worse | score >= 0.42 (max F1) | 74.84% | 78.43% | 25.36% |

**Read these numbers with care:** the legitimate class mixes popular domains with random everyday domains, but real traffic contains many more kinds of legitimate sites, so real-world false positives are likely higher than shown. The model judges the registered domain only (not the page, path or content), and it cannot judge individual sites hosted on shared platforms (github.io, netlify.app, ...).
<!-- RESULTS:END -->

## How it works

1. **Data** - public lists: phishing domains from [Phishing.Database](https://github.com/mitchellkrogza/Phishing.Database), legitimate domains from the OpenDNS top and random domain lists.
2. **Cleaning that prevents shortcuts** - every host is reduced to its registered domain (legitimate lists have almost no subdomains while phishing hosts do, so a model would just learn "has a subdomain = phishing"); shared hosting platforms (netlify.app, duckdns.org, ...) and label conflicts are removed.
3. **Features** - character n-grams of the domain + length, entropy, hyphens, digits, keyword and brand patterns, TLD.
4. **Evaluation** - train/validation/test split grouped by domain (no domain appears in two sets), compared against a hand-written-rules baseline and a Random Forest. Thresholds are chosen on validation data only; the test set is used once.
5. **Verdicts** - `PHISHING` (tuned for at most 5% false positives), `SUSPICIOUS` (max-F1 point), `LIKELY_SAFE`.
   The *indicators* shown in the response (brand in subdomain, raw IP, ...) only explain the input; they never change the score.

## Limitations (please read)

- The model judges the **registered domain name only** - not the page, the path, the content or the domain age. Real phishing detection needs those signals too.
- It cannot judge individual sites on shared platforms (github.io, netlify.app, ...); the API returns `NOT_SCORED` for them instead of guessing.
- Regional or institutional domains that are rare in the training data (for example some `.edu.eg` university sites) can be over-flagged. More diverse legitimate data is the first thing to add.
- Legitimate training domains are popular or randomly sampled everyday sites; real traffic is more varied, so false positives on small legitimate sites will likely be higher than the table shows.
- Phishing labels come from a community feed and contain some noise.

## Roadmap

- Add page/path/content features and domain-age (WHOIS) features
- Evaluate on a time-based split (train on older feeds, test on newer ones)
- Browser extension calling `/api/v1/detect`

## Project layout

```
backend/app/real_detector/   features.py  training.py  model.py  router.py  ui.html
backend/scripts/             fetch_data.py  train.py  patch_integration.py
backend/tests/real/          pytest suite
backend/models/              url_model.joblib  metrics.json
docs/RESULTS.md              latest results
```
