# FOX2 — Build Environment Discovery V2 Test-Artifact Execution Defect

Date: 2026-10-21
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01`

## Observation

The bounded read-only discovery V2 launched an invalid historical test-artifact executable from an old worktree. Windows displayed an "Unsupported 16-Bit Application" dialog for a path under:

`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B\agent_bridge\test_artifacts\...\versions\aaaa...\runtime\Scripts\python.exe`

This executable is part of a synthetic/historical test-artifact tree and is not a real FOX2 build Python environment.

## Root cause

Discovery V2 recursively enumerated every `python.exe` beneath FOX2 project/worktree roots and filtered only on the suffix `\Scripts\python.exe`.

That rule is too broad. It includes:
- synthetic test artifacts;
- copied installed runtime fixtures;
- version trees;
- packaged/runtime payloads;
- other non-venv executable fixtures.

The helper then attempted to start such a candidate to inspect Python package metadata, which triggered the Windows compatibility dialog before the candidate could be rejected semantically.

## State

CHAT independently remote-read the governed host-cert branch after the incident:

- remote head remains `768b35164fd740bb6a455ee50fc4dcaae331fed8`;
- PreExec receipt remains absent;
- executable Dispatch remains absent;
- host-cert Agent remains not started;
- package build/install/update/uninstall/reinstall remains NOT_RUN;
- no Bridge lifecycle mutation occurred from this discovery;
- prior host state remains reconciled as STOPPED / paused=true / zero active runtime.

## Verdict

`RECOVERED — DISCOVERY_V2_CANDIDATE_SCOPE_DEFECT / NO_GOVERNED_SIDE_EFFECT`

The Windows dialog is not evidence of host incompatibility and not evidence that a compatible build environment is absent.

## Next safe action

Do not run discovery V2 again.

Run a corrected read-only discovery that:

1. never recursively executes arbitrary `python.exe` files;
2. discovers venv candidates from PATH / Python Launcher / real `pyvenv.cfg` roots only;
3. excludes historical/synthetic trees such as `test_artifacts`, `artifacts`, `versions`, `runtime`, `reports`, `evidence`, `dist`, `build`, temp/cache/package trees;
4. validates a candidate as a PE executable before Process.Start, preventing NE/16-bit/corrupt fixture launch;
5. inspects only existing environments and never installs/upgrades anything;
6. preserves exact task branch and absent PreExec receipt.

Do not rerun PreExec v4 until discovery is reconciled.
