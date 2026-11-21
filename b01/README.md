# B1: findings per repository, C#, Go and Rust (production corpus, 21 November 2026)

Behind the article *Findings count is not analysis depth*.

| File | What it is |
|---|---|
| `query.sql` | The read-only query against our production database. Each repository at its most recent complete scan that recorded each dimension, taken before 2026-11-21 19:16 UTC |
| `per-repo.csv` | Its output: 1,857 public open-source repositories (644 C#, 520 Go, 693 Rust), with the commit scanned, the date, the engine version, production lines of code and the number of findings |
| `stats.py` | Every figure in the article from `per-repo.csv`: `python3 stats.py per-repo.csv` |
| `results.txt` | Its output |

**Read it this way.** A count here is everything our engine stored for that scan, over all dimensions, with no cap,
and it includes findings that are wrong: noise has not been taken out. It is not a ranking of these projects and says
nothing about the people who wrote them. The scans come from several engine versions, so compare repositories only
within one version; `stats.py` repeats the comparison inside each version that scanned at least ten repositories in
every language.

**Left out.** 71 repositories in these three languages with no complete scan that recorded each dimension. Nothing
was left out because of its count.

**Who measured.** Canine Development, on its own engine.
