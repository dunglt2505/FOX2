# FOX2 — CHAT PreExec BLOCKED Intake and Worker Quiescence / Singleton Admission Runbook
Date: 2026-10-19 | Role: CHAT | Scope: FOX2 Manual Local Admission Infrastructure WP only
State: CHAT_INTAKE_BLOCKED / GOVERNED_PROCEDURE_CANDIDATE / NOT_EFFECTIVE / NO_DISPATCH_EXECUTION_AUTHORITY
WP: `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`

## 0. Immutable evidence accepted for this intake

- Owner scoped full end-to-end authorization was recorded, source `c23d28bd56d9d06d64561dcf255b2d94227f6acc`; authority covers bounded Manual Local Admission infrastructure but does NOT waive PreExec/worker admission/no-replay or protected rights.
- Task source document: `482d26d71c5c95f028f9b4110349e4d318bcb342:docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/task.md`, task bytes SHA-256 `ffd9b35b8e98d1dc7ae824945cba963d96c8cd0e1cf67e42220ab2cacafab188`.
- Engineering contract candidate: `1177388dd8e75697778f25cd166cced672653b5d:docs/governance/releases/FOX2_MANUAL_LOCAL_ADMISSION_SOURCE_IMPACT_BOOTSTRAP_CANDIDATE_20261019.md`; SHA-256 `5a9a9913389051af65ab70b707c3f25bd10fd0d60be982aed3230c191e46eebc`.
- Frozen Policy/Dictionary/Routing and WP-only Registry: `c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359` / `b27f1085ee13d8dce56fd2735e100ea1616e6e23`.
- Actual immutable BLOCKED receipt: `1ce109b9a4c538b255c6d8ffc6be8b4dccecf65d:reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/preflight_receipt.json`.
  - SHA-256 independently recalculated by CHAT from GitHub UTF-8 content: `32eea3f51bcb5b4d0cb7c521dae94c7b526d666d4826c94ecb76a547f622be9e`.
  - Git blob SHA-1: `9f31447dc782e2219db7784d290c5b210e057650`.
  - Receipt publication commit changes exactly one path (the receipt). Checked remote task branch HEAD equals `1ce109b9a4c538b255c6d8ffc6be8b4dccecf65d`.
  - Source/task head embedded in historical receipt is correctly `482d26d71c5c95f028f9b4110349e4d318bcb342`, its publication parent.
- Host handoff furnished by Owner as uploaded `CHAT_HANDOFF.md`: task-specific shared `PreExec(Requirements(...))`, Git/GitHub byte readback, clean task worktree and no-replay search, worker snapshot `paused=true`, `stop_requested=false`, two Bridge worker processes at time of observation. These process-level claims are host-reported, NOT independently observed by CHAT from Windows.
- Remote protected refs at intake: control `work/FOX2-DISPATCH-chat` @ `3f885b2d24cb131b5e96dfdb67a44677599197e2`; Canary009 `work/FOX2-BRIDGE-FINAL-CANARY-009` @ `501822a33ef08c7365154913bbc677544856eee5`.

## 1. CHAT Intake Checklist v1.1 verdict

Identity / task binding: PASS from immutable receipt + existing source/Owner grant.
Remote publication / exact SHA-256: PASS.
Worktree owner, cleanliness, local writer and no replay for *new infrastructure WP*: PASS AT RECEIPT SNAPSHOT only; must recheck for activation.
CODEX `PINNED gpt-6.1-sol / medium / FULL_ACCESS`: PASS for bounded marker probe and aggregate `eligible_agent_route`; actual separate model telemetry/quota not independently exposed, not an unlimited capacity claim.
Sanitization/schema: host reports PASS; remote receipt is machine-readable sanitized v1 (no product tests).
Required `bridge_bootstrap_controls`: **FAIL material**, `BRIDGE_BOOTSTRAP_CONTROL_HOLD` / `CHECK_BRIDGE_BOOTSTRAP_CONTROLS`.
Overall preflight state: **BLOCKED**. Historical `dispatch_consumed=false` and `agent_execution_started=false` apply ONLY to new infra WP, not original Dispatch001/Canary009.
R0–R7 aggregate admission: **HOLD/BLOCKED** at material execution/worker readiness; R3/R5 must NOT be closed by successful CODEX probe or clean task worktree alone. Do not forge PASS for individual numbered routing stages without current evidence and controlling per-stage policy. CHAT final `PASS_TO_ASSIGN`: **DENIED_PENDING_NEW_PASS_RECEIPT**. New executable infrastructure Dispatch: **NOT_PUBLISHED**.

## 2. Findings about currently inspected Bridge runtime

Read-only code inspected at baseline `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`:

1. `desktop.py:DesktopWorker.run()` acquires `bridge.lock`, writes `stop_requested=false` at STARTING, operates polling loop while `paused=false`, and releases singleton lock on exit. A worker being PAUSED does not prove the OS lock is free.
2. `app.py:BridgeApp.start()` also acquires the same `bridge.lock` before one-shot operations; thus `e2e-once` cannot safely race an active worker.
3. `ledger.py:SQLiteLedger.control('request-exit')` sets `stop_requested=true`; `control('resume')` sets `paused=false` but does NOT reset `stop_requested`. Therefore the naive `request-exit -> wait -> resume -> e2e-once` path remains claim-blocked. Do not manually clear `stop_requested` via SQLite editing or synthetic control operations.
4. `e2e_runner.py:run_once()` checks `can_claim` and uses `ledger.claim_dispatch(... honor_controls=True)`. The latter atomically refuses claims when `paused` OR `stop_requested`. Status-only proof and momentary lock availability cannot substitute for claim admission.
5. `ops_runner.py` selects `auto_execute=true` Dispatches for `run-next`; resuming a resident worker can expose unrelated Dispatches to auto-execution. No implicit `resume`.
6. `startup.py` + `desktop_startup.ps1` govern a per-user logon scheduled task; changes require reversible host-operation approval and fresh evidence, not automatic runtime installation or unregistration by this document.
7. Present source has no established public CLI that atomically quiesces all worker processes, clears sticky `stop_requested` safely and transfers a singleton lease into exact one-shot `e2e-once`. A new mechanism or source-proven alternate supported path may be required. **DO NOT claim the original proposed Bridge bootstrap is executable until this gap is resolved.**

These are code findings for the inspected baseline only; compare actual installed runtime version and current process binaries before treating them as host facts.

## 3. Governed host quiescence and admission — controlled procedure, NOT an execution order

### Q0. Baseline inventory (read-only; HOST OPERATOR)

Inspect both observed worker process identities afresh (PIDs may change); per-process owner/SID, executable path, command line, parent/launcher, current vs legacy installation config and ledger, runtime version, process start time, lock-file root, tray presence and scheduled-task startup sources. Identify whether processes share a singleton, whether one is blocked attempting startup, or whether separate roots/ledgers permit competition.

Query current and legacy ledgers in read-only mode for all nonterminal executions, CLAIMED/RUNNING/PUBLISHING/NEEDS_RECONCILIATION statuses, control pause/stop flags and current_dispatch. Inspect manual marker and exact new WP identity. Record a sanitized bounded snapshot (no secrets, raw CLI dumps or credential-bearing paths).

If any process, owner, ledger, dispatch state or lock cannot be attributed deterministically: `HOLD_WORKER_IDENTITY_UNKNOWN`.

### Q1. Prevent new entrants (reversible design; no change before gate)

Identify logon scheduled task and tray/UI auto-restarts or competing supervisors. Design a reversible maintenance quiescence boundary for the specific FOX2 Bridge user, without affecting other users or other work. Record current startup state and rollback plan. Do not disable startup/stop/resume by guessing. No worker control mutation has been performed by CHAT.

Host must prove there are no eligible unrelated auto-execution entries that could run during any permitted control transition. If such entries exist, HOLD until individually reconciled; never consume them or clear ledger as a workaround.

### Q2. Quiesce worker process (host-controlled action only after Q0/Q1 accepted)

Prefer a supported graceful shutdown for each *identified* worker/config, with evidence of no in-flight Agent/publishing. Never kill workers with unverified side effects or assume an old process belongs to the current ledger. Prove OS process exit and stable no-worker state, plus relevant legacy ownership.

If `request-exit` is the selected supported shutdown path, preserve evidence that it sets `stop_requested=true`. Do not claim bootstrap-ready based on exit alone, and do not call `resume` as an alleged clear of this flag. If all observed shutdown paths leave the runtime claim-blocked, return `HOLD_STICKY_STOP_REQUESTED` and escalate an explicit source-bound control/lease remediation; do not bypass guard or mutate SQLite by hand.

### Q3. Singleton & control-state proof (host evidence; MUST hold into claim)

Demonstrate that the *same installed runtime* planned for one-shot execution can obtain the correct OS-backed `bridge.lock` exclusively and keep that protection continuously through source validation, durable claim and Agent launch. A temporary test-acquire/release by itself is insufficient proof because another supervisor can enter afterward.

The actual authorized admission path must atomically refuse already claimed/consumed/started new-WP Dispatch in both relevant stores. Neither a successful marker probe, a clear Git worktree, nor a nonexistent Dispatch row alone proves an actual viable activation contract.

Host must show `paused=false` and `stop_requested=false` at the time of claim **without** exposing unrelated workers to auto-execution; evidence must demonstrate a supported, reversible, race-free transition. If no current CLI supports this transition, `BRIDGE_BOOTSTRAP_ADMISSION=HOLD_UNIMPLEMENTED_CONTROL_HANDOFF`.

### Q4. Accepted remediation boundary

CHAT may approve a narrowly scoped **candidate** operator procedure after Q0/Q1; actual controls may be changed only by the governed HOST OPERATOR once safety criteria are satisfied. If current runtime lacks a safe control handoff, first publish a separate source-bound compatible host-control contract/change within Owner-granted bounded infrastructure scope; do not use an ad hoc direct SQLite edit, custom unrecorded Agent spawn or conversion of old `MANUAL_LOCAL` Dispatch001 to `BRIDGE`.

An engine/code/runtime change to implement this handoff must itself have independently valid PreExec/assignment/Dispatch or another previously effective execution path. If bootstrap cannot be established without bypassing those gates, STOP and request explicit architecture/governance resolution; no circular self-authorization.

### Q5. Fresh PreExec after remediation (append-only)

The original BLOCKED receipt at `1ce109b9...` is immutable history and MUST NOT be deleted or rewritten. At any new attempt, bind `Requirements.source_head` to the task branch's **fresh checked HEAD** (currently `1ce109b9...`); verify identical task.md bytes against immutable source commit `482d26d...`. Do not pretend the branch HEAD is still `482d26d...`.

Use a new exact receipt path matching shared v1 `reports/.../preexec/*.json`, for example `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/preflight_recheck_20261019_01.json`. Never use a legacy/other-WP profile. Shared `PreExec(Requirements(...))` should bind task-specific route/capabilities, preserve all material observations, check writer/WIP/remote head, publish only one report path and validate remote exact bytes. If preexec engine or source binding rejects the append-only plan, HOLD and resolve that contract: no historical receipt rewrite.

Only an actual fresh **PASS** receipt and CHAT independent Intake/R0–R7 acceptance can authorize `PASS_TO_ASSIGN` and subsequent immutable infrastructure executable Dispatch publication.

### Q6. Later Dispatch/one-shot & recovery (conditional; NOT AUTHORIZED NOW)

After Q5 PASS + CHAT acceptance, publish a separate exact executable Dispatch for infra WP, validate installed compatibility and run at most one claimed BRIDGE `e2e-once --dispatch-path <new infra dispatch>` through the proven singleton/control handoff. The actual durable claim must precede CODEX spawn. In any uncertainty, `NEEDS_RECONCILIATION`, no replay or alternate Agent. Results still require CHAT independent review and separate installed-runtime adoption.

Do not touch published original `FOX2-DISPATCH-PREEXEC-COMPAT-CODEX-001`, immutable Canary009, PR/main/merge/provider/broker/LIVE or installed release authority.

## 4. Next host-only handoff: bounded read-only Q0/Q1

Role: HOST OPERATOR / CODEX gpt-6.1-sol Medium for *read-only* host discovery; no executable Dispatch and no implementation.
Return: exact process-to-ledger-to-lock mapping, currently alive PIDs/executable versions, scheduled startup/tray state, per-ledger paused/stop/current_dispatch, terminal/nonterminal snapshots, supported shutdown semantics, a concrete race-free singleton/claim strategy or `HOLD_UNIMPLEMENTED_CONTROL_HANDOFF`; identify what would remain after `request-exit`.

STOP on identity uncertainty. No process kill, control resume/exit, startup toggle, consumption marker, SQLite writes, implementation code or real Dispatch test as part of Q0/Q1.

## 5. Canonical verdict

```text
HOST_PREFLIGHT_RECEIPT=BLOCKED
HOST_PREFLIGHT_PUBLICATION=PASS
RECEIPT_SHA256_MATCH=YES
CHAT_INTAKE=BLOCKED
ROUTING_R0_R7=HOLD_AT_MATERIAL_HOST_GATE
R3_R5_CLOSURE=NO
OWNER_CODE_AUTHORIZATION=APPROVED_BOUNDED
NEW_INFRA_DISPATCH=NOT_PUBLISHED
AGENT_IMPLEMENTATION=NOT_STARTED
WORKER_QUIESCENCE=NOT_PROVEN
BRIDGE_BOOTSTRAP_CONTROL_HANDOFF=UNVERIFIED_NOT_ESTABLISHED
NEXT_OWNER=HOST_OPERATOR_Q0_Q1_READ_ONLY
ORIGINAL_DISPATCH001=HOLD
CANARY009=HOLD
```
