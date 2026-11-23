#!/usr/bin/env python3
"""Backtest for the Rebel Football Calculator model (same math as index.html).

Usage / Cara pakai:
    python backtest.py matches.csv

CSV needs columns (football-data.co.uk format): Date, HomeTeam, AwayTeam, FTHG, FTAG
Download free CSVs from https://www.football-data.co.uk/data.php
Rows must be in date order (oldest first). Pure Python, no packages needed.
"""
import csv, math, sys
from collections import defaultdict, deque

AVG, W, HOME, AWAY = 1.35, 0.7, 1.10, 0.92
MIN_MATCHES = 3  # same as the app: at least 3 recent matches per team


def pois(l, k):
    return math.exp(-l) * l ** k / math.factorial(k)


def predict(h_form, a_form):
    """h_form / a_form: list of (scored, conceded) for the last 5 matches."""
    mix = lambda x: (x * W + AVG * (1 - W)) / AVG
    hgf = sum(f for f, _ in h_form) / len(h_form)
    hga = sum(c for _, c in h_form) / len(h_form)
    agf = sum(f for f, _ in a_form) / len(a_form)
    aga = sum(c for _, c in a_form) / len(a_form)
    lh = max(0.2, AVG * mix(hgf) * mix(aga) * HOME)
    la = max(0.2, AVG * mix(agf) * mix(hga) * AWAY)
    ph = pd = pa = over = 0.0
    for i in range(9):
        for j in range(9):
            p = pois(lh, i) * pois(la, j)
            if i > j: ph += p
            elif i == j: pd += p
            else: pa += p
            if i + j > 2.5: over += p
    s = ph + pd + pa
    return ph / s, pd / s, pa / s, over / s


def main(path):
    form = defaultdict(lambda: deque(maxlen=5))
    n = hit = base_hit = ou_hit = 0
    brier = 0.0
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            try:
                h, a = r["HomeTeam"], r["AwayTeam"]
                hg, ag = int(r["FTHG"]), int(r["FTAG"])
            except (KeyError, ValueError, TypeError):
                continue
            if len(form[h]) >= MIN_MATCHES and len(form[a]) >= MIN_MATCHES:
                ph, pd, pa, po = predict(list(form[h]), list(form[a]))
                probs = [ph, pd, pa]
                actual = 0 if hg > ag else 1 if hg == ag else 2
                n += 1
                hit += probs.index(max(probs)) == actual
                base_hit += actual == 0  # baseline: always pick home win
                ou_hit += (po > 0.5) == (hg + ag > 2.5)
                brier += sum((p - (1 if k == actual else 0)) ** 2 for k, p in enumerate(probs))
            form[h].append((hg, ag))
            form[a].append((ag, hg))
    if n == 0:
        sys.exit("No usable matches. Check the CSV columns / Tidak ada data yang bisa dipakai.")
    print(f"Matches tested / Laga diuji : {n}")
    print(f"1X2 accuracy / Akurasi 1X2  : {hit / n:.1%}")
    print(f"Baseline (always home)      : {base_hit / n:.1%}")
    print(f"Over/Under 2.5 accuracy     : {ou_hit / n:.1%}")
    print(f"Brier score (lower = better): {brier / n:.3f}  (random guess = 0.667)")
    if n < 300:
        print("Warning: fewer than 300 matches, result is not reliable / hasil belum bisa diandalkan.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
