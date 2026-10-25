#!/usr/bin/env bash
# q.sh <db> <sql-file> <out-file> : dispatch the READ-ONLY prod-query workflow, find its run by a marker row,
# wait (deadline 6 min), and save the run log to <out-file>. SELECT only; the workflow refuses anything else.
set -euo pipefail
db=$1; sqlf=$(realpath "$2"); out=$(realpath -m "$3")
repo=<checkout>
marker="blogliftmarker$(date +%s%N)"
sql="SELECT '${marker}' AS marker;
$(cat "$sqlf")"
since=$(date -u -d '-20 seconds' +%Y-%m-%dT%H:%M:%SZ)
cd "$repo"
gh workflow run prod-query.yml -f db="$db" -f sql="$sql" >/dev/null
deadline=$(( $(date +%s) + 900 ))
seen=""
while [ "$(date +%s)" -lt "$deadline" ]; do
  for id in $(gh run list --workflow prod-query.yml -L 15 --json databaseId,createdAt \
                -q ".[] | select(.createdAt >= \"$since\") | .databaseId"); do
    case " $seen " in *" $id "*) continue;; esac
    st=$(gh run view "$id" --json status -q .status)
    [ "$st" = completed ] || continue
    log=$(gh run view "$id" --log 2>/dev/null || true)
    if grep -q "$marker" <<<"$log"; then
      # strip the GitHub log prefix (job, step, timestamp)
      sed -E 's/^[^\t]*\t[^\t]*\t[0-9TZ:.-]+ //' <<<"$log" > "$out"
      echo "run $id -> $out"; exit 0
    fi
    seen="$seen $id"
  done
  sleep 5
done
echo "q.sh: deadline passed, marker $marker not found" >&2; exit 1
