"""B27: what a findings cap does to per-language noise rates, and the leave-one-repository-out span (B26)."""
import csv, collections, sys
rows = list(csv.DictReader(open(sys.argv[1])))
for r in rows:
    for k in ('n','noise'): r[k] = int(r[k])
print('total findings', sum(r['n'] for r in rows), ' noise', sum(r['noise'] for r in rows), ' repos', len(rows))
by = collections.defaultdict(list)
for r in rows: by[r['lang']].append(r)
rate = lambda rs: 100 * sum(r['noise'] for r in rs) / max(1, sum(r['n'] for r in rs))
lo, hi = int(sys.argv[2]), int(sys.argv[3])
print(f"\n{'lang':<11}{'repos':>6}{'pooled':>9}{'capped':>9}{'Δ':>7}{'kept':>6}   {'macro':>7}  leave-one-out span")
for lang in sorted(by):
    rs = by[lang]; capped = [r for r in rs if lo <= r['n'] <= hi]
    loo = [rate([x for x in rs if x is not r]) for r in rs]
    macro = sum(100*r['noise']/r['n'] for r in rs) / len(rs)
    print(f"{lang:<11}{len(rs):>6}{rate(rs):>8.1f}%{rate(capped):>8.1f}%{rate(capped)-rate(rs):>+7.1f}{len(capped):>6}   {macro:>6.1f}%  {min(loo):.1f}–{max(loo):.1f} %")
