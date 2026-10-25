"""E1 step 1 (before labels): every predictor for every labelled file, from the engine probe's methods."""
import csv, json, collections, os
proj = {'aoi': 'aoi', 'argoUML': 'argoUML', 'diarymanagement': 'diarymanagement', 'jsweet': 'Jsweet', 'junit4': 'junit4'}
meth = collections.defaultdict(list)
for p in proj.values():
    for l in open(f'methods/{p}.jsonl'):
        r = json.loads(l); meth[(p, r['path'])].append(r)
w = csv.writer(open('predictions.csv', 'w', newline=''))
w.writerow(['projectname', 'packageandclass', 'file', 'methods', 'cog_sum', 'cog_max', 'over15', 'cyc_sum', 'lines'])
for k in csv.DictReader(open('keys.csv')):
    p = proj[k['projectname']]; rel = '/'.join(k['path'].replace('\\', '/').split('/')[2:])
    ms = meth[(p, rel)]
    lines = sum(1 for l in open(f'src/{p}/sourcefiles/{rel}', errors='replace') if l.strip())
    w.writerow([k['projectname'], k['packageandclass'], rel, len(ms), sum(m['cognitive'] for m in ms),
                max((m['cognitive'] for m in ms), default=0), sum(m['cognitive'] > 15 for m in ms),
                sum(m['cyclomatic'] for m in ms), lines])
