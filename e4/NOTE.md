# E4 note (exploratory, after the frozen analysis)
The 5 "not good" patches under the frozen rule are the E2 BEFORE runs whose tests failed; E2's exploratory notes show
those failures pre-exist on the unchanged code (p20, p36) or were flaky (p04, re-run green twice). So no patch in E2
was actually bad, and E4 cannot estimate false approvals. Its measured result is the false-rejection rate on good
patches (6.1 %) and the reviewer's self-consistency (98.3 %). The question of false approvals moves to E6's patches,
which include hard methods where fixes can fail; it would be a new, pre-registered ask (E4b), not a re-analysis.
