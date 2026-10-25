#!/usr/bin/env bash
# q.sh "<sql>" [lines]: run a read-only prod query via prod-query.yml; find OUR run by a unique marker row, print its result.
m="m$(date +%s%N | tail -c 10)"
gh workflow run prod-query.yml -f db=kennel_watchdog -f sql="SELECT '$m' AS marker; $1" >/dev/null || exit 1
for t in $(seq 1 90); do
  sleep 8
  for id in $(gh run list --workflow=prod-query.yml -L 6 --json databaseId,status -q '.[] | select(.status=="completed") | .databaseId'); do
    log=$(gh run view $id --log 2>/dev/null | sed 's/\x1b\[[0-9;]*m//g')
    if grep -q " $m" <<<"$log"; then
      sed -E 's/^\S+\s+Run \(read-only\)\s+\S+Z ?//' <<<"$log" | awk -v m="$m" 'f; index($0, m) {f=1}' | grep -v -E "^##\[|Complete job|Cleaning up|^\(1 row\)$" | head -${2:-60}; exit 0
    fi
  done
done
echo "no run found for marker $m"; exit 1
