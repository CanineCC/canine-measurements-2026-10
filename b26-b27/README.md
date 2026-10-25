# B26 and B27 evidence

- `concentration.py` over the cycle-1 noise export (one CSV per language, the two "(1)" download duplicates skipped):
  `python3 -I concentration.py "<export dir>" <elixir csv>` → `concentration.txt`.
- `cycle1-per-repo.csv`: findings and noise per repository for cycle 1, one verification run per language, from a
  read-only production query (GitHub Actions `prod-query.yml`, run 40160534119, 2026-10-25), parsed by `parse_log.py`.
- `cap.py cycle1-per-repo.csv 50 250` → `cap-50-250.txt` (the 50–250 cap and the leave-one-repository-out span);
  `cap_sweep.py` → `cap-sweep.txt` (14 cap settings, 12 orderings).
- Per-language noise rates in these files are internal (publication-gated); the posts show ranks and counts only.
