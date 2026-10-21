# FOX2 — Package Lifecycle Uninstall Harness Correction A03

Task ID: `FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-A03`
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Stage: BUILD / TEST-HARNESS CORRECTION
Actor: CODEX
Model: `gpt-6.1-sol`
Thinking: `high`
Execution path: `MANUAL_LOCAL`
Permission profile: `FULL_ACCESS` within task allowlist only
Max Agent attempts: 1

## Why A03 exists

A01 was consumed safe-stop with no product change because its prompt confused product source baseline with execution starting HEAD.

A02 fixed that dual-base concept and reached PreExec PASS, but no implementation Agent started. Its first Dispatch was schema-invalid; its second Dispatch was schema-valid but the immutable A02 prompt hard-coded the first Dispatch sequence identity. Both A02 Dispatches are non-executable and unconsumed.

CHAT review:
- A01 recovery: `fff17cd828d9369af9cf36dc3892ce7412be7c65`
- A02 Dispatch001 schema rejection: `824406f8a5cd9bdccb412f2006b806b059c7308b`
- A02 Dispatch002 prompt-binding rejection: `9f7cf7500d0124729c7eb6c3a758d918b6a727fa`

A03 is a fresh assignment identity, not a replay.

## Goal

Correct the proven lifecycle-certification uninstall entrypoint defect without changing the accepted product uninstall safety contract.

The harness currently routes uninstall through the installed runtime, while the accepted product contract intentionally rejects installed-interpreter self-deletion and requires the stable external `<BridgeRoot>/uninstall.ps1` supervisor.

This is source/build/test only. Do not perform real install/update/uninstall/reinstall on the Owner host.

## Source and execution identity

Repository: `dunglt2505/FOX2`
Branch: `work/FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-FIX-20261021`

### PRODUCT_SOURCE_BASE

`b065a468279cbf63ae4bbfad7a0efaad1e6046e4`

This is the accepted product-code baseline. It is not the required current HEAD when CODEX starts.

### ASSIGNMENT_PARENT

`036de99a6d649bfcf9a427aa914809a9d53592c3`

This is the clean task-branch head after A02 PreExec receipt delivery and before A03 handoff publication.

### EXECUTION_START_HEAD

At execution time the exact current HEAD must equal the fresh executable Dispatch field:

`runtime_contract.base_sha`

The future Dispatch sequence number is intentionally **not** hard-coded in this task or prompt.

The launcher must verify the exact executable Dispatch identity, commit and blob before starting CODEX.

CODEX preflight must verify:
1. exact branch;
2. current HEAD == verified executable Dispatch `runtime_contract.base_sha`;
3. `PRODUCT_SOURCE_BASE` is an ancestor of current HEAD;
4. pre-start changes after `PRODUCT_SOURCE_BASE` are bounded handoff/PreExec evidence only and contain no unexplained product-code drift;
5. worktree clean and one writer.

Never require `HEAD == PRODUCT_SOURCE_BASE`.

## Proven defect

Phase-2 root cause:
`reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/PACKAGE_LIFECYCLE_UNINSTALL_ROOT_CAUSE_20261021.md`
commit `adaa169b7e35861d35bbd5d2ecdab1ae2ec43dde`.

The current lifecycle harness uses the installed interpreter for `cli('uninstall')`. The product correctly rejects that self-delete path and directs callers to stable external `uninstall.ps1`.

Historical Batch-B `UNINSTALL_PATH=FAIL` remains factual.

## Governance source set

- Registry/source release head: `d34da1e3b4918a902646621b487ca8ad3e05b0e0`
- Policy 2.0.0: `96175ac4f39197794a04e695f0046fa7ef9321fe`
- Dictionary 1.3: `b25f7f728de67cf8595bf24f22fcbd79ef50babc`
- Routing 1.4.0: `bcd008983b61349646a5198ff243069f81484fae`
- Git-first Protocol 12: `f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa`

## Required implementation

1. Change `agent_bridge/scripts/certify_user_lifecycle.py` so uninstall runs synchronously through stable external `<BridgeRoot>/uninstall.ps1` using PowerShell 7 from outside `versions`.
2. Do not use installed `versions/<sha>/runtime/Scripts/python.exe` for uninstall.
3. Capture bounded sanitized uninstall evidence:
   - stable external supervisor identity/kind;
   - exit code;
   - stdout;
   - stderr;
   - post-uninstall current pointer/version absence;
   - durable config/data preservation checks.
4. On non-zero uninstall: preserve bounded evidence and stop once. No retry, alternate entrypoint or hidden recovery.
5. Preserve `installation.uninstall()` installed-interpreter self-delete rejection.
6. Add focused regression coverage for stable supervisor selection, no installed `cli('uninstall')`, structured success evidence, non-zero failure evidence, and durable data/config/consumed identity preservation.
7. Real host lifecycle remains `NOT_RUN`.

## Allowed write paths

- `agent_bridge/scripts/certify_user_lifecycle.py`
- `agent_bridge/tests/test_installation.py`
- `agent_bridge/tests/test_rc1_package.py`
- one new directly-related `agent_bridge/tests/test_*lifecycle*.py` only if strictly necessary
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/package_lifecycle_fix/**`

Do not modify `installation.py`, `__main__.py`, governance, BRD, TechSpec, Feature Status, Dispatch history, G3/G4/Canary files. If the accepted product contract itself is proven defective, STOP and report.

## Required tests

- focused lifecycle/uninstall harness regressions;
- installation/package regressions;
- full `agent_bridge/tests`;
- static syntax/PowerShell parsing as applicable;
- changed-path allowlist;
- `git diff --check`;
- bounded secret scan;
- K1 `UNEXPLAINED=0`;
- Result Contract v2 validation.

## Acceptance

1. harness uses stable external `uninstall.ps1`;
2. no installed Python self-delete path is used by certification;
3. bounded exit/stdout/stderr evidence retained;
4. non-zero uninstall stops once without retry;
5. product self-delete guard remains green;
6. durable config/data/claims regressions remain green;
7. focused tests PASS;
8. full `agent_bridge/tests` PASS;
9. allowlist/secret/diff/K1 PASS;
10. real host lifecycle remains `NOT_RUN`;
11. report + evidence manifest pushed on this branch;
12. historical Batch-B failure remains factual.

## K1

Every material implementation hunk:
- REQUESTED
- NECESSARY_DEPENDENCY
- JUSTIFIED_GENERATED
- UNEXPLAINED

Required: `UNEXPLAINED=0`.

## Forbidden

- replay of A01;
- execution of either A02 Dispatch;
- real install/update/uninstall/reinstall;
- AppLocker/AppIDSvc/service/ProgramData ACL mutation;
- reboot;
- G3/G4/Canary;
- main/PR/merge;
- provider/broker/LIVE.

## Result delivery

Push permitted code/tests plus:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- bounded `evidence/package_lifecycle_fix/**`

Return observed remote result SHA outside the committed report. Status remains `PUSHED_UNREVIEWED` until CHAT result review.

## STOP

STOP truthfully if:
- fresh A03 task/prompt/PreExec/Dispatch binding mismatches;
- current HEAD differs from verified executable Dispatch runtime base;
- product baseline is not an ancestor;
- unexplained pre-start product-code drift exists;
- worktree dirty or competing writer exists;
- required change exceeds allowlist;
- accepted product uninstall contract is proven defective;
- model/effort/permission differs;
- auth/quota/runtime fails after attempt consumption;
- host lifecycle mutation would be required;
- tests require scope expansion.
