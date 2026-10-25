# E2/E3: exploratory notes (NOT part of the frozen analysis)

Read after `analyse.py` ran once as frozen (`results.txt`). Each is labelled exploratory in any post.

1. **Mechanism of the token gap.** First-call context is the same on both sides (median 17,396 vs 17,387 tokens) and
   the first file read is the same size, so the gap is in extra turns (mean 6.8 after vs 4.3 before). 52 of 60 AFTER
   runs hit `MSB1003` ("does not contain a project or solution file"): the agent runs `dotnet build` from the first
   folder under `engine/src/`. In BEFORE that folder IS the project (`CodeHealth.Core`); in AFTER it is `Core/`, which
   holds the slice projects one level down, next to the file. 0 of 60 BEFORE runs hit it. AFTER runs without the error
   still cost more (mean 102,880 vs 65,735 tokens; n = 8).
2. **The five BEFORE test failures are not the agent's.** On the unchanged code with the same filter: p20 and p36 fail
   1 test already (pre-existing); p04 passes 6,234/6,234, and the p04-before-1 patch, re-run twice, also passes
   6,234/6,234: the failure was flaky under box load.
3. **The gate's test filter is broader than designed.** It collects every `class X` in test files naming the type,
   including words in comments (`C`, `is`), so `FullyQualifiedName~.C` runs thousands of tests. That widens the
   behaviour check; it does not narrow it.
4. **The claim rule (E3) measured hedging, not over-claiming.** 1 of 120 runs "claims success" under the frozen rule
   because 118 of 120 final messages say, in words, that the agent did not run the tests or a complexity check and had
   not confirmed the score ("didn't" 111×, "did not" 17×). Every one of those 120 fixes held.
