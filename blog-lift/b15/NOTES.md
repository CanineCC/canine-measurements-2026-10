# B15 "What technical due diligence misses" (imprint 5be899c238f0469cb96f7e43546bace9), lift L9

Fetched 2026-10-25, about 17:30 UTC. Raw pages in `downloads/`.

## Example used

3b1b/manim, the most recent public report in which all three history signals (D16 Bus Factor, D34 Knowledge
Freshness, D35 Change Coupling) carry a finding.

- Public report: https://app.watchdog.canine.dev/api/oss/3b1b/manim/report (listed on https://watchdog.canine.dev/publicreports/)
- CAI page: https://codeassuranceindex.info/surveys/github/3b1b/manim/
- Saved: `downloads/3b1b__manim.html` (+ `.txt`), `downloads/cai-survey-3b1b_manim.html` (+ `.txt`), `downloads/publicreports.html`

## Figures (each on the report page above, re-read 2026-10-25)

| Figure | Where on the page |
|---|---|
| Measured 23 October 2026, 02:32 UTC, code version fafa083; rubric 2026.10.5; survey ID cd_235a5707821548778362fb35f1802c58 | header |
| CAI 59 out of 100 (CAI page: 58.8, commit fafa083a4fb274bba9cabde0b6e2f50ba6da0622) | header / CAI page |
| 22,971 lines of product code in 2 projects | header |
| D16 5.7/10: "31 source file(s) have their living knowledge concentrated in one author (>=90% of recent, decayed contribution)... Counted over 73 of the 105 production source files ... the rest are under the ~2,400-byte size floor" | D16 section |
| D16 method: time-decayed commit attribution, 6-month half-life | D16 section |
| Off-boarding risk: "anonymized user #1", 31 significant files lose their only recent owner: drawings.py, renderer/drawing.py, surface.py, interactive.py, gpu.py, window.py, camera.py, scene_file_writer.py (+23 more) | Appendix A, D16 |
| D34 9.4/10: "4 of 73 significant source file(s) are orphaned"; largest manimlib/module_loader.py; others logo/logo.py, manimlib/mobject/boolean_ops.py, manimlib/event_handler/event_dispatcher.py | D34 section, Appendix A |
| D35: "Strongest change-coupling: interactive.py<->scene.py 50%"; "5 of the 10 commits that touched whichever of the two files changed less often" | D35 section, Appendix A |
| D35 floors: each file >=10 revisions, >=5 shared commits, >=50% strength; sweeping commits excluded | D35 method |

## My own check (raw git, not on a public page; NOT quoted as a figure in the post except as described)

Blobless clone of github.com/3b1b/manim at fafa083 (`downloads/manim-git`). `git log --follow` gives 15 revisions of
interactive.py and 8 commits that touch both files (`downloads/git-cochange-both.txt`). Two of the eight are formatting
sweeps (9ef9961d "Sort imports", 72 files; 902a4f26 "Add white space after assert statements", 15 files), which the
D35 method drops. That leaves 6 vs the report's 5 of 10; the remaining gap is the report's own sweep rule, which I did
not reimplement. So the 5/10 is consistent in shape but NOT exactly reproduced by a naive git command. The post says
so in its method card rather than promising an exact reproduction.

## Notes and flags

- The pair interactive.py / scene.py sits exactly on the reporting floor (5 shared, 50 %). The post says so.
- Selection: manim was chosen because all three signals have a finding. Stated in the method card as an illustration,
  not a sample.
- The CAI codebase page does NOT link the producer's report (no href to app.watchdog.canine.dev on it; only
  "Measured by watchdog.canine.dev" as text). Decision 0003 says survey pages link producers' reports; that link is
  not there for manim (also not for oauth2-server, rustnet, atomvm, bsharp). The report is reachable from
  watchdog.canine.dev/publicreports/.
- The CAI page's engine line reads "codehealth-analyzer measure-2026.10.6+preprod-d36780c2d857": a "preprod" build
  string on a public production page. Not a post issue; worth the owner's eye.
- No contradiction with the post's claims found. The post's "four of the six critical modules have a single author" is
  illustrative wording, not a figure; left as is.
- Boundary "measures the codebase, never the people": the report anonymises the contributor; the post repeats that.
