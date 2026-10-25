# WP-40 §E4b results (frozen at tag wp40-e4b-freeze; analysis `analyse_e4b.py`, committed c51f4274a3 before E6's outcomes were read)

E4's reviewer (same model as the agent, no tools, shown the finding with its threshold of 15 and the diff, asked
whether the method is now at or below the threshold with behaviour unchanged) on all 120 E6 patches, 3 asks each.
Gate truth from E6: 94 good (held, behaviour passed), 26 bad (22 did not clear, 4 moved). None excluded.
Verdicts: 284 APPROVE, 74 REJECT, 2 UNPARSEABLE (counted in the denominators, as neither).

| | Asks | Wrong | Rate | 95 % bootstrap over patches |
|---|---|---|---|---|
| **False approvals** (APPROVE on a bad patch) | 78 | 17 | 21.8 % | 10.3 to 34.6 % |
| False rejections (REJECT on a good patch) | 282 | 14 | 5.0 % | 1.4 to 9.2 % |

- **4 of the 26 bad patches were approved by a majority**, 3 of them unanimously: m005-U-1 and m005-U-2 (method left at
  22, threshold 15, all three asks APPROVE), m032-U-3 (cleared by pushing a helper to 16, all three APPROVE), m048-U-2
  (left at 17, two of three APPROVE). 10 of the 26 drew at least one APPROVE.
- Self-consistency: 108 of 120 patches got three identical answers.
- All bad patches came from the unguided arm (E6), so the split by arm is the split by truth; G had no bad patch.
- E4 (on E2's patches, all good) measured false rejections only: 6.1 %. E4b agrees on that side (5.0 %) and adds the
  side E4 could not measure.
