# WP-40: Replications — questions our field publishes on

**Version 0.1 (pre-registration draft, NOT frozen)**
**Date: 2026-10-25**
**Series: Watchdog Benchmark Program, paper 40**
**Feeds:** blog B22 (§E1), B23 (§E2), B25 (§E3), B24 (§E4) — `docs/marketing/blog/PLAN.md`, "Method you can check"

---

> **STATUS: PRE-REGISTRATION DRAFT.** Nothing here has been run. Each experiment freezes separately: when its
> `[DECIDE BEFORE FREEZE]` marks are resolved, a signer records the freeze date and the commit of this file in
> its §Freeze line, and only then may its outcome data be opened. A change after freeze is an appended,
> dated amendment that says what it changes and whether any outcome had been seen. It is never a silent edit.
>
> **Frozen commits, kept reachable as tags:** E1 `wp40-e1-freeze` (`b1ed0ab162`, pushed before the labels were opened);
> E2–E4 `wp40-e2-freeze` (`42fae3dd6d`, pushed before the first counted run). A later rebase gives the same text new
> hashes on the branch; the tags are the record.

## 0. Why this paper exists

Our field publishes a steady stream of claims about code health and AI coding agents. Many are on the right
questions and rest on thin method: the number of units measured goes unstated, the sample is exercises rather
than real codebases, the instrument is checked against itself, and projections sit beside measurements
unlabelled. This paper runs three of those questions properly, under the series rules, and publishes the
result whatever it is.

Series rule, unchanged (README, 2026-08-14): **no tool, vendor or study is named in any published artefact
of this paper.** The experiments stand on their own question, ground truth and controls.

## 1. Rules common to all three

- **R1 — Loss is pre-defined.** Each experiment states, before freeze, the result that counts against us, and
  that result publishes in the same post, at the same length, as a favourable one.
- **R2 — n is the unit measured**, reported in the first table, never the size of the source dataset.
- **R3 — No exclusion on the outcome.** Exclusions are listed with their criterion, fixed before freeze, and
  counted in the results.
- **R4 — Spread with every number:** a 95 % interval (bootstrap over the top-level cluster: project or
  repository), the per-cluster distribution, and the leave-one-cluster-out range.
- **R5 — Measured and projected are never mixed.** This paper publishes no projection.
- **R6 — Engine pinned.** One frozen engine build per experiment; its version recorded from the run, not from
  the checkout (`index-how-a-check-fails`: verify on the engine the run used).
- **R7 — Agents gather, people decide.** No model gives a verdict anywhere in the scoring path.
- **R8 — Reproduction package:** inputs (or pinned commits), scripts, raw outputs, the frozen file.

---

## E1 — Do our maintainability signals agree with expert ratings?

**Question.** On classes that independent professionals rated for maintainability, how well does a ranking
derived from our engine's findings agree with the experts' consensus?

**Data.** *A Software Maintainability Dataset*, figshare 10.6084/m9.figshare.12801215, version 3, CC BY 4.0
(Schnappinger, Fietzke, Pretschner, ICSME 2020). Public part: **304 class evaluations, 5 open-source Java
projects** (ArgoUML, Art of Illusion, Diary Management, JUnit 4, JSweet), sources included, labels in
`labels.csv`. The study's full 519-class set is not public and is not used.

**Sealing.** `labels.csv` was downloaded on 2026-10-25 04:01 UTC+1 into a separate directory. sha256
`2448842f858f73bfa7d1631b8be3f16c7943ff76c65e6910410fc74dd120f531` (md5 matches figshare's computed md5
`d57d4ac53fc78ff78d375b1a44260fba`). Before freeze only its header row and its three key columns
(`projectname`, `packageandclass`, `path`) were read, to learn which files are labelled; no label column was read.

**Instrument.** The engine's own Java code model (its Spoon sidecar, built from the pinned engine) and its own D1/D2
complexity calculator, run over each project's shipped sources by a thin probe that prints every method
(`evidence/40-replications/e1/`). Cross-check: on JUnit 4 the probe returns 1,366 methods where the full CLI's D1 counts
1,360. Coverage of the labelled set: 302 of 304 files carry at least one method; the other 2 (Art of Illusion) are
files with no method bodies.

**Unit.** A labelled class is its file. Every method the code model places in that file counts toward it (the experts
were shown the whole file).

**Labels as numbers.** Each axis is a probability vector over the four Likert answers, 0 = strongly agree ... 3 =
strongly disagree. The value used is the expectation E = Σ k·P(k) (the Readme allows argmax or a weighted average; the
weighted average is chosen because it keeps the experts' uncertainty). Statements are positive for readability,
understandability and overall maintainability ("this code is easy to read" ...) and negative for complexity and
modularization ("this code is complex", "this code should be split up"). To give every axis the same direction,
**badness** = E for the positive statements and 3 − E for the negative ones: higher is worse on all five.

**Predictors.** All are computed and all are reported; one is primary.
- **Primary: total cognitive complexity of the file** (sum of D2's per-method score). Chosen because it is the engine's
  own measure of how hard code is to follow, aggregated without any weight we would have to choose.
- Secondary, reported beside it: the largest single method's cognitive score; the number of methods over D2's
  threshold of 15 (what a customer sees as findings); total cyclomatic complexity (D1).
- **Size baseline: non-blank lines in the file.** Reported for every axis, because a complexity signal that does no
  better than file length has not shown it measures anything beyond length.

**Outcomes.**
- Primary: Spearman ρ between the primary predictor and **overall** badness, n = 304.
- Secondary: the same for the other four axes; every secondary predictor on every axis; the size baseline on every
  axis; and the partial Spearman ρ of the primary predictor on each axis with file length held constant (ranks
  residualised on the rank of length).
- Interval: 95 % percentile bootstrap, 10,000 resamples, seed 20261025, classes resampled **within** each project
  (five projects are too few clusters for a cluster bootstrap; per-project ρ and the leave-one-project-out range are
  reported instead as the spread).
- Reference, from the dataset's own paper (no per-rater data is public, so no coefficient comparable to ρ exists):
  experts disagreed on at least one of the five answers in 73.4 % of rating pairs, and by more than a point per
  question on average in 17.2 %.
- Disagreement table: the 10 classes with the largest rank difference between the primary predictor and overall
  badness, each read from the code and classed *our miss*, *label debatable* (code shown), or *out of our scope*.

**How the sample was drawn, stated in the post.** The dataset's authors ordered files for labelling by clustering
static code metrics (cognitive complexity among them) so that edge cases are over-represented. A metric is therefore
being tested on a sample selected partly by metrics, which tends to raise correlations above what a random sample of
the same projects would give.

**Loss conditions.** (1) If the 95 % interval of the primary ρ on overall maintainability has an upper bound at or
below 0.3, the post says "weak agreement" in its first paragraph. (2) If the primary predictor's ρ on overall does not
exceed the size baseline's ρ (difference interval, same bootstrap, includes 0), the post says the complexity signal
added nothing measurable over file length, in its first paragraph.

**Exclusions.** None. The 2 files with no methods score 0 on every complexity predictor and stay in; a sensitivity
run without them is reported.

**Freeze:** 2026-10-25, the commit that introduced this paragraph (`git log -1 -- docs/benchmarks/40-replications.md`
at the E1 freeze). Labels opened only after it.


---

## E2 — Does the shape of the codebase change what an agent spends to fix the same defect?

**Question.** Give an AI coding agent the same real finding on the same method, once in our codebase before we split
it into vertical slices and once after. Does it spend fewer tokens, and does its fix hold more often, when the method
sits in a small slice instead of a large shared module?

**Why this design.** Comparisons of "healthy" against "unhealthy" files usually compare different code: the unhealthy
files are longer and do different things, so the comparison mostly measures length. Here the method is held fixed and
only its surroundings change.

**Snapshots.**
- BEFORE: tag `architecture-baseline-2026-09-18` (`5d04157a34`), set on 2026-09-18 as the fat-module baseline before the
  engine was sliced.
- AFTER: branch `cca-phase-2` at `a3f3f35ad9` (2026-10-24).
- Both exported with `git archive`; every `CLAUDE.md`, `AGENTS.md` and `.claude/` removed from both, so the agent reads
  code, not our working instructions.
- **Confound, stated plainly:** five weeks of other work separate the snapshots (detector fixes, the product split,
  new tests). The method body is identical; its project, neighbours, tests and the rest of the repository are not.
  The result is "this method in that codebase", not an isolated effect of slicing.

**Units.** Production methods (`src/`, `engine/src/`, test and fixture paths excluded) whose cognitive complexity is
over D2's threshold of 15 in BOTH snapshots, with a byte-identical body (whitespace-normalised sha1) and a unique match
in AFTER: **46 pairs**, all scored 16 or 17, all moved from the 298,146-line `CodeHealth.Core` project into a slice
project of 71 to 43,380 lines. Complexity by the engine's own per-method walk (the D1/D2 code), pinned engine
`a3f3f35ad9`. Draw: 20 pairs, `random.Random(20261025).sample` (`draw.json`); pilot 2 others (p37, p05), discarded.

**Task.** One fixed prompt per run, the finding as a report states it (method, file, line, score, threshold), asking
for a behaviour-preserving refactor to 15 or lower, the project still building, tests not edited, no commit. The prompt
asks for no verdict. Agent: Claude Code `claude -p`, model `claude-sonnet-5-5`, default effort, `--max-turns 120`,
45-minute wall limit, no MCP servers, no user settings, no session memory. Sandbox: `bwrap` with the real checkouts,
the other lanes and snapshots, and every session's memory replaced by empty mounts. Each run starts from the
snapshot's commit with a warm build. **3 runs per pair per side: 120 runs**, in a seeded shuffled order alternating
sides.

**Gate, deterministic, per run** (`gate.py`; no model is asked anything):
- **held:** the containing project builds; the method scores 15 or lower; no method in the touched files rose over 15.
- **did not clear:** builds, method still over 15. **moved:** method cleared, another method in the touched files rose
  over 15. **build failed**, **target missing** (method renamed or removed), **no change**, recorded as such.
- **behaviour:** the unit-test classes that name the type are run; passed / failed / untested. Behaviour is compared
  between sides only on pairs with such tests on both sides (18 of the 20).
- Tests edited: flagged.

**Outcomes.**
- Primary: ratio of total tokens (input + cache creation + cache read + output) AFTER / BEFORE, per pair (mean of its
  runs), summarised as the geometric mean over pairs with a 95 % bootstrap interval over pairs (10,000, seed 20261025).
- Also: cost, turns, characters of tool output read into context, wall time, build calls; the held rate per side and
  its difference with a pair-bootstrap interval; the behaviour outcome on the 18 pairs; per-pair spread.

**Loss conditions.** If the token-ratio interval includes 1.0, the post's headline is that we found no difference in
what the agent spent. If AFTER's held rate is not higher (interval includes 0), the post says so.

**Freeze:** 2026-10-25, the commit that introduced this section. No counted run before it; the 4 pilot runs are
discarded and published as pilot.

---

## E3 — Did the agent's fixes hold?

Answered by the E2 runs themselves: every run is graded held / did not clear / moved / build failed / target missing /
no change by the gate above, and the behaviour check runs the tests. The headline is the gap between what the agent
*said* (its final message) and what the gate found. The agent's final message is recorded verbatim and classified by
a fixed rule, not by a model: a run **claims success** when it ended normally with a non-empty diff and its final message contains none of "could not", "couldn't", "unable", "not able", "failed", "did not", "didn't", "cannot" (case-insensitive).

Separately, from our own records: the training register's "did-not-clear: 0" was recorded on 12 of 206 scored
repositories (`REGISTER.md`, now printed beside the number); 10 real did-not-clear events sit in rounds the fold does
not count. Both are reported, neither as a rate.

---

## E4 — Would an AI reviewer have caught the fixes that did not hold?

**Question.** On the E2 patches, whose outcome the deterministic gate already knows, how often does an AI reviewer
approve a patch that did not hold, and reject one that did?

**Method.** Every E2 patch with a non-empty diff is shown to a reviewer: `claude -p`, model `claude-sonnet-5-5`, fixed
prompt with the finding, the diff and the threshold, asking APPROVE or REJECT on "the method is now at or below the
threshold, behaviour is unchanged and the project still builds". No tools, no repository access. 3 independent asks per
patch.

**Outcomes.** False approvals (APPROVE on a patch the gate graded anything but held-with-tests-passing or held-
untested); false rejections; and self-consistency (share of patches whose 3 answers agree). Intervals by bootstrap over
patches.

**Freeze:** with E2.

---

## E5 — In production, how often did a fix an agent marked done fail to clear?

**Question.** When a coding agent tells Assert, through the MCP tool `resolve_finding`, that it fixed a finding, how
often does the next survey still find it?

**Population.** Every `FindingClaimStateChanged` event with `Kind = AgentResolved` in the production event store
(`events.mt_events`), all of them, no sampling. Structure read before freeze (no outcome): 5,251 such events on 6
repositories, 2026-06-13 to 2026-10-08. Which repositories they are, and whose, is reported with the result.

**Verdict per resolution, the product's own rule.** The deciding run is the first `ScanRunIngested` for the same
repository whose `StartedAt` (else `At`) is after the resolution's `At`, with `FindingsAreTheFullLedger = true` and
`Degraded = false`.
- **did not clear:** the fingerprint is in that run's `Findings`.
- **cleared:** the fingerprint is absent and the run's `DimensionStates` marks the finding's dimension `measured`
  (the dimension is taken from the latest earlier run whose ledger carries the fingerprint).
- **absent, not measured:** absent, but the dimension was not measured in that run, or `DimensionStates` is missing.
  Never counted as cleared (absence is not evidence when a dimension abstains).
- **unverified:** no deciding run exists.

**Outcomes.** Counts in all four buckets; the did-not-clear share of (did not clear + cleared) with a Wilson 95 %
interval and a repository-cluster bootstrap (10,000, seed 20261025); the same per repository, per dimension and per
agent name; the delay from resolution to deciding run.

**Loss condition.** None in the E1/E2 sense: every bucket publishes. If the share is small, the post says so.

**Read-only.** Run through the `prod-query` workflow (read-only transaction, statement gate). No row is written.

**Freeze:** tag `wp40-e5-freeze`.

---

## E6 — Does our finding help an agent fix hard code? (guided against unguided)

**Question.** On methods that are genuinely hard (cognitive complexity 25 or more), does an agent given Assert's
finding, with a way to re-measure, produce fixes that hold more often than an agent asked plainly to improve the code?

**Codebase.** The AFTER snapshot of E2 only (cca-phase-2 `a3f3f35ad9`, instruction files removed), so the E2
architecture effect cannot enter.

**Sample.** Production methods (`src/`, `engine/src/`, test and fixture paths excluded) with cognitive complexity of
25 or more by the engine's per-method walk, whose declaring type has at least one unit-test class named
`<Type>…Tests`. Draw 20 with `random.Random(20261025)`; pilot 2 others, discarded.

**Arms, one fixed prompt each:**
- **U (unguided):** "This method is hard to maintain: `<Type.Method>` in `<path>`. Improve its maintainability
  without changing its behaviour. The project must still build with `dotnet build` (warnings are errors). Do not edit
  tests. Leave the change in the working tree; do not commit." No metric, no threshold.
- **G (guided):** the finding as Assert states it: dimension, score, threshold 15, the engine's own driver summary
  for the method ("if/else 9 (19 pts) …"), plus a command `measure <file>` in the working tree that prints the
  engine's cognitive score for every method in the file (the stand-in for the MCP re-scan). Same last three sentences.

Model `claude-sonnet-5-5`, 3 runs per method per arm (120 runs), the E2 sandbox and harness, order shuffled by seed.

**Gate, deterministic.** As E2, with two corrections learned there: (1) the covering tests are the unit-test classes
named `<Type>…Tests` only; (2) the tests run first on the unchanged code; a run's test failure counts only if it fails
twice and passes on the unchanged code. Outcomes per run: held / did not clear / moved / build failed / target
missing / no change; behaviour passed / failed.

**Outcomes.**
- Primary: held-and-behaviour-passed rate, G minus U, with a 95 % bootstrap over methods.
- Secondary: tokens G/U (geometric mean of per-method ratios); the target method's complexity after; the change in
  total complexity of the touched files (to see a problem moved instead of solved); cost and wall time.

**Loss condition.** If the primary interval includes 0, the post's headline is that our finding did not change how
often the fix held. If G costs more tokens, that is reported beside it, in the same paragraph.

**Freeze:** tag `wp40-e5-freeze` (E5 and E6 are frozen together).

**Amendment 1, 2026-10-25, before any counted E6 run (no outcome seen; only the draw and one finding's text read).**
The G arm was to receive "the engine's own driver summary". For C# the engine emits none, by design: the driver clause
is "neutral sidecar path only, null on Roslyn" (`ComplexityScoring.MethodFinding`). G therefore receives the D2 finding's
**title and detail exactly as the engine words them**, produced by `ComplexityScoring.BuildResult` over the engine's
own C# walk (pinned engine), plus the `measure` command. Nothing else changes. The draw (`draw.json`): 50 eligible
methods, 20 drawn, pilot m-ids recorded there.

**Amendment 2, 2026-10-25 10:00, a harness fix found in the pilot (pilot discarded; committed
seconds after the driver started the first counted run, before any counted run finished or was read).** An agent that
waits on background work emits one `result` event per session segment; `usage` is per segment and `total_cost_usd`
is cumulative. The metrics extractor read only the last segment (a guided pilot run showed 29,242 tokens where the
sum is 424,084). E6 tokens and turns are therefore SUMMED over all result segments. E2's 120 runs were checked: each
has exactly one result event, so E2's figures are unaffected.

---

## E4b — Would an AI reviewer approve a fix that did not hold? (on E6's patches)

**Why.** E4 could not measure false approvals: none of E2's patches was bad. E6's methods are hard (complexity 25 to
87), so some fixes may fail.

**Method.** E4's reviewer, prompt and settings, unchanged (`e4/review.py`), on every non-empty E6 patch (both arms),
3 asks each. Frozen before E6's outcomes are read: committed while E6 runs, analysed only after E6's driver reports
ALL DONE.

**Gate truth.** A patch is **good** when E6's gate says `held` with behaviour `passed`; **bad** when the gate says
`did_not_clear`, `moved`, `build_failed`, `target_missing`, or behaviour `failed` (under E6's twice-and-baseline rule).
`baseline_failing` and gate errors are excluded and counted.

**Outcomes.** False approvals (APPROVE asks on bad patches, with a bootstrap over patches); false rejections (REJECT
asks on good patches); self-consistency; all split by arm. If there are no bad patches, that is the result and E4b
reports it.

**Freeze:** tag `wp40-e4b-freeze`.

---

## E4c — Does a stronger AI reviewer catch the fixes that did not hold? (E4b again, a stronger model)

**Why.** E4b's reviewer (claude-sonnet-5-5, the same model as the authors) approved 17 of 78 asks on E6's bad
patches. The obvious reply is "use a stronger reviewer". This tests that reply before B24 relies on E4b.

**Method.** E4b exactly (prompt, no tools, the finding with its threshold and the diff, 3 independent asks per patch,
same 120 E6 patches, same gate truth: 94 good, 26 bad), with one change: the reviewer model is `claude-opus-5-5`.
Script `e4/review_e4c.py` (E4b's `review6.py` with the model and output folder changed, nothing else).

**Outcomes.** False approvals (APPROVE asks on bad patches) and false rejections (REJECT asks on good patches), each
with a 95 % bootstrap over patches (seed 20261025); bad patches approved by a majority; and the paired difference
from E4b's reviewer on the same patches (bootstrap over patches).

**Loss condition (for B24's headline, "a second AI is not a gate").** If the stronger reviewer's false-approval rate
has a 95 % upper bound below 5 % AND its false-rejection rate is not above 10 %, B24 says in its first paragraph that
a stronger reviewer did catch these, and the gate's case rests on cost, consistency and not being persuadable, not on
catching more. Whatever the result, both reviewers are reported side by side.

**Freeze:** tag `wp40-e4c-freeze`, before the first ask.

**Amendment 1, 2026-10-25, after 51 of 360 asks (harness defect; method unchanged).** One ask exceeded the 600-second
subprocess timeout and the uncaught exception ended the run. The script now records such an ask as `TIMEOUT`
(counted, like UNPARSEABLE, as neither APPROVE nor REJECT) and the run resumes from where it stopped; nothing else
changes. Disclosed: the frozen analysis was run once on the 51 completed asks (17 patches) before the stop was
noticed. Those partial figures are not reported, and no part of the method, sample or loss condition is changed
after seeing them.

---

## E7 — The whole loop, on code we did not write

**Question.** E5's question, answered on well-known public repositories instead of our own: when a coding agent works
findings through the product's MCP tools and reports them fixed, how often does the next scan agree, and do the
project's own tests still pass?

**Population and draw.** Candidates: 17 well-known .NET repositories (`evidence/40-replications/e7/candidates-api.tsv`).
Eligible, by a rule that reads no outcome: GitHub-detected SPDX licence MIT, Apache-2.0, BSD-3-Clause or PostgreSQL
(NOASSERTION excluded); at least 3,000 stars; not archived; 10,000 to 400,000 non-blank production C# lines (tests,
samples, benchmarks-of-tests and generated files excluded; `sizes.tsv`); tests that need no external service (npgsql
excluded: PostgreSQL). Seven eligible; four drawn with `random.Random(20261025)`: **AvaloniaUI/Avalonia,
JamesNK/Newtonsoft.Json, dotnet/BenchmarkDotNet, serilog/serilog** (`draw.json`). Plus **umbraco/Umbraco-CMS**, named by
the owner before any draw, 420,655 production lines, above the band, and reported as such.

**Import.** Each repository is imported as a PRIVATE copy under the CanineCC organisation with its history (`git clone
--mirror`, push to a new private repository). No fork, no pull request, nothing is sent upstream. The default branch's
head at import is recorded and is the baseline.

**The loop, as a customer runs it.** The owner connects each private copy to the product (Watchdog until 2026-10-31,
Assert after) and mints one agent key per repository. The product scans it. Then, 10 times per repository and one task
per session, an agent (Claude Code, `claude-sonnet-5-5`, the E2 sandbox with network for the MCP server and git push)
gets one fixed prompt: *"This repository is connected to our code analysis through its MCP server. Call `audit`, then
`next_task`, claim that finding with `claim_finding`, fix it in the code, run the project's tests if you can, then call
`resolve_finding` with a one-line note. Commit with a message naming the finding and push to `origin` on the default
branch. Work exactly that one task, then stop."* No verdict is asked. After the 10th task, one rescan is requested.

**Verdict per fix.** E5's frozen rule, unchanged (`e5/verdict.sql`), on each copy: did not clear / cleared /
absent-not-measured / unverified.

**Behaviour per fix.** Each fix commit is checked out in a separate lane and the test projects that reference the
project it touched are run; first on the baseline commit. A failure counts only if it fails twice and passed on the
baseline.

**Outcomes.** Per repository and pooled: the four verdict buckets; the did-not-clear share of decided fixes (Wilson
95 %); behaviour passed / failed; by dimension; tokens and cost per task. Reported beside E5 (our own code).

**If a scan cannot finish.** A repository whose scan fails or exceeds the product's run budget is reported as such, with
the reason. It is not replaced: replacing it would select on an outcome.

**Loss condition.** None: every bucket publishes.

**Owner actions.** Grant the product's GitHub app access to the five private copies; connect them; mint one agent key
per repository into a file with mode 600 (never into chat).

**Freeze:** tag `wp40-e7-freeze`.

---

## Completion & signing

- [ ] All `[DECIDE BEFORE FREEZE]` marks resolved for the experiment being frozen
- [ ] Freeze line filled (date, commit of this file)
- [ ] Run; raw outputs archived in the package before analysis
- [ ] Results written against the pre-registered outcomes only; anything else labelled *exploratory*
- [ ] The blog post's method card filled from this paper, field by field
- [ ] Signed: ________________
