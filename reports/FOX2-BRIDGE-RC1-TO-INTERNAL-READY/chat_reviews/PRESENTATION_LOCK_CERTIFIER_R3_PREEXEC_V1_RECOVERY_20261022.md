# FOX2 — Presentation Lock Certifier R3 PreExec v1 Recovery

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3`
R3 publication: `ba9b8eda7de3c2aa53cf0e7aeee3249f60780b13`

## Observed Owner-host failure

The exact published R3 PreExec v1 started and verified:

- accepted source `085cc8302e824dbccf9cbef80422ed48894b9cb4`;
- R3 task/prompt/PreExec immutable blobs and SHA-256;
- dedicated worktree creation;
- clean worktree;
- no `agent_bridge` product drift;
- `TASK_ROUTE_ASSESSMENT`: MEDIUM / execution risk MEDIUM / safety override NO;
- selected route: CODEX / `gpt-6.1-sol` / medium.

It then stopped fail-closed at:

`TEST_PYTHON_PROBE_FAILED: ModuleNotFoundError: No module named 'pytest'`

for:

`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B\agent_bridge\.build-venv\Scripts\python.exe`

## FIRST_FAILURE

**PreExec capability-binding defect: build Python was incorrectly reused as test Python.**

The historical accepted build-environment discovery proves this `.build-venv` for deterministic package build dependencies. It does not prove or require the pytest dev extra.

The current task needs a test runner, not a package-build interpreter.

## Existing reusable evidence

Historical accepted Same-Host BUILD evidence at result `b065a468279cbf63ae4bbfad7a0efaad1e6046e4` records a real full Bridge test run using:

`C:\Users\Fox Le\AppData\Local\Programs\Python\Python313\python.exe -m pytest ... agent_bridge/tests`

with:

`606 passed`.

This is evidence of a previously compatible host test interpreter, not current capability proof. Because host tooling is time-dependent, a fresh read-only probe is still required.

## Side-effect reconciliation

CHAT remote-read the R3 branch after the failure:

- remote R3 head remains exactly `ba9b8eda7de3c2aa53cf0e7aeee3249f60780b13`;
- PreExec receipt: ABSENT;
- executable R3 Dispatch: ABSENT;
- Agent execution: NOT_STARTED;
- code edit: FALSE;
- package build/install/uninstall/reinstall: NOT_RUN;
- host lifecycle mutation: FALSE;
- G3/G4/Canary: HOLD.

No execution identity was consumed.

## Verdict

`RECOVERED / PREEXEC_V1_BLOCKED / NO_SIDE_EFFECT`

Do not rerun immutable PreExec v1.

Do not install pytest into the build venv.

Do not change the selected Medium route.

## Next safe action

Publish a fresh R3 PreExec v2 under the same immutable task/prompt. v2 must:

1. preserve R3 source/task/prompt/route;
2. treat the historical user-local Python 3.13 test runner as a candidate, not assumed PASS;
3. perform bounded read-only current discovery from:
   - `%LOCALAPPDATA%\Programs\Python\Python313\python.exe`;
   - PATH-resolved `python.exe`;
   - Python Launcher `py -0p` candidates when available;
4. accept only an existing Python 3.13 candidate that can import current `pytest>=8.3,<9` and `jsonschema`;
5. install/upgrade nothing;
6. then verify the already-selected CODEX / gpt-6.1-sol / medium route;
7. publish a receipt only on PASS.

Historical R3 PreExec v1 remains BLOCKED and is never promoted to PASS.
