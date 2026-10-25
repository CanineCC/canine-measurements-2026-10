# E1 — the 10 largest rank disagreements, read from the code

Primary predictor (total cognitive complexity of the file) against the experts' overall badness. Each was read in the
shipped source. Class: **our miss** (the engine got this wrong or could not see it), **label debatable** (code shown;
the reader decides), **out of scope** (the file is not the kind of code the predictor measures).

| # | class | ours | experts | class | reason |
|---|---|---|---|---|---|
| 1 | jsweet `def.dom.HTMLIFrameElement` | 0 (295 lines) | 2.87 (very hard) | out of scope | A binding declaration: public fields mirroring the DOM, no logic. Experts penalised form and size; control-flow complexity measures neither. |
| 2 | aoi `artofillusion.translators.POVExporter` | 0 (634 lines) | 2.74 | **our miss** | The engine's Java code model never read the file: it is ISO-8859-1, and every one of the 13 non-UTF-8 Java files across the five projects was silently left out of the model. An engine defect, reported and filed. |
| 3 | junit4 `junit.textui.TestRunner` | 14 (177 lines) | 0.00 (very easy) | our miss | Complexity spread over many short methods; the experts read it as easy and the sum ranks it in the upper third. A sum cannot tell one hard method from ten easy ones. |
| 4 | diarymanagement `TBA.Exceptions.NetworkDataException` | 0 (41 lines) | 1.85 | label debatable | Four constructors that pass a message or cause to `Exception`. |
| 5 | junit4 `org.junit.internal.AssumptionViolatedException` | 7 (75 lines) | 0.00 | our miss | Same shape as 3, at smaller scale. |
| 6 | junit4 `org.junit.runner.Description` | 14 (278 lines) | 0.01 | our miss | Same shape as 3. |
| 7 | argoUML `org.argouml.ui.SettingsTabLayout` | 0 (192 lines) | 1.22 | our miss | Most of the body is commented-out code under a TODO, which the paper reports experts penalise. Complexity cannot see it; the engine's explicit-debt dimension (D17) can, but it is not part of the frozen predictor. |
| 8 | junit4 `junit.framework.TestCase` | 9 (492 lines) | 0.01 | our miss | Long because of documentation; little logic. Experts rate it easy, the size baseline ranks it worse than we do. |
| 9 | jsweet `def.dom.HTMLFrameElement` | 0 (283 lines) | 1.13 | out of scope | As 1. |
| 10 | junit4 `org.junit.internal.TextListener` | 8 (83 lines) | 0.01 | our miss | Same shape as 3. |

Tally: our miss 7 (one an engine defect; four share one mechanism, summing many small methods), label debatable 1, out of scope 2.
