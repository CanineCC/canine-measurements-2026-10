"""WP-40 §E4b as frozen (tag wp40-e4b-freeze): E4's AI reviewer on every non-empty E6 patch, 3 asks each.

Gate truth: GOOD = E6 gate outcome held with behaviour passed. BAD = did_not_clear, moved, build_failed,
target_missing, or behaviour failed. Anything else (baseline_failing, gate errors, no_change) is excluded and
counted. Outcomes: false approvals (APPROVE asks on bad patches, bootstrap over patches), false rejections
(REJECT asks on good patches), self-consistency, all split by arm.
Usage: python3 -I analyse_e4b.py [asks_dir]   (default asks-e6). Writes results-e4b.json.
"""
import collections, glob, json, os, random, sys

E6 = os.path.expanduser('~/Hentet/kennel/blog-method/e6/runs/main')
ASKS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'asks-e6')
BAD_OUTCOMES = {'did_not_clear', 'moved', 'build_failed', 'target_missing'}


def truth(gate):
    if gate.get('outcome') == 'held' and gate.get('behaviour') == 'passed':
        return 'good'
    if gate.get('outcome') in BAD_OUTCOMES or gate.get('behaviour') == 'failed':
        return 'bad'
    return None


def rate_ci(rows, vote, rng):
    if not rows:
        return None
    draws = sorted(sum(v == vote for r in s for v in r['votes']) / sum(len(r['votes']) for r in s)
                   for s in ([rng.choice(rows) for _ in rows] for _ in range(10000)))
    return [draws[250], draws[9749]]


asks = collections.defaultdict(list)
for f in glob.glob(f'{ASKS}/*.json'):
    a = json.load(open(f))
    asks[a['run']].append(a['verdict'])

rows, excluded = [], collections.Counter()
for run, votes in sorted(asks.items()):
    gate_path = f'{E6}/{run}/gate.json'
    if not os.path.exists(gate_path):
        excluded['no gate.json'] += 1
        continue
    gate = json.load(open(gate_path))
    t = truth(gate)
    if t is None:
        excluded[f"{gate.get('outcome')}/{gate.get('behaviour')}"] += 1
        continue
    rows.append({'run': run, 'arm': run.split('-')[1], 'truth': t, 'outcome': gate['outcome'], 'votes': votes})

result = {'patches': len(rows), 'excluded': dict(excluded), 'by_arm': {}}
for arm in ('all', 'G', 'U'):
    sel = [r for r in rows if arm == 'all' or r['arm'] == arm]
    good = [r for r in sel if r['truth'] == 'good']
    bad = [r for r in sel if r['truth'] == 'bad']
    rng = random.Random(20261025)
    result['by_arm'][arm] = {
        'good': len(good), 'bad': len(bad),
        'false_approvals': sum(v == 'APPROVE' for r in bad for v in r['votes']),
        'asks_on_bad': sum(len(r['votes']) for r in bad),
        'false_approval_ci95': rate_ci(bad, 'APPROVE', rng),
        'false_rejections': sum(v == 'REJECT' for r in good for v in r['votes']),
        'asks_on_good': sum(len(r['votes']) for r in good),
        'false_rejection_ci95': rate_ci(good, 'REJECT', rng),
        'self_consistent': sum(len(set(r['votes'])) == 1 for r in sel),
        'bad_approved_by_majority': [r['run'] for r in bad if sum(v == 'APPROVE' for v in r['votes']) * 2 > len(r['votes'])],
    }
json.dump({'summary': result, 'rows': rows}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results-e4b.json'), 'w'), indent=1)
print(json.dumps(result, indent=1))
