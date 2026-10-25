# B13 "Survey clarity is not language quality" (imprint 2a0e370d95444b88a19fddd3caeccbfd), lift L11

Fetched 2026-10-25 17:29 UTC (`date -u` at download: Sun 25 Oct 17:29:57 UTC 2026).

## Source

- Live endpoint: https://watchdog.canine.dev/api/public/language-support, saved `downloads/lang-support.json`
- Languages page: https://watchdog.canine.dev/languages/, saved `downloads/languages.html` (+ `.txt`)

## Figures (lang-support.json as fetched)

- note: "FIT is survey clarity — how clearly a language leads to a complete architecture survey. It is NOT a measure of language or code quality." (the endpoint's own text has an em-dash; the post quotes only the last sentence)
- 17 languages; supportKind: 16 Deep, 1 Structural (JavaScript).

| Language | applicability | supportKind | band | signedOffOn | coveredLenses | notApplicableLenses |
|---|---|---|---|---|---|---|
| C# | 10 | Deep | FULL | **null** | DDD, Event sourcing, Event-driven, Vertical slice, Correctness, Structural | (none) |
| TypeScript | 8 | Deep | HIGH | 2026-07-18 | DDD, Event sourcing, Event-driven, Vertical slice, Structural | Syntax-level correctness, DI segregation, Compiled-output efficiency |
| Ruby | 6 | Deep | MEDIUM | 2026-07-13 | DDD, Event sourcing, Event-driven, Vertical slice, Correctness | DI, god-class/LCOM |
| JavaScript | 4 | Structural | LOW | 2026-07-18 | Structural, Module graph, Dependency hygiene, Complexity | Deterministic DDD/Event-sourcing model-shape lenses (advisory only - untyped) |

Summaries quoted/paraphrased: TypeScript "reads TypeScript with the TypeScript compiler's own tools"; JavaScript "reads
JavaScript with the TypeScript compiler's own tools. It reads how the modules depend on each other, how complex the code
is, how its classes are shaped and which code changes which data."

## ★ CONTRADICTIONS WITH THE POST

1. **"Each entry carries a sign-off date" is false for C#.** C#'s `signedOffOn` is `null` (the other 16 carry a date,
   2026-07-11 to 2026-07-18). Post revised: "every entry except C# carries a sign-off date". Product fix is the better
   one (give C# its date).
2. **The "Next" line overclaims the languages page.** The post says the languages page shows "the lenses that resolve
   and the date each was signed off". The page shows the band word (FULL ... LOW), the kind (Deep / Structural) and a
   summary per language, but NO sign-off dates and NO 0-10 number (grep of the saved page: no dates, no "/10"). The
   dates and numbers are only in the JSON endpoint. Post revised to link the endpoint for dates and numbers.
3. **The number cannot be derived from the lens list.** The post says the score is published "together with the thing
   that produces it: which lenses resolve". Covered-lens counts vs score: C# 6 -> 10, Dart 6 -> 8, Erlang 6 -> 7, Go
   6 -> 7, TypeScript 5 -> 8, Python 5 -> 7, Ruby 5 -> 6, Elixir 4 -> 8, JavaScript 4 -> 4. A reader trying to
   recompute it from the endpoint cannot. Post revised ("what lies behind it", and a paragraph saying the number is
   our summary until the endpoint breaks it down per lens). Product fix: publish the per-lens resolution behind it.
4. Not a contradiction but worth knowing: JavaScript's covered lenses include "Module graph", which B6 said needs a deep
   model (flagged in b6/NOTES.md).
5. Gate check (ARTICLE-BAR §2: no per-language depth figure before its gate): the 0-10 applicability number is already
   public on the live endpoint and the post already published per-language kinds; it is a coverage statement, not a
   depth-of-detection or noise measurement. I judged quoting it fine. If the owner reads "depth" to include this
   number, drop the four numbers and keep the kinds.
