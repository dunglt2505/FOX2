# FOX2 Bridge P0 — Native DEV Route Selection and Actual Host Admission Contract

**Date:** 2026-10-19 (Asia/Ho_Chi_Minh)
**Existing task only:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019` under Bridge RC1 Whole-WP.
**Stage:** CHAT route/source decision and host preflight handoff, NOT Agent implementation, executable Dispatch or runtime release.
**Disposition:** `NATIVE_DEV_ROUTE_SELECTED_IN_OWNER_DIRECTED_SCOPE / HOST_ADMISSION_UNKNOWN / EXECUTABLE_ASSIGNMENT_HOLD`.

## 1. Authority and immutable identity

- New direction: Owner's latest “làm tiếp đi” in response to the 2026-10-19 Bridge P0 root-cause analysis explicitly asks CHAT to continue validating and regularizing a separate native DEV route for repairing Bridge. Interpret this as permission to **prepare/select and validate the narrow route**, **not** a waiver of PreExec, grant to start any Agent, or permission to run the protected Dispatch.
- Existing bounded Owner code authorization, no reapproval required for same code scope: `work/FOX2-MANUAL-ADMISSION-OWNER-chat-20261019@c23d28bd56d9d06d64561dcf255b2d94227f6acc:docs/governance/releases/FOX2_MANUAL_LOCAL_ADMISSION_OWNER_EXECUTION_AUTHORIZATION_20261019.json`, blob `dbc397375bb50ff4d87e093b114d5dda44d159b7`. Owner intent: complete this same infrastructure task under appropriate guards. No widening of allowed source files.
- Projectwide human Governance: `main@e26fc7aa87e787852407261db90506b3516ba5de`, Policy v2.0.0, blob `2d373f374f906bf7959062050bbeae5350b0c482`. Policy explicitly allows independent native CLI DEV and forbids treating Bridge PAUSED as a DEV prerequisite if that route does not use Bridge. Later Owner ordering: **Bridge P0**, APP P1, recorded on `work/FOX2-BRIDGE-P0-OWNER-PRIORITY-20261019@f1725b031010433cb5a8795946c3d4d991b18abe`; PR #15 remains a separate publication step, not a product gate.
- Original task: `work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019@1ce109b9a4c538b255c6d8ffc6be8b4dccecf65d:docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/task.md`, blob `7a2d6405d39ee54fae8c44f979bf44bb700bcf3b`, SHA-256 `ffd9b35b8e98d1dc7ae824945cba963d96c8cd0e1cf67e42220ab2cacafab188`.
- Existing source implementation baseline: `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`. Owner grant preserves the task's WP-only historical source lock and Git-first Protocol v12. New attempts additionally **consult** latest Owner-approved human Governance; old Dispatches are never rebound.
- Immutable prior receipt `1ce109b9a4c538b255c6d8ffc6be8b4dccecf65d:reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/preflight_receipt.json`: `BLOCKED`, exact material `CHECK_BRIDGE_BOOTSTRAP_CONTROLS` failure. Historic CODEX `gpt-6.1-sol/medium/FULL_ACCESS` marker PASS applies only at its observed time. No claim of present authentication, quotas or machine readiness.
- Related root-cause report: `fa5b3e1edf8ce8c35689efa6ee0fe8e04efedb74:reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/CHAT_BRIDGE_P0_BOOTSTRAP_DEADLOCK_RESOLUTION_20261019.md`.

## 2. The precise route separation

**SELECTED ONLY FOR READINESS EVALUATION:** `EXECUTION_PATH=NATIVE_LOCAL_DEV`, `DELIVERY_OWNER=AGENT_PUSH_GIT_THEN_CHAT_INTAKE`; intended coding route: **CODEX PINNED gpt-6.1-sol / medium / FULL_ACCESS**, conditional on fresh proof. COPILOT NATIVE_AUTO/Balance is a candidate only if contemporary authentication and permission evidence pass; old `AUTH_REQUIRED` cannot silently disqualify an independently passing future run. CHAT handles source and Git review; WORK is not a coding agent.

This method MUST NOT be represented as `MANUAL_LOCAL` on the existing Bridge Dispatch normalizer, a `BRIDGE e2e-once` call, or `PASS_TO_ASSIGN`. It is a **separate legitimate native CLI implementation route** for the *same existing bounded WP*, not a fabricated installed Manual Local entrypoint. If the task's current route/contract cannot bind this method after inspection, status remains `HOLD_ROUTE_BINDING`; do not patch schema or immutable Dispatch to force it.

The old Bridge bootstrap probe (`CHECK_BRIDGE_BOOTSTRAP_CONTROLS`) is **not material to a proven Bridge-independent native DEV session**. However, the separate DEV prerequisites below are fully material and may be harder to satisfy. The original Bridge-route receipt remains permanently BLOCKED.

## 3. One bounded Windows host check — no Agent launch

**Task location (expected, MUST verify rather than assume):** `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`.

A host operator with actual machine access must return a sanitized, timestamped **read-only** observation of:

1. **Git/source:** current `origin/work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019` SHA, local `HEAD`, `git status --porcelain` count and allowlist, `git worktree list --porcelain` ownership. Check for conflicting writer. No `git reset --hard`, `clean`, checkout, fetch/rebase/push as part of the first read-only probe; remote refs can be checked via connector.
2. **CLI:** current `Get-Command codex,copilot,git,pwsh,python` presence and versions (no secrets or raw auth dumps). If permitted by host route policy, run the existing **marker-only** bounded `agent_probe` from `preexec/probes.py`, never a coding prompt. Record sanitized `PASS/FAIL/UNKNOWN` by route/model/effort/permission, timestamp and any capacity restriction, not imagined numeric quota.
3. **Attempt/ledger:** read-only check current and legacy dispatch/execution/consumption stores for the **new infrastructure WP identity**, including any started/claimed/ambiguous attempt; do **not** assume the protected Canary or Dispatch001 is unconsumed from this check. Confirm no Windows process is currently running another implementation for this task and no writer owns the worktree.
4. **Native single-use protection:** establish an actual available OS writer lock and a durable **native attempt record before CLI spawn**; specify which existing approved mechanism would hold the lock continuously through spawn, Git result and reconciliation. A preflight lock released before launch, a loose marker or clean `git status` alone is NOT enough. If a source-supported durable native mechanism is unavailable, return `HOLD_NATIVE_ATTEMPT_GUARD_UNAVAILABLE`, do not invent a launcher.
5. **Toolchain and dependencies:** only python/git/pwsh/pytest/jsonschema and route-specific tools needed to modify/test the six approved files. Installed Bridge worker PAUSED, `bridge.lock`, `dotnet`, WPF packaging and its `e2e-once` claim are **not** required for independent code implementation; they remain material later during installed adoption.

Stop and report `HOLD` on unknown source, path, writer, attempt, route permission, host evidence or native single-use guard. Do **not** resume/stop/kill Bridge workers, run `poll-once`, `run-next`, `e2e-once`, edit SQLite/ledgers, alter scheduled startup, or perform any code edit during this check.

## 4. Exact shared PreExec v1.1 recheck — after safe host discovery

The existing `agent_bridge/scripts/preexec.py --profile bridge` hard-binds **another WP** (`FOX2-BRIDGE-DESKTOP-BATCH-B`) and is **NOT** valid for this infrastructure task. Use the already-implemented generic `fox2_agent_bridge.preexec.PreExec(Requirements(...))` with task-specific arguments — no new engine/profile/fake receipt:
- `wp_id=FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`
- `branch=work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`
- `worktree=<observed absolute path>`
- `source_head=<current exact remote task branch HEAD, not the older task publication commit>`
- `task_path=docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/task.md`
- `receipt_path=reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/preflight_native_dev_20261019_01.json` (only if unused and authorized)
- `routes=valid agent_policy.validate_selection route dictionaries` for *observed* CODEX/COPILOT candidates, not copied from Canary
- `checks=<ONLY actually material native DEV probes with sanitized observations>`; include source/writer/attempt-guard checks without weakening the base engine's own checks
- `pinned_agent=` only if a single eligible Agent is deliberately selected through CHAT routing.

An actual shared PreExec publication may mutate **only its new append-only receipt path** after the host operator's authorized, guarded process; it must produce a **real PASS** or an honest BLOCKED/INFRA_FAILED, Git commit/push/remote byte readback and CHAT intake. Do **not** replace or delete the old `preflight_receipt.json`. The earlier `CHECK_BRIDGE_BOOTSTRAP_CONTROLS` remains BLOCKED for that **Bridge route**.

## 5. Scope, subsequent handoff and STOP

**Six Owner-approved primary code/test paths only:**
1. `agent_bridge/src/fox2_agent_bridge/dispatch_normalizer.py`
2. `agent_bridge/src/fox2_agent_bridge/e2e_runner.py`
3. `agent_bridge/src/fox2_agent_bridge/app.py`
4. `agent_bridge/src/fox2_agent_bridge/__main__.py`
5. `agent_bridge/tests/test_project_dictionary.py`
6. `agent_bridge/tests/test_e2e_runner.py`

Do not extend to `ledger.py`, `desktop.py`, `process_lock.py`, `ops_runner.py`, `agent_policy.py`, schemas, generated Dictionary or any other files without evidence of necessity and separately bound scope. No blanket `agent_bridge/**`.

Only after real host route admission + CHAT R0–R7 acceptance may CHAT publish a **new immutable source-bound native DEV handoff/attempt identity** and select an actually eligible Agent. That task uses **Git-first Task→Prompt→Agent code/tests/report/evidence push→CHAT independent review**. No executable Dispatch from this document. Code ACCEPTED is not Bridge INSTALLED. Installed adoption/worker quiescence, independent pre-Canary audit and Canary009 remain separate stages and permissions.

`POLICY_CHECK=PASS_SCOPED_HUMAN_DIRECTION`
`TASK_STATE_CHECK=HISTORICAL_BLOCKED_PRESERVED`
`ROUTING_R0_R7=READ_ONLY_PREPARATION_DONE; EXECUTION_GATE_R3_R5_UNKNOWN`
`OWNER_CODE_SCOPE=PREVIOUSLY_APPROVED_SIX_PATHS`
`NATIVE_DEV_ROUTE=SELECTED_FOR_HOST_ADMISSION_ONLY`
`HOST_CURRENT_ADMISSION=UNKNOWN`
`HOST_NATIVE_ATTEMPT_GUARD=UNKNOWN`
`CODE_ALLOWED_EXECUTION=HOLD_FRESH_NATIVE_PREEXEC_AND_CHAT_INTAKE`
`NEW_EXECUTABLE_DISPATCH=NOT_PUBLISHED`
`DISPATCH001=PROTECTED_UNCHANGED`
`CANARY009=PROTECTED_UNCHANGED`
`MAIN_MERGE=NOT_AUTHORIZED_BY_THIS_ROUTE`
`BROKER_PROVIDER_LIVE=NO`
