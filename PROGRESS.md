# WP-40 and the method-you-can-check wave — progress

Worktree `<checkout>` (branch `blog-method-wave`). Scratch and tooling in
`~/Hentet/kennel/blog-method/` (e1, e2, b26, tools). Engine for every measurement: cca-phase-2 `a3f3f35ad9`,
detached worktree `<checkout>`.

## Task list

- [x] B26 concentration re-derived from the cycle-1 export (`b26/concentration.py`): 9,071 rows, 268 repos, top 10 = 54.7 %, half the rows from 9 repos.
- [x] B27 cap re-derived from prod per-repo counts (read-only prod-query run 40160534119, `b26/cap.py`): 50–250 cap moves csharp −15.5, java +9.4 (documented +9.3); 14 cap choices give 12 orderings of 17 languages (`b26/cap_sweep.py`).
- [x] Found: the documented csharp leave-one-out span "11.2–24.4 %" does not reproduce; re-derived 9.9–27.1 %.
- [x] B24 figures verified from `docs/plans/deterministic-engine/adjudication/`: 12 of 14 first adjudications failed (not "every"); D26 50 / 32.5 / 77.8 % are three parameter versions, not one sample judged two ways; M4 A 0 vs B 767 rows.
- [x] B25: REGISTER "did-not-clear 0" was recorded on 12 of 206 scored repos; `register.py` now prints the coverage (test_register_flag_coverage, falsified).
- [x] E1 done (freeze b1ed0ab162, results 331da9168a): ρ 0.72 [0.65, 0.78] on overall; size baseline 0.71, difference +0.01 [−0.05, +0.07] → loss condition 2 holds; partial ρ given length 0.37. Disagreements: 7 our miss, 1 debatable, 2 out of scope. Engine defect found and filed on prod: every non-UTF-8 Java file silently left out of the code model, no partial warning (backlog 01a1715a-4a1c).
- [~] E2/E3 RUNNING (freeze 42fae3dd6d; driver `e2/driver.py`, log `e2/driver.log`): before = tag `architecture-baseline-2026-09-18`, after = cca-phase-2 `a3f3f35ad9`; 46 identical-body pairs over the D2 threshold; draw seed 20261025 (20 pairs × 2 sides × 3 repeats = 120 runs, pilot p37/p05 discarded). Harness `e2/run_one.sh`, gate `e2/gate.py`, metrics `e2/extract.py`. FREEZE §E2 before the first counted run.
- [ ] E4: LLM reviewer vs the deterministic gate, on the E2 patches.
- [x] WP-40 §E2/§E3/§E4 rewritten and frozen (42fae3dd6d).
- [ ] Draft B21–B27 in the new product structure (CCA, Assert, Assure, Assay), drafts/ + appendix updates.
- [x] **resourcecenter.canine.dev mockup** published https://claude.ai/artifact/8i4hmdnCyVBrT5wtSUSAV4 (source `~/Hentet/kennel/resourcecenter/mocks/`; done inline: the launch hook refused 3× on a busy box). Was: — hub (bento, ⌘K, filter tabs, typed cards), 3-column article view, product colours from the approved brand (`.claude/worktrees/cca-phase-2/docs/design/brand/`) as scoped accents under one site identity; publish as an Artifact; mocks in `~/Hentet/kennel/resourcecenter/mocks/`. Launch hook refused twice (busy box) — retry each iteration.
- [ ] **LATER (owner, 2026-10-25): revisit the VSA layout for agents, then re-measure with the E2 harness** — goal: fewer
  tokens AND faster AND same-or-better held rate. E2 baseline to beat: AFTER/BEFORE tokens 1.86, wall 0.63, held 60/60.
  Mechanism to address first: 52/60 AFTER runs built from `engine/src/Core/` (no project there). Re-run = same draw,
  same prompt, same model, a third snapshot.

## Owner GO, 2026-10-25 (later)
- [x] E6 done (74b3a07231): guided 60/60 held, unguided 34/60, +43 points (25 to 63); limits in e6/RESULTS.md. B25 harder-code section filled; B28 (Assure) drafted.
- [x] E4b done: false approvals 17 of 78 asks (21.8 %, 10 to 35), 4 of 26 bad patches approved by majority; e4/RESULTS-E4b.md. B24's reviewer section filled.
- [x] E7 prepared: frozen (wp40-e7-freeze), five PRIVATE copies under CanineCC (e7-umbraco-cms, e7-avalonia, e7-newtonsoft-json, e7-benchmarkdotnet, e7-serilog). Owner after 2026-11-01: grant app access, connect, mint keys.
- [x] B21–B27 drafted (B25 held for E6/E7); full review of all posts: `docs/marketing/blog/REVIEW-2026-10-25.md`.
- [x] Revised the 10 REVISE posts and the 5 merges in imprint (still InReview, nothing published); log in blog/REVIEW-2026-10-25.md.
- [ ] Resource center GO: imprint step 1 (approval gap + signature hash + publish hold), then the proposal's order (subagent when the box admits).
- [x] D28 GO: on main 3a102b4f1a (all 31 test projects green, Agents re-run after the final rebase).
- [ ] VSA revisit KEPT (owner): refactor our layout with the E2 lessons, then re-measure.
- [x] Java non-UTF-8: backlog 01a1715a-4a1c (filed and verified). llm-bakeoff red: backlog 01a1717e-05b0.
