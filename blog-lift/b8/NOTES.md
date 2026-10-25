# B8 "What not fixing it costs" (imprint 75b69230b0804c1fa1becdd0a192de28), lift L10

Fetched 2026-10-25, about 17:30 UTC. Raw pages in `downloads/`.

## Example used

atomvm/AtomVM, current report format (one of only 4 of the 28 public reports that print a cost figure at all:
atomvm, github/spec-kit, DualBrain/bsharp (percentage only), domcyrus/rustnet (old format)).

- Public report: https://app.watchdog.canine.dev/api/oss/atomvm/AtomVM/report
- CAI page: https://codeassuranceindex.info/surveys/github/atomvm/atomvm/
- Saved: `downloads/atomvm__AtomVM.html` (+ `.txt`), `downloads/cai-survey-atomvm_atomvm.*`, plus rustnet and bsharp reports for the flags below.

## Figures (AtomVM report, Diagnosis card "What hard-to-read code costs each year", re-read 2026-10-25)

- Measured 23 October 2026, 00:14 UTC, code version 3a9ea46 (CAI page: 3a9ea46b8cf28066caf126c46119dc58f950de5f), rubric 2026.10.5, survey ID cd_84a9fdf170364ce78ae1ee45ff8135b6.
- Four code-quality dimensions (cyclomatic, cognitive, duplication, cohesion) "average 7.3 out of 10".
- Extra work "2% to 5% on every change".
- "about 13,203 lines over the last 90 days, which is about 53,546 lines a year".
- "an estimated 2.7 to 17.8 engineer-days a year".
- Method line: changed lines measured; two assumptions: "code scoring 8 out of 10 or more adds no extra work, and each point below 8 adds 2.5% to 5.6% to every change; and an engineer changes 150 to 400 lines in a day. The result is a range for planning, not a measurement."
- Arithmetic check: 53,546 / 400 x 2 % = 2.68; 53,546 / 150 x 5 % = 17.85. Reproduces 2.7 to 17.8.
- Partial abstention, public: DualBrain/bsharp report (https://app.watchdog.canine.dev/api/oss/DualBrain/bsharp/report, 21 Oct 2026) prints the 7.3 / "2% to 5%" sentence and no yearly figure.

## ★★ CONTRADICTIONS WITH THE POST (flag to owner)

1. **The post's core claim about the product is out of date.** The post says the product prints two numbers (debt =
   effort band of the ranked fix; interest) and their ratio ("how long the debt takes to pay for itself"). The current
   report prints ONLY the interest (extra work per change, and per year). The debt and break-even were removed on
   2026-10-14 (owner review; the card "charged the whole yearly cost of hard-to-read code to whichever action ranked
   first, even one unrelated to it"). Post revised: the debt bullet now says the report does not price it, and why.
2. **A public report still prints the removed, defective figure.** domcyrus/rustnet
   (https://app.watchdog.canine.dev/api/oss/domcyrus/rustnet/report, measured 14 Oct 2026 05:49 UTC) says "The
   top-ranked fix costs roughly 1-3 engineer-days once. Not doing it costs about 24.2-161.3 engineer-days every
   year ... breaks even in roughly 1-2 months". Its top-ranked fix is "Resolve the 1 No ADRs found finding(s) in ADR
   Quality": writing an ADR does not remove code-quality drag, which is exactly the defect. It is live on the public
   report list. NOT used in the post. Owner decision: re-survey rustnet or leave it.
3. **"Same sentence" is not what the product prints.** The post says every figure carries its range and assumption "in
   the same sentence as the number". In the current card the assumptions are in the next paragraph ("How this is
   estimated"); rustnet's older card had them in a separate "Method" sentence too. Post revised to say "directly under
   the number". (The post itself now puts figure + assumption in one sentence.)
4. **A second assumption the post called measured.** The post lists "the code-quality signals" as Measured and only the
   lines-per-engineer-day band as Assumed. The report names TWO assumptions: the drag per point below 8 (2.5 %-5.6 %)
   and the 150-400 lines. The signals are measured; turning them into a drag percentage is assumed. Post revised.
5. **The printed drag does not reproduce from the stated rule.** At 7.3 the stated rule gives 0.7 x 2.5 % = 1.75 % to
   0.7 x 5.6 % = 3.9 %; the report prints 2 % to 5 %. The product holds the range at a minimum of 2 % and 5 %, which
   the method line does not say. (Our account, from the product's behaviour; not on the public page.) The post says so
   in one sentence. Better fix: add the floor to the method line in the product, then drop that sentence.
6. **Refusal list is out of date.** The post lists five refusals incl. "nothing is ranked". Current behaviour: no card
   when product code is under 2,000 lines, when no code-quality signal is measured, or when the signals average 7.5 or
   more; the yearly part only is dropped (percentage stays) when there is no churn signal, a window under 30 days, or
   zero churn. "Nothing is ranked" no longer applies. Also: the method line says "8 or more adds no extra work" but
   the card abstains from 7.5, so code at 7.5-7.9 gets no figure although the stated rule would give one. Post
   revised. **Image `media:df26d68865354fada488ba0e56db4850` ("the five conditions") is now wrong and needs redrawing**;
   kept in place in post.md.
7. Post said "150–400" with an en-dash; ARTICLE-BAR forbids en-dashes. Replaced with hyphens/"to".

## Other defects seen while reading (not post claims)

- The public report list links 29 entries but only 28 are reports: https://app.watchdog.canine.dev/api/oss/ruben-rasmussen/auth/report serves the public survey list instead of a report (saved as `_shared/downloads/reports/ruben-rasmussen__auth.html`). A broken link on a public page.
