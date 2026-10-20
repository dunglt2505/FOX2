# FOX2 F0 — CHAT safety correction and bounded acceptance

Date: 2026-10-20 (Asia/Saigon). Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`.
Feature: `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION`. Actor: CHAT direct; no Agent assignment.

**Verdict: ACCEPT scoped offline safety correction/test subgates; full F0 BUILD remains BLOCKED.**
Fixed a demonstrated configured-root admission bypass. Independently ingested Owner's original 254-test raw evidence. New focused suite: **267 PASS**; affected runtime consumers: **88 PASS**, both zero failures/errors/skips and process exit 0.

## Sources, authority, task and routing

- Baseline code: `185bc9493d4a9e27f7a463d87313fc03ce32634d`; intake: `4cdb2b26861eeb3a84d31536d6c4138731ad60c8`. Remote branch heads confirmed before work.
- New non-main branch: `work/FOX2-BRIDGE-F0-CHAT-CRASH-REVIEW-20261020`. Safety source: `ba1cbdf2c8bc2b74bd7cac7f6a43065a54c5d4f0`; final code/test source: `611ec26c28484de740e963d86de6b00946f1492d`.
- Live project Governance Registry read from its specified `work/FOX2-POLICY-V200-OWNER-OVERRIDE-RELEASE-20261019` branch; blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`. Policy 2.0.0, Dictionary 1.3, Routing 1.4 and Protocol 12 selected by that scoped release chain. Historic in-flight machine identities are unchanged.
- All 34 original locked Git objects were rehashed against blob/SHA-256: `source_verification.json`. Original task/source lock is evidence, not a replayable assignment. BRD-00/06/08 v0.5 and M1 acceptance v0.4 unchanged. Bridge TechSpec v0.7 remains candidate.
- `SOURCE_BYTES_VERIFIED=YES`; current Owner message directly authorizes these bounded offline edits/review/status writes. Historical Owner release records are CHAT transcriptions, without independent cryptographic signature; no new global authority/effectivity assertion. `RUNTIME_ENFORCED=NOT_ATTESTED`.
- R0 existing Whole-WP BUILD/BLOCKED; R1 offline safety only; R2 current Owner authorization + verified historic source objects; R3 Python 3.13/pytest 8.3.5/Git observed; R4 CHAT direct, no delegated lane; R5 dedicated new branch/worktree, one code writer, no Agent invoked; R6 non-main publication/readback required; R7 exact scope, tests, delivery and STOP recorded here. Agent executable assignment is NOT issued and its fresh PreExec/quota/admission remain HOLD.

## Findings, correction and K1 trace

### Configured runtime root bypass — REPRODUCED, CORRECTED

`desktop.initialize_runtime` previously set cross-root UNKNOWN only when `config.bridge_root == default BRIDGE_ROOT`. A legitimate custom root supplied through `--config` therefore minted `SINGLE_ROOT`; shared direct `claim_dispatch` accepted a new identity without retirement proof. The added regression failed at the actual claim before the fix (`red.xml`, 1 FAIL/3 PASS).

The initializer now persists `DENY_CROSS_ROOT_UNKNOWN` for **every configured runtime root**. Root relocation is not proof of exclusive dispatch authority. Legacy snapshot discovery stays restricted to the canonical root; this change does not inspect a legacy installed DB from an alternate runtime root. Ordinary direct single-database fixture initialization retains compatibility. No positive runtime-admission API was added.

K1 `NECESSARY_DEPENDENCY`: `agent_bridge/src/fox2_agent_bridge/desktop.py`, one runtime initializer argument plus explanation. `REQUESTED`: `agent_bridge/tests/test_runtime_ledger.py`, alternate configured-root fresh/preexisting-state denial, reopening, zero rows, abrupt checkpoints and configuration-failure recovery.

K1 `NECESSARY_DEPENDENCY`: `agent_bridge/tests/test_lock_logging_health.py`, the broader consumer test still expected schema 4 even though baseline F0 already migrates to 5. Correct to 5 and add an assertion that the health runtime remains denied. This third test path is specifically bound under the current Owner's bounded CHAT correction scope, not added to or replayed through consumed Attempt06. Existing no-Agent assertions are retained.

### Crash windows — bounded offline evidence

| Exit boundary exercised by a separate Python runner process | Durable stage | Recovery / replay |
|---|---|---|
| Immediately after successful committed claim, before worker/checkpoint update | UNKNOWN | NEEDS_RECONCILIATION; identity retained; second claim denied |
| After CLAIMED checkpoint, before adapter entry | CLAIMED | SAFE_NOT_STARTED; identity still consumed; no retry granted |
| Inside fake adapter, before exit result/checkpoint | RUNNING | NEEDS_RECONCILIATION; identity retained; no verifier/relaunch |
| After harmless Python child really executed, before adapter returns | RUNNING | NEEDS_RECONCILIATION; same retained claim; no second claim |

Each test observes exit code 72, marker boundaries, exactly one dispatch/execution row, idempotent reconciliation and denied replay. The fake adapter replaces the adapter registry before runner entry. **No paid CLI was spawned.** The synthetic child case proves a child ran; it does not prove supervision of a still-living real Agent, Windows power-loss/fsync behavior, or installed recovery.

`CLAIMED` is safe-not-started only under the actual runner ordering: durable RUNNING intent precedes adapter invocation. A crash between claim commit and CLAIMED checkpoint yields UNKNOWN, conservatively retained. No recovery branch deletes the consumed identity.

### No-spawn, root/path, controls and configuration

- Original six cross-root negatives remain byte-for-byte in protected `test_e2e_runner.py`, blob `7b2a2c48e6bf4225d849dc7a7a32126652b0c3be`; six raw JUnit cases PASS in both Owner baseline and new focused suite.
- Existing no-spawn fixture denies before result-parent preparation and adapter entry, with no dispatch/execution rows. Installed-root direct-claim, alternate DB and canonical relative alias tests remain PASS. These do not certify arbitrary volume/hard-link aliases or hostile database copying.
- Eight new recovery cases cover AGENT_EXITED/PUBLISHING with zero exit but durable capacity failure, wrong pinned model, reasoning or permission profile. Verification is forbidden; all retain NEEDS_RECONCILIATION and deny replay. Missing observed CLI metadata remains unobserved; these tests do not turn NOT_EXPOSED into exact configuration proof.
- Same-database atomicity, sticky denial, concurrency, pause/stop, original schema migrations and unrelated single-root fixture behavior pass the focused suite. A raw SQLiteLedger initialized outside known installed roots has no independently proven global authority; it remains a low-level fixture API. This report certifies configured runtime entrypoints, not arbitrary direct hostile callers or old executable retirement.

## Evidence and testing

Raw Owner JUnit and log were available at the exact provided temporary path, copied without changing bytes, parsed and hashed. SHA-256 matches `ACDFA9E021E1EFDB34A6EBFC3457074D68F11B2CAAAD37CDAF04680B43B6BCB9` and `653F7944D59A5DA245C4F8055F0FBBDA04F0C57E32B8E10B52E36765675E0292`. All 254 testcase nodes have no failure/error/skip; six protected cases and four prior new safety cases are present. Source association remains Owner-output + matching raw hashes, not a signed execution attestation.

New six-module focused run at `ba1cbdf...`: 267 PASS in 252.23s, exit 0. Final source `611ec26...` differs only in the health test outside this selection; all selected modules, conftest and production source bytes are identical. Five consumer modules at final `611ec26...`: 88 PASS in 59.72s, exit 0. Commands, counts, source relation and failed-case lists are in `test_summary.json`; raw logs/JUnit and `evidence_hashes.json` accompany them.

Earlier failures are preserved: sandbox run 212 PASS/3 FAIL/43 ERROR (Git MSYS object creation denied and temp probe restrictions); first broader run 72 PASS/16 FAIL (15 WinError 206 long fixture paths, plus stale schema expectation). Git fixture push succeeded under authorized host execution. Final consumer run used exact locked source in `C:/Users/Fox Le/AppData/Local/Temp/f0safe_611ec26`, avoiding long paths, without registry/global Git changes or weakened assertions. These failures are not relabeled PASS; separate corrected executions supply the final results.

## Result Contract and exact remaining gates

Attempt06 remains consumed after model-capacity failure. Local exit/partial observation and remote snapshot `d2c595be123fa041720fd0467f9d94b2d4318bca` were inspected. Remote read of its expected `evidence_manifest.json` returned NOT_FOUND. No Agent-authored Result v2 was delivered. This CHAT-authored report, test summary and hash inventory do **not** impersonate that contract.

`_verify_result` verifies branch/clean worktree/ancestry/remote head/path allowlist/declared file+stdout acceptance. It does not itself validate the Agent Result v2 schema or decide CHAT ACCEPT. `PUSHED_UNREVIEWED` after reconciliation is publication status only. A future eligible Result must satisfy exact task/source/tuple, schema v2 with FormatChecker, file hashes/K1/tests and independent CHAT intake. No new schema enforcement or positive installed route is claimed here.

| Gate | Current verdict / exact residual |
|---|---|
| Owner 254 raw JUnit/log independent intake | ACCEPT_SCOPED; raw bytes, counts and expected hashes verified |
| Configured-root DENY correction + preserved six + crash/config negatives | ACCEPT_SCOPED_OFFLINE at locked code source |
| Affected consumer regression | ACCEPT_SCOPED_OFFLINE, 88/88 |
| Original Attempt06 Result Contract v2 | NOT_DELIVERED / NO_REPLAY; cannot synthesize Agent authorship |
| Formal complete F0 delivery/build gate | BLOCKED; a CHAT delivery substitution would require an explicit scoped disposition, not implicit conversion of the old result to PASS |
| F1 durable legacy retirement / dual-version shared authority | NOT_VERIFIED; frozen old binary may still claim from its own database |
| Installed exact-source adoption, supported controls/lease, rollback and positive admission | NOT_RUN/HOLD; no installed state changed or tested |
| Real Agent crash/living-child recovery and installed restart | NOT_RUN; synthetic process evidence only |
| Whole-WP final acceptance | NOT_ATTESTED; offline subgates do not supply the seven final gates below |

The seven inherited final gate names/exit expectations remain: `CANARY_009_EXACTLY_ONCE` (one exact real admitted run), `EXACT_AGENT_CONFIGURATION` (observed pinned model/medium/adapter/prompt), `FULL_ACCESS_PERMISSION` (actual launch profile), `RESULT_REMOTE_READBACK` (BRIDGE-owned exact authorized Canary result), `USAGE_SNAPSHOT` (real exposed usage or honest NOT_EXPOSED), `RESTART_NO_REPLAY` (same consumed identity after authorized installed restart), `CHAT_FINAL_REMOTE_INTAKE` (all applicable gates independently accepted). These are NOT_RUN/HOLD for the Canary subject. Prior RC1/C3 accepted evidence stays historical; this review does not revoke it or certify this new source as installed.

## Delivery, status and next lawful action

Only this feature's operational row is updated from intake `4cdb2b2...`; the other feature row is structurally identical. BUILD/BLOCKED, F1 HOLD, Canary009 HOLD and INTERNAL_READY NOT_ATTESTED persist. No Governance Registry/Dictionary/Policy/source lock/Dispatch/old receipt changed. No main/merge, Worker/control/startup mutation, provider/broker/LIVE or Agent call.

`GOAL_MET=YES_FOR_BOUNDED_SAFETY_CORRECTION_AND_REVIEW; NO_FOR_FULL_F0_OR_INTERNAL_READY`.
`NEXT_SAFE_ACTION=REMOTE_READBACK_THIS_DELIVERY_AND_SCOPED_CHAT_ACCEPTANCE; FORMAL_DELIVERY_DISPOSITION_BEFORE_FULL_F0`.
`REAL_BLOCKER=ORIGINAL_AGENT_RESULT_V2_MISSING_WITH_CONSUMED_IDENTITY; INSTALLED_F1_AND_FINAL_EXECUTION_GATES_OUTSIDE_CURRENT_SCOPE`.
No Owner manual Windows run is required for the completed offline checks. No background execution is promised.

Skill coverage: source-resolver, governance-preflight, agent-route-runtime, result-review, feature-certification, execution-recovery and status-roadmap = REQUIRED/APPLIED, actual v0.3.6 files read and release hashes checked (explicit LF normalization where installed files use CRLF). Prompt Builder/Thread Handoff = NOT_APPLICABLE, no new actor/task assignment. BRD change control/Dictionary impact/publication = NOT_APPLICABLE, no semantic/source-identity release. No mandatory Skill unavailable.
