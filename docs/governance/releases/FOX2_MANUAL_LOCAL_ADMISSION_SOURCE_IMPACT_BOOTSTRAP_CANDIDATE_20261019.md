# FOX2 — Manual Local Admission: Contract, Source Impact & Bootstrap
Status: CANDIDATE_SOURCE_LOCKED / NOT_EFFECTIVE / NO_EXECUTION_AUTHORITY
Date: 2026-10-19 | Project: FOX2 ONLY | Prepared by: CHAT
Scope: unblock bounded PreExec compatibility task without rewriting existing Dispatch.
This is a candidate engineering decision record, not an effective Policy/Schema release, admission certificate, code grant or Agent launch.

## A. Frozen bindings and observed facts

Repository `dunglt2505/FOX2`. Frozen WP-only Registry `b27f1085ee13d8dce56fd2735e100ea1616e6e23`; governance `c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359`; Bridge runtime inspected at `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`.

Existing compatibility task: `FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018`; source `502f2aefbda35e4fec134dfb9d5f15f3222660d5`, current task HEAD `fd3141f8e825931f9ee17d68c740e3b36230aa96`, PreExec v1 receipt `fd3141f8e825931f9ee17d68c740e3b36230aa96` and CHAT intake `b2879ed71d55fd9e4488c8dcef0a2fff012f7d9c`.

Immutable compatibility Dispatch: `FOX2-DISPATCH-PREEXEC-COMPAT-CODEX-001` at control `work/FOX2-DISPATCH-chat` commit `3f885b2d24cb131b5e96dfdb67a44677599197e2`, blob SHA-1 `f2c95af3a32ee859e96351232fa2c6d824186d53`, SHA-256 `645fac3550868aa980df3897a066599e8927d3217ff4a44881b0353e8db3da7c`. Route is `CODEX / PINNED gpt-6.1-sol / medium / FULL_ACCESS / MANUAL_LOCAL / AGENT / max_runs=1`. This Dispatch is PUBLISHED, not proved ACTIVATED. No relabel, rebinding, replacement, duplicate, replay, or code under its authority while admission is HOLD.

Canary009: protected task HEAD `501822a33ef08c7365154913bbc677544856eee5`; never claim/run/replay, edit control/prompt/head, or change installed runtime for it.

Host operator's latest read-only report (not independently observed by CHAT): remote bytes and heads verified; current/legacy ledger rows absent for this task, manual marker absent, worker PAUSED, worktree clean. These observations do not establish an activation mechanism or independently prove Agent never started: `HOST_ADMISSION=HOLD`, `AGENT_STARTED=UNKNOWN`.

### Why admission is blocked (source inspection, not inference from names)

- Dictionary v1.2 includes `MANUAL_LOCAL` as an accepted machine identity, but that alone does not implement activation.
- `agent_bridge/src/fox2_agent_bridge/dispatch_normalizer.py` rejects execution_path other than `BRIDGE` for Bridge auto-execution.
- `agent_bridge/src/fox2_agent_bridge/__main__.py` has `e2e-once` (explicit exact dispatch) and `run-next`; it has no dedicated `MANUAL_LOCAL` admission entrypoint.
- `agent_bridge/src/fox2_agent_bridge/ledger.py` has atomic `claim_dispatch`, but no authorized manual caller is established.
- `agent_bridge/src/fox2_agent_bridge/desktop.py` imports `manual_consumption.json` into `NEEDS_RECONCILIATION`; adding an ID is NOT an execution permit.
- `agent_bridge/tests/test_project_dictionary.py` contains fail-closed non-BRIDGE rejection tests.
- `agent_bridge/src/fox2_agent_bridge/e2e_runner.py` does pre-claim validation then durable claim; current auto Bridge path is not synonymous with MANUAL_LOCAL.
- A worker PAUSED state and existing worker processes require independent host lock/claim checks. Never silently resume, stop, or bypass the control.

## B. Candidate target Manual Local Admission v0.1 (not yet implemented)

Design one explicit operator-initiated manual entrypoint, tentatively `manual-once --dispatch-path <exact canonical path>`, sharing the existing authoritative Bridge transport, validators, ledger, lock and Agent adapter. The entrypoint name is PROPOSED; do not invoke it before implementation/adoption.

Semantic invariants:
1. Explicit invocation only; no poller `run-next` selection of MANUAL_LOCAL and no silent conversion of `MANUAL_LOCAL` to `BRIDGE`.
2. Verify effective WP-only authority; exact immutable dispatch commit/blob/SHA-256; Dictionary/Policy/task/Owner/CHAT receipt; immutable prompt commit/blob/SHA-256; model, effort, Full Access, worktree/base, allowed paths and protected rights. Recheck live remote branch heads and local worktree.
3. Inspect current and legacy ledger, execution records/checkpoints, any manual consumption/recovery markers, active processes and worker locks. Unknown, conflicting or previously claimed/started/consumed must STOP.
4. Obtain OS-backed shared runtime singleton/exclusive writer protection and atomically create exactly one durable dispatch claim + execution attempt BEFORE Agent launch, with immutable dispatch hash, agent tuple, source lock and initial checkpoint. No time-of-check/time-of-use gap. Missing or failed durable write => NO SPAWN.
5. Respect PAUSED/stop_requested and competing worker controls; any alteration of controls needs separate governed host approval and must not expose unrelated executable Dispatches.
6. Launch only selected CODEX, exact pinned `gpt-6.1-sol / medium / FULL_ACCESS`, and max one actual attempt. Preserve credential safety; do not disclose raw auth output.
7. Persist SPAWN_ATTEMPTED / RUNNING / EXITED / PUBLISHING / completed-or-NEEDS_RECONCILIATION evidence with precise semantics. After ambiguous spawn, crash, timeout or nonzero exit, fail closed. Do not auto-retry, even when prior step may have failed before model launch, until a separately approved recovery decision and proven no-replay semantics.
8. AGENT delivers only authorized non-main task branch/report paths; final publish/readback is not `CHAT_ACCEPTED` or `RELEASED_EFFECTIVE`.
9. Preserve v1 PreExec semantics, existing Dispatch/receipt bytes, current Bridge auto-execution for `BRIDGE`, legacy ledger safety and Canary009 hold.
10. Reject manual activation before toolchain build/tests/adoption and independent CHAT acceptance.

Acceptance: synthetic fixture + disposable remote integration tests covering exact hash drift, wrong target/route/agent/model/effort, PAUSED, competing writer/process, pre-existing/legacy consumed, marker-only reconciliation, atomic race double claim, crash before/after claim/spawn, failed checkpoint, remote drift, WIP, file allowlist, false push/readback, and no rerun after uncertain outcome. Explicit proof that BRIDGE continues to reject automatic MANUAL_LOCAL. No actual Canary009 or Dispatch001 execution during tests.

## C. Source-impact / proposed allowlist

Review baseline `f3d6468...` and current task before implementation. Proposed *core* code changes for the dedicated admission infrastructure WP (NOT covered by the previous compatibility coding task's grant):
- `agent_bridge/src/fox2_agent_bridge/dispatch_normalizer.py`: mode-sensitive selection; auto BRIDGE rejection unchanged.
- `agent_bridge/src/fox2_agent_bridge/e2e_runner.py`: reuse checked validation/claim/adapter pipeline, explicit operator-triggered manual mode; no cloned execution engine.
- `agent_bridge/src/fox2_agent_bridge/app.py`: bounded manual entrypoint orchestration with shared lifecycle.
- `agent_bridge/src/fox2_agent_bridge/__main__.py`: explicit CLI command and arguments.
- `agent_bridge/tests/test_project_dictionary.py`: positive manual-only entrypoint and auto rejection.
- `agent_bridge/tests/test_e2e_runner.py`: end-to-end synthetic/negative/race/replay contract.

Conditional dependencies, NOT automatically allowed for code modification: `ledger.py`, `desktop.py`, `process_lock.py`, `codex_adapter.py`, `agent_policy.py`, `config.py`, `ops_runner.py`, `dispatch_poller.py`, `project_dictionary.py`, `generate_project_dictionary.py`, or their tests. Each needs specific failure/consumer proof and new CHAT scope decision, with Owner code authorization where required. No wildcard `agent_bridge/**`.

Documentation/report candidates live only under a separately created infrastructure task; do not edit the existing immutable Dispatch001 or its coding prompt. Schema v3/Dictionary v1.2 remain unchanged unless material compatibility proof establishes a governed source-change requirement. All material diff hunks require K1 classification: `REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED`.

## D. Bootstrap dependency resolution (safe staged route)

**D0 / NOW: Candidate-only publication.** CHAT can publish this decision record on an isolated non-main docs branch and exact-byte remote readback. It is neither a new executable Dispatch nor admission.

**D1 / Before any new code:** create a separate SOURCE_READY infrastructure WP for manual-admission implementation with explicitly bounded Owner code authority for C's core paths, fresh PreExec v1, CHAT intake/R0–R7, exact agent route and own executable Dispatch. Do not reuse compatibility Dispatch001, its receipt, or the protected Canary. This is a genuine dependency task, not a workaround to self-authorize code.

**D2 / Bootstrap via an existing mechanism:** use a separately validated `execution_path=BRIDGE` Dispatch for D1. The baseline exposes explicit `fox2-bridge e2e-once --dispatch-path <new-infrastructure-dispatch>` backed by atomic ledger claim; this is a CONDITIONAL candidate bootstrap route, not automatic permission or tested host readiness. Verify installed compatible runtime, correct control config, exclusive lock, paused/stop controls and absence of competing/auto-eligible work. If any required host condition is unresolved, HOLD; do NOT silently resume workers, bypass lock, mutate ledger/marker, change Dispatch001 to BRIDGE, or spawn an unrecorded CODEX.

**D3 / Acceptance:** after D1 code/test/report Git push, CHAT reviews diff, all impacted consumers/tests, exact readback, safety and release scope. Separate authorized installed-runtime adoption with rollback/readback proof; no hot-swap of active worker.

**D4 / Unblock existing Dispatch001:** repeat only fresh time-sensitive admission observations and use adopted, verified explicit MANUAL_LOCAL mechanism. Verify no previous claim/attempt in all stores, and protected Canary untouched. If PASS, invoke existing immutable Dispatch001 at most once; its separate PreExec compatibility implementation remains limited to its original 4 code paths and 3 candidate contract paths.

**Fallback:** if the existing BRIDGE execution mechanism cannot meet D2's paused/lock/control/host constraints, STOP and return to CHAT for a source-bound alternative bootstrap design; no fresh synthetic entrypoint, local shortcut, duplicate Dispatch or exception disguised as PASS.

## E. Gate / responsibility

Candidate source design: CHAT (this document). Infrastructure implementation: CODEX after independent D1+D2 admission (not presently started). Independent review as needed only for material system-level risk. CHAT alone accepts result and governs installed adoption. Original compatibility task and Canary009 remain on HOLD until D4.

```text
MANUAL_LOCAL_CONTRACT=CANDIDATE_NOT_EFFECTIVE
SOURCE_IMPACT=PROPOSED_BOUNDED_NOT_CODE_APPROVED
BOOTSTRAP=CONDITIONAL_EXISTING_BRIDGE_ROUTE
DISPATCH001=PUBLISHED_HOLD_NO_ACTIVATION
HOST_ADMISSION=HOLD
AGENT_STARTED=UNKNOWN
CANARY009=HOLD
```
