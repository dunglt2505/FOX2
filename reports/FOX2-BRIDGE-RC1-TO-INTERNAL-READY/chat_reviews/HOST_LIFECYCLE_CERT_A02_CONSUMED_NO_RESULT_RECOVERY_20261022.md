# FOX2 — CHAT Execution Recovery — Host Lifecycle Cert A02 CONSUMED / NO RESULT

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-RC1`
Stage: TEST
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02`
Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02-CODEX-001`

## Verdict

**RECOVERED — CONSUMED_NO_RESULT / CERTIFICATION_NOT_RUN / FRESH ATTEMPT REQUIRED**

The A02 Dispatch is permanently consumed and MUST NOT be replayed.

CODEX started and exited 0, but intentionally refused host lifecycle execution because the immutable prompt required it to observe CHAT acceptance/PASS_TO_ASSIGN, a fresh executable A02 Dispatch with exact remote readback, and the Owner-visible PowerShell 7 launcher. Those artifacts were created after the prompt and were not available in the Agent's task-branch execution context.

This is an execution-envelope visibility defect, not a product failure and not a lifecycle TEST result.

## Observed execution outcome

Owner-host launcher reached the durable consume point and started CODEX.

Final launcher state:
- CODEX exit: 0;
- Dispatch consumed: true;
- no replay: true;
- local task HEAD after: `76913f36b461689a84e8b4acf57a9ef83a98828d`;
- remote task HEAD after: `76913f36b461689a84e8b4acf57a9ef83a98828d`;
- remote advanced: false;
- changed path count: 0;
- unauthorized path count: 0;
- report changed: false;
- manifest changed: false;
- result delivery: `NEEDS_RECONCILIATION`;
- G3/G4/Canary remained false.

CODEX terminal message:
- classification: BLOCKED;
- lifecycle certification: NOT_RUN;
- no package build;
- no host mutation;
- no repository write/commit/push.

## Remote reconciliation

CHAT independently verified after the consumed attempt:
- A02 task branch remains exactly `76913f36b461689a84e8b4acf57a9ef83a98828d`;
- Dispatch control branch remains exactly `8dceb41112d8240ec579ddede23b8ae6a9d06662`;
- no Git result commit exists.

Current Governance source bytes remain unchanged:
- Registry blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`;
- source-resolution blob `186fdbc72dc1b22e97330895142d68600591ac21`;
- Dictionary blob `6c8f30e2e6b07f2e65e45c14faab99672d036083`;
- Policy blob `2d373f374f906bf7959062050bbeae5350b0c482`;
- Routing blob `14d2e95e419cc67c3e0cf851cc806a96cf885b7e`;
- Git-first Protocol blob `d34a022f2bda39a167a404c8530e57b30f337cb9`.

## Root cause

A02 prompt was correctly immutable before PreExec/Dispatch publication, but it also required the Agent itself to verify later-created authorization artifacts.

The launcher verified those later artifacts before CODEX start, but then passed only the exact immutable prompt body plus a limited environment set. The Agent therefore could not prove, from its own visible execution context, the exact PASS_TO_ASSIGN / fresh Dispatch / Owner-launch authorization it was told to require.

This creates a circular handoff visibility problem:

`prompt published → PreExec PASS → PASS_TO_ASSIGN → Dispatch published → launcher verifies all → Agent receives pre-Dispatch prompt only → Agent cannot see post-prompt authorization → BLOCKED`.

## Corrective design for fresh A03

Do not weaken authorization checks.

Fresh A03 will instead use an explicit runtime execution envelope defined by the immutable prompt before assignment:

1. The prompt names the exact environment variables and remote Git refs the launcher must supply at execution time.
2. After A03 PreExec PASS, CHAT publishes A03 PASS_TO_ASSIGN and one fresh A03 Dispatch.
3. The Owner-visible launcher verifies all immutable evidence and sets:
   - `FOX2_DISPATCH_ID`;
   - `FOX2_DISPATCH_COMMIT`;
   - `FOX2_RUNTIME_BASE`;
   - `FOX2_ACCEPTED_SOURCE`;
   - `FOX2_PASS_TO_ASSIGN_COMMIT`;
   - `FOX2_PASS_TO_ASSIGN_PATH`;
   - `FOX2_CONTROL_BRANCH`;
   - `FOX2_STATUS_BRANCH`;
   - `FOX2_PREEXEC_RECEIPT_COMMIT`.
4. The A03 Agent must independently fetch/read those runtime-provided immutable refs and verify:
   - supplied Dispatch ID/commit resolves to the expected A03 Dispatch path on the control branch;
   - supplied PASS_TO_ASSIGN commit resolves to the expected A03 PASS_TO_ASSIGN path on the status branch;
   - supplied runtime base equals the A03 PreExec receipt commit;
   - task/prompt/source bindings match;
   - permission scope is report/evidence-only;
   - max_runs=1.
5. Only then may host lifecycle mutation begin.

The prompt does not hard-code a future Dispatch commit or PASS_TO_ASSIGN commit; it hard-codes the required verification mechanism and expected artifact identities/paths, avoiding the circularity while preserving fail-closed authorization.

## No replay / historical truth

Never replay:
- `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01-CODEX-001`;
- `FOX2-DISPATCH-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A01-CODEX-001`;
- `FOX2-DISPATCH-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02-CODEX-001`;
- `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02-CODEX-001`.

A02 remains `CONSUMED_NO_RESULT`, not PASS and not an A03 substitute.

## NEXT_SAFE_ACTION

Create a fresh Host Lifecycle Certification A03 task/prompt on a fresh non-main branch from accepted product source `085cc8302e824dbccf9cbef80422ed48894b9cb4`, publish exact immutable bindings, then run a fresh A03 route-specific PreExec before any new Dispatch.

G3 remains locked.
