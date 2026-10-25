# WP-40 §E5 evidence (frozen as tag wp40-e5-freeze)

`verdict.sql` run once per repository through the read-only `prod-query` workflow (`q.sh` finds its own run by a marker
row), outputs `019….txt`; `total.py` → `results.txt`. All 5,251 `AgentResolved` events are accounted for.

**Whose data.** The six repositories are all our own: CanineCC/kennel.canine.dev (4,716 resolutions),
CanineCC/unfold.canine.dev, CanineCC/RETIRED.watchdog.canine.dev, seedvaultstudio/continuum, seedvaultstudio/lawnofwar,
code-assurance-initiative/CodeAssuranceIndex. No customer repository has an agent resolution. This is dogfooding.

**Exploratory, labelled, not part of the frozen analysis:**
- 382 of the 588 did-not-clear are D28 (secrets in git history): a working-tree change cannot remove a secret from
  history, yet the agent resolved them. Without D28: 206 of 3,892 decided (5.3 %; D28 had 382 did-not-clear and 15 cleared). That is an advice/product finding
  (D28's remediation must say "rotate, then rewrite history or accept"), not only an agent one.
- "cleared" means the fingerprint is absent and the dimension was measured. A fingerprint-scheme change between engine
  versions would also look like that; the mass D1/D2 clearing of 2026-10-02..08 has not been checked for it.
- The repository-cluster bootstrap is uninformative with 3 decided repositories (12.5–100 %); report the pooled
  Wilson interval with that caveat beside it.
