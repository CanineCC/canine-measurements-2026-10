"""The deterministic gate for one run: does the build pass, did the engine's own complexity walk clear the method
without moving the problem, and do the tests that exercise the type still pass. No model is asked anything."""
import json, os, re, subprocess, sys
side, pid, out = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3])
E = os.path.expanduser('~/Hentet/kennel/blog-method/e2'); lane = f'{E}/lanes/gate-{side}'
PROBE = os.path.expanduser('~/Hentet/kennel/blog-method/tools/complexity-probe/bin/Release/net10.0/ComplexityProbe')
BL = '<checkout>/tools/build-lock.sh'
m = {p['id']: p for p in json.load(open(f'{E}/pairs.json'))}[pid][side]
env = dict(os.environ, DOTNET_ROOT='<home>/.dotnet-microsoft')
sh = lambda cmd, **k: subprocess.run(cmd, cwd=lane, capture_output=True, text=True, env=env, **k)
def probe(files):
    files = sorted({f for f in files if f.endswith('.cs') and os.path.exists(os.path.join(lane, f))})
    if not files: return []
    r = sh([PROBE, lane, f'{out}/probe.tmp'] + files)
    if r.returncode != 0: raise SystemExit(f'probe failed {r.returncode}: {r.stderr[-1500:]}')
    return [json.loads(l) for l in open(f'{out}/probe.tmp')]
patch = open(f'{out}/patch.diff').read()
touched = sorted(set(re.findall(r'^\+\+\+ b/(.+)$', patch, re.M)) | set(re.findall(r'^--- a/(.+)$', patch, re.M)))
g = {'side': side, 'pair': pid, 'touched': touched, 'empty_patch': not patch.strip(),
     'tests_edited': any(re.search(r'(^|/)tests?/|\.Tests?[./]', t) for t in touched)}
sh(['git', 'reset', '-q', '--hard']); sh(['git', 'clean', '-qfd'])
before = {(r['path'], r['method']): r['cognitive'] for r in probe(touched + [m['path']])}
ap = sh(['git', 'apply', '--whitespace=nowarn', f'{out}/patch.diff']) if patch.strip() else None
g['patch_applies'] = ap is None or ap.returncode == 0
after_rows = probe(touched + [m['path']]) if g['patch_applies'] else []
after = {(r['path'], r['method']): r['cognitive'] for r in after_rows}
T = 15
tgt = after.get((m['path'], m['method']))
g['target_cognitive_after'] = tgt
g['target_present'] = tgt is not None
newly_over = [f'{k[0]}::{k[1]}={v}' for k, v in after.items() if v > T and k != (m['path'], m['method']) and before.get(k, 0) < v]
g['newly_over_threshold'] = newly_over
g['max_cognitive_in_touched_files_after'] = max(after.values(), default=None)
b = sh(['timeout', '2400', BL, '--', 'dotnet', 'build', m['csproj'], '-v', 'q', '-nologo']) if g['patch_applies'] else None
g['build_ok'] = bool(b and b.returncode == 0)
g['build_errors'] = (re.findall(r'error [A-Z]+\d+[^\n]*', (b.stdout + b.stderr)) if b else [])[:10]
# tests: every test class declared in a unit-test file that names the type
classes = set()
for dp, dn, fn in os.walk(f'{lane}/engine/tests/CodeHealth.Tests.Unit'):
    dn[:] = [x for x in dn if x not in ('bin', 'obj')]
    for f in fn:
        if f.endswith('.cs'):
            s = open(os.path.join(dp, f), errors='replace').read()
            if re.search(r'\b' + re.escape(m['type']) + r'\b', s): classes |= set(re.findall(r'\bclass\s+(\w+)', s))
g['test_classes'] = sorted(classes)
def run_tests():
    if not classes: return None
    flt = '|'.join(f'FullyQualifiedName~.{c}' for c in sorted(classes))
    t = sh(['timeout', '3600', BL, '--', 'dotnet', 'test', 'engine/tests/CodeHealth.Tests.Unit', '--filter', flt, '-v', 'q', '-nologo'])
    txt = t.stdout + t.stderr
    num = lambda k: sum(int(x) for x in re.findall(k + r':\s+(\d+)', txt))
    return {'exit': t.returncode, 'passed': num('Passed'), 'failed': num('Failed'), 'total': num('Total'), 'tail': txt[-1500:]}
g['tests'] = run_tests() if g['build_ok'] else None
sh(['git', 'reset', '-q', '--hard']); sh(['git', 'clean', '-qfd'])
cleared = g['build_ok'] and tgt is not None and tgt <= T
g['outcome'] = ('no_change' if g['empty_patch'] else 'patch_does_not_apply' if not g['patch_applies'] else
                'build_failed' if not g['build_ok'] else
                'target_missing' if tgt is None else
                'did_not_clear' if tgt > T else 'moved' if newly_over else 'held')
t = g['tests']
g['behaviour'] = ('untested' if t is None else 'tests_failed' if t['failed'] > 0 or t['exit'] != 0 else 'tests_passed')
json.dump(g, open(f'{out}/gate.json', 'w'), indent=1); print(json.dumps({k: g[k] for k in ('outcome', 'behaviour', 'target_cognitive_after', 'newly_over_threshold')}))
