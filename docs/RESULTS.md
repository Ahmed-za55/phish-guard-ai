# Results

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
