# L7 (B11 "A number you can re-derive"): notes, 2026-10-25

Everything here was run on the dev box as an anonymous reader would: no token, no account, public URLs only.
Full command log with outputs: `transcript.txt` (produced by `commands.sh`). Downloads are in `downloads/`, the
clone in `scorer-src/`, my helper scripts and generated inputs in `work/`.

## What a reader can get

1. Pages (all HTTP 200, fetched 18:29 CET): `/`, `/registry/`, `/verify/`, `/page-cli/`, `/implementations/`,
   `/surveys/`, `/surveys/lang/csharp/`, `/surveys/github/afterlutz/akkatecture/`.
2. The reference scorer source is public: `api.github.com/repos/code-assurance-initiative/CodeAssuranceIndex`
   reports `"private": false`; an anonymous `git clone --depth 1` (empty HOME, no credentials) succeeded at commit
   `c053a0260d7ba677e839ad9eb12c37d4048fd171` (2026-10-22 11:13:56 +0200).
3. Build: `dotnet build src/Cai.Cli -c Release` (.NET SDK 10.0.113), 0 errors, 4 warnings (XML doc params), 7.3 s.
4. The production public key set: `GET https://api.codeassuranceindex.info/api/registry/keys` (HTTP 200) returns one
   key, `cai-ed25519-2026-07`, Ed25519, `AQzI0jyJzu_Dv8g3RB4feO50Pk_3ejsD-X3k5u-auJ4`, active.

## What a reader can NOT get (findings, recorded precisely)

- **F1. No real signed delivery is obtainable anonymously.** The registry's read routes
  (`GET /api/registry/deliveries`, `/deliveries/{id}`, `/deliveries/{id}/metadata`) are `RequireAuthorization()` in
  the public source (`src/Cai.Web.Registry/Endpoints/RegistryEndpoints.cs`); only `/keys` and `/health` are anonymous.
  The survey page for AfterLutz/Akkatecture embeds no evidence bundle and no package (the only machine-readable data
  on it is the three widget attributes: headline, trend series, eight lens scores). Its link card "Verify this score
  yourself / Reproduce the number from the published evidence" points to `/verify/`, which has no download either.
  So the claim on the survey page ("reproduce the number from the published evidence") is not true for an anonymous
  reader today: the dimension evidence is not published, and no production-signed package is reachable. Likely a
  product defect (or a missing route: a public-record delivery download). I could not empirically confirm the 401
  because of F4; the source is unambiguous.
- **F2. The command the /page-cli/ page prints does not run.** The page says `cai score ./evidence.json --rubric
  <version>`. The CLI takes `--rubrics DIR` (the archive directory); with `--rubric` it exits 2:
  `error: score needs --rubrics <dir> (the published rubric archive)...` (transcript step 1). The repo README has the
  correct form.
- **F3. The page and the repo disagree on the packages.** /page-cli/ says Cai.Scoring and Cai.Delivery are
  "published by the Initiative to GitHub Packages". The public `src/Cai.Scoring/Cai.Scoring.csproj` says
  "NOT PUBLISHED YET: publish-packages.yml has never run and neither package exists on nuget.org or GitHub Packages".
  Build-from-source works, so this blocks nobody, but one of the two statements is wrong.
- **F4. Anonymous API budget was exhausted from this box.** Every `/api/rubrics/...` and `/api/registry/deliveries`
  call returned `429 rate limit exceeded` (with `retry-after: 1`, also after waiting 70 s), so I could not fetch the
  published catalog over the API to compare it with the git archive, nor call `/api/verify`. The limit is 15/day per
  IP and the box shares its IP with other sessions; a stranger on a fresh IP would likely get through. Worth knowing:
  the rate limit makes the API route a poor "check it yourself" path; the git archive is the dependable one.
- **F5 (observation, not checked further).** The production survey page says it was "Measured by watchdog.canine.dev
  using codehealth-analyzer measure-2026.10.3+preprod-fddbc92cb8df". A `+preprod` build label on a production
  corpus page is either a label leak or a corpus measured with a preprod-built engine. Someone should look.
- **F6 (wording on the CAI site, not ours).** /page-cli/ says "the honest instruction for an anonymous third party is
  to clone the repository"; /badge/ is described in the repo README as "the honest mark-usage policy".

## What I recomputed, and whether it matched

### A. The signed sample delivery (public, but a sample: key `cai-ed25519-sample`, not trusted by production)

- File `examples/cai-delivery.sample.json`, sha256 `bf94cd1127c109b990f18e52e85fa6b30db886266775320eef65dee87d90a324`;
  key set `examples/cai-delivery.keys.json`, sha256 `864536d4c1981914349f67351e68df6319ec11e52ea8ceec6879691343d0337c`.
- Reference program: `cai verify-delivery ... --keys ... --rubrics rubrics` gives
  `✓ signature verified — signed by codeassuranceindex.info (key cai-ed25519-sample), Ed25519`, subject
  `acme/checkout-api @ 3f9a1c2`, verdict `CAI 70.3 (Strong) · rubric rubric-2026.08.15`, and
  `✓ headline reproduces from embedded evidence (70.3 = claimed 70.3)`, exit 0.
- Independent check (my own 40-line Python, `work/ed25519_check.py`, RFC 8785-style canonicalisation + the
  `cryptography` 46.0.5 Ed25519 verifier): sha256 of the canonical payload
  `04ac0b86d794bdd5e1ff9c3fd845f98f8e61769b336b9c90911b850a1272aeb6`, signature VALID. So the signature format is
  checkable without the reference program.
- Tamper test: verdict 70.31 changed to 79.31 (one character). Canonical payload hash becomes
  `99b291bc4556d140e8170f2c8d18a80fe6b70accf53c90d56d99f38756539955`; my verifier says INVALID (exit 1); the
  reference program says `✗ SIGNATURE INVALID: signature does not verify (tampered payload or wrong key)` (exit 1).
- Note: /verify/ describes a separate "content hash" carried in the package. The sample package carries no such
  field (only `payload` and `signature {alg, keyId, canon, value}`); the signature over the canonical payload is what
  binds the content. Minor docs mismatch, not chased further.

### B. A real published survey: AfterLutz/Akkatecture (public repo), partial recompute

- Page: `https://codeassuranceindex.info/surveys/github/afterlutz/akkatecture/`, saved copy sha256
  `7d0994ab563d3b10670997b91b60a29bab855c7acbf96328d71c36532dbb1b9d`. It publishes: headline **57.8 (Adequate)**,
  22 October 2026, commit `3b948b48a78db9b10565acae946690158571dd26`, rubric `rubric-2026.10.5`, and eight lens scores:
  Code Health 54.5, Architecture 97.1, Maturity 51.5, Production-Readiness 70.7, Security & Compliance 67.1,
  Domain Modelling 97.9, Event-Driven 83.2, Performance 66.1 (Event Sourcing and Accessibility dark, "does not call
  for them"). Trend series `[55.2, 55.8, 56.1, 54.8, 55.5, 57.8]`, 20 July to 22 October 2026.
- Rubric catalog `rubrics/rubric-2026.10.5/rubric-catalog.json` from the clone, sha256
  `16476f49f4b69d5dcac8ea69659957257c7488611eda9e69ad0636c7d93515c3`; it pins `acrossLensQ 0.55`.
- Reference program, lens-only bundle built from the page's numbers (`work/extract_lenses.py`):
  `cai score` gives **CAI 57.8 (Adequate)** with weights maturity 0.454, codeHealth 0.250, performance 0.137,
  securityCompliance 0.076, productionReadiness 0.042, eventDriven 0.023, architecture 0.013, domainModelling 0.007.
  `cai verify` gives `✓ reproduced ... (claimed 58, Δ0.05)`, exit 0.
- Independent re-implementation (`work/owa.py`, 15 lines: rank worst first, weight 0.55^r, normalise, sum):
  **57.8455**, claimed 57.8, delta 0.0455. The page rounds lens scores to one decimal, so a delta under 0.05 is
  what rounding alone allows.
- **What this does and does not prove.** It proves the last stage (eight lens scores to the headline, under the
  rubric the page names) reproduces from published numbers, with two independent implementations. It does NOT
  recompute the lens scores from dimension evidence, and it does NOT verify a production signature, because neither
  the evidence nor the signed package is published (F1).
- Display nit: `cai verify` prints "CAI 58 ... claimed 58, Δ0.05" (integers), so the two numbers it compares are not
  visible in its own output.

## Post edits (post.md)

- New measured section "We checked one ourselves" + "Check it yourself" with the real commands, and the method card
  as a list.
- Corrected "Measured" class on "What that requires in practice": the four items are the delivery format (checked on
  the sample), but for public surveys only commit + rubric + lens scores are published today (F1). Said plainly.
- Determinism sentence now names evidence + rubric (the measurement version moves evidence; see L8 notes).
- No new gated numbers. No em-dashes. No "honest". Byline kept.

## The post's "Check it yourself" block, run verbatim

`reader-run/check.sh` is the code block extracted from `post.md` byte for byte (plus `set -e`), run in an empty
folder with only HOME and PATH set: fresh anonymous clone, build (0 errors, 7.1 s), then both checks. Exit 0.
Output in `reader-run/check.out`: `✓ signature verified`, `✓ headline reproduces ... (70.3 = claimed 70.3)`,
`CAI 57.8 (Adequate)`, `✓ reproduced ... (claimed 58, Δ0.05)`. In the post, the expected-output comment for step 1
is paraphrased ("signature verified, signed by ...") because the program's own line contains an em-dash.
