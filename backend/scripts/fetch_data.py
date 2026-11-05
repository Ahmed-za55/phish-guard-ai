"""Download a real labeled dataset of REGISTERED DOMAINS -> backend/data/dataset.csv

Phishing  : Phishing.Database "ACTIVE domains" feed (community-maintained)
Legitimate: OpenDNS "top domains" (popular sites) + OpenDNS "random domains" (everyday, mostly
            obscure sites) - mixing both avoids a model that only learns "popular = safe".

No account or API key needed. Run from the backend/ folder:
    python scripts/fetch_data.py            # up to 10,000 per class
    python scripts/fetch_data.py --n 5000

Cleaning steps (each one prevents a shortcut the model could otherwise cheat with):
  1. every host is collapsed to its registered domain (legit lists have ~0% subdomains, phishing 68%)
  2. registered domains with 50+ phishing hosts are dropped: they are shared hosting platforms
     (netlify.app, duckdns.org...), not "phishing domains"
  3. phishing domains that also appear in the legitimate lists are dropped
"""
import argparse
import random
import sys
from collections import Counter
from pathlib import Path

import requests

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

from app.real_detector.features import normalize_host, registered_domain  # noqa: E402

RAW = "https://raw.githubusercontent.com"
SOURCES = {
    "phishing_database": f"{RAW}/mitchellkrogza/Phishing.Database/master/phishing-domains-ACTIVE.txt",
    "opendns_top": f"{RAW}/opendns/public-domain-lists/master/opendns-top-domains.txt",
    "opendns_random": f"{RAW}/opendns/public-domain-lists/master/opendns-random-domains.txt",
}
OUT = BACKEND / "data" / "dataset.csv"
PLATFORM_THRESHOLD = 50


def download(url: str) -> list[str]:
    print(f"Downloading {url}")
    r = requests.get(url, timeout=180, headers={"User-Agent": "phish-guard-ai-research"})
    r.raise_for_status()
    lines = [ln.strip().lower() for ln in r.text.splitlines()]
    return [ln for ln in lines if ln and not ln.startswith("#") and " " not in ln]


def to_registered(hosts: list[str]) -> list[str]:
    out = []
    for h in hosts:
        try:
            out.append(registered_domain(normalize_host(h)))
        except ValueError:
            continue
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10_000, help="max domains per class")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    legit_by_source = {k: sorted(set(to_registered(download(SOURCES[k])))) for k in ("opendns_top", "opendns_random")}
    legit_all = set().union(*legit_by_source.values())

    ph_regs = to_registered(download(SOURCES["phishing_database"]))
    counts = Counter(ph_regs)
    platforms = {d for d, c in counts.items() if c >= PLATFORM_THRESHOLD}
    phishing = sorted(d for d in counts if d not in platforms and d not in legit_all)
    print(f"Phishing: {len(counts):,} registered domains; dropped {len(platforms)} shared platforms "
          f"and {len(set(counts) & legit_all)} domains also seen in legit lists")

    # legit: half from the popular list, the rest from the random list, no domain twice
    n = min(args.n, len(phishing), len(legit_all))
    top = rng.sample(legit_by_source["opendns_top"], min(n // 2, len(legit_by_source["opendns_top"])))
    taken = set(top)
    pool = [d for d in legit_by_source["opendns_random"] if d not in taken]
    rnd = rng.sample(pool, min(n - len(top), len(pool)))
    legit = [(d, "opendns_top") for d in top] + [(d, "opendns_random") for d in rnd]
    phishing = rng.sample(phishing, min(len(legit), len(phishing)))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        f.write("host,label,source\n")
        for d in phishing:
            f.write(f"{d},1,phishing_database\n")
        for d, src in legit:
            f.write(f"{d},0,{src}\n")
    print(f"Wrote {OUT}  ({len(phishing):,} phishing + {len(legit):,} legitimate registered domains)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
