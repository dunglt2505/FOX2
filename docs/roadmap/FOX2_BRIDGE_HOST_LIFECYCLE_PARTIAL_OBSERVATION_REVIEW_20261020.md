# FOX2 — CHAT Review: Read-only Windows Host Writer/Lifecycle Partial Observation

**Date / provenance:** Owner-provided direct PowerShell 7 JSON from FOXLE-PC, observed `2026-10-20T06:49:53.5511683Z` (2026-10-20 13:49 ICT). `FOX2_HOST_WRITER_LIFECYCLE_OBSERVATION_V1`. **Review type:** bounded source-grounded READ_ONLY partial observation, **NOT** CODEX audit completion or installed runtime certification. CHAT did **not** execute the Windows probes, see private process arguments or independently verify machine identity. Host output says `host_mutation=NONE_REQUESTED`; it is not a machine-wide no-side-effect audit.

**Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` · **Feature:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION` · **Status:** `BUILD/BLOCKED` · **Related host-audit one-shot:** CONSUMED/NO_REPLAY.

## Source / task state

- Governance source: `d34da1e3b4918a902646621b487ca8ad3e05b0e0` human scoped Policy v2.0.0 CODE-FIRST; installed machine enforcement NOT_ATTESTED. Status registry before review `6926ef0306ae1f1a3893449285e969a3ea1aac2a:docs/roadmap/FOX2_FEATURE_STATUS.json`.
- Previous host-audit marker reconciliation `c6e9966eed688bb8b3286e1a2feda5acd129b5cd`: marker valid/consumed per Owner host output, associated result Git branch `work/FOX2-BRIDGE-LEGACY-LIFECYCLE-READONLY-RESULT-20261020@3167d8502588dd106f9a4cea8ef931e9148040ff` remains unchanged, Agent `report.md/evidence_manifest.json` absent. Do not replay.
- Actual CODEX Attempt03 `a3ad10d490993fb4ed4ccfd7d1a73f74cc465581`: six legacy/current root negative no-replay tests FAIL; synthetic current-exit then legacy-restart fixture duplicated claim. This is a safety violation **under fixture semantics**, not evidence of actual old binary currently active.

## Host observations (all are scoped snapshot, not continuous proof)

| Probe | Observation | Permitted inference |
|---|---|---|
| CODEX processes | two processes, neither had observed FOX2 or old audit signature in its command-line signature classification | `CODEX_FOX2_WRITER=NOT_OBSERVED_BY_SIGNATURE`, not `ONE_WRITER_PASS` or evidence no other CODEX context/child writer |
| Other FOX2 process candidates | **3** | actual name/path/args/child-parent associations **NOT_IN_OUTPUT**; cannot label Worker or active dispatch writer |
| Legacy root | `exists=true` | old directory exists; unknown contents/entrypoints |
| Current root | `exists=true` | new directory exists |
| Legacy root `launch.ps1` | `false` | only this exact path absent; no inference retirement or no executable |
| Current root `launch.ps1` | `true` | launcher present, not launch observed |
| Scheduled Task | one `OTHER_FOX2_CANDIDATE`, disabled, 1 trigger | task identity and actual target **NOT_OBSERVED**; cannot assert this is the legacy writer |
| Scheduled Task | `CURRENT_SID_FOX2_BRIDGE`, Ready/enabled, 1 trigger | current-user startup entry is eligible; Ready is not Running nor evidence of authorization to resume |
| Registry HKCU/HKLM Run/RunOnce | 0 FOX2 matches in 4 probed key classes | bounded absence only; 32-bit/WOW6432Node and other surfaces not yet exhausted |
| Matching services | 0 | bounded absence only |
| Startup shortcut targets | NOT_INSPECTED | **UNKNOWN** |
| Script errors | empty | success on visited probes only, not all startup surfaces |
| one_writer | UNKNOWN | **R5 remains HOLD** |
| durable_legacy_retirement | NOT_VERIFIED | safety gate remains BLOCKED |

## Correct next technical question

Before any new CODEX task/Manual Local route, distinguish these specific **three non-CODEX FOX2 candidates** by PID, process/executable basename, root category (LEGACY/CURRENT/OTHER/UNKNOWN), command-line pattern flags **without exporting raw command lines**, parent relationship, start time and whether executable could write the legacy/current ledger. Inspect actual scheduled-task ACTION executable/root-class for both tasks (without raw arguments/SID); inspect .lnk targets in user/common Startup folders and accessible Run/RunOnce/WOW6432Node. Need independent claim-time durable retirement/fencing proof beyond process snapshot, including after process restart.

Do **not** infer that two CODEX command signatures are sufficient to PASS one-writer; they are not. Do **not** infer the disabled OTHER task is legacy or that enabled current task should be run. Do **not** execute any launcher, change scheduled tasks, start/stop Worker, open SQLite/marker payloads, modify registry/startup, touch old CODEX marker or send raw host telemetry to the public repository.

CHAT should first use **direct one-off PowerShell 7 read-only process/task/shortcut attribution** (OWNER_MANUAL_EXECUTION requires full script visible in CHAT). This is separate from the consumed CODEX Agent audit, and its output is not automatically a Git Result v2 submission. No new Agent handoff is selected while current host writer/process authority remains UNKNOWN.

## Decision / gate

`HOST_OBSERVATION_RECEIVED=YES` · `SCOPE=PARTIAL` · `AGENT_INVENTORY=NOT_RUN` · `ONE_WRITER=UNKNOWN` · `LEGACY_RETIREMENT=NOT_VERIFIED` · `BUILD=BLOCKED` · `TEST=SIX_NO_REPLAY_FAIL` · `CANARY009=HOLD` · `INTERNAL_READY=NOT_ATTESTED`.
**NEXT_SAFE_ACTION:** exact attribution of 3 FOX2 process candidates + scheduled-task action classes + startup shortcut targets, without launching CODEX or editing host state. Until verifiable durable old-writer retirement, continue conservative fail-closed design; no Attempt04 coding, no retry or marker removal.

**Skill coverage (actually read):** fox2-execution-recovery REQUIRED/APPLIED; fox2-result-review REQUIRED/APPLIED (bounded negative result, no Agent result); fox2-source-resolver REQUIRED/APPLIED (source/status), fox2-agent-route-runtime APPLIED (CHAT-direct vs host-only), fox2-governance-preflight APPLIED (READ_ONLY stage), fox2-status-roadmap APPLIED (lazy feature); fox2-agent-prompt-builder NOT_APPLICABLE to this direct observation (required only if any NEW Agent task follows).
