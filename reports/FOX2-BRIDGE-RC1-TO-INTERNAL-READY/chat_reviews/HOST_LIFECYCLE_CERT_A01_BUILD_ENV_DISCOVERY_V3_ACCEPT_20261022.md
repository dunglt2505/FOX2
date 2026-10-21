# FOX2 — Host Lifecycle Cert A01 Build Environment Discovery V3 Acceptance

Date: 2026-10-22
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01`

## Governed state before discovery

- task branch: `work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-20261021`
- branch head: `768b35164fd740bb6a455ee50fc4dcaae331fed8`
- PreExec receipt: absent
- executable Dispatch: absent
- host-cert Agent: not started
- package lifecycle mutation: NOT_RUN

## Discovery result

The corrected read-only discovery V3 found three safe Python candidates and executed only native-PE/path-validated candidates.

Exactly one existing environment satisfies the deterministic package-build contract:

Alias:
`WORKTREES/FOX2-BRIDGE-DESKTOP-BATCH-B/agent_bridge/.build-venv/Scripts/python.exe`

Observed:
- isolated: true
- Python: 3.13
- platform: win32
- pip: 26.2.1
- setuptools: 84.0.0
- wheel: 0.48.0
- build: 1.6.1
- jsonschema: 4.26.0
- attrs: 26.1.0
- referencing: 0.37.0
- rpds-py: 2026.9.1
- jsonschema-specifications: 2025.9.1

Dotnet:
- ready: true
- version: 8.0.426

The other discovered Python environments did not satisfy the build contract and are not eligible.

## Safety result

Discovery V3 reported:
- Git mutation: false
- host lifecycle mutation: false
- package build: false
- PreExec rerun: false
- tool installation: false

## Verdict

`ACCEPT — EXISTING BUILD CAPABILITY VERIFIED`

No environment provisioning is needed.

## Next safe action

Do not rerun PreExec v4.

Publish a fresh immutable PreExec v5 that binds the exact already-existing build environment above and validates its observed versions before any executable Dispatch can be issued.

The v5 receipt must expose a bounded alias rather than raw host-local build path, preserve the prior v4 BLOCKED history, and keep package build/install/update/uninstall/reinstall NOT_RUN during PreExec.
