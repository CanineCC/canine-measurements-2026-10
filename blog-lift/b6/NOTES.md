# B6 "Architecture you cannot draw by hand" (imprint cf47fb5bbcff48dd9e93492dee2f5061), lift L11

Fetched 2026-10-25, about 17:30 UTC. Raw pages in `downloads/`.

## What the brief asked, and what exists publicly

- **A project reference with no type dependency behind it: NO PUBLIC EXAMPLE.** None of the 28 public reports prints a
  "reference with nothing behind it" finding or anything equivalent (searched all report texts for unused/declared
  reference wording). The post keeps its fixture example (A -> B -> C -> A) as our own account.
- **Nearest true example used instead: the two grains disagreeing in the other direction**, on DualBrain/bsharp: the
  project graph is acyclic, the module graph inside one project has a loop.

## Example used

DualBrain/bsharp (B#, a BASIC compiler and interpreter written in VB.NET).

- Public report: https://app.watchdog.canine.dev/api/oss/DualBrain/bsharp/report (sections "Architecture: module dependency graph", "Architecture: which parts of the code depend on which", D5 Coupling, AX3)
- CAI page: https://codeassuranceindex.info/surveys/github/dualbrain/bsharp/
- Repository tree at the pinned commit (GitHub API): `downloads/github/tree.json`
- Saved: `downloads/DualBrain__bsharp.html` (+ `.txt`), `downloads/cai-survey-dualbrain_bsharp.*`, `downloads/thephpleague__oauth2-server.*` (for flag 1)

## Figures (bsharp report, re-read 2026-10-25)

- Measured 21 October 2026, 15:58 UTC, code version 77caa74 (CAI page: 77caa74c1eecb57922f4f195106400babfa001b4), rubric 2026.10.5, survey ID cd_39b60f2c11004e16b0e6e9eb4f1c153e. 12,706 lines of product code in 4 projects. CAI 70 (CAI page 69.7).
- Project grain: D5 "4 projects, 0 dependency cycle(s), 0 unstable depended-on project(s)"; AX3 Project dependency cycles 10.0/10; project graph drawn as bsc -> bsharp, bsi -> bsharp; "3 inter-project edges".
- Module grain: "14 modules, with 25 dependencies between them. One loop runs through 5 of the modules, marked above the diagonal."
- Above-diagonal cells: 6 -> 12 `Bsharp.CodeAnalysis.Syntax` uses `Bsharp.CodeAnalysis` (4 pairs, e.g. `Lexer -> DiagnosticBag`); 8 -> 9 `Symbols` uses `Binding` (6 pairs, e.g. `GlobalArraySymbol -> BoundExpression`); 9 -> 12 `Binding` uses `Bsharp.CodeAnalysis` (3 pairs, e.g. `Binder -> DiagnosticBag`); 10 -> 12 `Emit` uses `Bsharp.CodeAnalysis` (7 pairs, e.g. `Emitter -> Diagnostic`).
- `Bsharp.CodeAnalysis` uses Emit, Text, Syntax, Symbols, Binding. Loop members: Bsharp.CodeAnalysis, Syntax, Symbols, Binding, Emit (= 5, matches).
- Repo tree at 77caa74: all of `bsharp/CodeAnalysis/{Binding,Syntax,Symbols,Emit}` and `Diagnostic.vb`, `DiagnosticBag.vb` are in project `bsharp/bsharp.vbproj`. So the loop is inside one project, which is why the project grain cannot see it.

## ★ CONTRADICTIONS / FLAGS

1. **"Tests and samples are out by default" is not what the public module graphs show.** bsharp's matrix lists a
   module `samples` (the repo has `samples/hello.vb`, a sample output file), and thephpleague/oauth2-server's matrix
   includes `OAuth2ServerExamples.Entities` and `OAuth2ServerExamples.Repositories` with real edges (7 and 17 type
   pairs into the library). Example trees named `samples/` or `examples/` are evidently not excluded from the module
   graph. Post claim left in place but softened in post.md to "tests are out by default"; owner/engine should decide
   whether example trees should be excluded (D34 already excludes "example/demo trees", so two dimensions disagree).
2. bsharp's matrix also has modules `Microsoft.VisualBasic`, `My` and `(global)`. The post says platform references are
   excluded; these may be namespaces declared in the repo itself (VB's My namespace pattern), so I did NOT verify this
   as a contradiction. Worth one look.
3. Not a post claim, boyscout: the bsharp report's finding "Solution references a project that does not exist ...
   `bsharp.tests/bsharp.tests.vbproj`": the tree has `bsharp.tests/bsharp.Tests.vbproj` (capital T). It is missing on a
   case-sensitive file system and present on Windows. Arguably correct for Linux CI, but the finding text should say
   it is a case mismatch.
4. The public report's node-link caption reads "Any dashed red edge points upward or sideways, a layering smell or
   cycle" (bsharp, atomvm, others, current format). This is the "cycles or layering violations" wording B5 says was
   corrected. Flagged in b5 as well.
5. **Strongest public evidence for flag 1: tj/commander.js** (https://app.watchdog.canine.dev/api/oss/tj/commander.js/report,
   JavaScript, saved `downloads/tj__commander.js.*`). Matrix: "13 modules, with 6 dependencies"; modules include
   `examples`, `tests` and four `examples.*` modules, and ALL 6 dependencies are examples.* -> lib.command / lib.help.
   The library's own modules have no edges between them in the drawn graph. The `tests` module appears as a node with
   no edges. So for this codebase the published module graph is a graph of its examples.
6. **"Needs a deep model" vs JavaScript.** The post said the module graph "works wherever the language is modelled
   deeply". The live language endpoint lists "Module graph" among JavaScript's covered lenses although JavaScript is
   Structural, and commander.js (JavaScript) has a module matrix. Post sentence revised to say the module graph
   reaches Structural JavaScript too.
