"""WP-40 §E4c (E4b with a stronger reviewer model): an AI reviewer, given the finding and the diff, approves or rejects each E2 patch; 3 independent asks.
No tools, no repository, no session memory. The gate's outcome is NOT shown to the reviewer."""
import json, os, re, subprocess, sys, glob
E2 = os.path.expanduser('~/Hentet/kennel/blog-method/e6'); OUT = os.path.expanduser('~/Hentet/kennel/blog-method/e4/asks-e4c')
os.makedirs(OUT, exist_ok=True)
cands = {c['id']: c for c in json.load(open(f'{E2}/candidates.json'))}
PROMPT = """You are reviewing a patch before it is merged.

The finding it is meant to fix: `{method}` in `{path}` had a cognitive complexity of {cognitive}; the threshold is 15.
The author was asked to refactor the method to a cognitive complexity of 15 or lower, without changing its behaviour,
keeping the project building (warnings are errors), without editing tests.

The diff:

```diff
{diff}
```

Does this patch meet all three conditions: the method is now at or below the threshold, behaviour is unchanged, and
the project still builds? Answer with exactly one word on the first line, APPROVE or REJECT, then one sentence of reason."""
def ask(run, k):
    o = f'{OUT}/{os.path.basename(run)}-{k}.json'
    if os.path.exists(o): return
    mid = os.path.basename(run).split('-')[0]
    m = cands[mid]; diff = open(f'{run}/patch.diff').read()
    if not diff.strip(): return
    prompt = PROMPT.format(method=m['method'], path=m['path'], cognitive=m['cognitive'], diff=diff[:60000])
    try:
      r = subprocess.run(['bwrap', '--dev-bind', '/', '/', '--tmpfs', os.path.expanduser('~/RiderProjects'), '--tmpfs', os.path.expanduser('~/Hentet'),
                        '--tmpfs', os.path.expanduser('~/.claude/projects'), '--chdir', '/tmp', '--die-with-parent', '--',
                        'claude', '-p', prompt, '--model', 'claude-opus-5-5', '--output-format', 'json', '--tools', '',
                        '--setting-sources', 'local', '--strict-mcp-config', '--no-session-persistence'],
                       capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
      json.dump({'run': os.path.basename(run), 'k': k, 'verdict': 'TIMEOUT', 'text': '', 'cost_usd': None, 'usage': None}, open(o, 'w'), indent=1)
      print(os.path.basename(run), k, 'TIMEOUT', flush=True); return
    try: res = json.loads(r.stdout)
    except Exception: res = {'error': r.stdout[-500:] + r.stderr[-500:]}
    text = (res.get('result') or '').strip()
    first = text.split('\n', 1)[0].strip().upper()
    verdict = 'APPROVE' if first.startswith('APPROVE') else 'REJECT' if first.startswith('REJECT') else 'UNPARSEABLE'
    json.dump({'run': os.path.basename(run), 'k': k, 'verdict': verdict, 'text': text, 'cost_usd': res.get('total_cost_usd'), 'usage': res.get('usage')}, open(o, 'w'), indent=1)
    print(os.path.basename(run), k, verdict, flush=True)
runs = sorted(glob.glob(f'{E2}/runs/main/*'))
for run in runs:
    if not os.path.exists(f'{run}/gate.json'): continue
    for k in (1, 2, 3): ask(run, k)
