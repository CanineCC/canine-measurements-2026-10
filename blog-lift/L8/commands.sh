#!/usr/bin/env bash
# L8 transcript: determinism and rubric pinning, with the reference scorer built in ../L7 from the public clone.
set -u
S=../L7/scorer-src/CodeAssuranceIndex
CAI=$S/src/Cai.Cli/bin/Release/net10.0/cai
R=$S/rubrics
run() { echo "\$ $*"; "$@"; echo "[exit $?]"; echo; }
run git -C $S log -1 --format='%H %cd'
echo "## 1. The same evidence, scored twice (public sample: full dimension fold)"
run sh -c "$CAI score inputs/evidence.sample.json --rubrics $R > runs/sample.run1.txt"
run sh -c "$CAI score inputs/evidence.sample.json --rubrics $R > runs/sample.run2.txt"
run sha256sum runs/sample.run1.txt runs/sample.run2.txt
run cmp runs/sample.run1.txt runs/sample.run2.txt
run cat runs/sample.run1.txt
echo "## 2. The same, for the Akkatecture survey's published lens scores"
run sh -c "$CAI score inputs/akkatecture.lenses.json --rubrics $R > runs/akkatecture.run1.txt"
run sh -c "$CAI score inputs/akkatecture.lenses.json --rubrics $R > runs/akkatecture.run2.txt"
run sha256sum runs/akkatecture.run1.txt runs/akkatecture.run2.txt
run cmp runs/akkatecture.run1.txt runs/akkatecture.run2.txt
echo "## 3. The rubric version the evidence names, and what the scorer does without the archive"
run python3 -I -c "import json,sys; print(json.load(open(sys.argv[1]))['rubricVersion'])" inputs/evidence.sample.json
run $CAI score inputs/evidence.sample.json
echo "## 4. The same sample evidence relabelled under each archived rubric version"
run cat runs/sweep/sample-across-rubrics.txt
run sh -c "ls $R | grep -c '^rubric-'"
