"""Pre-registered draw: 20 of the 46 identical-body pairs, seed 20261025; the pilot is 2 pairs from the remainder
(discarded). The run order interleaves sides and repeats so neither side runs at a quieter hour of the box."""
import json, random
pairs = [p['id'] for p in json.load(open('pairs.json'))]
rng = random.Random(20261025)
sample = sorted(rng.sample(pairs, 20))
rest = [p for p in pairs if p not in sample]
pilot = rng.sample(rest, 2)
runs = [(p, side, rep) for p in sample for side in ('before', 'after') for rep in (1, 2, 3)]
rng.shuffle(runs)
json.dump({'seed': 20261025, 'sample': sample, 'pilot': pilot, 'order': runs}, open('draw.json', 'w'), indent=1)
print('sample', sample); print('pilot', pilot); print(len(runs), 'runs')
