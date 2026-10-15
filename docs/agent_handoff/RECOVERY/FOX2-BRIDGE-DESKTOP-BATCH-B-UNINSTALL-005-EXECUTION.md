# FOX2 Bridge Batch B — Dispatch 005 Exact Uninstall Execution Prompt

**Status:** EXECUTION PROMPT / MAY EXECUTE ONLY THROUGH A VALIDATED, NEW, SINGLE-USE DISPATCH 005
**WP:** FOX2-BRIDGE-DESKTOP-BATCH-B (continuation; no new feature WP)
**Source task head:** `0fee5424a6f1f032490518a0a816931c6624875c`
**Source code checkpoint:** `6a31409e0f3d46d4f2b2fc2bc48464ecff86e257`
**Bound policy:** Dictionary v1.2 -> Policy V1.8.9 -> Routing Index V1.3.0; Git-first Protocol v12.
**Controlling technical scope:** `docs/agent_handoff/RECOVERY/FOX2-BRIDGE-DESKTOP-BATCH-B-UNINSTALL-005.md` at control SHA `cac8dd3c876c9b1c9763f865cc0b9b7611cd791b`.
**Route:** CODEX CLI / PINNED gpt-6.1-sol / Medium / FULL_ACCESS / MANUAL_LOCAL / delivery_owner=AGENT.
**Exclusions:** no main/PR/merge/deploy/Production/provider/broker/LIVE; no writes beyond `agent_bridge/**` and `reports/BRIDGE-DESKTOP-BATCH-B/**`.

## Mandatory pre-start STOP check

- Resolve this immutable source and prompt SHA from the Dispatch 005 JSON, verify exact branch/worktree/source HEAD and clean tree at `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B`.
- Verify source-current PreExec receipt at `0fee5424a6f1f032490518a0a816931c6624875c:reports/BRIDGE-DESKTOP-BATCH-B/preexec/local_preflight.json` is PASS and binds code head `6a31409e`, and route CODEX gpt-6.1-sol Medium Full Access. Copilot AUTH_REQUIRED is recorded; do not silently substitute.
- Verify exact Codex current auth/capacity and applied FULL_ACCESS; Windows packaging toolchain; exclusive writer lock, no concurrent task writer; no uncontrolled Agent process. If any UNKNOWN/FAIL material prerequisite: STOP without source mutation.
- Dispatch 001/002/003/004 are already CONSUMED. NEVER replay, resume, reinterpret or re-run them. Claim 005 at most once, including after failure.
- **Critical precondition: prior installed runtime integrity is UNKNOWN after failed 004 uninstall. Do NOT run any uninstall, installer, update, re-launch, restart or deletion on the existing per-user runtime before read-only reconciliation**. Examine only metadata/provenance, exact owned version receipts, current pointer, effective interpreter, Windows PID/handle ownership, Worker STOPPED and startup task state, lock availability and data preservation. If safety remains uncertain, STOP and publish sanitized inspection evidence only. Never delete unrelated or unowned files.

## Narrow technical objective

The 004 Tray graceful-exit fix and 5 focused Tray regressions PASSED on Windows. Preserve that fix, the 17 already restored files, and all prior accepted Batch A / Shared PreExec work. Repair ONLY the **installed uninstall** defect and its direct lifecycle test harness, without changing dispatch/replay/trading semantics.

Hypothesis A (not yet host-confirmed): `installation.uninstall` executes from installed `versions/<sha>/runtime/Scripts/python.exe`, synchronously waits on a base Python helper, and the child deletes the still-in-use parent executable. Windows may deny that removal.
Hypothesis B: `sys._base_executable -I` executed outside runtime may lack dependencies of installed wheel. Confirm via safe read-only import/process observations; do not mask a missing dependency as A.

Implement robust per-user uninstall only with **external helper outside version tree** and a provable completion acknowledgement. It must not require deleting an executable whose owning process still runs. Safe design verifies exact executable/process ownership and waits for it to exit before owned version removal. Use fixed, sanitized receipt under preserved reports; discriminate REQUESTED vs VERIFIED removal. Never report UNINSTALLED until genuinely verified. Validate all versions and ownership before destructive work; preserve data/config/ledger/reports, all dispatch consumption claims, logs and FOX2 worktrees; prevent links/junction traversal and unowned paths; no privilege elevation or automatic relaunch. On partial failure, STOP with truthful bounded evidence and no blind retry. Do not arbitrarily kill processes.

Add focused regression coverage: own-executable Windows parent/child race, standalone helper import dependencies, timeout/abandoned request, dirty/unowned/junction version, lock held, incomplete removal, receipt completion, ledger no-replay, safe reinstall. Use isolated temporary fixtures before installed-runtime certification. Avoid adding nonessential new process orchestration.

## Test/evidence sequence and cost limits

1. **Read-only** host diagnosis + source proof; if UNKNOWN, STOP.
2. Narrow implementation + targeted tests with correctly configured `PYTHONPATH=agent_bridge/src`; run focused tests only until stable.
3. Perform installed uninstall/reinstall lifecycle only after objective safety verification of exact owned runtime and offline package SHA. No ambiguous or unsafe deletion.
4. Once installed lifecycle PASS, certify the same 24 Batch B gates. Reuse existing still-valid evidence for previously passed gates, but prove current-code materially impacted checks. Run full Bridge pytest **once** after the final code change, not repeatedly.
5. Run exact staged path allowlist, diff check, sanitized secret scan; publish code/evidence only on `work/FOX2-BRIDGE-DESKTOP-BATCH-B` with exact commit SHA and remote readback. Truthful status `PUSHED_UNREVIEWED` if all certified; otherwise `STOPPED_NEEDS_RECONCILIATION / BRIDGE_READY=NO` with narrow WIP evidence.
6. Do NOT launch a real trading/broker/provider write, change Git main, merge or deploy. Real certification dispatch must use an isolated, authorized canary and preserve ledger semantics.

Do not reread the whole repository or redo accepted Batch A, Shared PreExec or Tray work. Prior 354/354 pytest (before 004) and Tray 5/5 PASS are evidence, not certification on this new code. No claim that 24 gates are PASS until verified.

## Machine acceptance set (24 gates)

`FIRST_RUN_SETUP`, `PER_USER_INSTALL`, `INSTALLER_PACKAGE`, `UPDATE_PATH`, `UNINSTALL_PATH`, `STARTUP_SINGLE_INSTANCE`, `SANITIZED_DIAGNOSTICS_BUNDLE`, `INSTALLED_TRAY_WORKER`, `PROJECT_DICTIONARY_BINDING`, `DISPATCH_V3_SCHEMA_BINDING`, `DISPATCH_V3_STRUCTURAL_CONFORMANCE`, `DISPATCH_V3_RUNTIME_COMPATIBILITY`, `V2_COMPATIBILITY`, `V06_COMPATIBILITY`, `REAL_ELIGIBLE_FOX2_DISPATCH`, `EXACT_AGENT_CONFIGURATION`, `FULL_ACCESS_PERMISSION`, `RESULT_REMOTE_READBACK`, `USAGE_SNAPSHOT`, `RESTART_NO_REPLAY`, `FULL_BRIDGE_TESTS`, `CHANGED_PATH_ALLOWLIST`, `SECRET_SCAN`, `GIT_DIFF_CHECK`.

## Mandatory STOP and delivery

STOP for source drift, WIP/writer conflict, invalid auth/quota/permission, unsafe process/file ownership, runtime or installation integrity UNKNOWN, dependency uncertainty, absent test fixture, replay risk, code outside allowlist, destructive operation without prevalidated safety, failure of a required gate, sensitive exposure or Git publication/readback failure. On STOP: preserve installation state and exact consumed claims, publish sanitized WIP reports if safely possible, then relinquish writer lock. No second agent run on the same Dispatch.

Only CHAT can accept `INTERNAL_FOX2_BRIDGE_READY`. Agent result is never release authorization.
