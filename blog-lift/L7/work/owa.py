# Independent re-implementation of the published across-lens fold: rank lenses worst to best, the rank-r lens
# weighs q^r (r = 0, 1, ...), weights normalised to sum to 1, headline = sum(score * weight). q from the rubric catalog.
import sys, json
bundle = json.load(open(sys.argv[1]))
q = json.load(open(sys.argv[2]))["scoring"]["acrossLensQ"] if len(sys.argv) > 2 else 0.55
s = sorted(l["score"] for l in bundle["lenses"])
w = [q ** r for r in range(len(s))]
t = sum(w)
h = sum(x * wi / t for x, wi in zip(s, w))
print(f"q={q} lenses={len(s)} headline={h:.4f} claimed={bundle.get('headlineScore')} delta={abs(h - bundle.get('headlineScore', h)):.4f}")
