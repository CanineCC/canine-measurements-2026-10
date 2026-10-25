"""WP-40 §E5: total the frozen per-repository verdicts (one *.txt per repository, from verdict.sql)."""
import re, glob, collections, math, random, json
names = {'019e6f15-88f0':'unfold','019e6f15-7c98':'continuum','019f4dd3-45b6':'kennel','019e6f15-9b82':'RETIRED.watchdog','019e6f15-8bc6':'lawnofwar','019f007f-3ab7':'CodeAssuranceIndex'}
V = ('cleared','did_not_clear','absent_not_measured','absent_dimension_unknown','unverified')
tot = collections.Counter(); per = collections.defaultdict(collections.Counter); dims = collections.defaultdict(collections.Counter)
for f in sorted(glob.glob('019*.txt')):
    repo = names[f[:13]]
    for l in open(f):
        m = re.match(r"\s*(\w+)\s*\|\s*(\S*)\s*\|\s*(\d+)\s*\|", l)
        if m and m.group(1) in V:
            v, d, n = m.group(1), m.group(2), int(m.group(3)); tot[v] += n; per[repo][v] += n; dims[d][v] += n
def wilson(k, n, z=1.96):
    p = k/n; c = (p + z*z/(2*n)) / (1 + z*z/n); h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n); return round(100*(c-h),1), round(100*(c+h),1)
k, n = tot['did_not_clear'], tot['did_not_clear'] + tot['cleared']
print('ALL', {v: tot[v] for v in V}, 'total', sum(tot.values()))
print(f'did not clear, share of decided: {k}/{n} = {100*k/n:.1f} %  Wilson {wilson(k,n)}')
reps = [(c['did_not_clear'], c['did_not_clear'] + c['cleared']) for c in per.values() if c['did_not_clear'] + c['cleared']]
rng = random.Random(20261025); bs = sorted(sum(a for a,_ in s)/sum(b for _,b in s) for s in ([rng.choice(reps) for _ in reps] for _ in range(10000)))
print(f'repository-cluster bootstrap ({len(reps)} repositories with decided resolutions): {100*bs[250]:.1f} to {100*bs[9749]:.1f} %')
for r, c in sorted(per.items()):
    d = c['did_not_clear'] + c['cleared']; print(f'  {r:<20}', {v: c[v] for v in V if c[v]}, f'share {100*c["did_not_clear"]/d:.1f} %' if d else '(nothing decided)')
print('did not clear, by dimension:', sorted(((v['did_not_clear'], d) for d, v in dims.items() if v['did_not_clear']), reverse=True)[:10])
json.dump({'total': tot, 'per_repo': per, 'by_dimension': dims}, open('results.json', 'w'), indent=1)
