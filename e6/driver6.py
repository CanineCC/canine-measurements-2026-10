"""Run the frozen E6 draw: one agent lane per arm in draw order, ONE gate queue (both arms gate in the same lane).
Resumable: a run with metrics.json is not re-run; one with gate.json is not re-gated."""
import json, os, subprocess, threading, time
E6 = os.path.expanduser('~/Hentet/kennel/blog-method/e6'); order = json.load(open(f'{E6}/draw.json'))['order']
out = lambda m, a, r: f'{E6}/runs/main/{m}-{a}-{r}'; done = {'U': False, 'G': False}
def runner(arm):
    for m, a, r in order:
        if a != arm or os.path.exists(f'{out(m,a,r)}/metrics.json'): continue
        subprocess.run([f'{E6}/run_one6.sh', a, m, str(r), out(m, a, r)])
        subprocess.run(['python3', '-I', f'{E6}/extract.py', out(m, a, r)], capture_output=True)
        print(time.strftime('%H:%M:%S'), 'ran', m, a, r, flush=True)
    done[arm] = True
def gater():
    while True:
        pend = [(m, a, r) for m, a, r in order if os.path.exists(f'{out(m,a,r)}/metrics.json') and not os.path.exists(f'{out(m,a,r)}/gate.json')]
        if not pend:
            if all(done.values()): return
            time.sleep(20); continue
        m, a, r = pend[0]
        g = subprocess.run(['python3', '-I', f'{E6}/gate6.py', 'run', m, out(m, a, r)], capture_output=True, text=True)
        print(time.strftime('%H:%M:%S'), 'gated', m, a, r, g.stdout.strip() or g.stderr[-300:], flush=True)
        if not os.path.exists(f'{out(m,a,r)}/gate.json'):
            open(f'{out(m,a,r)}/gate-error.txt', 'w').write(g.stderr); open(f'{out(m,a,r)}/gate.json', 'w').write('{"outcome":"gate_error"}')
ts = [threading.Thread(target=runner, args=(a,)) for a in ('U', 'G')] + [threading.Thread(target=gater)]
[t.start() for t in ts]; [t.join() for t in ts]; print('ALL DONE', flush=True)
