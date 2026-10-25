# Canine Development: measurements behind the "method you can check" articles (October 2026)

This is the reproduction package the method cards in our articles refer to. Every figure in those articles comes
from a file here, a query here, or a public page the article links. Paths that pointed into our machines are
rewritten as `<checkout>`, `<scratch>` and `<home>`.

**Who measured:** Canine Development, which builds the Canine Code Analyzer (behind Assert, Assure and Assay) and has
an interest in good results. That is why the analyses were fixed in advance where the card says so.

## What is here

| Folder | Experiment | Article |
|---|---|---|
| `PREREGISTRATION-WP-40.md` | The pre-registrations (E1 to E7, E4b, E4c), with every dated amendment | all |
| `e1/`, `e1-encfix/` | E1: complexity against expert maintainability ratings (304 Java classes); the re-run after our encoding fix (exploratory) | *Does a maintainability score agree with experts?* |
| `e2/` | E2: the same 20 methods before and after we split our codebase into slices, 120 agent runs | *Does the shape of a codebase change what an agent spends?* |
| `e4/` | E4, E4b, E4c: an AI reviewer against the deterministic gate, on easy and hard patches, two reviewer models | *A gate an agent cannot talk its way past* |
| `e5/` | E5: how many agent-reported fixes the next scan confirmed, on our own repositories | *Your agent says it is fixed. Who checks?* |
| `e6/` | E6: an agent given our finding against an agent asked plainly, 20 hard methods, 120 runs | the same two articles |
| `e7/` | E7: the pre-registered run on public repositories (not yet run) | (forthcoming) |
| `b2-classes/` | The five-class split of one verification cycle's noise | *What a false positive actually is* |
| `b26-b27/` | Concentration of noise in a few repositories; the findings-cap sweep | *Ten repositories wrote half the result* |
| `blog-lift/` | Worked examples and production queries behind the revised articles (B1, B5, B6, B8, B9, B10, B11, B13, B15, B16) | each article's method card |

## What is not here, and why

- **Our engine's source.** The patches in `e2/runs` and `e6/runs` are diffs of our own code, so they show fragments of
  it; the engine itself is not published. The public scorer that turns evidence into a CAI score is open:
  https://github.com/code-assurance-initiative/CodeAssuranceIndex
- **Customer data.** Production queries were read-only and the files keep only aggregates and public open-source
  repository names.
- **The datasets we did not create.** E1's expert labels are on figshare (Schnappinger, Fietzke and Pretschner,
  ICSME 2020, CC BY 4.0); `e1/` gives their sha256 so you can check you have the same file.

## Limits stated in the articles, repeated here

Several experiments measure our own code with our own agents (E2, E5, E6). Verification-cycle noise was classified by
our machine judge, and the human agreement check had not been done when this package was made. AI agents, not people,
adjudicated the deterministic-engine rounds. E7, on public repositories, is pre-registered and not yet run.

## Licence

Text and data: CC BY 4.0. Scripts: MIT. See `LICENSE`.
