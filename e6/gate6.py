"""WP-40 §E6 gate (deterministic): build, the engine's complexity walk, and the <Type>...Tests unit-test classes with a
baseline on the unchanged code; a test failure counts only if it fails twice and the baseline passes. No model asked."""
import json, os, re, subprocess, sys
mode = sys.argv[1]   # 'baseline' <mid>  |  'run' <mid> <outdir>
E = os.path.expanduser('~/Hentet/kennel/blog-method'); E6 = f'{E}/e6'; lane = f'{E}/e2/lanes/gate-after'
PROBE = f'{E}/tools/complexity-probe/bin/Release/net10.0/ComplexityProbe'; BL = '<checkout>/tools/build-lock.sh'
c = {x['id']: x for x in json.load(open(f'{E6}/candidates.json'))}[sys.argv[2]]
env = dict(os.environ, DOTNET_ROOT='<home>/.dotnet-microsoft')
sh = lambda cmd: subprocess.run(cmd, cwd=lane, capture_output=True, text=True, env=env)
units = [t for t in c['testProjects'] if 'Integration' not in t]
flt = '|'.join(f'FullyQualifiedName~.{k}' for k in c['testClasses'])
def tests():
    res = []
    for t in units:
        r = sh(['timeout', '3600', BL, '--', 'dotnet', 'test', t, '--filter', flt, '-v', 'q', '-nologo'])
        txt = r.stdout + r.stderr; num = lambda k: sum(int(x) for x in re.findall(k + r':\s+(\d+)', txt))
        res.append({'project': t, 'exit': r.returncode, 'passed': num('Passed'), 'failed': num('Failed'), 'total': num('Total'),
                    'failedNames': re.findall(r'^\s+Failed (\S+)', txt, re.M)[:10]})
    return res
ok = lambda ts: all(t['exit'] == 0 and t['failed'] == 0 and t['total'] > 0 for t in ts)
def clean(): sh(['git', 'reset', '-q', '--hard']); sh(['git', 'clean', '-qfd'])
def probe(files):
    files = sorted({f for f in files if f.endswith('.cs') and os.path.exists(os.path.join(lane, f))})
    if not files: return {}
    o = f'{E6}/probe.tmp'; r = sh([PROBE, lane, o] + files)
    if r.returncode: raise SystemExit('probe failed: ' + r.stderr[-800:])
    return {(x['path'], x['method']): x['cognitive'] for x in map(json.loads, open(o))}
if mode == 'baseline':
    clean(); b = sh(['timeout', '2400', BL, '--', 'dotnet', 'build', c['csproj'], '-v', 'q', '-nologo'])
    ts = tests(); rec = {'build_ok': b.returncode == 0, 'tests': ts, 'tests_ok': ok(ts)}
    os.makedirs(f'{E6}/baseline', exist_ok=True); json.dump(rec, open(f'{E6}/baseline/{c["id"]}.json', 'w'), indent=1)
    print(c['id'], 'baseline', rec['build_ok'], rec['tests_ok'], [(t['passed'], t['failed']) for t in ts]); sys.exit(0)
out = os.path.abspath(sys.argv[3]); patch = open(f'{out}/patch.diff').read()
touched = sorted(set(re.findall(r'^\+\+\+ b/(.+)$', patch, re.M)) | set(re.findall(r'^--- a/(.+)$', patch, re.M)))
g = {'mid': c['id'], 'touched': touched, 'empty_patch': not patch.strip(), 'tests_edited': any(re.search(r'(^|/)tests?/|\.Tests?[./]', t) for t in touched)}
clean(); before = probe(touched + [c['path']])
ap = sh(['git', 'apply', '--whitespace=nowarn', f'{out}/patch.diff']) if patch.strip() else None
g['patch_applies'] = ap is None or ap.returncode == 0
after = probe(touched + [c['path']]) if g['patch_applies'] else {}
tgt = after.get((c['path'], c['method'])); g['target_cognitive_after'] = tgt
g['newly_over_threshold'] = [f'{k[0]}::{k[1]}={v}' for k, v in after.items() if v > 15 and k != (c['path'], c['method']) and before.get(k, 0) < v]
g['touched_total_cognitive_before'] = sum(before.values()); g['touched_total_cognitive_after'] = sum(after.values())
b = sh(['timeout', '2400', BL, '--', 'dotnet', 'build', c['csproj'], '-v', 'q', '-nologo']) if g['patch_applies'] else None
g['build_ok'] = bool(b and b.returncode == 0); g['build_errors'] = re.findall(r'error [A-Z]+\d+[^\n]*', (b.stdout + b.stderr) if b else '')[:8]
base = json.load(open(f'{E6}/baseline/{c["id"]}.json'))
if g['build_ok']:
    t1 = tests(); g['tests_first'] = t1
    if ok(t1): g['behaviour'] = 'passed'
    else:
        t2 = tests(); g['tests_second'] = t2
        g['behaviour'] = 'passed' if ok(t2) else ('failed' if base['tests_ok'] else 'baseline_failing')
else: g['behaviour'] = None
clean()
g['outcome'] = ('no_change' if g['empty_patch'] else 'patch_does_not_apply' if not g['patch_applies'] else 'build_failed' if not g['build_ok']
                else 'target_missing' if tgt is None else 'did_not_clear' if tgt > 15 else 'moved' if g['newly_over_threshold'] else 'held')
json.dump(g, open(f'{out}/gate.json', 'w'), indent=1); print(json.dumps({k: g[k] for k in ('outcome', 'behaviour', 'target_cognitive_after')}))
