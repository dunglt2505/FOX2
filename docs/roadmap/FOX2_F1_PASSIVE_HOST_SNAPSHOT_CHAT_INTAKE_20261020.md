# FOX2 — CHAT intake: passive F1 host snapshot (2026-10-20)

**Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`. **Feature:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION`. **Stage:** `BUILD / BLOCKED`. **Mode:** `CHAT_DIRECT_READ_ONLY_HOST_RESULT_INTAKE`, no new Agent task/attempt, no F1 installed execution.

## Provenance and snapshot integrity

Owner pasted a JSON console output generated with a read-only PowerShell 7 script in the active conversation. Declared schema `FOX2_F1_PASSIVE_HOST_SNAPSHOT_V1`, `mode=READ_ONLY_NO_AGENT_NO_SQLITE`, observed time `2026-10-20T14:13:09.9894901Z`, PowerShell `7.6.7`, `agent_invoked=false`, `runtime_modified=false`.

**Evidence grade:** `OWNER_HOST_REPORTED_SNAPSHOT / CHAT_PARSED_IN_CONVERSATION`, **not** cryptographically signed host attestation, full raw host file readback, remote machine inspection, current-state continuous proof or an Agent Result. No claims that any unrelated Agent was not running. The original stdout JSON is conversation-held; this report deliberately excludes raw command lines, SID, local user directory paths, actual process IDs, and binary/pointer SHA-256. These are not automatically published to the public Git repository.

## Exact bounded findings

- Both configured canonical **legacy/current root directories present** and reported non-reparse at observed paths. This does NOT close alternate/reparse paths, old worktrees, manual start, non-canonical roots, or installed-source provenance.
- Legacy SQLite DB **PRESENT**, reported 294,912 bytes and non-reparse; manual consumption marker **ABSENT at only the inspected path**. The DB's contents/consumed IDs were **not read**. Do not delete, migrate, snapshot or alter this file as a shortcut.
- Known legacy `launch.ps1` and desktop launcher file paths **ABSENT**, but a restartable old binary/other launch path cannot be excluded.
- Current pointer and `launch.ps1` **PRESENT** with Owner-reported SHA-256, and two candidate executable files had hashes. The reported executable entries have only ordinal IDs, not executable names or version/package-relative paths; SHA-256 provenance **cannot be tied to Git implementation source `611ec26...`**, installed version, runtime process image or `current.json` target from these fields alone. The current desktop launcher at one inspected scripts path is absent, which does not demonstrate missing installed launcher since `launch.ps1` exists.
- **Three process matches**: two Python processes whose commands refer to current root, and one `FOX2.Bridge.Desktop.exe` whose executable and command refer to current root. Parent/supervisor lineage not independently resolved; no proof of Worker command mode, paused/stop controls, actual claim or one-writer lease.
- Two Scheduled Task entries were returned: one current Bridge logon candidate `Ready` with `pwsh.exe` and current-root reference, one other FOX2 candidate `Disabled` with `pwsh.exe`, `OTHER_FOX2_REFERENCE`. **The output also contains `SCHEDULED_TASK_INVENTORY_UNKNOWN`**; therefore enumeration is **PARTIAL/ERROR**, never a complete negative survey. The other disabled task's exact legacy/current lineage is UNKNOWN. `Ready` is task state, not proof of Worker readiness.
- No matching FOX2 Windows Service entries were returned under the script's name/path predicate; service probe did not report an error. This is a scoped negative, not global retirement.
- The output explicitly reported `worker_control_state=NOT_ATTESTED` and `durable_legacy_retirement=NOT_VERIFIED`. These are preserved, not promoted.

## F1 gate disposition against prior matrix

| Gate | Reviewed status | Justification |
|---|---|---|
| G1 Old/current executable and full launcher/supervisor identity | `PARTIAL/UNKNOWN` | Two new candidate executable digests but no package paths/names or installed provenance; Scheduled Task enumeration incomplete |
| G2 Worker state and exclusive writer | `UNKNOWN` | Three process matches but controls/lease/parent scope absent |
| G3 Durable old writer retirement | `NOT_VERIFIED / HOLD` | Legacy DB present; missing known launch files and Disabled task insufficient to prevent old binary restart |
| G4 Durable consumed-identity convergence across both roots | `UNKNOWN/PROTECTED` | Legacy DB contents not examined under an authorized read-only evidence route |
| G5 F1 positive authority transition | `NOT_IMPLEMENTED/NOT_VERIFIED` | Offline F0 source intentionally uses persistent `DENY_CROSS_ROOT_UNKNOWN`, not positive installed admission |
| G6 Installed exact-source adoption, rollback | `NOT_RUN/UNKNOWN` | No source-to-installed package/pointer/hash lineage |
| G7 Installed real restart/no-replay | `NOT_RUN/HOLD` | No operational activation or real Agent run |
| G8 Seven final Canary/RC1 gates | `NOT_RUN/HOLD` | Out of F1 host inventory scope |

**CHAT result-review verdict:** `ACCEPT_SCOPED_PASSIVE_HOST_OBSERVATIONS`, `HOST_EVIDENCE_INCOMPLETE`, `F1_INSTALLED_ADMISSION_HOLD`, `NO_AGENT_RESULT_CLAIM`. This is an intake of Owner-provided observation, not a test PASS for a larger gate.

## Source and governance

- Projectwide Governance Registry on approved non-main release branch: blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`, scoped human Policy v2.0.0, Dictionary v1.3, Routing v1.4; installed enforcement **NOT_ATTESTED**.
- Final offline F0 source `611ec26c28484de740e963d86de6b00946f1492d`; F0 scoped alternative delivery receipt `4d3330f8f0cf1f3aeaaacc611ff406301858ebbc`. Original CODEX Attempt06 remains `CONSUMED / RESULT_V2_NOT_DELIVERED / NO_REPLAY`.
- Prior F1 readiness matrix: `cdfdb703abe83c76f7aaac7cbd14e5b020a7b106:docs/roadmap/FOX2_F1_LEGACY_RETIREMENT_ADMISSION_READINESS_20261020.md`.
- R0 feature already OPEN/BUILD/BLOCKED; R1 passive host evidence; R2 scoped Owner-supplied output; R3 host PreExec not required for CHAT analysis and report only; R4 CHAT directly; R5 no Agent or installed writer activated, Git commit only on existing non-main branch; R6 readback before acceptance; R7 no runtime mutation/release. `ASSIGNMENT_CHECK=NOT_APPLICABLE`. A future executable host/Agent route still requires separate capability/one-writer/PreExec/source admission.

## Exact next safe action

A **targeted read-only correction** of the partial Scheduled Task inventory error, and non-sensitive binding of the two executable digests to *file names and relative package classes* plus passive parent-process identity. Do not repeat a full generic host audit, inspect SQLite rows, dump `current.json` contents, emit raw task arguments/command-lines, change running tasks/Worker, or enable positive claims. New output must remain private in Chat until vetted. Only once authority/supervisor identities and installed provenance become defensible may CHAT select an F1 design candidate and separately admit any implementation/retirement/rollback steps.

`GOAL_MET=YES_PASSIVE_SNAPSHOT_INTAKE_ONLY`; `F1_READY=NO`; `NEXT_SAFE_ACTION=TARGETED_PASSIVE_EVIDENCE_REPAIR`; `REAL_BLOCKER=SCHEDULED_TASK_INVENTORY_PARTIAL_AND_NO_DURABLE_LEGACY_FENCE_OR_INSTALLED_PROVENANCE`.

Skill coverage: `fox2-source-resolver`, `fox2-result-review`, `fox2-feature-certification`, `fox2-status-roadmap`, `fox2-execution-recovery`, `fox2-governance-preflight` = REQUIRED/APPLIED; `fox2-agent-prompt-builder` = NOT_APPLICABLE (no Agent assignment).

**STOP preserved:** no original Attempt replay; no installed runtime/database/Worker changes, policy or trust release, Canary009/COMPAT001/main/merge/provider/broker/LIVE.
