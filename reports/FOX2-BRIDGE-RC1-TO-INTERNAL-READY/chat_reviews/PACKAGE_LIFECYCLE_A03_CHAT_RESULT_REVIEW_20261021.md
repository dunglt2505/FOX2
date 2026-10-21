# FOX2 — CHAT Result Review — Package Lifecycle A03

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-A03`
Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-PACKAGE-LIFECYCLE-A03-CODEX-001`
Result branch: `work/FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-FIX-20261021`
Observed remote result SHA: `2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb`

## Verdict

**CHAT_ACCEPT — PACKAGE LIFECYCLE HARNESS BUILD CORRECTION ONLY**

This acceptance is scoped to the A03 source/test-harness correction and its offline/fixture regression evidence.

It does **not** certify:
- real Owner-host install/update/uninstall/reinstall;
- a current package installation on the physical Lenovo host;
- G3/G4;
- AppLocker/AppIDSvc/service/ACL mutation;
- Canary/final C4;
- main/merge/provider/broker/LIVE;
- `INTERNAL_FOX2_BRIDGE_READY`.

## Immutable assignment / result chain

Verified:
- product source baseline: `b065a468279cbf63ae4bbfad7a0efaad1e6046e4`;
- execution start head: `e052082afd7279f21611d76669dc8e761c003e79`;
- A03 task: `ac12501e1b3c94a0e75b72adc7dc78743d18e660`;
- task blob: `264c1bb54e985d8cd3a73df21072b04271b79d6c`;
- task SHA-256: `b6bbe42d781939a1b05b1dd2aa3fd985677d970b783ab8c2a30b11e9ada85c7e`;
- A03 prompt: `39d6a8f36dd573a4fb9e61a5d4102a15e9b3a80f`;
- prompt blob: `23e562253b1d61f413ed6378a218ba903f87d92e`;
- prompt SHA-256: `25ff86531e9841a9cc8cde6259f0fc9512fe8949c98a57457d689c61bcabce77`;
- A03 PreExec PASS: `e052082afd7279f21611d76669dc8e761c003e79`;
- A03 executable Dispatch: `9ddb2154d87fc88ccbdfd4c3e9550574f0bb6a66`;
- Dispatch blob: `bfa449e8b9050b0f524ac5c8552e95eb3bccb7e4`;
- Dispatch Schema v3 validation: PASS;
- implementation commit: `fab3642b818415428ae3f67965430e3ea0b11401`;
- result/evidence commit: `2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb`.

Remote task branch independently read back at the exact result SHA supplied outside the Agent report.

A01 remains consumed/no-replay. Neither A02 Dispatch was executed.

## Ancestry and changed-path review

`e052082a... → fab3642b...`:
- exactly one implementation commit;
- only:
  - `agent_bridge/scripts/certify_user_lifecycle.py`;
  - `agent_bridge/tests/test_rc1_package.py`.

`fab3642b... → 2faa33f9...`:
- exactly one result/evidence commit;
- only authorized report/evidence paths.

No forbidden product path was changed.

The following accepted product-contract files are byte-identical between execution base and result:
- `agent_bridge/src/fox2_agent_bridge/installation.py`;
- `agent_bridge/src/fox2_agent_bridge/__main__.py`.

## Implementation semantics

CHAT reviewed the actual result bytes.

The lifecycle harness now:
1. selects `BridgeRoot/uninstall.ps1`;
2. invokes it synchronously through PowerShell 7;
3. executes with `cwd=BridgeRoot`, outside version directories;
4. removes inherited `PYTHONPATH` / `PYTHONHOME` from the uninstall child;
5. records supervisor type/path/content SHA-256;
6. records exit code plus bounded sanitized stdout/stderr;
7. performs current-pointer/version/durable config/data/consumption checks;
8. writes uninstall evidence before any reinstall;
9. on nonzero, timeout, start failure or postcondition failure raises once without retry or alternate uninstall entrypoint;
10. keeps installed Python for existing control/status operations but does not use it for uninstall.

Product `installation.uninstall()` remains unchanged and continues to deny installed-interpreter self-deletion in favor of stable external `uninstall.ps1`.

## Regression evidence

Focused/final lifecycle coverage verifies:
- stable external supervisor chosen;
- installed Python never calls `uninstall`;
- exactly one supervisor attempt;
- success evidence checkpointed before reinstall;
- nonzero supervisor exit prevents reinstall;
- timeout/start/postcondition/config/consumption/unreadable-check failure paths persist evidence and stop;
- supervisor or parent interpreter under `versions` is denied before launch;
- redaction occurs before output truncation;
- durable fixture bytes and consumed identities remain preserved.

Observed tests:
- initial focused: **8 PASS**;
- final lifecycle cases: **11 PASS**;
- installation/package: **62 PASS**;
- final full suite: **617 PASS**, zero failure/error/skip.

## Preserved initial full-suite failure

The original full run is preserved as:

**592 PASS / 25 FAIL**

All 25 failures were in unchanged `agent_bridge/tests/test_preexec.py` and surfaced as `GIT_OPERATION_FAILED`.

The retained validation history records a read-only reproduction:
- original Git command: exit 128;
- same object with `core.longpaths=true`: exit 0;
- same object bytes read: 4920;
- root cause: Git for Windows MAX_PATH in a deeply nested test fixture.

The final full run did **not** alter repository/global Git configuration, code or tests. It supplied `core.longpaths=true` only to child Git processes via `GIT_CONFIG_COUNT/GIT_CONFIG_KEY/GIT_CONFIG_VALUE`.

Therefore:
- the initial 25 FAIL remain historical factual FAIL and are not rewritten;
- they are classified as a reproduced test-environment limitation, not an A03 implementation regression;
- final required full suite under the corrected process environment is 617 PASS.

## Static / security / K1

Verified evidence states:
- Python syntax PASS;
- stable supervisor PowerShell parse PASS with PowerShell 7 and zero parse errors;
- changed-path allowlist PASS;
- `git diff --check` PASS;
- bounded secret scan PASS;
- K1 `UNEXPLAINED=0`;
- product contract unchanged PASS;
- real host lifecycle NOT_RUN.

CHAT independently recomputed every manifest-listed evidence SHA-256 from Git result bytes:

**18 / 18 evidence hashes matched.**

Result Contract:
- `contract_version=2.0`;
- report and evidence manifest are present;
- result contract validation PASS;
- changed-path coverage PASS;
- submission remains `PUSHED_UNREVIEWED` until this CHAT receipt.

## Acceptance matrix

- Stable external supervisor: PASS
- No installed-Python self-delete path in certification: PASS
- Bounded sanitized exit/stdout/stderr evidence: PASS
- Nonzero/failure stop-once semantics: PASS
- Product self-delete guard preserved: PASS
- Durable fixture/config/data/consumption regressions: PASS
- Focused lifecycle regressions: PASS
- Installation/package suite: PASS
- Full suite: PASS in documented process-only long-path environment
- Allowlist/diff/secret/K1: PASS
- Result Contract v2: PASS
- Historical Batch-B `UNINSTALL_PATH=FAIL`: preserved
- Real host lifecycle: **NOT_RUN**

## Uncovered surfaces

The following remain intentionally unverified:
1. real Owner-host uninstall via the corrected harness;
2. real current-package uninstall/postconditions;
3. real reinstall and durable-state preservation after the uninstall;
4. rollback/current-package lifecycle certification;
5. G3/G4 and final Canary/C4.

Fixture tests do not substitute for those stages.

## NEXT_SAFE_ACTION

Issue a fresh Git-first host lifecycle certification task using the accepted A03 implementation/result as source.

That next task must:
- use exact accepted result `2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb`;
- perform fresh route/host PreExec;
- explicitly authorize only the required current-package install/update/uninstall/reinstall lifecycle on the Owner physical host;
- retain rollback and durable state evidence;
- stop before G3/AppLocker/service/ACL mutation;
- produce a new result receipt for CHAT review.

No A03 replay is permitted.
