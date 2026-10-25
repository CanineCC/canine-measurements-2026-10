# WP-40 §E6 results (frozen at tag wp40-e5-freeze, amendments 1 and 2)

Run 2026-10-25, 120 counted runs (20 methods × 2 arms × 3), model claude-sonnet-5-5, AFTER snapshot
cca-phase-2 `a3f3f35ad9`. Analysis `analyse6.py` (committed in c51f4274a3, before any outcome was read);
output `results6.json`. Per-run gate, metrics, patch and prompt under `runs/`.

## Pre-registered outcomes

| | Guided (G) | Unguided (U) |
|---|---|---|
| Held, behaviour passed | **60 of 60** | **34 of 60** |
| Did not clear (target still over 15) | 0 | 22 |
| Moved (target cleared, another method pushed over 15) | 0 | 4 |
| Build failed / behaviour failed / no change | 0 / 0 / 0 | 0 / 0 / 0 |

- **Primary, G minus U:** +43.3 points, 95 % bootstrap over methods **25.0 to 63.3**. The interval excludes 0, so
  the loss condition does not fire.
- **Tokens G/U** (geometric mean of per-method ratios): 0.94, interval 0.76 to 1.17. No measurable difference.
- **Target complexity after**, median: G 9, U 12. **Touched files' total complexity**, median change: G −8.5, U −7.
- **Cost:** G $6.42, U $5.83 (G +10 %). **Wall time**, median: G 157 s, U 62 s (G 2.5×).
- Excluded runs: none.

## What the numbers do and do not say (read before quoting the headline)

1. **Most of the effect is knowing the target.** U was never told the threshold. Its 22 misses ended at 16, 16, 16,
   17, 17, 17, 18, 18, 20, 20, 20, 22, 23, 23, 24, 24, 27, 33, 35, 49, 49, 49 (the three 49s are one method, m021, which started at 77). Most
   were real improvements that stopped short of a line U could not see. "Held" is defined by our threshold, so a
   guided agent has an advantage built into the question. That is the pre-registered question ("does Assert's
   finding, with a way to re-measure, help"), and it is also the honest limit of the answer.
2. **G optimised to the line.** 10 of 60 guided runs stopped at exactly 15, the threshold. An agent given a number
   aims at the number. Whether 15 is a better method than 16 is not something this experiment measures.
3. **Behaviour never failed in either arm**, under the covering unit-test classes named `<Type>…Tests`. That says the
   refactors did not break those tests; it does not say the tests cover every path of these methods.
4. **The "moved" cases are only in U**: 4 runs (3 on one method) cleared the target by pushing a helper over 15.
   Re-measuring the whole file, which G could do, is what prevents that.
5. Scope: one codebase (ours, the AFTER snapshot), one model, methods of complexity 25 to 87 with unit tests.
