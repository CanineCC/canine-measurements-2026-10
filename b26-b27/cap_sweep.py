"""B27: every plausible findings cap gives a different league table. Sweep (lower, upper) caps and report, per
language, the range of rates and of ranks it can be given, and how many distinct orderings the sweep produces."""
import csv, collections, sys, itertools
rows = list(csv.DictReader(open(sys.argv[1])))
for r in rows: r['n'] = int(r['n']); r['noise'] = int(r['noise'])
by = collections.defaultdict(list)
for r in rows: by[r['lang']].append(r)
langs = sorted(by)
lows, highs = [0, 10, 25, 50, 100], [100, 250, 500, 1000, 10**9]
rate = lambda rs: 100 * sum(r['noise'] for r in rs) / sum(r['n'] for r in rs)
orders, per = set(), collections.defaultdict(list)
cells = 0
for lo, hi in itertools.product(lows, highs):
    if lo >= hi: continue
    rates = {}
    for l in langs:
        rs = [r for r in by[l] if lo <= r['n'] <= hi]
        if len(rs) >= 3: rates[l] = rate(rs)          # a language with < 3 repos left is not rated
    if len(rates) < len(langs): continue
    cells += 1
    ranked = sorted(rates, key=rates.get)
    orders.add(tuple(ranked))
    for i, l in enumerate(ranked): per[l].append((rates[l], i + 1))
print(f"{cells} cap choices that leave every language >= 3 repositories; {len(orders)} distinct orderings of {len(langs)} languages")
print(f"{'lang':<11}{'rate min':>9}{'rate max':>9}{'rank best':>10}{'rank worst':>11}   (rank 1 = quietest)")
for l in langs:
    rs = per[l]
    print(f"{l:<11}{min(x for x,_ in rs):>8.1f}%{max(x for x,_ in rs):>8.1f}%{min(k for _,k in rs):>10}{max(k for _,k in rs):>11}")
