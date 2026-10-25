# WP-40 §E1 evidence

Dataset: M. Schnappinger, A. Fietzke, A. Pretschner, *A Software Maintainability Dataset*, figshare,
doi:10.6084/m9.figshare.12801215 v3, CC BY 4.0; paper: *Defining a Software Maintainability Dataset*, ICSME 2020.
`keys.csv` reproduces the dataset's three key columns under that licence. The labels themselves are not copied here:
fetch them from figshare and check the sha256 in `SEAL.txt`.

Order of work, each step timestamped in `SEAL.txt` / `FREEZE.txt`: labels sealed by hash; key columns read; analysis
frozen (commit b1ed0ab162, pushed); predictions written and hashed (`predictions.csv`); labels opened; `analyse.py`
run once (`results.txt`, `results.json`); disagreements read from the code (`disagreements.md`).

Instrument: `JavaProbe.*` built against the pinned engine (cca-phase-2 a3f3f35ad9) with its Java sidecar; re-run with
`scan`-style environment from `scan.sh` and `python3 -I predict.py && python3 -I analyse.py 10000`.
