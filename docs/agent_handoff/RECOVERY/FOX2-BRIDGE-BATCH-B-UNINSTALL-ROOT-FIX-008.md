# FOX2 Bridge Batch B — Windows Self-Uninstall Root Fix + Recovery 008

## Role
Single bounded correction inside the EXISTING `FOX2-BRIDGE-DESKTOP-BATCH-B` whole-WP.

## Immutable state

Task branch:
`work/FOX2-BRIDGE-DESKTOP-BATCH-B`

Current source head:
`0c739db91553ab8dd39a30b221f079b9538b0836`

Dispatches 001–007 are CONSUMED. NEVER replay or resume them.

Current governance remains:
- Project Dictionary v1.2
- Policy V1.8.9
- Routing Index v1.3.0
- PreExec Evidence v1.1
- Dispatch Schema v3
- Git-first Protocol v12
- Bridge Technical v0.7 Candidate REV10

Writable:
- `agent_bridge/**`
- `reports/BRIDGE-DESKTOP-BATCH-B/**`

Everything else READ-ONLY.

No main/PR/merge/deploy/provider/broker/LIVE authority.

## Preserve the successful 007 fix

Dispatch 007 fixed installer environment contamination and proved:
- 22 focused installer tests PASS;
- 367 full Bridge tests PASS;
- deterministic package build PASS;
- contaminated parent `PYTHONPATH/PYTHONHOME` no longer leaks into install subprocesses;
- disposable install/setup/update/Tray/Worker/diagnostics PASS.

Do NOT redesign or revert that fix.

## Root cause evidence — uninstall self-delete orchestration

007 stopped at the first disposable installed `uninstall` call.

Evidence:
- outer installed CLI exit 2;
- inner error crossed the existing sanitized installation subprocess boundary;
- uninstall had already removed most files;
- exactly one receipt-bearing current version remained with only five files;
- `runtime/Scripts/python.exe` still existed;
- durable config/data/logs/reports remained;
- real user runtime was untouched.

Current production logic detects that `sys.executable` is inside `root/versions/**`, then synchronously spawns `sys._base_executable` to perform deletion and WAITS for that child.

On Windows this leaves the parent installed interpreter alive while the child attempts `shutil.rmtree()` over the directory containing that running parent executable. This is an invalid self-delete orchestration and is consistent with the observed partial deletion and surviving runtime Python.

Treat this as the correction target. Do not broaden scope to packaging, PreExec, routing, frontend or business runtime.

## Required design property

When uninstalling an installed Bridge version on Windows, no process executing from the version directory may remain alive while that version directory is deleted.

The implementation must preserve safe CLI semantics and must not report `UNINSTALLED` before deletion is actually complete.

Acceptable design families include:
- an actual process overlay/handoff to the base interpreter where the installed interpreter no longer remains alive during deletion; or
- a stable external bootstrap outside `versions/**` with a completion protocol that proves the installed parent exited before deletion.

The Agent must choose the smallest correct Windows-safe design and prove it with real disposable execution.

Do NOT:
- use reboot-time deletion as success;
- blindly retry `shutil.rmtree`;
- ignore sharing/access errors;
- kill arbitrary processes;
- weaken receipt/path/link ownership checks;
- delete durable `config/`, `data/`, `logs/`, or `reports/`;
- claim uninstall success while files remain.

## Mandatory focused tests

Add regression coverage for:
1. installed-runtime uninstall handoff does not synchronously wait while the installed interpreter remains the deletion target;
2. helper/bootstrap runs outside the owned version tree;
3. completion is verified before success is reported;
4. absent startup task remains idempotent;
5. unowned version directories still fail closed before deletion;
6. durable data and consumed-dispatch state remain preserved;
7. helper arguments/environment are bounded/sanitized;
8. current installer environment isolation regressions from 007 remain PASS.

Run focused tests, then full Bridge suite exactly once after substantive code changes.

## Mandatory disposable lifecycle

Build package twice and prove byte identity.

In a NEW disposable user profile, keep deliberate parent `PYTHONPATH/PYTHONHOME` contamination and run:

```text
package
-> install
-> setup
-> repeated setup/idempotence
-> update
-> normal installed launcher
-> duplicate Tray / duplicate Worker lock rejection
-> graceful exit / lock release
-> diagnostics
-> uninstall
-> prove versions empty + current pointer/launcher removed
-> prove durable config/data/logs/reports preserved
-> reinstall
-> setup
-> prove consumed identities 001–008 cannot replay across fresh processes
-> restart Tray/Worker
-> diagnostics
```

If ANY disposable lifecycle gate fails: STOP. Do not touch the real runtime.

## Conditional real-user recovery

Only after the complete disposable lifecycle PASS:

1. inspect the quarantined real per-user Bridge root read-only first;
2. prove every version target is within the fixed Bridge root and has sufficient ownership evidence;
3. preserve durable config/data/logs/reports and ledger/manual-consumption evidence;
4. reconcile the historical partial-uninstall state without blind deletion;
5. if a version is already partial, remove only the owned version/pointer artifacts that can be proven to belong to Bridge;
6. install the exact newly certified deterministic package;
7. setup remains PAUSED until certification;
8. verify startup task ownership/name/SID before any mutation;
9. verify installed Tray/Worker health and single instance;
10. prove Dispatches 001–008 cannot replay.

If ownership is ambiguous or durable-data safety cannot be proven: STOP and publish evidence.

## Certification scope in 008

After successful real recovery, close every gate that can be proven without inventing a new control-branch canary:

- FIRST_RUN_SETUP
- PER_USER_INSTALL
- INSTALLER_PACKAGE
- UPDATE_PATH
- UNINSTALL_PATH
- STARTUP_SINGLE_INSTANCE
- SANITIZED_DIAGNOSTICS_BUNDLE
- INSTALLED_TRAY_WORKER
- PROJECT_DICTIONARY_BINDING
- DISPATCH_V3_SCHEMA_BINDING
- DISPATCH_V3_STRUCTURAL_CONFORMANCE
- DISPATCH_V3_RUNTIME_COMPATIBILITY
- V2_COMPATIBILITY
- V06_COMPATIBILITY
- EXACT_AGENT_CONFIGURATION where current installed configuration can truthfully prove it
- FULL_ACCESS_PERMISSION where current execution proof applies
- RESTART_NO_REPLAY
- FULL_BRIDGE_TESTS
- CHANGED_PATH_ALLOWLIST
- SECRET_SCAN
- GIT_DIFF_CHECK

Do NOT fabricate:
- REAL_ELIGIBLE_FOX2_DISPATCH;
- RESULT_REMOTE_READBACK;
- USAGE_SNAPSHOT;
if they require a new immutable control-branch certification canary.

If 008 leaves only those genuine final canary gates, report:
`BRIDGE_RECOVERED_READY_FOR_FINAL_CANARY`

Do NOT report `INTERNAL_FOX2_BRIDGE_READY` unless every normative required gate is actually PASS.

## Evidence / Git

Use a new `reports/BRIDGE-DESKTOP-BATCH-B/evidence/core008/**` namespace.

Preserve all 001–007 evidence byte-for-byte.

Before publication:
- changed path allowlist PASS;
- secret scan PASS;
- `git diff --check` PASS;
- exact branch push;
- exact remote readback.

If incomplete, publish truthful `STOPPED_NEEDS_RECONCILIATION`.
