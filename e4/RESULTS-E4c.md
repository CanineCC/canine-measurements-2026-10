# WP-40 §E4c results (frozen at tag wp40-e4c-freeze; amendment 1 recorded before the run resumed)

E4b repeated with one change, the reviewer model: claude-opus-5-5 instead of claude-sonnet-5-5. Same prompt, no tools,
the finding with its threshold and the diff, 3 asks per patch, the same 120 E6 patches and the same gate truth (94 good,
26 bad). None excluded. Verdicts: 247 APPROVE, 83 REJECT, 23 TIMEOUT, 7 UNPARSEABLE (TIMEOUT and UNPARSEABLE count in
the denominators as neither, per amendment 1).

| | E4b (claude-sonnet-5-5) | E4c (claude-opus-5-5) | stronger minus E4b, paired over patches |
|---|---|---|---|
| False approvals (APPROVE on a bad patch) | 17 of 78 asks, 21.8 % (10 to 35) | 19 of 78, 24.4 % (11.5 to 38.5) | +2.6 points (−5.1 to +11.5) |
| False rejections (REJECT on a good patch) | 14 of 282, 5.0 % (1.4 to 9.2) | 26 of 282, 9.2 % (5.0 to 14.2) | +4.3 points (+1.4 to +7.4) |
| Bad patches approved by a majority | 4 of 26 | 7 of 26 | 4 are approved by a majority under both |
| Patches with three identical answers | 108 of 120 | 84 of 120 | |

**Loss condition** (upper bound of false approvals below 5 % and false rejections not above 10 %): does **not** fire.
The stronger reviewer did not catch the bad patches better (the paired difference includes zero and leans the wrong
way), and it rejected more good patches. The four bad patches approved by both reviewers' majorities are m005-U-1 and
m005-U-2 (method left at 22, threshold 15), m032-U-3 (complexity moved into a helper at 16) and m048-U-2 (left at 17).
The deterministic gate caught all 26.
