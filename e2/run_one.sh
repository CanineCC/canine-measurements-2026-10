#!/usr/bin/env bash
# run_one.sh <side> <pairId> <rep> <lane-dir> <out-dir>
# One agent run on one finding, in a sandbox that shows the agent only its own lane.
set -uo pipefail
side=$1 pid=$2 rep=$3 lane=$4 out=$5
E=$HOME/Hentet/kennel/blog-method/e2
mkdir -p "$out"
prompt=$(python3 -I - "$E/pairs.json" "$pid" "$side" "$E/prompt.txt" <<'PY'
import json, sys
pairs = {p['id']: p for p in json.load(open(sys.argv[1]))}
m = pairs[sys.argv[2]][sys.argv[3]]
print(open(sys.argv[4]).read().format(method=m['method'], path=m['path'], line=m['line'], cognitive=m['cognitive']))
PY
)
printf '%s' "$prompt" > "$out/prompt.txt"
( cd "$lane" && git reset -q --hard && git clean -qfd )          # same start state every run (bin/obj kept: ignored)
git -C "$lane" rev-parse HEAD > "$out/start-sha.txt"
start=$(date +%s)
# bwrap: the real checkouts, the other lanes and snapshots, and every session's memory are simply not there.
timeout 2700 bwrap --dev-bind / / \
  --tmpfs "$HOME/RiderProjects" --tmpfs "$HOME/Hentet" --tmpfs "$HOME/.claude/projects" \
  --bind "$lane" "$lane" --chdir "$lane" --die-with-parent \
  --setenv PATH "$HOME/.local/share/blog-method-shim:$PATH" \
  -- claude -p "$prompt" --model claude-sonnet-5-5 --output-format stream-json --verbose \
     --setting-sources local --strict-mcp-config --no-session-persistence \
     --permission-mode bypassPermissions --max-turns 120 \
  > "$out/stream.jsonl" 2> "$out/stderr.txt"
echo $? > "$out/exit.txt"
echo $(( $(date +%s) - start )) > "$out/wall-seconds.txt"
git -C "$lane" add -A -N . 2>/dev/null; git -C "$lane" diff > "$out/patch.diff"
git -C "$lane" diff --stat > "$out/diffstat.txt"
