# FOX2 — Package Lifecycle Uninstall Harness Correction A01

Task ID: `FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-A01`  
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`  
Stage: BUILD / TEST-HARNESS CORRECTION  
Actor: CODEX  
Model: `gpt-6.1-sol`  
Thinking: `high`  
Execution path: `MANUAL_LOCAL`  
Permission profile: `FULL_ACCESS` within this task allowlist only  
Max Agent attempts: 1

## Goal

Correct the proven lifecycle-certification uninstall entrypoint defect without changing the accepted product uninstall safety contract.

Historical Batch-B certification invoked `fox2_agent_bridge uninstall` through the installed interpreter under `versions/<sha>/runtime`. The product correctly rejects self-deletion from that interpreter and requires the stable external `<BridgeRoot>/uninstall.ps1` supervisor. The certification harness must exercise the supported stable supervisor instead.

This task is source/build/test only. Do not perform real install/uninstall on the Owner host.

## Immutable source lock

Repository: `dunglt2505/FOX2`  
Branch: `work/FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-FIX-20261021`  
Exact base SHA: `b065a468279cbf63ae4bbfad7a0efaad1e6046e4`

Accepted same-host BUILD:
- implementation: `be883bb8106ca1c058b2b34765e55c2529fe883f`
- result/evidence: `b065a468279cbf63ae4bbfad7a0efaad1e6046e4`
- CHAT review: `278daa5aff70b2e17a2bf3b563cbcd2585cd2f7f`

Phase-2 root-cause review:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/PACKAGE_LIFECYCLE_UNINSTALL_ROOT_CAUSE_20261021.md`
- commit: `adaa169b7e35861d35bbd5d2ecdab1ae2ec43dde`

Governance source set for this new task:
- Registry/source release head: `d34da1e3b4918a902646621b487ca8ad3e05b0e0`
- Policy 2.0.0: `96175ac4f39197794a04e695f0046fa7ef9321fe`
- Dictionary 1.3: `b25f7f728de67cf8595bf24f22fcbd79ef50babc`
- Routing 1.4.0: `bcd008983b61349646a5198ff243069f81484fae`
- Git-first Protocol 12: `f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa`

BRD-09 REV3 and Bridge TechSpec v0.7 REV10 remain global CANDIDATE. This bounded correction is governed by the accepted Whole-WP source/result chain above; no global document promotion is implied.

## Proven defect

Current `agent_bridge/scripts/certify_user_lifecycle.py`:
- binds `python = <BridgeRoot>/versions/<sha>/runtime/Scripts/python.exe`;
- its `cli()` helper invokes that installed interpreter;
- performs `results['uninstall'] = cli('uninstall')`.

Current `fox2_agent_bridge.__main__.py` routes `uninstall` directly to `installation.uninstall()`.

Current `installation.uninstall()` intentionally denies when `sys.executable` is under the installed `versions` tree and instructs callers to use stable `uninstall.ps1`.

Therefore the lifecycle harness is calling the unsupported self-delete path. Preserve the historical `UNINSTALL_PATH=FAIL`; do not rewrite old evidence.

## Required implementation

1. Update lifecycle certification so uninstall is invoked through the stable external:
   `<BridgeRoot>/uninstall.ps1`
   using PowerShell 7, synchronously and from outside `versions`.

2. Do not invoke the installed Python interpreter for uninstall.

3. Capture lifecycle uninstall evidence including:
   - exact entrypoint kind: stable external supervisor;
   - exit code;
   - bounded/sanitized stdout;
   - bounded/sanitized stderr;
   - whether `current.json` and version directories were removed;
   - durable config/data preservation checks.

4. On non-zero uninstall:
   - retain the bounded sanitized failure evidence;
   - fail the lifecycle certification immediately;
   - do not retry or switch entrypoint automatically.

5. Preserve the product safety contract:
   - `installation.uninstall()` must continue to reject installed-interpreter self-deletion;
   - stable external `uninstall.ps1` / `uninstall.py` remains the supported path;
   - no blind deferred deletion or hidden retry.

6. Add focused regression coverage proving:
   - lifecycle certification selects stable external `uninstall.ps1`;
   - it never calls installed `cli('uninstall')`;
   - success path records structured uninstall evidence;
   - non-zero supervisor exit preserves sanitized exit/stdout/stderr evidence and stops;
   - durable data/config and consumed identities remain preserved by existing product semantics.

7. Keep real per-user install/update/uninstall/reinstall execution **NOT_RUN** in this coding task.

## Allowed write paths

Product/harness:
- `agent_bridge/scripts/certify_user_lifecycle.py`

Tests:
- `agent_bridge/tests/test_installation.py`
- `agent_bridge/tests/test_rc1_package.py`
- a new directly-related `agent_bridge/tests/test_*lifecycle*.py` only if strictly necessary

Result/evidence:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/package_lifecycle_fix/**`

Do not modify `installation.py`, `__main__.py`, governance, BRD, TechSpec, Feature Status, Dispatch history, G3/G4/Canary files unless a test proves the accepted product contract itself is defective. If such a defect is discovered, STOP and report it; do not expand scope silently.

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

Historical FAIL/NOT_RUN receipts must remain immutable.

## Acceptance

1. certification harness uses stable external `uninstall.ps1`;
2. no installed Python self-delete path is used by certification;
3. uninstall exit/stdout/stderr evidence is retained in bounded sanitized form;
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

Classify every material hunk:
- REQUESTED
- NECESSARY_DEPENDENCY
- JUSTIFIED_GENERATED
- UNEXPLAINED

Required: `UNEXPLAINED=0`.

## Forbidden

- real install/update/uninstall/reinstall on Owner host;
- AppLocker mutation;
- AppIDSvc mutation;
- Windows service install/start/stop/delete;
- ProgramData authority ACL mutation;
- reboot;
- G3/G4 adoption;
- Canary009 or any old Canary replay;
- main/PR/merge;
- provider/trading broker/LIVE;
- replay of the consumed same-host BUILD Dispatch.

## Result delivery

Agent must push:
- permitted code/tests;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`;
- bounded `evidence/package_lifecycle_fix/**`.

Return the observed remote result SHA outside the committed report. Status after push is `PUSHED_UNREVIEWED` until CHAT applies `fox2-result-review`.

## STOP

STOP and report BLOCKED/REWORK if:
- source/task/prompt/branch binding drifts;
- worktree is dirty before start;
- competing task-scoped writer exists;
- required fix needs modification outside allowed paths;
- product uninstall contract itself is proven defective;
- CODEX model/effort/permission differs;
- auth/quota/runtime fails after attempt consumption;
- tests cannot be made green without drive-by changes;
- any host lifecycle mutation would be required to prove BUILD correctness.
