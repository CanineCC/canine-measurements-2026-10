import json, sys, collections, re
def load(n):
    rows=[json.loads(l) for l in open(f'methods-{n}.jsonl')]
    prod=[r for r in rows if re.match(r'^(src|engine/src)/', r['path']) and not re.search(r'(?i)(/tests?/|\.tests?[./]|fixture|testdata|/obj/)', r['path'])]
    return prod
b,a=load('before'),load('after')
T=15
hb=[r for r in b if r['cognitive']>T]; ha=[r for r in a if r['cognitive']>T]
print('production methods before/after', len(b), len(a), ' over threshold', len(hb), len(ha))
ia=collections.defaultdict(list)
for r in ha: ia[(r['method'],r['bodyHash'])].append(r)
pairs=[(r,ia[(r['method'],r['bodyHash'])][0]) for r in hb if len(ia[(r['method'],r['bodyHash'])])==1]
print('identical-body pairs over threshold (unique in after):', len(pairs))
def area(p):
    m=re.match(r'^(src/[^/]+|engine/src/[^/]+(/[^/]+)?)', p); return m.group(1) if m else p
c=collections.Counter(area(x['path'])+'  ->  '+area(y['path']) for x,y in pairs)
for k,v in c.most_common(25): print(v,k)
moved=sum(1 for x,y in pairs if x['path']!=y['path']); print('pairs whose file path changed:', moved)
json.dump([{'before':x,'after':y} for x,y in pairs], open('pairs.json','w'), indent=1)
