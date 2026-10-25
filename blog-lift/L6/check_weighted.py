#!/usr/bin/env python3
"""Sanity check of the reconstruction: the served order must be non-increasing in gain/effort x (1 + lift/100),
within rounding (gain +-0.05, lift +-0.5 %). Counts adjacent served pairs that violate it beyond that tolerance."""
import re, sys
from collections import defaultdict
EW = {"low": 1.0, "medium": 2.0, "high": 4.0}
by = defaultdict(list)
for line in open(sys.argv[1], encoding="utf-8"):
    p = [x.strip() for x in line.split("|")]
    if len(p) == 15 and re.match(r"^[0-9a-f]{8}-", p[0]) and p[9] != "true" and p[10] and p[11] in EW and p[12] != "":
        by[p[0]].append((int(p[5]), float(p[10]), EW[p[11]], int(p[12])))
pairs = bad = 0
for ts in by.values():
    ts.sort()
    for a, b in zip(ts, ts[1:]):
        pairs += 1
        a_max = (a[1] + 0.05) / a[2] * (1 + (a[3] + 0.5) / 100 if a[3] else 1)
        b_min = max(0, b[1] - 0.05) / b[2] * (1 + max(0, b[3] - 0.5) / 100 if b[3] else 1)
        if a_max < b_min:   # a served above b although even a's largest possible key is below b's smallest
            bad += 1
print(f"adjacent served pairs: {pairs}; pairs ordered against the reconstructed weighted key beyond rounding: {bad}")
