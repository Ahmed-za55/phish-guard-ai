import random

import pandas as pd


def synthetic_frame(n: int = 300, seed: int = 7) -> pd.DataFrame:
    """PLUMBING-ONLY data (clearly separable on purpose). It proves the code path works;
    it says nothing about real-world accuracy, which is measured by scripts/train.py."""
    rng = random.Random(seed)
    words = ["garden", "pizza", "school", "river", "music", "travel", "books", "coffee", "photo", "sports"]
    rows = []
    for i in range(n):
        rows.append((f"{rng.choice(words)}{rng.choice(words)}.com", 0))
        rows.append((f"secure-login-verify-{rng.randint(10000, 99999)}-{rng.choice(words)}.xyz", 1))
    df = pd.DataFrame(rows, columns=["host", "label"])
    return df.drop_duplicates("host").reset_index(drop=True)
