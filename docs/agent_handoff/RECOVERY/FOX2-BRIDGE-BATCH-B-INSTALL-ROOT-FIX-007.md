# FOX2 Bridge Batch B — Install Environment Root Fix + Closure Certification 007

## Role
Implementation / recovery certification inside the EXISTING `FOX2-BRIDGE-DESKTOP-BATCH-B` whole-WP.

## Immutable context

Current task branch:
`work/FOX2-BRIDGE-DESKTOP-BATCH-B`

Current remote head:
`ce7a8253926b7489c79311e26d7dc75ba8c81fc6`

Dispatches 001–006 are CONSUMED. NEVER replay or resume any of them.

Current accepted governance:
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

Everything else is read-only.

No main/PR/merge/deploy/provider/broker/LIVE authority.

## Root cause evidence — CONFIRMED

Dispatch 006 built deterministic package:

`6e96ee19ea103e7bd606a63abf071d00de6fa3c6cd1663b8d9d921b01d70b3a9`

The isolated install stopped at `INSTALLED_MODULE_PROOF` with:

`ModuleNotFoundError: No module named 'fox2_agent_bridge'`

Owner then ran a non-dispatch A/B proof using that exact package and wheel:

```text
package_sha_match          = true
wheel_has_bridge_package   = true

contaminated parent env:
  PYTHONPATH=<Bridge source>
  venv_exit                = 0
  pip_exit                 = 0
  installed_import_pass    = false

clean parent env:
  PYTHONPATH absent
  venv_exit                = 0
  pip_exit                 = 0
  installed_import_pass    = true

real_runtime_touched       = false
dispatch_executed          = false
uninstall_invoked          = false
```

Therefore the material defect is the installer subprocess environment contract: installation subprocesses inherit Python path/home state from the invoking process, allowing pip/install behavior to diverge from the isolated `python -I` module proof.

Do NOT redesign packaging. Do NOT replace the wheel format. The exact wheel contains the Bridge package and installs correctly in a clean environment.

## Required root fix

Make the production installation subprocess boundary hermetic with respect to inherited Python interpreter path configuration.

At minimum:
1. subprocesses launched through the installation execution helper must not inherit `PYTHONPATH`;
2. they must not inherit `PYTHONHOME`;
3. this must apply to venv creation, offline pip install and installed-runtime proof;
4. preserve the current bounded/sanitized error contract;
5. do not weaken `-I` proof, package hash verification, manifest verification, path ownership or ProcessLock behavior;
6. do not add network dependency to installed-runtime package installation.

Prefer one small central environment-sanitization helper or equivalent root fix rather than per-call patches.

## Mandatory regression evidence before touching real user runtime

Add focused tests proving:
- inherited `PYTHONPATH` is stripped from installation subprocesses;
- inherited `PYTHONHOME` is stripped;
- ordinary non-Python environment needed by the subprocess remains preserved;
- subprocess failure remains sanitized/fail-closed;
- the exact install sequence remains venv -> offline pip -> isolated module proof.

Then:
- run focused installer tests;
- run the full Bridge test suite;
- rebuild the user package twice and prove deterministic equality;
- in a NEW disposable user profile, run the full Core lifecycle using a deliberately contaminated parent environment and prove the root fix defeats the contamination.

Required isolated lifecycle:
```text
package
-> install
-> first-run setup
-> repeat setup/idempotence
-> update
-> startup/single-instance
-> Tray/Worker
-> diagnostics
-> uninstall
-> reinstall
-> durable config/data/consumption preservation
-> restart/no-replay
```

If any isolated lifecycle gate fails: STOP. Do not touch the real installed Bridge.

## Conditional real per-user recovery

ONLY after every isolated lifecycle gate above PASSes:

1. inspect the existing per-user Bridge root without blind deletion;
2. prove ownership of every version path before removal/reconciliation;
3. preserve intended durable `config/`, `data/`, `logs/`, `reports/`;
4. reconcile the damaged partial-uninstall state safely;
5. install the exact newly certified deterministic package;
6. run setup/startup/Tray/Worker health;
7. prove no replay of Dispatches 001–006.

If ownership or durable-data safety cannot be proven: STOP and publish evidence. Do not force cleanup.

## Final Bridge certification — one cycle

After real runtime recovery, close the whole Batch B acceptance set in one cycle:

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
- REAL_ELIGIBLE_FOX2_DISPATCH
- EXACT_AGENT_CONFIGURATION
- FULL_ACCESS_PERMISSION
- RESULT_REMOTE_READBACK
- USAGE_SNAPSHOT or NOT_EXPOSED_WITH_EXECUTION_PROOF
- RESTART_NO_REPLAY
- FULL_BRIDGE_TESTS
- CHANGED_PATH_ALLOWLIST
- SECRET_SCAN
- GIT_DIFF_CHECK

Final success marker is only valid when all required gates PASS:

`INTERNAL_FOX2_BRIDGE_READY`

No deferred uninstall is allowed at final success.

## Git/evidence

Preserve all historical 001–006 evidence byte-for-byte.

Publish only on:
`work/FOX2-BRIDGE-DESKTOP-BATCH-B`

Required new evidence should be under a new bounded 007/core007 namespace and must not rewrite historical reports.

Before success:
- changed-path allowlist PASS;
- secret scan PASS;
- `git diff --check` PASS;
- commit/push exact task branch;
- exact remote readback PASS.

If final certification is incomplete, report `STOPPED_NEEDS_RECONCILIATION` truthfully. Never fabricate PASS.
