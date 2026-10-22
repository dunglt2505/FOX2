# FOX2 — CHAT Result Review — Host Lifecycle Certification A04

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-RC1`
Stage: TEST
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04`
Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04-CODEX-001`
Runtime base: `6d1d2a70f2d1cc47e44f70a0ba6cd07cd3985713`
Agent result: `92394d0ae68911c98bcdaa40aaa76ed56de66881`

## Verdict

**CHAT_REWORK — A04 truthful FAIL accepted; lifecycle TEST exit gate NOT accepted.**

A04 Dispatch is permanently consumed and MUST NOT be replayed.

The Agent result is accepted as a truthful, well-delivered FAIL / REWORK_REQUIRED report. It is not a lifecycle PASS and does not unlock G3/G4/Canary.

## Independent Git/result intake

CHAT remote-read verified:

- result SHA `92394d0ae68911c98bcdaa40aaa76ed56de66881`;
- result is a descendant of runtime base `6d1d2a70f2d1cc47e44f70a0ba6cd07cd3985713`;
- result branch advanced and remained the authorized non-main A04 branch;
- 35 changed paths;
- 0 unauthorized paths;
- all changes restricted to:
  - `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`;
  - `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`;
  - `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert_a04/**`;
- no `agent_bridge` source/test code changed in the Agent result;
- worktree reported clean;
- package-source worktree reported clean;
- Result Contract v2 schema blob `b7617cc5c75c288c7997c64536a22fb836b8200b`;
- evidence manifest validates with zero schema errors;
- evidence count 34;
- changed-path inventory count 35;
- K1 `UNEXPLAINED=0`;
- secret/privacy scan PASS;
- `git diff --check` PASS;
- remote delivery evidence records immutable fetch/readback and hash verification;
- delivery remains `PUSHED_UNREVIEWED` until this CHAT decision.

The result's historical FAIL/NOT_RUN states remain authoritative and are not promoted.

## Material progress accepted from A04

A04 resolved the prior A03 provenance problem and proved materially more of the real-host path.

Accepted evidence includes:

1. runtime authorization envelope / immutable Git binding PASS;
2. orchestration worktree no product drift PASS;
3. dedicated package-source worktree detached at exact accepted source PASS;
4. accepted builder blob `2417212e5677a2061e3957544a99e2ba80f46f4d` PASS;
5. builder `source_git_commit()` returned exact accepted source PASS;
6. exact package build executed once, exit 0;
7. package SHA-256 `f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee`;
8. package manifest source commit exactly `085cc8302e824dbccf9cbef80422ed48894b9cb4`;
9. 59 source-file, 40 wheel-module and 255 payload hash checks PASS;
10. stale exact-current WPF bounded surfacing/inspect/graceful cleanup PASS;
11. exact per-user install/update PASS;
12. installed state STOPPED / paused=true / setup_complete=true / current_dispatch=null;
13. Worker/legacy absent;
14. lifecycle launched twice and reached exact-current singleton presentation;
15. no lifecycle rerun;
16. stable uninstall attempts = 0;
17. reinstall attempts = 0;
18. consumed identities preserved;
19. host remained usable and safe after first failure;
20. final read-only observation showed exact installed source/package, SQLite quick_check=ok, one exact-current WPF and Worker/legacy=0.

## First failure

The first real lifecycle failure is:

`PermissionError: [Errno 13] Permission denied: BridgeDesktop/desktop.lock`

at:

`agent_bridge/scripts/certify_user_lifecycle.py:157`

during the live presentation-lock probe:

`with lock.open('r+b'):`

Accepted source:
`085cc8302e824dbccf9cbef80422ed48894b9cb4`

Accepted lifecycle script blob:
`7e62103ea4876833f67794a927a2a54622a59ea5`

The current implementation treats a failed live lock open as an accepted held-lock proof only when:

`getattr(error, 'winerror', None) == 32`

and re-raises all other OSError shapes.

The actual Owner-host Python 3.13 execution surfaced `PermissionError(errno=13)`; the result did not record a usable `winerror == 32`, so the accepted handler re-raised.

## Root cause classification

**BUILD/test-harness compatibility defect in presentation-lock certification semantics.**

This is not evidence that WPF singleton locking itself is broken.

The accepted WPF implementation opens:

`BridgeDesktop/desktop.lock`

using .NET:

`new FileStream(..., FileAccess.ReadWrite, FileShare.None)`

and keeps the FileStream alive for the presentation lifetime.

The existing offline lifecycle fixture models:
- held live lock as PermissionError with synthetic `winerror=32`;
- access-denied as PermissionError with synthetic `winerror=5`.

That fixture did not cover the real Owner-host Python 3.13 exception shape `PermissionError(errno=13)` with no accepted `winerror=32` classification.

A04 therefore exposed a missing Windows-real exception compatibility case in the certification code/tests.

## Required correction semantics

Do NOT simply accept every PermissionError as “lock held.”

The correction must preserve the distinction between a real held presentation lock and unrelated file access/ACL failure.

Required robust design:

1. Before launching the current presentation, while no WPF presentation owns the file:
   - if `desktop.lock` already exists, prove the same current user can open it read/write;
   - if it does not exist, absence is allowed before first launch.
2. Launch the exact current WPF presentation and prove exact PID/path/singleton.
3. During the live presentation:
   - require the lock file exists;
   - attempt the same read/write open;
   - accept Windows `PermissionError(errno=EACCES/13)` as held-lock evidence only when the pre-live accessibility/identity conditions make an unrelated persistent ACL denial impossible;
   - retain support for explicit sharing-violation `winerror=32`;
   - log bounded exception classification (type/errno/winerror), not private path content.
4. After explicit graceful UI exit and zero WPF:
   - require the same lock file becomes read/write openable again.
5. Never modify lock bytes merely to test ownership.
6. Preserve fail-closed behavior for:
   - lock missing while live;
   - lock unexpectedly openable while WPF is live;
   - pre-live access already denied;
   - lock remains inaccessible after WPF exit;
   - duplicate/mismatched presentation;
   - unsafe control state.
7. Add regression coverage for the actual A04 shape:
   `PermissionError(errno=13, winerror absent/None)`.
8. Keep historical fixture coverage distinguishing persistent access-denied/ACL failure from real transient held-lock behavior.

## Why this is BUILD rework, not A05 TEST-only retry

The consumed A04 Dispatch cannot be replayed.

A fresh host TEST with unchanged source would deterministically execute the same accepted `certify_user_lifecycle.py` logic and can reproduce the same incompatibility.

Therefore the next safe step is a bounded BUILD correction of the lifecycle certification script + its focused tests, then CHAT acceptance of that new source, followed by a fresh Host Lifecycle TEST (A05) using a new package built from the corrected accepted source.

## Host state after A04

Current evidence shows:

- exact package remains installed;
- exact accepted source remains installed;
- control state STOPPED;
- paused=true;
- setup_complete=true;
- current_dispatch=null;
- Worker/legacy=0;
- one exact-current WPF remains live at mandated failure stop;
- SQLite quick_check=ok;
- configuration/manual-consumption/dispatch identities preserved;
- database logical table hashes preserved;
- stable uninstall NOT_RUN;
- reinstall NOT_RUN.

The live WPF must be handled only by the next authorized pre-exec/test flow. Do not force kill it.

## Historical truth

Preserve:
- A01: historical FAIL;
- A02: consumed/no-result;
- A03: consumed, truthful provenance-blocked result, lifecycle NOT_RUN;
- A04: consumed, truthful real-host FAIL at presentation-lock proof.

None may be replayed or rewritten as PASS.

## NEXT_SAFE_ACTION

Open one bounded BUILD correction inside the same Whole-WP:

`FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERT-REWORK-A01`

Base:
`085cc8302e824dbccf9cbef80422ed48894b9cb4`

Allowed product/test paths only:
- `agent_bridge/scripts/certify_user_lifecycle.py`
- `agent_bridge/tests/test_lifecycle_wpf_contract.py`

Required focused + full regression evidence, no WPF product change unless evidence proves one is necessary.

After CHAT accepts the correction, create fresh Host Lifecycle Certification A05 with new source/package provenance and no replay of A04.

G3 remains locked.
