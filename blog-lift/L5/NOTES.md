# L5 (B1 "Findings count is not analysis depth"): figures re-derived from production, 2026-10-25

All queries ran through the read-only workflow `prod-query.yml` (database `kennel_watchdog`), dispatched by
`../tools/q.sh`. SELECT only. Each `.sql` here has its raw run log next to it as `.out`.

## Population (ratio.sql, second statement)

- Unit: one repository = its most recent metric point that is not a bridge run, not degraded, not partial
  (`IncompleteReason` null) and carries a dimension-state map.
- Corpus = `Repositories.CorpusLanguage` in (csharp, go, rust), not hidden.
- C#: 410 corpus repositories, 409 with a qualifying scan. Go: 260 / 259. Rust: 448 / 444. Total analysed: 1,112.
- Findings per repository = sum of `run_dimension_metrics.FindingCount` over every dimension of that run (the
  same uncapped total the admin findings inspector uses).
- Scan dates: 2026-08-05 to 2026-10-25; 402 of 409 C#, 252 of 259 Go and 442 of 444 Rust scans are from October.

## Findings per repository (ratio.out)

| | C# | Go | Rust |
|---|---:|---:|---:|
| repositories | 409 | 259 | 444 |
| median | 23 | 32 | 45.5 |
| mean | 55.9 | 99.6 | 94.1 |
| p25 to p75 | 11 to 49 | 16 to 81 | 21.75 to 84 |
| max | 1,124 | 4,083 | 2,037 |
| median production LOC | 6,246 | 5,123 | 43,799 |
| median findings per KLOC | 4.06 | 4.57 | 0.97 |
| pooled findings per KLOC | 1.47 | 2.01 | 0.56 |

Ratios (computed from the above):

- C#/Go: median 23/32 = **0.72x**; mean 55.9/99.6 = **0.56x**.
- C#/Rust: median 23/45.5 = **0.51x**; mean 55.9/94.1 = **0.59x**.
- Per KLOC (median): C#/Go 4.06/4.57 = 0.89x; C#/Rust 4.06/0.97 = **4.19x**. Pooled: 0.73x and 2.63x.
  The per-repository and per-KLOC ratios point in opposite directions for C# vs Rust, because the median Rust
  repository in this corpus is seven times the size of the median C# one (43,799 vs 6,246 production lines).

Size dependence (robust.out, last statement): correlation of ln(findings+1) with ln(LOC+1):
C# 0.395, Go 0.743, Rust 0.492 (raw Pearson 0.300 / 0.651 / 0.403).

Tails (robust.out): largest C# 1,124 (phongnguyend/Practical.CleanArchitecture, 93,556 LOC); largest Go 4,083
(golang/go, 874,728 LOC); largest Rust 2,037 (juspay/hyperswitch, 919,298 LOC). Every language has repositories
at 0 findings. Comparing the largest of one language with the smallest of another gives any ratio you like,
which is how the original 10 to 20x arose.

## Engine builds (robust.out, same-engine.out, loc-pair.out)

The latest scans are not on one engine build: C# and Go mostly `measure-2026.10.3+preprod-fddbc92cb8df`
(321 C#, 162 Go, 36 Rust; 2026-10-21 to 10-23), Rust mostly `preprod-fe8540b5da9b` (403 Rust; 2026-10-08 to 10-14).
Per-build slices (each repository's latest clean run on that build):

| build | C# n / median | Go n / median | Rust n / median | C#/Go | C#/Rust |
|---|---|---|---|---:|---:|
| measure-2026.10.3 | 321 / 22 | 162 / 22.5 | 36 / 33 | 0.98x | 0.67x |
| measure-2026.10.6 | 76 / 32.5 | 81 / 68 | 2 / 291.5 | 0.48x | (n=2) |
| preprod-fe8540b5da9b | 89 / 27 | 89 / 75 | 406 / 47 | 0.36x | 0.57x |

The slices differ mainly in WHICH repositories they hold (median LOC 4,048 C# on 10.3 vs 52,315 on fe8540);
the 10 C# repositories scanned on both builds have identical LOC on both (loc-pair.out), so LOC is not a build
artefact. C#/Go ranges 0.36x to 0.98x and C#/Rust 0.51x to 0.67x across every slice with n >= 36. In no slice
does C# emit more findings per repository than Go or Rust.

## Dimensions resolved (ratio.out)

`dims_measured` = entries of the run's dimension-state map with state `measured` (confidence > 0, no capability
gap). The map lists 42 dimensions per run (median, every language).

- Median dimensions resolved: C# 27, Go 24, Rust 26 (means 27.07, 24.19, 25.71). Gaps (state `gap`) are 0 at the
  median: applicable median equals measured median in every language.

**NOT put in the post.** ARTICLE-BAR §2: "no per-language depth or noise figure before the measurement that owns
it clears its gate", and the appendix trap for B1 says the same. These three medians are a per-language depth
figure. They are recorded here only. If the owner wants them published, that is a gate decision, not an edit.

## Compared with the July 2026 figure the post cites

The July review (training corpus: 66 C#, 53 Go, 68 Rust audited repositories, `tools/train/metrics/*.jsonl`) had
medians 396.5 / 461 / 337, so C#/Go 0.86x, C#/Rust 1.18x (medians), 1.18x and 1.29x (means). Different unit
(training-round audited findings, an engine that still ran model-backed dimensions), so only the ratios compare.
Then C# sat between Go and Rust; today it is below both on every slice.

## What in the existing post the data contradicts

1. "Roughly parity, with the direction of the difference depending on which repositories you draw." Today the
   direction does not depend on the draw: C# is below Go and Rust per repository on every slice (0.36x to 0.98x).
2. "We were not wrong that some languages resolve more of the catalogue than others. That difference is real and
   it held." The July source behind it was C# 75.0 % vs Go/Rust 41.7 % (~1.8x). Today's medians are 27 / 24 / 26
   resolved dimensions, a far smaller difference (1.04x to 1.13x). Whatever the gated figure turns out to be, "it
   held" is not supported by today's data, and the sentence is a per-language depth claim besides. Removed.
3. "Class: Measured, over our full training corpus." The figure is now from the production corpus scans.

## Not available

- Rubric version per scan was not pulled (only engine build). The engine build names are in this file.
- A public per-repository file for outside checking does not exist (worklist L19: no public reproduction package).

## Catalogue size (catalogue.sql)

The dimension-state map lists 42 dimensions on 1,111 of the 1,112 scans (one Rust scan lists 39).
