# FOX2 — Host Lifecycle Cert A01 PreExec v4 Reconciliation — Build Python Discovery

Date: 2026-10-21
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01`

## Observed second v4 run

The reconciled host-state recovery succeeded:
- Bridge state before rerun: `STOPPED`;
- `paused=true`;
- `stop_requested=true`;
- durable active execution: none;
- active Worker/Tray runtime: zero;
- no package lifecycle mutation occurred.

The exact immutable PreExec v4 then reran and stopped at:

`COMPATIBLE_ISOLATED_BUILD_PYTHON_NOT_FOUND`.

## Evidence boundary

This failure does **not** prove that no compatible build Python exists on the host.

PreExec v4 searches only:
- the host-cert worktree `agent_bridge` subtree; and
- `C:\Projects\FOX2\agent_bridge`.

The build contract in `agent_bridge/scripts/build_user_package.py` requires an already-provisioned isolated Python environment satisfying the package-build requirements, but it does not require that environment to live under either of those two specific search roots.

Historical installed package evidence proves a deterministic package had previously been produced, but does not provide a current build-Python path or prove that the old build environment still exists.

## State

- task branch remote head unchanged at `768b35164fd740bb6a455ee50fc4dcaae331fed8`;
- PreExec receipt absent;
- executable Dispatch absent;
- Agent not started;
- package build/install/update/uninstall/reinstall NOT_RUN;
- host lifecycle mutation false;
- G3/G4/Canary HOLD.

## Verdict

`RECOVERED / PREEXEC_BLOCKED — COMPATIBLE_BUILD_PYTHON_NOT_FOUND_IN_V4_SEARCH_SCOPE`

Do not classify this as `CAPABILITY_ABSENT` yet.

## Next safe action

Perform one bounded read-only discovery over FOX2 project/worktree Python environments and PATH-resolved Python executables.

For each candidate, inspect only:
- path alias;
- isolated flag;
- Python major/minor;
- platform;
- setuptools;
- wheel;
- build;
- jsonschema;
- attrs;
- referencing;
- rpds-py;
- jsonschema-specifications.

Do not install or upgrade anything.

If a compatible existing candidate is found, issue a fresh PreExec artifact or bounded recovery identity that binds its exact path/versions; do not silently mutate v4.

If no compatible candidate exists after bounded discovery, classify `CAPABILITY_ABSENT` and require a separately authorized build-environment provisioning action rather than installing tools inside this TEST task.
