"""B26: how concentrated is a cycle's noise in a few repositories? Reads the cycle-1 noise export (one row per
adjudicated noise finding), de-duplicates the two '(1)' download copies, and prints the figures the post uses."""
import csv, glob, collections, sys, os
d = sys.argv[1]
files = sorted(f for f in glob.glob(os.path.join(d, '*.csv')) if '(1)' not in f) + sys.argv[2:]
rows = [r for f in files for r in csv.DictReader(open(f, newline=''))]
repos = collections.Counter(r['repo'] for r in rows)
print(f"rows {len(rows)}  repositories {len(repos)}  languages {len({r['language'] for r in rows})}")
top = repos.most_common(10); s = sum(v for _, v in top)
print(f"top 10 repositories carry {s} of {len(rows)} rows = {100*s/len(rows):.1f} %")
for k in (1, 3, 5, 20):
    t = sum(v for _, v in repos.most_common(k)); print(f"  top {k:>2}: {100*t/len(rows):.1f} %")
# share of repositories needed to reach half the rows
acc = 0
for i, (_, v) in enumerate(repos.most_common(), 1):
    acc += v
    if acc >= len(rows) / 2: print(f"half the rows come from {i} of {len(repos)} repositories ({100*i/len(repos):.1f} %)"); break
# two rankings of (dimension, kind): by rows, and by repositories hit
kind = lambda r: (r['dimension'], r['title'])
by_rows = collections.Counter(kind(r) for r in rows)
reach = collections.defaultdict(set); langs = collections.defaultdict(set)
for r in rows: reach[kind(r)].add(r['repo']); langs[kind(r)].add(r['language'])
print("\nTOP 5 KINDS BY ROWS (rows, repos hit, share of its rows from its single largest repo)")
for k, v in by_rows.most_common(5):
    big = collections.Counter(r['repo'] for r in rows if kind(r) == k).most_common(1)[0][1]
    print(f"  {v:>5} rows  {len(reach[k]):>3} repos  {100*big/v:5.1f} %  {k[0]} · {k[1][:70]}")
print("\nTOP 5 KINDS BY REPOSITORIES HIT (repos, languages, rows)")
for k in sorted(reach, key=lambda k: (-len(reach[k]), -by_rows[k]))[:5]:
    print(f"  {len(reach[k]):>3} repos  {len(langs[k]):>2} langs  {by_rows[k]:>5} rows  {k[0]} · {k[1][:70]}")
dims = collections.Counter(r['dimension'] for r in rows)
print("\nTOP 5 DIMENSIONS BY ROWS, with their largest single repository's share")
for dm, v in dims.most_common(5):
    rc = collections.Counter(r['repo'] for r in rows if r['dimension'] == dm)
    print(f"  {dm:>5} {v:>5} rows  {len(rc):>3} repos  largest repo {100*rc.most_common(1)[0][1]/v:5.1f} %")
