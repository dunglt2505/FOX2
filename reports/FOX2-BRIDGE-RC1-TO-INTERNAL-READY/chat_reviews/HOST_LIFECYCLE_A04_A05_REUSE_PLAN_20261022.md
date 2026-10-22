# FOX2 — CHAT A04→A05 Reuse-First Continuation Plan

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-RC1`

## Decision

A04 is CLOSED as truthful `CHAT_REWORK / FAIL`; its consumed Dispatch is never replayed.

A05 must NOT repeat A04 work that already passed when that evidence is still applicable to the same runtime subject.

The Host Lifecycle gate will be certified as a **composite evidence chain**:

`A04 accepted prerequisite evidence + corrected certification-harness evidence + A05 continuation-only runtime evidence`.

This is valid only while the runtime package subject remains exactly:

- package SHA-256: `f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee`
- package source commit: `085cc8302e824dbccf9cbef80422ed48894b9cb4`
- source inventory SHA-256: `6d76f99ce9fcc62bbcf9f2450a45bc920c28b2fd70828353c0a8fea096c5de73`

## Critical correction to the previous plan

`agent_bridge/scripts/certify_user_lifecycle.py` is an external test/certification harness. The package builder does not include that file in the installed runtime payload.

A04 package contents are derived from:
- Python runtime modules under `agent_bridge/src`;
- selected desktop/F1 resources;
- self-contained WPF payload.

A harness-only correction therefore does NOT, by itself, invalidate the already-built and installed runtime package.

Accordingly, the previously published Presentation Lock Rework A01 plan that implied “corrected source → rebuild/install a new package before A05” is too broad.

The following unpublished/unconsumed execution setup is superseded BEFORE execution:
- rework PreExec publication: `4d0ae5636ac91969c2a15416f8f0bd50d581d180`
- receipt: ABSENT
- coding Dispatch: ABSENT
- Agent started: FALSE

Do not run that PreExec.

## A04 evidence to reuse — no rerun

CHAT already accepted the following as truthful material A04 PASS evidence:

1. authorization envelope / source/task/Dispatch integrity;
2. split orchestration/package-source worktree design;
3. exact package-source provenance probe;
4. exact package build executed once;
5. package SHA-256 `f99c7add…`;
6. package manifest exact source `085cc830…`;
7. 59 source-file hashes PASS;
8. 40 wheel-module hashes PASS;
9. 255 payload hashes PASS;
10. stale exact-current WPF bounded cleanup PASS;
11. per-user install/update exact package PASS;
12. exact installed pointer/receipt PASS;
13. STOPPED / paused / setup_complete / current_dispatch=null PASS;
14. Worker/legacy absent;
15. launch-twice reached one exact-current WPF singleton;
16. package/current/source identity preserved after first failure;
17. SQLite quick_check PASS;
18. durable logical state / consumed identities preserved at the A04 failure checkpoint.

These remain historical accepted prerequisites. They are not rerun merely because the external certifier changes.

## A04 evidence that cannot be promoted

The following are NOT_RUN/FAIL and remain so until A05 continuation provides evidence:

- live presentation-lock classification: FAIL;
- UI inspect/check after the failed lock gate: NOT_RUN;
- graceful exit after that live presentation: NOT_RUN;
- zero WPF + lock release after exit: NOT_RUN;
- post-exit safe state: NOT_RUN;
- stable external uninstall: NOT_RUN;
- uninstall postconditions: NOT_RUN;
- durable preservation across uninstall: NOT_RUN;
- same exact package reinstall: NOT_RUN;
- final installed safe state: NOT_RUN.

## Certification-harness correction scope

Keep the bounded BUILD rework, but classify its output as **certifier/harness source**, not a new runtime package source.

Allowed files:
- `agent_bridge/scripts/certify_user_lifecycle.py`
- `agent_bridge/tests/test_lifecycle_wpf_contract.py`

Required correction:

- do not accept all PermissionError instances;
- support the real A04 `PermissionError(errno=13, winerror absent/None)`;
- use differential proof;
- explicit `winerror=32` remains accepted;
- persistent ACL/access failure remains rejected;
- lock bytes never modified;
- negative tests remain fail-closed.

For the A04 continuation case, a valid strong differential proof is:

`exact live WPF -> live lock open denied -> explicit graceful exit -> zero exact WPF -> same lock read/write open succeeds`.

This proves the denial was transient and presentation-lifetime-bound without requiring a second package install.

For a fresh-from-zero harness execution, a pre-live openability proof may additionally be used.

## A05 must be continuation-only

A05 is not a rerun of A04.

A05 should be named/treated as a fresh **continuation attempt** because A04 Dispatch was consumed, but it inherits applicable A04 evidence.

### Fresh read-only entry checks

A05 PreExec may re-observe dynamic state without re-performing passed mutations:

- current installed package SHA is still `f99c7add…`;
- installed receipt source remains `085cc830…`;
- existing package archive exists at:
  `C:\Projects\FOX2-artifacts\host_lifecycle_cert_a04\FOX2-Bridge-085cc830-A04.zip`;
- archive SHA-256 remains `f99c7add…`;
- runtime control is STOPPED/paused/setup_complete/current_dispatch=null;
- Worker/legacy absent;
- current WPF count is 0 or 1 and any live WPF is exact-current;
- corrected certifier commit/tests are CHAT_ACCEPTED;
- historical A04 consumed identity is preserved.

These are state-validity checks, not reruns of package build/install.

### Continuation behavior

If one exact-current WPF from A04 remains live:
1. use it; do not relaunch merely to repeat singleton evidence;
2. run corrected live-lock classification;
3. UI inspect/check;
4. explicit graceful exit;
5. require zero WPF;
6. require same lock becomes read/write openable;
7. require post-exit safe control.

If zero WPF exists at A05 entry:
- launch the exact already-installed package only as needed to establish the missing live state;
- do not rebuild or reinstall first;
- historical A04 launch-twice singleton evidence remains accepted;
- one fresh launch is sufficient unless current-state evidence reveals a new singleton anomaly.

If wrong/multiple WPF processes exist, STOP; do not manufacture PASS.

### Remaining lifecycle tail — must run

After corrected presentation proof:
1. capture a fresh bounded durable baseline immediately before destructive uninstall;
2. run stable external uninstall exactly once;
3. verify immediate uninstall postconditions;
4. compare durable data/config/manual-consumption against the fresh baseline;
5. reinstall the SAME exact A04 package archive `f99c7add…`;
6. verify current pointer/source/setup/paused/current_dispatch=null;
7. verify consumed identities and durable state;
8. no G3/G4/Canary.

This is the first stable uninstall/reinstall for the A04 runtime package and therefore is not a rerun.

## Fallback rule

Only if the exact A04 package archive is missing/corrupted may CHAT consider an artifact-recovery build.

Such a build:
- must reproduce the same runtime source `085cc830…`;
- is artifact recovery only, not a new product build acceptance;
- must not occur automatically;
- must not silently change the package subject.

If the archive is present and hash-valid, rebuild is forbidden as unnecessary repetition.

## Composite Host Lifecycle acceptance

CHAT may accept the Host Lifecycle exit gate only if all required gate rows are covered by the union of:

1. A04 CHAT-reviewed PASS evidence;
2. CHAT-accepted harness correction tests;
3. A05 continuation evidence.

A05 does not rewrite A04 FAIL to PASS. Instead:

- A04 remains CLOSED_REWORK;
- A05 closes the previously uncovered/failed rows;
- Host Lifecycle feature gate becomes ACCEPTED only when the composite matrix has no FAIL/NOT_RUN required rows.

## Next safe action

1. Supersede the current unrun Presentation Lock Rework A01 task/prompt/PreExec with an R2 contract that explicitly classifies the correction as external-certifier-only and requires continuation support/tests.
2. Run the new R2 coding PreExec.
3. Fresh coding Dispatch once.
4. CHAT result review and accept corrected certifier.
5. Publish A05 continuation-only task/PreExec/Dispatch:
   - reuse A04 package/build/install evidence;
   - no build;
   - no pre-lifecycle install/update;
   - continue presentation proof then uninstall/reinstall tail.
6. CHAT composite result review.
7. Only after composite Host Lifecycle ACCEPTED may G3 entry resume.

## STOP

Do not:
- replay A04;
- run PreExec `4d0ae563…`;
- rebuild the package while exact A04 archive is available and valid;
- reinstall before A05 presentation continuation merely to recreate already-passed state;
- convert historical A04 FAIL/NOT_RUN into PASS;
- unlock G3 before composite Host Lifecycle acceptance.
