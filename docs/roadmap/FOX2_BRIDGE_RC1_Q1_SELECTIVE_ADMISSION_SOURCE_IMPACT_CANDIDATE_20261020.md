# FOX2 Bridge RC1 — Q1 Selective Admission: Source Impact and Minimal Contract

**Date:** 2026-10-20 (Asia/Ho_Chi_Minh)  
**Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` (existing); supporting WP `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019` is not replayed or renamed.  
**Actor:** CHAT / direct Git source-and-contract analysis.  
**State:** `CHAT_DESIGN_CANDIDATE / NOT_EFFECTIVE / NO_CODE_ASSIGNMENT / NO_RUNTIME_ADMISSION / CANARY009_HOLD`.  
**Change type:** CHAT-owned non-main engineering decision document only. This is not a Policy, Dictionary, BRD, TechSpec or Dispatch release.

## 1. Policy, task state and immutable source resolution

- **Current human governance for new CHAT analysis:** Projectwide Registry `d34da1e3b4918a902646621b487ca8ad3e05b0e0:docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json`; source resolution at the same commit under `docs/governance/releases/FOX2_CURRENT_SOURCE_RESOLUTION_20261019.json` selects scoped Policy 2.0.0 / Dictionary 1.3 / Routing 1.4.0 / Git-first v12. `OWNER_APPROVED_PRINCIPLE` and scoped governance publication do not attest Windows runtime adoption. The original Bridge RC1 tasks retain frozen Policy 1.8.9 / Dictionary 1.2 / Routing 1.3 / Protocol v12 at source-set `c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359`, scoped Registry `b27f1085ee13d8dce56fd2735e100ea1616e6e23`.
- **Engineering baseline:** `work/FOX2-BRIDGE-DESKTOP-BATCH-B@f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`. Original historical technical/C3 evidence accepted only for that frozen subject; C3 intake `435154487e8e9bf6eab54a12f1f329e63787aa84`.
- **Original bridge control:** `work/FOX2-DISPATCH-chat@3f885b2d24cb131b5e96dfdb67a44677599197e2`; Canary worktree `work/FOX2-BRIDGE-FINAL-CANARY-009@501822a33ef08c7365154913bbc677544856eee5`. Original Canary009 v0.6 contains `runtime_contract.auto_execute=true`, `max_runs=1`, `delivery_owner=BRIDGE`; its v3 final-cert fixture is validation-only. Do not edit either identity.
- **Infrastructure dependency:** Owner-granted bounded manual admission infrastructure `c23d28bd56d9d06d64561dcf255b2d94227f6acc`; task baseline `482d26d71c5c95f028f9b4110349e4d318bcb342`; current receipt branch `1ce109b9a4c538b255c6d8ffc6be8b4dccecf65d` has **PreExec BLOCKED** at `CHECK_BRIDGE_BOOTSTRAP_CONTROLS`, not `PASS_TO_ASSIGN`. The grant lists primary paths and conditionally allows impact-proven shared dependencies only after CHAT scope binding. It must not be silently stretched to a generic control-plane redesign.
- **COMPAT001:** Original immutable manual-local CODEX Dispatch at control `3f885b2...`, max_runs=1, remains `PUBLISHED/ACTIVATION_HOLD/NO_REPLAY`; no accepted implementation/result. Do not reuse its permission or replay it to bootstrap this contract.
- **Q0 Owner observation (20 Oct):** Owner pasted a **partial** host-produced sanitized JSON, not an uploaded hash-bound original result. Installed package hash matched certified RC1; per-user worker `PAUSED`, `paused=true`, `stop_requested=false`, `current_dispatch=null`, `current_execution=null`; canonical SID logon task enabled and legacy recovery task disabled. Current + legacy inspected dispatch/execution tables had zero exact COMPAT001/Canary009/infra matches; current `candidate_discoveries` had Canary009 = 1. Existing `bridge.lock` metadata read failed; continuous OS lease owner was **NOT_VERIFIED**. One observed Worker/launcher process classified OTHER_ROOT, so process lineage not completely attested. Unrelated auto-exec candidates NOT_VERIFIED. Zero bounded matches ≠ never started, and a heartbeat ≠ execution/admission.
- **Live Git readback before this candidate document:** Bridge `f3d6468...`; Control `3f885b2...`; Canary `501822a...`; infrastructure `1ce109b9...`; prior CHAT roadmap `93b4305a...`. These are Git observations, not live Windows execution.

## 2. Verified source semantics and risk

| Producer / consumer | Exact frozen source and observed behavior | Q1 impact |
|---|---|---|
| Resident Worker, `desktop.py:DesktopWorker.run,tick` | Holds `ProcessLock(.../data/bridge.lock)` for entire run; on PAUSED tick returns without `ops.run_next()`; `stop_requested` stops loop. | No second `BridgeApp` instance should compete for lock; no blanket Worker resume. A resident-worker selective path requires an explicit *new* gated in-worker command and must not enable default polling. |
| OS lock, `process_lock.py` | `msvcrt.locking(LK_NBLCK)` protects byte range; lock metadata PID is not continuous ownership proof. | Keep one owner and lock for validation → claim → spawn; new lock code NOT justified by source inspection alone. |
| External one-shot, `app.py:BridgeApp.start/e2e_once`, `__main__.py` | `BridgeApp.start()` acquires same lock; `e2e-once` calls `BridgeE2ERunner.run_once`. | Current separate CLI cannot execute beside resident Worker; new request transport/API may be necessary. No safe command exists in this baseline. |
| E2E, `e2e_runner.py:run_once` | Polls control branch and writes discovery evidence *before* exact dispatch validation; resolves/creates worktree before durable claim; validates source/prompt then claims and starts Agent. | A selective variant must not reuse the discovery/poll side effect; share existing validators/adapter/result pipeline with narrowly separated preclaim checks. No unbound worktree/Agent side effects. |
| Automatic selector, `ops_runner.py:_eligible_dispatch,run_next` | Picks any matching discovered `auto_execute=true` ID not already present in current ledger; one Canary candidate exists in Q0. | Do not call normal `run_next` to implement exact selective request. Preserve default selection semantics while paused. No current source evidence requires editing `ops_runner.py`. |
| Atomic ledger, `ledger.py:claim_dispatch` | `BEGIN IMMEDIATE`, refuses `paused OR stop_requested` when `honor_controls=True`; existing ID rejects duplicate; inserts dispatch CLAIMED + execution RUNNING in one transaction. `control('request-exit')` sets stop_requested=true while `control('resume')` only toggles paused. | Current paused state cannot admit a claim. New *explicit, scoped* maintenance permit/claim transaction must be designed; NEVER simply pass `honor_controls=False` or globally clear flags. stop_requested always denies new work. |
| Dispatch interface, `dispatch_normalizer.py` and `e2e_runner._validate_dispatch` | Schema v2/v3 `execution_path!=BRIDGE` rejected for auto-execution; legacy v0.6 Worker Canary supported; common validation binds branch/worktree/model/permission/source. | Canonical BRIDGE-selective route must preserve normalizer; MANUAL_LOCAL support is **separate, not silently relabeled**. New schema/Dictionary current pointer NOT justified here. |
| CLI / operator control, `__main__.py`, `desktop.control` | Fixed CLI has status/pause/resume/check-now/request-exit, no supported authenticated exact-dispatch maintenance request; `control status` may call initializing routines. | Requires a distinct admission request protocol/identity, not ad-hoc SQLite edits or an undocumented CLI argument. |
| Tests / source consumers | `tests/test_desktop.py` includes pause/lock/no-replay tests; `test_e2e_runner.py` covers immutable dispatch, single-use claim and post-start ambiguity; `test_ops_runner.py` tests auto_execute opt-in; `test_project_dictionary.py` covers schema/legacy fail-closed. | Must extend exact affected suites with maintenance admission negative/race/restoration tests; all historic PASS remains historical, not fresh implemented tests. |

## 3. Minimal selective admission architecture — **CANDIDATE, not executable**

### Choice A — preferred design to validate, resident Worker owns admission

Introduce a single-purpose, *explicitly authorized* maintenance request routed to the **already running** Worker that holds the OS singleton. The Worker remains `PAUSED` for ordinary discovery and `run-next`; it may process the **exact independently authorized target ID** solely through a new separate maintenance lane, not through an ordinary resume or generic poll. A GUI/tray message, unsigned file or raw local control command is **not** sufficient authorization. The request must bind immutable Git Dispatch blob SHA256/path/control commit, task/prompt/source hashes, permitted actor/model/effort, Owner/CHAT scope, result delivery, freshness/expiry/nonce and task-specific PreExec receipt. Authenticate the operator/host principal by an actually supported trusted mechanism; if provenance or current code capability is unknown, fail closed.

**Atomic state machine, proposed:** `REQUESTED_UNTRUSTED → VALIDATED_NOT_CLAIMED → [one transaction: exact grant/identity check, paused=true, stop_requested=false, no competing or historical claim, durable grant consumption + dispatch/execution claim] → CLAIMED → SPAWN_ATTEMPTED → RUNNING → RESULT_PUSHED_UNREVIEWED or NEEDS_RECONCILIATION → CHAT_ACCEPT/HOLD`. No agent may launch before a durable transaction has completed. Keep `stop_requested` a hard deny. `paused=true` must continue blocking *normal* auto claims; **only** a versioned, Owner-authorized scoped maintenance rule may permit an exact claim with a verified grant. If the governance policy does not allow such selective pause semantics, this option is `HOLD_SEMANTIC_AUTHORITY`, not a covert exception.

The selective implementation must skip `poll_once`/generic candidate selection, use exact pinned immutable Dispatch and the existing common validation, leave Canary009 and every unrelated `auto_execute=true` candidate untouched, preserve the continuous Worker-held OS lock into the durable claim and spawn, and block concurrently submitted/repeated/grant-drift requests. Existing Worker heartbeat/recovery must not reset or revive a one-shot permit. After ambiguous postclaim failure, preserve consumed identity and `NEEDS_RECONCILIATION`; no fallback second-run. Export sanitized evidence sufficient for immutable Git result/CHAT intake.

**Mandatory design/host proof before coding/adoption:** (i) source-supported authenticated request transport and SID/process identity; (ii) actual ownership of installed Worker and current + legacy ledgers; (iii) proof that paused-only maintenance admission can satisfy Policy/Owner semantic boundaries; (iv) transactional grant + claim atomicity under concurrent process and restart; (v) no default `run_next` exposure. These are currently unverified.

### Choice B — alternate, separate one-shot takeover

A host-managed quiescence/maintenance boundary might shut down the existing Worker, prevent all startup entrants, and transfer exclusive singleton ownership to one-shot `BridgeApp`. But this is **NOT supported/verified at the present Q0**: `request-exit` leaves `stop_requested=true`, `resume` does not clear it, `paused` blocks claim, and lock transfer has a time-of-check-to-time-of-use gap. Any alternative must have its own bounded contract and tests; do not construct a local sequence of unsafe manual control/SQLite changes.

### Separation from MANUAL_LOCAL

Choice A can serve as a canonical BRIDGE operational admission/control mechanism, but it **does not implement** `MANUAL_LOCAL` semantics of already published COMPAT001. Any downstream manual-local entrypoint must retain its own mode-sensitive normalizer/approval, use verified shared validation/claim/provenance and be accepted separately. Bridge readiness must not be blocked indefinitely by an optional manual-local path unless the actual readiness gates require it.

## 4. Source-impact allowlist decision: no coding permission from this document

| Path | Change classification | Exact reason / guard |
|---|---|---|
| `agent_bridge/src/fox2_agent_bridge/desktop.py` | **REQUIRED_IF_CHOICE_A_ADOPTED** — Owner infrastructure conditional shared dependency | Resident Worker must consume only the exact authenticated maintenance request while normal paused polling remains blocked. |
| `agent_bridge/src/fox2_agent_bridge/ledger.py` | **REQUIRED_IF_CHOICE_A_ADOPTED** — Owner infrastructure conditional shared dependency | Durable single-use maintenance permit and original atomic claim must be one serializable transaction; old `honor_controls=True` defaults unchanged. |
| `agent_bridge/src/fox2_agent_bridge/e2e_runner.py` | **REQUIRED_IF_CHOICE_A_ADOPTED** — existing primary infrastructure path | Share validation, worktree and immutable prompt verification, Agent adapter, checkpoints and delivery without preclaim poll/discovery; keep normal run_once unchanged. |
| `agent_bridge/src/fox2_agent_bridge/__main__.py` | **CONDITIONAL** — existing primary infrastructure path | Only if a supported authenticated operator-request CLI is chosen; should not spawn Agent or take Worker lock itself. |
| `agent_bridge/src/fox2_agent_bridge/app.py` | **CONDITIONAL** — existing primary infrastructure path | Only if request processing needs an app-layer API; no second BridgeApp alongside live Worker. |
| `agent_bridge/src/fox2_agent_bridge/dispatch_normalizer.py` | **NO_CHANGE_FOR_CANONICAL_BRIDGE_SELECTIVE** | MANUAL_LOCAL future separate scope, automatic BRIDGE-only rejection retained. |
| `agent_bridge/src/fox2_agent_bridge/ops_runner.py` | **NO_CHANGE_UNLESS_PROVEN_FAILURE** | Must not select maintenance requests or unrelated Canary; existing paused no-poll remains intact. |
| `agent_bridge/src/fox2_agent_bridge/process_lock.py` | **NO_CHANGE_UNLESS_PROVEN_FAILURE** | Reuse the existing resident OS lock; Q0 failed metadata read does not prove a lock-library defect. |
| `agent_bridge/src/fox2_agent_bridge/dispatch_poller.py` | **NO_CHANGE_UNLESS_PROVEN_FAILURE** | Selective path skips poller; avoid modifying global discovery/cursor semantics. |
| `agent_bridge/src/fox2_agent_bridge/agent_policy.py`, `config.py`, generated Dictionary/schema | **NO_CHANGE_UNLESS_CONSUMER_PROOF** | No source evidence presently requires changed routing, global config or identity/release version. |
| `agent_bridge/tests/test_desktop.py`, `test_e2e_runner.py` | **REQUIRED_IF_CHOICE_A_ADOPTED** | Negative/race/stage tests for resident claim and exact execution. |
| `agent_bridge/tests/test_ops_runner.py`, `test_project_dictionary.py` | **REGRESSION_RUN_REQUIRED; FILE_EDIT_CONDITIONAL** | Prove existing automatic selection and MANUAL_LOCAL fail-closed semantics remain unchanged. |

No blanket `agent_bridge/**`. CHAT must bind any proved dependent file's exact allowed path under the existing Owner infrastructure approval and applicable trust-source scope **before** a fresh executable assignment. If altering the Worker to run selectively while PAUSED materially exceeds the Owner's previously approved infrastructure scope, separate Owner authorization is required and original BLOCKED receipt remains BLOCKED.

## 5. Acceptance / negative tests (all NOT_RUN for proposed code)

1. **PAUSED isolation:** worker paused remains paused; ordinary `tick`/run-next cannot select Canary009 or any discovered unrelated auto-executable ID.
2. **Exact target and provenance:** wrong Dispatch/prompt/task commit, SHA256, Owner, schema, source head, branch/worktree, model/effort/FULL_ACCESS, SID, expiry/nonce or Git remote readback → NO CLAIM, NO SPAWN.
3. **PreExec:** missing, stale, wrong-WP or BLOCKED PreExec receipt and pending current authority → NO CLAIM, NO SPAWN. Old immutable receipt not rewritten.
4. **Controls:** stop_requested true always denies; ordinary paused claim denies; scoped maintenance claim requires exact valid grant, never generic `honor_controls=False` to bypass policy.
5. **Race:** two requests, two Worker candidates, same/other ledger and simultaneous pause/stop update yield at most one durable attempt; denied requests cannot leave partial claim/permit.
6. **Historical no-replay:** existing FAILED, CLAIMED, RUNNING, PUBLISHING, NEEDS_RECONCILIATION, manually consumed or unknown execution identity (current/legacy/marker) → NO SPAWN. Never infer never-started from empty subset tables.
7. **Crash stages:** before claim, after claim/before spawn, during Agent, after push/before ACK, after restart → no accidental second spawn; honest NEEDS_RECONCILIATION when evidence uncertain.
8. **Control transport:** untrusted host request, non-owner SID, stale process owner, spoofed file/JSON, malicious request, OS-lock drift and missing package identity fail closed.
9. **No poll side effect:** exact maintenance request does not call discovery polling or advance ordinary control cursor; only the exact permitted immutable target is addressed.
10. **Delivery & K1:** no unrelated file changes; report/evidence_manifest + exact non-main remote result SHA; change classes REQUESTED/NECESSARY_DEPENDENCY/JUSTIFIED_GENERATED; no code or result considered accepted until CHAT remote-readback.
11. **Installed adoption:** dispose-only test instance first; after code acceptance separate authority for installation/quiescence and rollback, installed package hash, real singleton, stale/legacy reconciliation and no-replay; no hot-swap of active Worker.
12. **Frozen compatibility:** old v1 PreExec regression, v3 schema/normalizer and legacy v0.6 Canary remain unchanged and validated; cannot promote fresh code/unit PASS to RC1 C4/Canary PASS.

**Acceptance threshold:** actual focused + regression logs, negative cases, K1 diff, single-writer/host provenance and CHAT Result Review. Until then `ALL_NEW_IMPLEMENTATION_TESTS=NOT_RUN`; `CANARY009=HOLD`; `INTERNAL_FOX2_BRIDGE_READY=NOT_ATTESTED`.

## 6. Routing R0–R7, assignment check and next safe action

| Gate | Scope-specific result |
|---|---|
| POLICY_CHECK | CHAT's read-only source review/candidate document is within Owner-directed Bridge assessment; not a grant for runtime or new model/execution. |
| TASK_STATE_CHECK | Reused existing Bridge Whole-WP, infrastructure blocked receipt and protected COMPAT001/Canary; no new Dispatch or task identity. |
| SOURCE_RESOLUTION | Used current Owner-approved scoped human Registry and frozen RC1 identity separately; no new `EFFECTIVE`, no silent rebind. |
| R0 / R1 | Reuse Q0 Owner-observed snapshot and accepted C3; existing RC1 `TEST/BLOCKED`; design candidate only, no repeat C1/audit. |
| R2 | Owner grant `c23d28...` supports infrastructure candidate analysis; for changed Worker/ledger contract verify exact scope and bind impact-proven allowlist before an executable task. |
| R3 / R5 | CHAT Git connector can do read-only analysis and permitted non-main docs publication; Windows exclusive writer, worker OS lock, CODEX auth/quota and actual deployment permission **NOT_VERIFIED**, cannot imply admission. |
| R4 | CHAT DIRECT-FIRST for source impact; no CODEX/COPILOT/WORK assignment. Host/Agent only for residual authorized work. |
| R6 | This candidate document must be published only to existing CHAT-owned non-main branch and independently fetched as exact Git content/blob/SHA; no Library effective document release requested. |
| R7 / ASSIGNMENT_CHECK | `GO_CHAT_DOC_CANDIDATE_ONLY`; `HOLD_EXECUTABLE_ASSIGNMENT`; `NO_CANARY`, no Worker control change, release or LIVE. |

**Skills:** REQUIRED/APPLIED: `fox2-source-resolver`, `fox2-governance-preflight`, `fox2-agent-route-runtime`, `fox2-execution-recovery`, `fox2-techspec-validator`, `fox2-strategic-agent-triage`, `fox2-document-publication`. NOT_APPLICABLE: `fox2-agent-prompt-builder` (no new Agent handoff), `fox2-result-review` (no Agent result), `fox2-dictionary-impact` (no Dictionary/field-change proposal), `fox2-brd-change-control` (no BRD change), `fox2-thread-handoff` (no context transfer). Cloud-host shared matrix file separately UNAVAILABLE; Skill-embedded routing applies.

**Decision:** `CHOICE_A=PREFERRED_DESIGN_CANDIDATE_NOT_ATTESTED`; `CHOICE_B=UNSUPPORTED_ON_CURRENT_EVIDENCE`; `Q1_SOURCE_IMPACT=COMPLETE_FOR_CANDIDATE`; `CODEX_IMPLEMENTATION=HOLD`; `NEXT_SAFE_ACTION=bind exact selective-admission authority/maintenance semantics and resolve route-specific bootstrap without circular PreExec; then govern bounded coding/tests on existing Whole-WP`. Any future implementation change requires actual supported host path or a separately authorized independent offline DEV route that does not falsely convert the blocked BRIDGE task into a native task.

**NO** editing historical source, existing Dispatch/prompt/receipt, Feature Status Registry release status, production code, main merge, Worker restart, canary claim or broker/LIVE as a result of this record.
