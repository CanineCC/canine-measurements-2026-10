"""B1 figures from per-repo.csv. Usage: python3 stats.py per-repo.csv"""
import csv, statistics as st, math, collections, sys
rows = [(int(r['production_loc']), int(r['findings']), r['engine'], r['language'])
        for r in csv.DictReader(open(sys.argv[1] if len(sys.argv) > 1 else 'per-repo.csv'))]
LANGS = ('csharp', 'go', 'rust')

def summary(rows, tag):
    out = {}
    for L in LANGS:
        xs = [r for r in rows if r[3] == L]
        if len(xs) < 10:
            return False  # a version is compared only when each language has at least ten repositories
        f = [x[1] for x in xs]
        k = [x[1] / x[0] * 1000 for x in xs if x[0] > 0]
        out[L] = (len(xs), st.median(f), st.mean(f), st.median(k), st.median(x[0] for x in xs), max(f), sum(v == 0 for v in f))
    print(tag)
    for L, v in out.items():
        print(f"  {L}: n={v[0]} median={v[1]} mean={v[2]:.1f} per-KLOC median={v[3]:.2f} median LoC={v[4]:.0f} max={v[5]} zero={v[6]}")
    c, g, r = out['csharp'], out['go'], out['rust']
    q = lambda a, b: f"{a / b:.2f}"
    print(f"  C#/Go median {q(c[1], g[1])} mean {q(c[2], g[2])} | C#/Rust median {q(c[1], r[1])} mean {q(c[2], r[2])}"
          f" | per KLOC C#/Rust {q(c[3], r[3])} C#/Go {q(c[3], g[3])}")
    return True

summary(rows, f'ALL (n={len(rows)})')
for v, n in collections.Counter(r[2] for r in rows).most_common():
    if n >= 30:
        summary([r for r in rows if r[2] == v], f'ENGINE {v} (n={n})')
for L in LANGS:
    xs = [(math.log(r[0]), math.log(r[1])) for r in rows if r[3] == L and r[0] > 0 and r[1] > 0]
    mx = st.mean(a for a, _ in xs); my = st.mean(b for _, b in xs)
    sxy = sum((a - mx) * (b - my) for a, b in xs); sxx = sum((a - mx) ** 2 for a, _ in xs); syy = sum((b - my) ** 2 for _, b in xs)
    print(f"{L}: log-log r={sxy / math.sqrt(sxx * syy):.2f}, doubling size multiplies findings by {2 ** (sxy / sxx):.2f} (n={len(xs)})")
