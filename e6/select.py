"""WP-40 §E6 draw, as frozen: production methods with cognitive >= 25 in the AFTER snapshot whose declaring type has a
unit-test class named <Type>...Tests; 20 drawn with random.Random(20261025), pilot 2 others."""
import json, re, os, random, collections
SNAP = os.path.expanduser('~/Hentet/kennel/blog-method/e2/snap-after')
rows = [json.loads(l) for l in open(os.path.expanduser('~/Hentet/kennel/blog-method/e2/methods-after.jsonl'))]
prod = [r for r in rows if re.match(r'^(src|engine/src)/', r['path']) and not re.search(r'(?i)(/tests?/|\.tests?[./]|fixture|testdata|/obj/)', r['path']) and r['cognitive'] >= 25]
tests = collections.defaultdict(list)   # test class name -> files
for base in ('tests', 'engine/tests'):
    for dp, dn, fn in os.walk(os.path.join(SNAP, base)):
        dn[:] = [d for d in dn if d not in ('bin', 'obj')]
        for f in fn:
            if f.endswith('.cs'):
                for c in re.findall(r'\bclass\s+(\w+Tests?)\b', open(os.path.join(dp, f), errors='replace').read()):
                    tests[c].append(os.path.relpath(os.path.join(dp, f), SNAP))
def classes_for(t): return sorted(c for c in tests if re.match(r'^' + re.escape(t) + r'\w*Tests?$', c))
cands = []
seen = set()
for r in sorted(prod, key=lambda r: (r['path'], r['line'])):
    t = r['method'].split('.')[0]; cl = classes_for(t)
    key = (r['path'], r['method'])
    if cl and key not in seen:
        seen.add(key); cands.append({**r, 'type': t, 'testClasses': cl, 'testFiles': sorted({f for c in cl for f in tests[c]})})
rng = random.Random(20261025)
ids = [f'm{i:03d}' for i in range(len(cands))]
for i, c in zip(ids, cands): c['id'] = i
sample = sorted(rng.sample(ids, 20)); rest = [i for i in ids if i not in sample]; pilot = rng.sample(rest, 2)
runs = [(m, arm, rep) for m in sample for arm in ('U', 'G') for rep in (1, 2, 3)]; rng.shuffle(runs)
json.dump(cands, open('candidates.json', 'w'), indent=1)
json.dump({'seed': 20261025, 'sample': sample, 'pilot': pilot, 'order': runs}, open('draw.json', 'w'), indent=1)
print(len(prod), 'methods >= 25;', len(cands), 'with a <Type>...Tests class; sample', len(sample))
by = {c['id']: c for c in cands}
for i in sample: c = by[i]; print(i, c['cognitive'], c['method'][:55], c['path'].split('/')[1], len(c['testClasses']), 'test classes')
