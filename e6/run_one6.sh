#!/usr/bin/env bash
# run_one6.sh <arm U|G> <mid> <rep> <out>: one agent run, sandboxed to its own lane, with its arm's PATH.
set -uo pipefail
arm=$1 mid=$2 rep=$3 out=$4; E6=$HOME/Hentet/kennel/blog-method/e6; lane=$E6/lanes/$arm
mkdir -p "$out"
prompt=$(python3 -I - "$E6" "$mid" "$arm" <<'PY'
import json, sys
E6, mid, arm = sys.argv[1:4]
c = {x['id']: x for x in json.load(open(f'{E6}/candidates.json'))}[mid]
print(open(f'{E6}/prompt-{arm}.txt').read().format(method=c['method'], path=c['path'], line=c['line'], title=c.get('findingTitle', ''), detail=c.get('findingDetail', '')))
PY
)
printf '%s' "$prompt" > "$out/prompt.txt"
( cd "$lane" && git reset -q --hard && git clean -qfd )
start=$(date +%s)
timeout 2700 bwrap --dev-bind / / --tmpfs "$HOME/RiderProjects" --tmpfs "$HOME/Hentet" --tmpfs "$HOME/.claude/projects" \
  --bind "$lane" "$lane" --chdir "$lane" --die-with-parent \
  --setenv PATH "$HOME/.local/share/blog-method-shim/$arm:$PATH" \
  -- claude -p "$prompt" --model claude-sonnet-5-5 --output-format stream-json --verbose \
     --setting-sources local --strict-mcp-config --no-session-persistence --permission-mode bypassPermissions --max-turns 120 \
  > "$out/stream.jsonl" 2> "$out/stderr.txt"
echo $? > "$out/exit.txt"; echo $(( $(date +%s) - start )) > "$out/wall-seconds.txt"
git -C "$lane" add -A -N . 2>/dev/null; git -C "$lane" diff > "$out/patch.diff"; git -C "$lane" diff --stat > "$out/diffstat.txt"
