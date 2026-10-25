#!/usr/bin/env bash
# L7 transcript: every command a reader runs, offline after the clone and the page download. Run from L7/.
set -u
S=scorer-src/CodeAssuranceIndex
CAI=$S/src/Cai.Cli/bin/Release/net10.0/cai
run() { echo "\$ $*"; "$@"; echo "[exit $?]"; echo; }
run git -C $S log -1 --format='%H %cd'
run sha256sum downloads/survey-akkatecture.html $S/rubrics/rubric-2026.10.5/rubric-catalog.json $S/examples/cai-delivery.sample.json $S/examples/cai-delivery.keys.json
echo "## 1. The command the /page-cli/ page prints"
run $CAI score $S/examples/evidence.sample.json --rubric rubric-2026.10.5
echo "## 2. The signed sample delivery: signature + re-fold (reference program)"
run $CAI verify-delivery $S/examples/cai-delivery.sample.json --keys $S/examples/cai-delivery.keys.json --rubrics $S/rubrics
echo "## 3. The same signature, checked without the reference program"
run python3 -I work/ed25519_check.py $S/examples/cai-delivery.sample.json $S/examples/cai-delivery.keys.json
echo "## 4. One byte of the verdict changed (70.31 -> 79.31)"
run python3 -I work/ed25519_check.py work/tampered.sample.json $S/examples/cai-delivery.keys.json
run $CAI verify-delivery work/tampered.sample.json --keys $S/examples/cai-delivery.keys.json --rubrics $S/rubrics
echo "## 5. A real published survey: AfterLutz/Akkatecture, from the numbers its page publishes"
run python3 -I work/extract_lenses.py downloads/survey-akkatecture.html work/akkatecture.lenses.json
run $CAI score work/akkatecture.lenses.json --rubrics $S/rubrics
run $CAI verify work/akkatecture.lenses.json --rubrics $S/rubrics
run python3 -I work/owa.py work/akkatecture.lenses.json $S/rubrics/rubric-2026.10.5/rubric-catalog.json
echo "## 6. The production key set vs the sample key"
run cat downloads/registry-keys.json
