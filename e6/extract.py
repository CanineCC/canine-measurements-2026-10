"""Metrics from one run's stream-json transcript: tokens, cost, turns, and what the agent had to read."""
import json, sys
out = sys.argv[1]
ev = [json.loads(l) for l in open(f'{out}/stream.jsonl') if l.strip().startswith('{')]
results = [e for e in ev if e.get('type') == 'result']
# A session that waits on background work emits one result per segment: usage is per segment, cost is cumulative.
res = results[-1] if results else {}
u = {k: sum((r.get('usage') or {}).get(k) or 0 for r in results) for k in ('input_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens', 'output_tokens')}
tools, reads, result_chars = [], set(), 0
for e in ev:
    msg = e.get('message', {})
    for c in msg.get('content', []) if isinstance(msg.get('content'), list) else []:
        if c.get('type') == 'tool_use':
            tools.append((c.get('name'), c.get('input', {})))
            if c.get('name') == 'Read': reads.add(c['input'].get('file_path'))
        if c.get('type') == 'tool_result':
            cc = c.get('content'); result_chars += len(cc if isinstance(cc, str) else json.dumps(cc))
bash = [t[1].get('command', '') for t in tools if t[0] == 'Bash']
m = {
    'subtype': res.get('subtype'), 'is_error': res.get('is_error'), 'num_turns': sum(r.get('num_turns') or 0 for r in results), 'result_segments': len(results),
    'duration_ms': sum(r.get('duration_ms') or 0 for r in results), 'cost_usd': res.get('total_cost_usd'),
    'input_tokens': u.get('input_tokens'), 'cache_creation_input_tokens': u.get('cache_creation_input_tokens'),
    'cache_read_input_tokens': u.get('cache_read_input_tokens'), 'output_tokens': u.get('output_tokens'),
    'tool_calls': len(tools), 'read_calls': sum(1 for t in tools if t[0] == 'Read'), 'files_read': len(reads),
    'search_calls': sum(1 for t in tools if t[0] in ('Grep', 'Glob')), 'bash_calls': len(bash),
    'build_calls': sum('dotnet build' in b for b in bash), 'test_calls': sum('dotnet test' in b for b in bash),
    'tool_result_chars': result_chars,
}
m['total_tokens'] = sum(m[k] or 0 for k in ('input_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens', 'output_tokens'))
json.dump(m, open(f'{out}/metrics.json', 'w'), indent=1); print(json.dumps(m))
