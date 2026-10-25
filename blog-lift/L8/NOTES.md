# L8 (B10 "What a score is for"): notes, 2026-10-25

Reference scorer: the one built in `../L7/scorer-src/CodeAssuranceIndex` from an anonymous clone of the public repo at
commit `c053a0260d7ba677e839ad9eb12c37d4048fd171` (2026-10-22). Command log with outputs: `transcript.txt`
(`commands.sh`). Inputs in `inputs/` (copied from the clone and from L7's page extraction), outputs in `runs/`.

## 1. Determinism: the same evidence scored twice

- Public sample evidence (`examples/evidence.sample.json`, 14 dimensions + 2 meta-dimensions, names
  `rubric-2026.08.15`), full dimension-to-headline fold, run twice: both outputs sha256
  `cedfeaec45ceeb56d5ab118c3898d8eba6116fe5152a14756411a2bb50fb167c`, `cmp` exit 0. Result `CAI 70.3 (Strong)`,
  maturity 65.1 weight 0.457, securityCompliance 72.0 weight 0.251, productionReadiness 74.6 0.138, architecture 77.3
  0.076, codeHealth 79.9 0.042, performance 80.0 0.023, accessibility 85.0 0.013.
- AfterLutz/Akkatecture lens-only bundle (from the survey page, see L7), run twice: both sha256
  `211e7c3c4449e6e09154ce150fa95f81fb21bcf1f68f0d4d312563a4adcdd4d9`, `cmp` exit 0. Result `CAI 57.8 (Adequate)`.
- Scope of the claim: same input file, same build, same machine, two runs. It shows the fold has no hidden state
  (no clock, no randomness, no network). It does not show cross-machine or cross-build determinism; I ran one box.

## 2. The rubric version the delivery names

- The sample evidence names `rubric-2026.08.15`; the signed sample package names it in `payload.rubricVersion` and
  `payload.evidence.rubricVersion`, and `cai verify-delivery` prints `rubric rubric-2026.08.15` (L7 transcript).
- The Akkatecture page names `rubric-2026.10.5`, and its history panel says
  "Rubric changed (rubric-2026.10.1 → rubric-2026.10.5): scores are not directly comparable" between its previous
  and current measurement (CAI 56 → 58). That is the page flagging a rubric change on a real codebase.
- Without `--rubrics`, `cai score` refuses (exit 2): "A CAI number is only meaningful under the rubric it was computed
  with, so there is nothing to fold under without it." There is no default rubric.

## 3. One fixture under two rubric versions

No public fixture exists that is scored under two rubric versions with two different numbers. What I ran instead: the
same sample evidence, its `rubricVersion` field relabelled to each of the 49 archived versions, folded each time.

- 18 versions (rubric-2026.06.0 through rubric-2026.08.17) fold it to **70.3**, the same number.
- 31 versions (rubric-2026.08.18 onward) **refuse** it, exit 2:
  - 08.18 to 10.2 (28 versions): "Dimension 'D8' is declared in category 'code-quality', but rubric ... publishes it
    in 'testing' ... the re-homing must mint a new rubric version".
  - 10.3 to 10.5 (3 versions): "'M1' is a meta-dimension in rubric ... and was sent as a dimension ... This rubric
    version is closed".
- Reading: a newer rubric does not silently re-price old evidence; when the evidence does not fit the newer rules the
  scorer refuses it rather than produce a number. So "show both" has this answer here: the second
  rubric gives no number at all. (Relabelling the field is my experiment, not something a producer does.)

## 4. Corrections the post needed (claims re-checked)

- **"a golden-snapshot tripwire fails the build when a fixture's scores move while the rubric version has not"**: out
  of date. Our engine's tripwire (in our private build, not public) has been keyed on the MEASUREMENT version since
  measure-2026.10.1: scores that move without a measurement-version bump fail the build; a rubric bump is always a
  measurement bump too. The post now says this and states it as our account. What the public repo itself enforces:
  every rubric version from rubric-2026.09.13 on must pin its own scoring constants (q values, gate, band cutlines),
  and evidence that contradicts the named rubric is refused (section 3 above).
- Bands 25/50/70/90 and labels Critical/Weak/Adequate/Strong/Exemplary: match the rubric-2026.10.5 catalog
  (`bands: poor 25, fair 50, healthy 70, exemplary 90`) and the repo README.
- "headline band never more than one band above the weakest category": matches the public coherence cap (number
  unchanged, label capped).
- Worked example added for "the weakest area pulls the headline down": Akkatecture's eight lens scores have an
  equal-weight mean of **73.5 (73.5125, Strong)**; the published worst-first headline is **57.8 (Adequate)**.
  Maturity (51.5) carries 45.4 % of the weight, Domain Modelling (97.9) 0.7 %.
- "A dimension that cannot be measured abstains": real example on the same page, Event Sourcing and Accessibility
  lenses dark ("this codebase's architecture does not call for them").

## 5. Findings carried over from L7 that touch this post

- The survey page's "Reproduce the number from the published evidence" is not possible anonymously (no evidence
  published; registry reads need an account).
- The production page's measurer line reads `measure-2026.10.3+preprod-fddbc92cb8df`.

## 6. The post's "Check it yourself" block, run verbatim

`reader-run/check.sh` is the block from `post.md`, run with `bash -x` in an empty folder (fresh anonymous clone,
fresh build, 6.4 s). Output `reader-run/check.out`: run1/run2 sha256 both
`cedfeaec45ceeb56d5ab118c3898d8eba6116fe5152a14756411a2bb50fb167c`, the SAME hash as the runs on the L7 build, so two
independent clones and builds on this machine gave identical bytes. `head -1` = `CAI 70.3 (Strong)  ·  rubric
rubric-2026.08.15`. No-archive call refused. Relabelled to rubric-2026.10.5: refused with the M1 message. The script
exits 2 because its last command is the intended refusal.
