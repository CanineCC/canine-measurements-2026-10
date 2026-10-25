"""B2: the five-class split of cycle 1's adjudicated noise, by rows and by repositories reached (B26: rows measure the
draw). Reads the cycle-1 noise export, the 16 language files plus elixir's, '(1)' download copies removed."""
import csv, glob, collections, os, random
d = os.path.expanduser('~/Hentet/kennel/human - noise, cycle0')
files = sorted(f for f in glob.glob(d + '/*.csv') if '(1)' not in f) + [os.path.expanduser('~/Hentet/noise-elixir-cycle1-noise.csv')]
rows = [r for f in files for r in csv.DictReader(open(f, newline=''))]
repos = sorted({r['repo'] for r in rows})
print(f'files {len(files)} rows {len(rows)} repositories {len(repos)} languages {len({r["language"] for r in rows})}')
by_class = collections.Counter(r['verdict'] for r in rows)
reach = {c: len({r['repo'] for r in rows if r['verdict'] == c}) for c in by_class}
per_repo = collections.defaultdict(collections.Counter)
for r in rows: per_repo[r['repo']][r['verdict']] += 1
rng = random.Random(20261025)
def share(sample, c):
    tot = sum(sum(per_repo[x].values()) for x in sample); return sum(per_repo[x][c] for x in sample) / tot
for c, n in by_class.most_common():
    bs = sorted(share([rng.choice(repos) for _ in repos], c) for _ in range(5000))
    loo = [share([x for x in repos if x != y], c) for y in repos]
    print(f'{c:16s} rows {n:5d} = {100*n/len(rows):5.1f} %  [repo-bootstrap {100*bs[125]:.1f} to {100*bs[4874]:.1f}]  '
          f'leave-one-out {100*min(loo):.1f} to {100*max(loo):.1f}  repositories {reach[c]} of {len(repos)}')
adv = collections.Counter((r['verdict'], r['advisory']) for r in rows)
print('scored vs advisory:', dict(adv))
