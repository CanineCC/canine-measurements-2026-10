"""WP-40 §E4 as frozen: AI reviewer vs the deterministic gate, on the E2 patches, 3 asks each."""
import json, glob, os, collections, random
E2 = os.path.expanduser('~/Hentet/kennel/blog-method/e2')
asks = collections.defaultdict(list)
for f in glob.glob('asks/*.json'):
    a = json.load(open(f)); asks[a['run']].append(a['verdict'])
rows = []
for run, vs in sorted(asks.items()):
    g = json.load(open(f'{E2}/runs/main/{run}/gate.json'))
    good = g['outcome'] == 'held' and g['behaviour'] in ('tests_passed', 'untested')
    rows.append({'run': run, 'good': good, 'votes': vs})
n = len(rows); allv = [v for r in rows for v in r['votes']]
print(f'patches {n}, asks {len(allv)}:', dict(collections.Counter(allv)))
good = [r for r in rows if r['good']]; bad = [r for r in rows if not r['good']]
fa = sum(v == 'APPROVE' for r in bad for v in r['votes']); fr = sum(v == 'REJECT' for r in good for v in r['votes'])
print(f'gate-good patches {len(good)}, gate-not-good {len(bad)} (frozen rule: anything but held with tests passed or untested)')
print(f'false approvals: {fa} of {3*len(bad)} asks on not-good patches; false rejections: {fr} of {3*len(good)} asks on good patches ({100*fr/(3*len(good)):.1f} %)')
cons = sum(len(set(r['votes'])) == 1 for r in rows); print(f'self-consistent (3 of 3 agree): {cons} of {n} patches ({100*cons/n:.1f} %)')
rng = random.Random(20261025)
bs = sorted(sum(v == 'REJECT' for r in s for v in r['votes']) / (3 * len(s)) for s in ([rng.choice(good) for _ in good] for _ in range(10000)))
print(f'false-rejection rate 95 % bootstrap over patches: {100*bs[250]:.1f} to {100*bs[9749]:.1f} %')
split = [r['run'] for r in rows if len(set(r['votes'])) > 1]; print('patches with split verdicts:', len(split), split[:8])
json.dump(rows, open('results.json', 'w'), indent=1)
