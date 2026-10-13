# FOX2 — M1 BRD ↔ Technical Transition Mapping v0.1

**Status:** `RELEASED_EFFECTIVE / TRACEABILITY`  
**Purpose:** prove semantic preservation while splitting released BRD-00/06/08 v0.4 into BRD v0.5 Candidate REV3/REV2 set + M1 Technical Spec v0.1.  
**Released source commit:** `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`  
**Data Contract/schema:** released v0.4, unchanged.  
**Rule:** requirement/acceptance meaning is preserved unless a future explicit Owner-approved semantic change says otherwise.

## 1. Requirement-level preservation matrix

| Requirement | Released source | Released BRD | Technical/Contract home | Existing acceptance IDs | Expected-source pointer | Disposition |
|---|---|---|---|---|---|---|
| `FOX2-00-R01` | `docs/brd_mirror/FOX2-BRD-00_v0.4.md` @ `955e74ff...` | `FOX2-BRD-00_v0.5.md` | KEEP_BRD; implementation traceability via M1 Tech §15 | `FOX2-00-T01` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-00-R02` | `docs/brd_mirror/FOX2-BRD-00_v0.4.md` @ `955e74ff...` | `FOX2-BRD-00_v0.5.md` | KEEP_BRD; Technical state evidence via M1 Tech §14–§16 | `FOX2-00-T05` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-00-R03` | `docs/brd_mirror/FOX2-BRD-00_v0.4.md` @ `955e74ff...` | `FOX2-BRD-00_v0.5.md` | KEEP_BRD; Data Contract v0.4 missing/nullable semantics + M1 Tech §4 | `FOX2-00-T02`, `FOX2-N1-T03` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-00-R04` | `docs/brd_mirror/FOX2-BRD-00_v0.4.md` @ `955e74ff...` | `FOX2-BRD-00_v0.5.md` | KEEP_BRD; Data Contract v0.4 provenance/PIT semantics + M1 Tech §4 | `FOX2-N1-T01`, `FOX2-N1-T06` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-00-R05` | `docs/brd_mirror/FOX2-BRD-00_v0.4.md` @ `955e74ff...` | `FOX2-BRD-00_v0.5.md` | KEEP_BRD; M1 Tech §9/§13 enforce no broker-write surface | `FOX2-00-T03` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-00-R06` | `docs/brd_mirror/FOX2-BRD-00_v0.4.md` @ `955e74ff...` | `FOX2-BRD-00_v0.5.md` | KEEP_BRD; M1 Tech §13 security/private-scope boundary | `FOX2-06-T13`, `FOX2-08-T04` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-00-R07` | `docs/brd_mirror/FOX2-BRD-00_v0.4.md` @ `955e74ff...` | `FOX2-BRD-00_v0.5.md` | KEEP_BRD; implementation ownership reflected by M1 Tech §2/§3 | `FOX2-00-T01`, `FOX2-00-T06` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-00-R08` | `docs/brd_mirror/FOX2-BRD-00_v0.4.md` @ `955e74ff...` | `FOX2-BRD-00_v0.5.md` | KEEP_BRD; governance owned by Policy, no Technical redefinition | `FOX2-00-T90` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-00-R09` | `docs/brd_mirror/FOX2-BRD-00_v0.4.md` @ `955e74ff...` | `FOX2-BRD-00_v0.5.md` | KEEP_BRD; M1 Tech §2/§3 dependency direction only | `FOX2-00-T01`, `FOX2-00-T91` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-00-R10` | `docs/brd_mirror/FOX2-BRD-00_v0.4.md` @ `955e74ff...` | `FOX2-BRD-00_v0.5.md` | KEEP_BRD; M1 Tech §5 DSM + §7 provider + §11 UI isolation | `FOX2-00-T04`, `FOX2-06-T14`, `FOX2-N1-T12` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-00-R11` | `docs/brd_mirror/FOX2-BRD-00_v0.4.md` @ `955e74ff...` | `FOX2-BRD-00_v0.5.md` | KEEP_BRD; M1 Tech §16 phase/authority gates + Roadmap v0.4 | `FOX2-00-T05`, `FOX2-00-T06`, `FOX2-00-T07` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R01` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §4 Data Contract use + §8 provider mapping | `FOX2-06-T18`, `FOX2-06-T24` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R02` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §5 DSM selection + §14 technical state model | `FOX2-06-T06`, `FOX2-06-T07`, `FOX2-N1-T02` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R03` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §5 DSM/calendar evaluation + Data Contract v0.4 | `FOX2-06-T03`, `FOX2-N1-T09` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R04` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §6 store revisioning + §7 WS/recovery | `FOX2-06-T10`, `FOX2-06-T19`, `FOX2-06-T20`, `FOX2-06-T21`, `FOX2-06-T22` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R05` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §4 DTO separation + §13 private/public security boundary | `FOX2-06-T13` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R06` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §7 provider auth boundary + §13 secret handling | `FOX2-06-T09`, `FOX2-06-T16` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R07` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §9 API allowlist + §13 no broker/order surface | `FOX2-06-T05`, `FOX2-06-T16` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R08` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §5 DSM ownership/selection + §9 unified API | `FOX2-06-T15`, `FOX2-08-T08` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R09` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §5 rights/provenance + §7 provider transport + §13 security | `FOX2-06-T16`, `FOX2-06-T24` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R10` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §5 typed capability/source-selection decision | `FOX2-06-T06`, `FOX2-06-T07`, `FOX2-06-T08`, `FOX2-06-T11` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R11` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §6 SQLite observation/revision store | `FOX2-06-T12`, `FOX2-06-T17`, `FOX2-06-T23` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R12` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §7 reconnect/backfill/backpressure + §14 state model | `FOX2-06-T19`, `FOX2-06-T20`, `FOX2-06-T22` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R13` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §5 rights/expiry reevaluation + §13 secrets/security | `FOX2-06-T09`, `FOX2-N1-T07` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R14` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §4 typed contracts + §9 API behavior | `FOX2-N1-T11`, `FOX2-06-T18` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R15` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §5 no synthetic fallback + §13 fixture isolation | `FOX2-06-T14`, `FOX2-N1-T12` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R16` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §2 architecture boundary + §7 provider allowlist + §13 isolation | `FOX2-WS08`, `FOX2-06-T16` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R17` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §6 SQLite observation store | `FOX2-06-T17`, `FOX2-06-T12`, `FOX2-N1-T06` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R18` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §7 Provider/WebSocket + §19 pinned provider appendix | `FOX2-WS01`, `FOX2-WS02`, `FOX2-WS03`, `FOX2-WS04`, `FOX2-06-T19` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R19` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §8 Provider mapping + §19 pinned provider appendix | `FOX2-WS05`, `FOX2-WS07`, `FOX2-06-T22`, `FOX2-06-T24` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-06-R20` | `docs/brd_mirror/FOX2-BRD-06_v0.4.md` @ `955e74ff...` | `FOX2-BRD-06_v0.5.md` | M1 Tech §4 Data Contract use + §5 capability gates + Contract v0.4 | `FOX2-N1-T02`, `FOX2-N1-T07`, `FOX2-06-T23` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-08-R01` | `docs/brd_mirror/FOX2-BRD-08_v0.4.md` @ `955e74ff...` | `FOX2-BRD-08_v0.5.md` | M1 Tech §9 API design + §11 frontend rendering | `FOX2-08-T05`, `FOX2-N1-T10` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-08-R02` | `docs/brd_mirror/FOX2-BRD-08_v0.4.md` @ `955e74ff...` | `FOX2-BRD-08_v0.5.md` | M1 Tech §9 API design + §11 frontend/chart behavior | `FOX2-08-T02`, `FOX2-08-T03`, `FOX2-08-T10`, `FOX2-08-T11` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-08-R03` | `docs/brd_mirror/FOX2-BRD-08_v0.4.md` @ `955e74ff...` | `FOX2-BRD-08_v0.5.md` | M1 Tech §11 source/state UI + §14 technical state model | `FOX2-08-T06`, `FOX2-08-T07`, `FOX2-08-T11` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-08-R04` | `docs/brd_mirror/FOX2-BRD-08_v0.4.md` @ `955e74ff...` | `FOX2-BRD-08_v0.5.md` | M1 Tech §4 assessment/DTO contract + §11 rendering consistency | `FOX2-08-T13` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-08-R05` | `docs/brd_mirror/FOX2-BRD-08_v0.4.md` @ `955e74ff...` | `FOX2-BRD-08_v0.5.md` | M1 Tech §11 private-view rendering + §13 security boundary | `FOX2-08-T04`, `FOX2-06-T13` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-08-R06` | `docs/brd_mirror/FOX2-BRD-08_v0.4.md` @ `955e74ff...` | `FOX2-BRD-08_v0.5.md` | M1 Tech §11 UI boundary + §13 no-order surface | `FOX2-08-T04` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-08-R07` | `docs/brd_mirror/FOX2-BRD-08_v0.4.md` @ `955e74ff...` | `FOX2-BRD-08_v0.5.md` | M1 Tech §11 responsive/navigation/data diagnostics | `FOX2-08-T01`, `FOX2-08-T02`, `FOX2-08-T12` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-08-R08` | `docs/brd_mirror/FOX2-BRD-08_v0.4.md` @ `955e74ff...` | `FOX2-BRD-08_v0.5.md` | M1 Tech §9 FOX2 API boundary + §11 no direct provider/DB access | `FOX2-08-T08`, `FOX2-08-T13` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-08-R09` | `docs/brd_mirror/FOX2-BRD-08_v0.4.md` @ `955e74ff...` | `FOX2-BRD-08_v0.5.md` | M1 Tech §11 provenance panel + §14 state model + Contract v0.4 | `FOX2-08-T05`, `FOX2-08-T06`, `FOX2-08-T07` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-08-R10` | `docs/brd_mirror/FOX2-BRD-08_v0.4.md` @ `955e74ff...` | `FOX2-BRD-08_v0.5.md` | M1 Tech §5 no synthetic fallback + §11 investor UI + §13 fixture isolation | `FOX2-N1-T12`, `FOX2-08-T13` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-08-R11` | `docs/brd_mirror/FOX2-BRD-08_v0.4.md` @ `955e74ff...` | `FOX2-BRD-08_v0.5.md` | M1 Tech §9 diagnostics API + §11 settings UI + §13 secret redaction | `FOX2-06-T15`, `FOX2-08-T08` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-08-R12` | `docs/brd_mirror/FOX2-BRD-08_v0.4.md` @ `955e74ff...` | `FOX2-BRD-08_v0.5.md` | M1 Tech §11 frontend screen/chart contract + §14 state model | `FOX2-08-T02`, `FOX2-08-T03`, `FOX2-08-T11`, `FOX2-08-T12` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-08-R13` | `docs/brd_mirror/FOX2-BRD-08_v0.4.md` @ `955e74ff...` | `FOX2-BRD-08_v0.5.md` | M1 Tech §10 watchlist compare-and-replace/persistence | `FOX2-08-T10` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-08-R14` | `docs/brd_mirror/FOX2-BRD-08_v0.4.md` @ `955e74ff...` | `FOX2-BRD-08_v0.5.md` | M1 Tech §11 responsive/accessibility/reviewability | `FOX2-08-T09`, `FOX2-08-T12` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |
| `FOX2-08-R15` | `docs/brd_mirror/FOX2-BRD-08_v0.4.md` @ `955e74ff...` | `FOX2-BRD-08_v0.5.md` | M1 Tech §12 refresh/network behavior + §9 API boundary | `FOX2-08-T14`, `FOX2-08-T13` | same released BRD path + `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` + requirement map | `PRESERVE_NO_SEMANTIC_CHANGE` |

## 2. Acceptance semantic resolution

For every retained acceptance ID, the normative scenario/expected outcome resolves to:

1. the exact released owner BRD v0.4 at commit `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`;
2. `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv`; and
3. `docs/acceptance/FOX2_M1_V04_CHANGE_CONTRACT_AND_REQUIREMENT_MAP.md`.

Where the CSV says “Theo expected trong owner BRD”, the owner BRD v0.4 expected text remains the semantic source until an explicit approved replacement exists. The split never treats ID preservation alone as semantic preservation proof.

## 3. Moved technical material

- BRD-06 R17 implementation mechanics → M1 Tech §6.
- BRD-06 R18/R19 provider WS/codec details → M1 Tech §7/§8 plus pinned Appendix §19.
- BRD-08 route/API/persistence/polling/rendering HOW → M1 Tech §9–§12.
- Data Contract/schema semantics remain in released Contract v0.4; they are referenced, not duplicated.

## 4. Lifecycle separation

**Document effectivity:** document supersession follows exact Owner approval and Library publication/readback. Git verification does not determine document effectivity.

**Executable handoff readiness:** Git mirror/readback, exact source-set binding, worktree/host/writer checks and `GIT_SOURCE_READY=YES` govern a dependent DEV handoff separately.

A Git mirror failure does **not** invalidate a successfully published document; it blocks only the Git-dependent implementation handoff. No WP may mix released v0.4 BRD with Candidate Technical material and call the mixed set authoritative.

## 5. Preservation counts

- BRD-00: 11/11 requirements.
- BRD-06: 20/20 requirements.
- BRD-08: 15/15 requirements.
- Total: 46/46.
- Acceptance Matrix baseline: 105 unique IDs, all runtime status remains `NOT_RUN` unless separately evidenced.

## 6. Release boundary

This mapping grants no DEV/Git/provider/broker/LIVE authority. It records the released BRD↔Technical traceability split.