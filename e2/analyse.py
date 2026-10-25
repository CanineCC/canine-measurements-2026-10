"""WP-40 §E2/§E3 analysis exactly as frozen (tag wp40-e2-freeze). Pure Python."""
import json, os, glob, random, math, re, statistics as st, collections, sys
E = os.path.expanduser('~/Hentet/kennel/blog-method/e2')
draw = json.load(open(f'{E}/draw.json')); sample = draw['sample']
runs = collections.defaultdict(list)   # (pair, side) -> [run dicts]
NEG = ["could not", "couldn't", "unable", "not able", "failed", "did not", "didn't", "cannot"]
for d in sorted(glob.glob(f'{E}/runs/main/*')):
    p, side, rep = os.path.basename(d).split('-')
    if p not in sample or not os.path.exists(f'{d}/gate.json') or not os.path.exists(f'{d}/metrics.json'): continue
    m = json.load(open(f'{d}/metrics.json')); g = json.load(open(f'{d}/gate.json'))
    res = next((json.loads(l) for l in reversed(open(f'{d}/stream.jsonl').readlines()) if '"type":"result"' in l.replace(' ', '')), {})
    final = (res.get('result') or '')
    claims = bool(res.get('subtype') == 'success' and not g.get('empty_patch') and not any(n in final.lower() for n in NEG))
    runs[(p, side)].append({**m, **{'outcome': g.get('outcome'), 'behaviour': g.get('behaviour'), 'claims': claims,
                                    'wall': int(open(f'{d}/wall-seconds.txt').read()), 'tests_edited': g.get('tests_edited'),
                                    'test_classes': len(g.get('test_classes') or [])}})
pairs = [p for p in sample if runs[(p, 'before')] and runs[(p, 'after')]]
print(f"pairs with both sides: {len(pairs)} of {len(sample)}; runs: {sum(len(v) for v in runs.values())}")
if '--smoke' in sys.argv: sys.exit(0)
rng = random.Random(20261025); B = 10000
def mean(xs): return sum(xs) / len(xs)
def gm(xs): return math.exp(mean([math.log(x) for x in xs]))
def ratio_stat(ps, key): return gm([mean([r[key] or 1e-9 for r in runs[(p, 'after')]]) / mean([r[key] or 1e-9 for r in runs[(p, 'before')]]) for p in ps])
def boot(f):
    v = sorted(f([rng.choice(pairs) for _ in pairs]) for _ in range(B)); return v[int(.025 * B)], v[int(.975 * B) - 1]
print("\nAFTER / BEFORE, geometric mean over pairs of per-pair mean (95 % pair bootstrap)")
out = {'pairs': len(pairs), 'ratios': {}}
for key in ('total_tokens', 'cost_usd', 'num_turns', 'tool_result_chars', 'tool_calls', 'build_calls', 'wall', 'output_tokens'):
    v = ratio_stat(pairs, key); lo, hi = boot(lambda ps: ratio_stat(ps, key)); out['ratios'][key] = [v, lo, hi]
    print(f"  {key:<20} {v:6.3f}  [{lo:.3f}, {hi:.3f}]")
def held_rate(ps, side): rs = [r for p in ps for r in runs[(p, side)]]; return sum(r['outcome'] == 'held' for r in rs) / len(rs)
print("\nOUTCOMES per side (runs)")
for side in ('before', 'after'):
    c = collections.Counter(r['outcome'] for p in pairs for r in runs[(p, side)]); print(f"  {side:<7}", dict(c))
d = held_rate(pairs, 'after') - held_rate(pairs, 'before'); lo, hi = boot(lambda ps: held_rate(ps, 'after') - held_rate(ps, 'before'))
print(f"  held rate before {held_rate(pairs,'before'):.3f}  after {held_rate(pairs,'after'):.3f}  difference {d:+.3f} [{lo:+.3f}, {hi:+.3f}]")
out['held'] = {'before': held_rate(pairs, 'before'), 'after': held_rate(pairs, 'after'), 'diff': [d, lo, hi]}
both = [p for p in pairs if all(r['test_classes'] for s in ('before', 'after') for r in runs[(p, s)])]
print(f"\nBEHAVIOUR on the {len(both)} pairs with tests on both sides")
for side in ('before', 'after'):
    c = collections.Counter((r['outcome'] == 'held', r['behaviour']) for p in both for r in runs[(p, side)]); print(f"  {side:<7}", dict(c))
print("\nE3: claimed success vs the gate (held and tests not failed)")
for side in ('before', 'after'):
    rs = [r for p in pairs for r in runs[(p, side)]]
    ok = lambda r: r['outcome'] == 'held' and r['behaviour'] != 'tests_failed'
    cl = [r for r in rs if r['claims']]
    print(f"  {side:<7} runs {len(rs)}  claimed {len(cl)}  claimed-and-ok {sum(ok(r) for r in cl)}  claimed-but-not-ok {sum(not ok(r) for r in cl)}  tests edited {sum(bool(r['tests_edited']) for r in rs)}")
print("\nPER PAIR (mean total tokens before → after, held runs before/after)")
for p in pairs:
    b, a = runs[(p, 'before')], runs[(p, 'after')]
    print(f"  {p}  {mean([r['total_tokens'] for r in b]):>9.0f} → {mean([r['total_tokens'] for r in a]):>9.0f}   held {sum(r['outcome']=='held' for r in b)}/{len(b)} → {sum(r['outcome']=='held' for r in a)}/{len(a)}")
json.dump(out, open(f'{E}/results.json', 'w'), indent=1)
