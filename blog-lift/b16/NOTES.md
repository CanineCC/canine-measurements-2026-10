# B16 "A rebuild range is not a valuation" (imprint a5e2cc6b87814afbb3bdd0aed391082c), lift L10

Fetched 2026-10-25, about 17:30 UTC. Raw pages in `downloads/`.

## Example used

3b1b/manim, current report format (every one of the 28 public reports prints a rebuild range; manim is the most recent
one whose derivation block is in the current wording; the list's 29th link is not a report, see b8/NOTES.md).

- Public report: https://app.watchdog.canine.dev/api/oss/3b1b/manim/report
- CAI page: https://codeassuranceindex.info/surveys/github/3b1b/manim/
- Saved: `downloads/3b1b__manim.html` (+ `.txt`), `downloads/cai-survey-3b1b_manim.*`, `downloads/domcyrus__rustnet.*` (older format, for the flags)

## Figures (manim report, block "Rebuild cost", re-read 2026-10-25)

- Measured 23 October 2026, 02:32 UTC, code version fafa083, rubric 2026.10.5.
- Headline: "Rebuild cost: about €26,000 · Estimate"
- "Cost to rebuild €8,500 to €43,000, for 141 to 448 hours of work, about 0.2 person-years for one engineer"
- "Difficulty of the problem Standard, judged from the kind of software and how it is built."
- "Quality factor ×0.8 at a score of 59. ... the factor is ×1.0 at a score of 70, lower below it and higher above it."
- "Size Medium: 22,971 lines of product code"
- Method: hours priced "at €60 to €95 an hour"; declarations and boilerplate at a fast rate, logic at a slower one; logic multiplied by difficulty and quality factor; "can be about 30% off either way, and it moves most with the hourly rate and the difficulty"; "every line is priced as straight logic, which keeps the estimate on the low side".
- Arithmetic check: 141 h x €60 = €8,460 -> €8,500; 448 h x €95 = €42,560 -> €43,000. Reproduces.

## ★★ CONTRADICTIONS WITH THE POST (flag to owner)

1. **"Never a point" is false on every public report.** The post: "every figure is a range ... never a point", and "a
   point figure is what gets quoted". The manim report's headline is "Rebuild cost: about €26,000", and its Diagnosis
   says "This code would cost about €26,000 to build again, about 0.2 person-years". Every public report's header line
   that carries a size line prints "Estimated rebuild effort: about N person-years" (or "rebuild ~N person-years"). Post revised to say what is true (the range is printed and
   the point sits beside it). Better fix: drop the point headline in the product.
2. **The three refusals are NOT printed with the rebuild range on any of the 28 public reports.** "not a quotation, a
   valuation, or a certified figure" appears on exactly one public report (domcyrus/rustnet, 14 Oct), and there it is
   attached to the (since removed) payback figure, not to the rebuild range. In the product, the wording lives in
   Assay's remediation-exposure sentence (decision reports, not public). So the post's "Measured. This is the published
   wording" and "printed with the number rather than buried in a methodology appendix" are true only of Assay's
   remediation exposure, not of the public rebuild range. No public example of the refusals beside a rebuild range
   exists. Post revised to say where they are printed and where not.
3. **The assumption is a price, not only productivity.** The post says the conversion rests on "an assumption about how
   much software an engineer-day produces". The report states its assumptions as an hourly rate (€60 to €95),
   per-line rates for boilerplate vs logic, a difficulty tier and a quality factor. Post revised.
4. **Derivation not in the same sentence.** The post: "a range with its derivation method stated in the same sentence".
   The report puts the range in one line and the method in a separate "How the estimate is made" paragraph. Post
   revised to "printed with it".
5. **Older public reports use the word "value"/"valuation".** domcyrus/rustnet (14 Oct): section title "Rebuild cost &
   value ~ Modeled"; leytonoday/Atlas-API-Modular-Monolith (29 June): "Rebuild cost & value" and "Evidence: valuation:
   Small, ~0.1 person-years rebuild". The current format (manim) says "Rebuild cost". Stale public reports carry the
   very framing the post refuses; owner may want them re-surveyed.
6. **The 0.1 person-year floor contradicts the hours on small codebases (public, defect).**
   kvaps/keepass-url-overrides (28 lines): "Cost to rebuild €8 to €40, for 0 to 0 hours of work, about 0.1 person-years
   for one engineer". silviucpp/ezstd: "Cost to rebuild €190-€950 (0.1 person-years (3-10 h), ~1 engineer)". 0.1
   person-years is roughly 170 hours, not 0 or 3-10. valehasadli/emitrix: 12 to 37 hours, "about 0.1 person-years".
   The person-year figure appears to be floored at 0.1. A reader checking the arithmetic the post invites would find
   it. Product fix needed (print hours, or "under 0.1 person-years"). Not used in the post.
