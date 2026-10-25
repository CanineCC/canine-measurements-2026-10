# L6 (B9 "The fix you should do first is not the biggest one"): figures re-derived from production, 2026-10-25

Read-only workflow `prod-query.yml` (`kennel_watchdog`), dispatched by `../tools/q.sh`. SELECT only.

## How the ranking is computed (engine source, read on main b37a548fe4)

- `RuleRecommendationEngine.ByImpactPerEffort`: key = `ScoreGainPoints / EffortWeight(Effort) * ChurnWeight`,
  EffortWeight Low 1 / Medium 2 / High 4; ties by ScoreGainPoints desc, DimensionId, Action (ordinal). Unlock
  rows follow the ranked ones. The report's list is capped at 8 (`max = 8`).
- `ChurnPriority`: from D15's hotspot findings (worst first), boost = MaxBoost(1.0) x (count - rank) / count;
  `WeightFor(files)` = 1 + the boost of the group's HOTTEST file, so the weight is in [1, 2]. No D15 hotspot ->
  every weight 1.0.
- `EngineeringReportRenderer.BuildTasks` -> `ConsolidateByRootCause` folds tasks sharing a primary file into the
  first (best-ranked) one; `RankReasonFor` writes the task's own gain (0.1 pts), its effort, and the lift
  ("lifted N%", N = (weight - 1) x 100, whole percent), or "no change-frequency signal".
- `SprintPlanRenderer` stores those consolidated tasks as tickets; the server keeps them in the repository bundle
  document (`events.mt_doc_repositorybundle.data -> SprintPlan -> Tickets`), one per repository, for the
  repository's latest full-picture run.

## Data (tickets.sql -> tickets-titles.out; hot.sql -> hot.out; d15.sql -> d15.out)

- 6,862 repository bundles with a ticket list (security-watch bundles excluded); 18 skipped because their tickets
  predate RankReason, leaving **6,844 repositories**. Scans completed 2026-08-03 to 2026-10-25 (223 bundles carry
  no CompletedAt); 6,398 completed on or after 2026-09-25 (the "recent" subset, same picture: 227 changed by the
  point reading).
- 51,228 tickets (served order = churn-weighted order). `tickets.out` is the same export with an md5 in place of
  the title (first run; superseded by `tickets-titles.out`, which is the input to every figure below).
- Sanity check (`check_weighted.py` -> `check_weighted.out`): 43,792 adjacent served pairs, **0** ordered against
  the weight reconstructed from RankReason beyond rounding. The reconstruction matches the engine.

## Result (analyse.py -> analyse.out, per-repository detail.json)

Unweighted order = the served tickets re-sorted by own gain / effort weight with the engine's tie-breaks.

- **6,369 of 6,844**: no served task carries a lift, so the two orders are identical by construction. Of these,
  4,920 had no D15 hotspot at all (D15 found none or did not apply; 715 of all 6,844 scans had shallow history),
  and 1,449 had hotspots but none of their top-8 tasks touches a hot file.
- **1,924 of 6,844** repositories had at least one D15 hotspot; **475** had a lifted task among the served 8.
- Top 5 changed by churn weighting (order or membership):
  - **point reading: 229** (membership differs on 124; the #1 task differs on 47);
  - **changed in all 200 rounding draws: 169** (membership 104, #1 38) = proven lower bound;
  - **changed in at least one draw: 384** (membership 187, #1 163) = upper bound.
  - unchanged in every draw: 91; 1 undetermined (a task beyond the served 8 could not be excluded).
- Lifted tickets: 540; median lift 100 % (the task touches the repository's hottest file), min 2 %, max 100 %.
- Of the 475 repos with a lifted task in the 8, the lifted tasks sit inside the top 5 on 269 (1 lifted: 249,
  2: 19, 3: 1) and only below it on 206.

## Why it is a range, not one number

- The sprint plan stores gain rounded to 0.1 point. Where two tasks of different dimensions print the same gain,
  their gain/effort order is not recoverable; 200 draws perturb each (dimension, printed gain) by up to +-0.05.
  Tasks of the same dimension with the same printed gain are taken as genuinely equal, ordered by the engine's
  own text tie-break (the ticket title carries the action text).
- A folded ticket's other members (same primary file, another dimension) are not in the sprint plan; their
  unweighted key is drawn anywhere between the host's key and the ticket's ImpactPoints / 1. Run with only one
  of the two perturbations (scratch copies of analyse.py): fold only -> 198 changed in every draw, 50 depending on
  the draw; gain rounding only -> 199 changed in every draw, 180 depending. Gain rounding drives the width.
- Only the top 8 (before consolidation) are stored. A change found among the served tickets is proven (if the
  true unweighted top 5 equalled the served top 5, it would be the top 5 of any subset containing it). "Unchanged"
  is claimed only when no task beyond the cap can intrude (its weighted key, and hence its unweighted key, is at
  most the smallest served weighted key) or when an unlock row shows the ranked list was exhausted.
- The full uncapped, unrounded list exists in each run's `tasks.json` bundle file, which is not in the database
  and not reachable from the read-only query workflow. That is what blocks one exact number.

## What in the existing post the data contradicts or qualifies

- Nothing in the post's description of the mechanism is contradicted: the cap (weight at most 2.0, max lift seen
  100 %), the hottest-file rule and "no signal = weight 1.0" all match the code and the data.
- The post implies churn reorders most lists ("Change frequency belongs in the ranking. Not as a tiebreak: as a
  weight."). On today's corpus it changes the top 5 of 169 to 384 repositories of 6,844 (2.5 % to 5.6 % of them);
  on 6,369 it changes nothing because no top task touches a hot file. The rewrite says so. (The corpus is mostly
  pinned open-source checkouts; 4,920 had no hotspot in the D15 window, so this says little about an active
  customer repository.)
- "A group of findings takes its hottest file, not its average" is true; the post said nothing measured about how
  often it matters. Median lift 100 % says lifted tasks typically touch THE hottest file.
