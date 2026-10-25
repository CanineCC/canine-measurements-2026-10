# B5 "A dependency matrix shows cycles, not layering" (imprint c252bf0d5ee5422ebb170d0803ee720c), lift L11

Fetched 2026-10-25, about 17:30 UTC. Raw pages in `downloads/`.

## Example used

thephpleague/oauth2-server. Of the 28 public reports, 4 show a mark above the diagonal (thephpleague/oauth2-server:
loop through 7 of 15 modules; DualBrain/bsharp: 5 of 14; ciren/cilib: 5 of 31; 3b1b/manim: 2 of 81). oauth2-server
chosen because every above-diagonal mark traces to one type, which makes the example readable.

- Public report: https://app.watchdog.canine.dev/api/oss/thephpleague/oauth2-server/report (section "Architecture: which parts of the code depend on which")
- CAI page: https://codeassuranceindex.info/surveys/github/thephpleague/oauth2-server/
- Source at the pinned commit: https://github.com/thephpleague/oauth2-server/blob/ff56f654a1cf9f83ba1943a2c078acac92b9d023/src/CryptKeyInterface.php
- Saved: `downloads/thephpleague__oauth2-server.html` (+ `.txt`), `downloads/cai-survey-thephpleague_oauth2-server.*`, `downloads/github/*.php` (4 source files at ff56f65), `downloads/github__spec-kit.*` (40-module cap)

## Figures (oauth2-server report, re-read 2026-10-25)

- Measured 20 October 2026, 20:49 UTC, code version ff56f65 (CAI page: ff56f654a1cf9f83ba1943a2c078acac92b9d023), rubric 2026.10.5, survey ID cd_21bea770485848bbb6d24ecca2fc1ef5. CAI 76 (CAI page 75.5). 5,560 lines of product code in 1 project.
- "15 modules, with 26 dependencies between them. One loop runs through 7 of the modules, marked above the diagonal."
- Above-diagonal cells ("part of a loop"), all into row/column 13 `League.OAuth2.Server`:
  - 5 -> 13 `League.OAuth2.Server.Entities`: 1 pair, `AccessTokenEntityInterface -> CryptKeyInterface`
  - 8 -> 13 `League.OAuth2.Server.ResponseTypes`: 1 pair, `AbstractResponseType -> CryptKeyInterface`
  - 10 -> 13 `League.OAuth2.Server.AuthorizationValidators`: 1 pair, `BearerTokenValidator -> CryptKeyInterface`
  - 11 -> 13 `League.OAuth2.Server.Grant`: 2 pairs, `AbstractGrant -> CryptKeyInterface`, `GrantTypeInterface -> CryptKeyInterface`
  - So 4 marks, 5 type pairs, one target type.
- `League.OAuth2.Server` (row 13) uses 2 EventEmitting, 5 Entities, 6 Repositories, 7 RequestTypes, 8 ResponseTypes, 10 AuthorizationValidators, 11 Grant.
- Loop members (derived from the cells, matches the printed 7): League.OAuth2.Server, Entities, Repositories (6 -> 5 -> 13), RequestTypes (7 -> 5 -> 13), ResponseTypes, AuthorizationValidators, Grant. EventEmitting uses nothing, so it is not in the loop.
- Source check at ff56f65: `CryptKeyInterface` is declared in namespace `League\OAuth2\Server` (src/CryptKeyInterface.php line 5); `AccessTokenEntityInterface` (namespace `...\Entities`) has `setPrivateKey(CryptKeyInterface $privateKey)`; `AbstractResponseType` has `protected CryptKeyInterface $privateKey`; `BearerTokenValidator` has `setPublicKey(CryptKeyInterface $key)`. Confirmed.
- Matrix cap: github/spec-kit report "The table shows the 40 modules with the most connections; 136 more are left out to keep it readable." Matches the post's "the matrix at 40".

## Notes and flags

- No contradiction with the matrix claims in B5 (but see the caption below). The post's description of the cell (distinct type pairs) and the ordering matches the report's own legend.
- The "move CryptKeyInterface to its own namespace" remark in post.md is my reading of the matrix (Opinion), and the post says moving a public interface is a breaking change for a library's users.
- The matrix includes `OAuth2ServerExamples.Entities` and `OAuth2ServerExamples.Repositories` (the repository's examples tree). Relevant to B6's "tests and samples are out by default"; flagged in b6/NOTES.md.
- The CAI page does not link the report (see b15/NOTES.md).

## ★ CONTRADICTION found while reading other reports

- The post says our documentation once claimed the instrument detected "cycles or layering violations", and that the
  wording was corrected in three places. The public reports' NODE-LINK graph caption still reads: "Project
  dependencies, layered top-to-bottom; arrows show direction. Any dashed red edge points upward or sideways, a
  layering smell or cycle. A clean layered graph has none." (current format, e.g. atomvm/AtomVM 23 Oct, DualBrain/bsharp
  21 Oct; 9 of the 28 public reports carry it on 2026-10-25). It is the project-level drawing, not the matrix, but a reader of this post
  who opens a report will meet the very claim the post says was withdrawn. Product caption fix needed; the post is
  left as is.
