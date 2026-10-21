# FOX2 — Package Lifecycle Uninstall Harness Correction A02

Task ID: `FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-A02`  
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`  
Stage: BUILD / TEST-HARNESS CORRECTION  
Actor: CODEX  
Model: `gpt-6.1-sol`  
Thinking: `high`  
Execution path: `MANUAL_LOCAL`  
Permission profile: `FULL_ACCESS` within this task allowlist only  
Max Agent attempts: 1

## Why A02 exists

A01 Dispatch `FOX2-DISPATCH-BRIDGE-RC1-PACKAGE-LIFECYCLE-A01-CODEX-001` is permanently consumed.

A01 made no product-code changes. CODEX stopped safely before editing because the immutable prompt incorrectly required current HEAD to equal the historical accepted product source baseline `b065a468279cbf63ae4bbfad7a0efaad1e6046e4`, while the executable Dispatch correctly required the task branch to start at the later PreExec receipt head `b224f029bc911c0a131342b8ac142fdd4952a96f`.

CHAT review:
`reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/PACKAGE_LIFECYCLE_A01_CONSUMED_SAFE_STOP_REVIEW_20261021.md`
commit `fff17cd828d9369af9cf36dc3892ce7412be7c65`.

A02 is a fresh attempt identity, not a replay.

## Goal

Correct the proven lifecycle-certification uninstall entrypoint defect without changing the accepted product uninstall safety contract.

Historical Batch-B certification invoked `fox2_agent_bridge uninstall` through the installed interpreter under `versions/<sha>/runtime`. The product correctly rejects self-deletion from that interpreter and requires the stable external `<BridgeRoot>/uninstall.ps1` supervisor. The certification harness must exercise the supported stable supervisor instead.

This task is source/build/test only. Do not perform real install/uninstall on the Owner host.

## Corrected source/execution identity model

Repository: `dunglt2505/FOX2`  
Branch: `work/FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-FIX-20261021`

### PRODUCT_SOURCE_BASE

`b065a468279cbf63ae4bbfad7a0efaad1e6046e4`

This is the accepted same-host BUILD result/evidence baseline from which product-code semantics are evaluated.

Accepted same-host chain:
- implementation: `be883bb8106ca1c058b2b34765e55c2529fe883f`
- result/evidence: `b065a468279cbf63ae4bbfad7a0efaad1e6046e4`
- CHAT review: `278daa5aff70b2e17a2bf3b563cbcd2585cd2f7f`

### ASSIGNMENT_PARENT

`b224f029bc911c0a131342b8ac142fdd4952a96f`

This is the clean remote task-branch head after the A01 PreExec PASS receipt was delivered and before A02 handoff publication.

### EXECUTION_START_HEAD

**Do not hard-code this task file's publication parent or PRODUCT_SOURCE_BASE as the executable current HEAD.**

For the eventual A02 execution, the exact starting HEAD is the fresh executable Dispatch field:

`Dispatch.runtime_contract.base_sha`

That SHA will be created only after A02 task/prompt publication and fresh task-specific PreExec receipt delivery.

At execution time CODEX must verify:

1. current branch equals the bound A02 branch;
2. current HEAD equals the exact fresh Dispatch `runtime_contract.base_sha`;
3. `PRODUCT_SOURCE_BASE` is an ancestor of current HEAD;
4. commits between `PRODUCT_SOURCE_BASE` and `EXECUTION_START_HEAD` that precede implementation are bounded to A01/A02 governance, handoff, review and PreExec evidence; they are not product-code acceptance;
5. no implementation/product code outside the A02 allowlist changed before CODEX starts.

A02 must **never** require `HEAD == PRODUCT_SOURCE_BASE`.

## Root-cause evidence

Phase-2 root-cause review:
- path: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/PACKAGE_LIFECYCLE_UNINSTALL_ROOT_CAUSE_20261021.md`
- commit: `adaa169b7e35861d35bbd5d2ecdab1ae2ec43dde`

Proven defect:
- `agent_bridge/scripts/certify_user_lifecycle.py` binds installed `versions/<sha>/runtime/Scripts/python.exe`;
- its `cli()` helper invokes that installed interpreter;
- lifecycle certification performs uninstall through `cli('uninstall')`;
- product `installation.uninstall()` intentionally rejects self-deletion from the installed interpreter;
- stable external `<BridgeRoot>/uninstall.ps1` / `uninstall.py` is the supported path.

Preserve historical Batch-B `UNINSTALL_PATH=FAIL` exactly as historical evidence.

## Governance source set

- Registry/source release head: `d34da1e3b4918a902646621b487ca8ad3e05b0e0`
- Policy 2.0.0: `96175ac4f39197794a04e695f0046fa7ef9321fe`
- Dictionary 1.3: `b25f7f728de67cf8595bf24f22fcbd79ef50babc`
- Routing 1.4.0: `bcd008983b61349646a5198ff243069f81484fae`
- Git-first Protocol 12: `f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa`

BRD-09 REV3 and Bridge TechSpec v0.7 REV10 remain global CANDIDATE. This bounded correction does not promote them.

## Required implementation

1. Update lifecycle certification so uninstall is invoked synchronously through stable external:
   `<BridgeRoot>/uninstall.ps1`
   using PowerShell 7 and an execution context outside `versions`.

2. Do not invoke the installed Python interpreter for uninstall.

3. Capture structured lifecycle uninstall evidence:
   - entrypoint kind/identity = stable external supervisor;
   - exit code;
   - bounded sanitized stdout;
   - bounded sanitized stderr;
   - post-uninstall current pointer/version absence;
   - durable config/data preservation checks.

4. On non-zero uninstall:
   - persist bounded sanitized exit/stdout/stderr evidence;
   - stop lifecycle certification immediately;
   - do not retry;
   - do not switch entrypoint automatically.

5. Preserve product safety:
   - `installation.uninstall()` continues to reject installed-interpreter self-deletion;
   - stable `uninstall.ps1` / `uninstall.py` remains supported path;
   - no blind deferred deletion or hidden recovery.

6. Add focused regression coverage proving:
   - lifecycle certification selects stable external `uninstall.ps1`;
   - it never calls installed `cli('uninstall')`;
   - success path records structured uninstall evidence;
   - non-zero supervisor exit preserves sanitized exit/stdout/stderr and stops once;
   - durable data/config and consumed identities remain preserved by product semantics.

7. Real per-user install/update/uninstall/reinstall remains **NOT_RUN** in this coding task.

## Allowed write paths

Product/harness:
- `agent_bridge/scripts/certify_user_lifecycle.py`

Tests:
- `agent_bridge/tests/test_installation.py`
- `agent_bridge/tests/test_rc1_package.py`
- one new directly-related `agent_bridge/tests/test_*lifecycle*.py` only if strictly necessary

Result/evidence:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/package_lifecycle_fix/**`

Do not modify `installation.py`, `__main__.py`, governance, BRD, TechSpec, Feature Status, Dispatch history, G3/G4/Canary files. If a focused test proves the accepted product contract itself defective, STOP and report; do not expand scope.

## Required tests

At minimum:
1. focused lifecycle/uninstall harness regressions;
2. existing installation/package regressions;
3. full `agent_bridge/tests`;
4. static syntax/PowerShell parsing as applicable;
5. changed-path allowlist;
6. `git diff --check`;
7. bounded secret scan;
8. K1 `UNEXPLAINED=0`;
9. Result Contract v2 validation.

Historical FAIL/NOT_RUN evidence remains immutable.

## Acceptance

1. certification harness uses stable external `uninstall.ps1`;
2. no installed Python self-delete path is used by certification;
3. uninstall exit/stdout/stderr evidence is bounded and retained;
4. non-zero uninstall fails once with no retry/replay;
5. product self-delete guard remains green;
6. durable config/data/claims preservation regressions remain green;
7. focused tests PASS;
8. full `agent_bridge/tests` PASS;
9. allowlist/secret/diff/K1 PASS;
10. real lifecycle host execution remains `NOT_RUN`;
11. report + evidence manifest are pushed on this branch;
12. historical Batch-B `UNINSTALL_PATH=FAIL` remains factual.

## K1

Every material implementation hunk must be:
- REQUESTED
- NECESSARY_DEPENDENCY
- JUSTIFIED_GENERATED
- UNEXPLAINED

Required: `UNEXPLAINED=0`.

## Forbidden

- replay of A01 Dispatch or attempt;
- real install/update/uninstall/reinstall on Owner host;
- AppLocker mutation;
- AppIDSvc mutation;
- Windows service install/start/stop/delete;
- ProgramData authority ACL mutation;
- reboot;
- G3/G4 adoption;
- Canary009 or any old Canary replay;
- main/PR/merge;
- provider/trading broker/LIVE.

## Result delivery

Agent must push:
- permitted code/tests;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`;
- bounded `evidence/package_lifecycle_fix/**`.

Return the observed remote result SHA outside the committed report. Status after push is `PUSHED_UNREVIEWED` until CHAT applies `fox2-result-review`.

## STOP

STOP and report truthfully if:
- fresh Dispatch/task/prompt/PreExec binding mismatches;
- current HEAD differs from fresh Dispatch `runtime_contract.base_sha`;
- PRODUCT_SOURCE_BASE is not an ancestor;
- pre-start product-code drift exists outside bounded handoff/PreExec evidence;
- worktree is dirty before start;
- competing task-scoped writer exists;
- required fix needs modification outside allowed paths;
- accepted product uninstall contract is proven defective;
- model/effort/permission differs;
- auth/quota/runtime fails after attempt consumption;
- tests require drive-by scope expansion;
- any host lifecycle mutation would be required to prove BUILD correctness.
