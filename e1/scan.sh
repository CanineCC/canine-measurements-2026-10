#!/usr/bin/env bash
# scan.sh <project>: the pinned engine (cca-phase-2 a3f3f35ad9) over one dataset project's shipped sources.
set -uo pipefail
p=$1; E1=$HOME/Hentet/kennel/blog-method/e1; src=$E1/src/$p/sourcefiles
[ -d "$src/.git" ] || (cd "$src" && git init -q && git add -A && git -c user.name=ds -c user.email=ds@local commit -qm "dataset $p as shipped")
CLI=<checkout>/engine/src/CodeHealth.Cli/bin/Release/net10.0/codehealth
export DOTNET_ROOT=<home>/.dotnet-microsoft DOTNET_GCHeapHardLimit=0x200000000 CODEHEALTH_NO_LLM=1
export JAVA_HOME=<home>/.sdkman/candidates/java/current PATH=<home>/.sdkman/candidates/java/current/bin:$PATH
export CODEHEALTH_JAVA_SIDECAR_JAR=<checkout>/engine/sidecars/java-spoon/target/codehealth-java-sidecar.jar
rm -rf "$E1/out/$p"; mkdir -p "$E1/out/$p"
choom -n 1000 -- $CLI analyze "$src" --output "$E1/out/$p" --quiet > "$E1/out/$p.log" 2>&1
echo "exit $?" >> "$E1/out/$p.log"
