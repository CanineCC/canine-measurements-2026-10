"""Run the frozen E2 draw: per side, one agent lane in draw order and one gate queue behind it. Resumable: a run with
metrics.json is not re-run, a run with gate.json is not re-gated."""
import json, os, subprocess, threading, time, sys
E = os.path.expanduser('~/Hentet/kennel/blog-method/e2')
order = json.load(open(f'{E}/draw.json'))['order']
def outdir(p, s, r): return f'{E}/runs/main/{p}-{s}-{r}'
done = {s: False for s in ('before', 'after')}
def runner(side):
    for p, s, r in order:
        if s != side: continue
        o = outdir(p, s, r)
        if os.path.exists(f'{o}/metrics.json'): continue
        subprocess.run([f'{E}/run_one.sh', s, p, str(r), f'{E}/lanes/{s}-1', o])
        subprocess.run(['python3', '-I', f'{E}/extract.py', o], capture_output=True)
        print(time.strftime('%H:%M:%S'), 'ran', p, s, r, flush=True)
    done[side] = True
def gater(side):
    while 'done' not in open(f'{E}/gate-warm.log').read(): time.sleep(30)   # never build a lane twice at once
    while True:
        pending = [(p, s, r) for p, s, r in order if s == side and os.path.exists(f'{outdir(p,s,r)}/metrics.json')
                   and not os.path.exists(f'{outdir(p,s,r)}/gate.json')]
        if not pending:
            if done[side]: return
            time.sleep(20); continue
        p, s, r = pending[0]
        g = subprocess.run(['python3', '-I', f'{E}/gate.py', s, p, outdir(p, s, r)], capture_output=True, text=True)
        print(time.strftime('%H:%M:%S'), 'gated', p, s, r, (g.stdout.strip() or g.stderr[-300:]), flush=True)
        if g.returncode != 0: open(f'{outdir(p,s,r)}/gate-error.txt', 'w').write(g.stderr)
        if not os.path.exists(f'{outdir(p,s,r)}/gate.json'): open(f'{outdir(p,s,r)}/gate.json', 'w').write('{"outcome":"gate_error"}')
ts = [threading.Thread(target=f, args=(s,)) for s in ('before', 'after') for f in (runner, gater)]
[t.start() for t in ts]; [t.join() for t in ts]; print('ALL DONE', flush=True)
