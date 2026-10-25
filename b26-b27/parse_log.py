import re, sys, csv
out = csv.writer(open(sys.argv[2], 'w', newline=''))
out.writerow(['run','lang','arm','date','repo','n','noise','noise_in_scope','n_in_scope'])
for line in open(sys.argv[1], encoding='utf-8', errors='replace'):
    line = re.sub(r'\x1b\[[0-9;]*m', '', line)
    m = re.search(r'Z\s+([0-9a-f-]{36})\s*\|(.*)$', line)
    if not m: continue
    cells = [c.strip() for c in m.group(2).split('|')]
    if len(cells) != 8: continue
    out.writerow([m.group(1)] + cells)
