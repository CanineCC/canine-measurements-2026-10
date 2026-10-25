"""E1 step 2: the analysis exactly as frozen in WP-40 §E1 (commit b1ed0ab162). Pure Python, no tuning."""
import csv, json, random, re, statistics as st, collections, sys
AX = ['readability', 'understandability', 'complexity', 'modularization', 'overall']
NEG = {'complexity', 'modularization'}
PRED = ['cog_sum', 'cog_max', 'over15', 'cyc_sum', 'lines']
def vec(s): return [float(x) for x in re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', s)]
lab = {}
for r in csv.DictReader(open('sealed/labels.csv', newline='')):
    b = {}
    for a in AX:
        v = vec(r[a]); assert len(v) == 4, (a, r[a]); e = sum(k * p for k, p in enumerate(v)) / sum(v)
        b[a] = 3 - e if a in NEG else e
    lab[(r['projectname'], r['packageandclass'])] = b
rows = []
for r in csv.DictReader(open('predictions.csv')):
    x = {k: float(r[k]) for k in PRED}; x.update(lab[(r['projectname'], r['packageandclass'])]); x['proj'] = r['projectname']
    x['methods'] = int(r['methods']); x['id'] = r['packageandclass']; rows.append(x)
def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); rk = [0.0] * len(v); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): rk[o[k]] = (i + j) / 2 + 1
        i = j + 1
    return rk
def pearson(a, b):
    ma, mb = st.fmean(a), st.fmean(b); sa = sum((x - ma) ** 2 for x in a) ** .5; sb = sum((y - mb) ** 2 for y in b) ** .5
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb) if sa and sb else float('nan')
def rho(rs, p, a): return pearson(rank([r[p] for r in rs]), rank([r[a] for r in rs]))
def resid(y, x):
    mx, my = st.fmean(x), st.fmean(y); bb = sum((a - mx) * (b - my) for a, b in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    return [b - my - bb * (a - mx) for a, b in zip(x, y)]
def prho(rs, p, a):
    L = rank([r['lines'] for r in rs]); return pearson(resid(rank([r[p] for r in rs]), L), resid(rank([r[a] for r in rs]), L))
byp = collections.defaultdict(list)
for r in rows: byp[r['proj']].append(r)
rng = random.Random(20261025); B = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
boot = [[r for p in byp.values() for r in rng.choices(p, k=len(p))] for _ in range(B)]
def ci(f):
    v = sorted(f(b) for b in boot); return v[int(.025 * B)], v[int(.975 * B) - 1]
out = {'n': len(rows), 'projects': {p: len(v) for p, v in byp.items()}, 'B': B, 'cells': {}}
print(f"n = {len(rows)}  {out['projects']}  bootstrap B = {B}\n")
print(f"{'axis':<18}" + ''.join(f"{p:>22}" for p in PRED) + f"{'cog_sum | lines':>22}")
for a in AX:
    line = f"{a:<18}"
    for p in PRED:
        v = rho(rows, p, a); lo, hi = ci(lambda b: rho(b, p, a)); out['cells'][f'{a}/{p}'] = [v, lo, hi]
        line += f"{v:>8.3f} [{lo:.2f},{hi:.2f}]".rjust(22)
    v = prho(rows, 'cog_sum', a); lo, hi = ci(lambda b: prho(b, 'cog_sum', a)); out['cells'][f'{a}/partial'] = [v, lo, hi]
    line += f"{v:>8.3f} [{lo:.2f},{hi:.2f}]".rjust(22); print(line)
d = rho(rows, 'cog_sum', 'overall') - rho(rows, 'lines', 'overall')
lo, hi = ci(lambda b: rho(b, 'cog_sum', 'overall') - rho(b, 'lines', 'overall')); out['primary_minus_size'] = [d, lo, hi]
print(f"\nprimary − size baseline on overall: {d:+.3f} [{lo:+.3f}, {hi:+.3f}]")
print("\nper project, primary on overall (and size baseline):")
for p, v in sorted(byp.items()): print(f"  {p:<16} n={len(v):>3}  ρ={rho(v,'cog_sum','overall'):+.3f}  size ρ={rho(v,'lines','overall'):+.3f}")
loo = [rho([r for r in rows if r['proj'] != p], 'cog_sum', 'overall') for p in byp]; out['loo'] = [min(loo), max(loo)]
print(f"leave-one-project-out range, primary on overall: {min(loo):.3f}–{max(loo):.3f}")
sens = [r for r in rows if r['methods'] > 0]; print(f"sensitivity without the {len(rows)-len(sens)} method-less files: ρ={rho(sens,'cog_sum','overall'):.3f}")
pr, lr = rank([r['cog_sum'] for r in rows]), rank([r['overall'] for r in rows])
dis = sorted(range(len(rows)), key=lambda i: -abs(pr[i] - lr[i]))[:10]
print("\n10 largest rank disagreements (primary vs overall badness):")
for i in dis:
    r = rows[i]; print(f"  {r['proj']:<14} {r['id'][:60]:<60} cog_sum={r['cog_sum']:.0f} lines={r['lines']:.0f} overall_badness={r['overall']:.2f}  rank {pr[i]:.0f} vs {lr[i]:.0f}")
out['disagreements'] = [rows[i]['id'] for i in dis]
json.dump(out, open('results.json', 'w'), indent=1)
