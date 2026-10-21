# FOX2 — CHAT Result/Recovery Review — Package Lifecycle A01 Consumed Safe Stop

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Consumed task: `FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-A01`
Consumed Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-PACKAGE-LIFECYCLE-A01-CODEX-001`

## Observed execution

Owner launcher reported:
- CODEX process started and exited 0;
- CODEX stopped at its preflight before edits because required HEAD in the immutable prompt was `b065a468279cbf63ae4bbfad7a0efaad1e6046e4` while actual clean task branch HEAD was `b224f029bc911c0a131342b8ac142fdd4952a96f`;
- no edits, tests, host lifecycle actions, commits or push were performed;
- remaining checks were NOT_RUN;
- local HEAD after execution: `b224f029bc911c0a131342b8ac142fdd4952a96f`;
- remote HEAD after execution: same;
- worktree dirty after: false;
- durable attempt claim state: `EXITED_CONSUMED`;
- Dispatch consumed: true;
- no replay: true;
- result delivery: `NO_RESULT_OBSERVED`.

CHAT independently remote-read the task branch and confirmed it remains exactly `b224f029bc911c0a131342b8ac142fdd4952a96f`.

## Immutable binding comparison

A01 product/task source baseline:
`b065a468279cbf63ae4bbfad7a0efaad1e6046e4`.

A01 prompt explicitly required:
`Exact starting base: b065a468279cbf63ae4bbfad7a0efaad1e6046e4`.

A01 executable Dispatch correctly bound:
`runtime_contract.base_sha = b224f029bc911c0a131342b8ac142fdd4952a96f`,
because that runtime head contains the task-specific PreExec PASS receipt.

Therefore the Agent observed a real immutable assignment contradiction and correctly executed the STOP condition.

## Result-review classification

- Git result commit: **ABSENT**
- `report.md`: **NOT_PRODUCED**
- `evidence_manifest.json`: **NOT_PRODUCED**
- implementation diff: **NONE**
- tests: **NOT_RUN**
- real host lifecycle mutation: **NOT_RUN / FALSE**
- product code acceptance: **UNCHANGED**
- A01 Dispatch: **CONSUMED — NO REPLAY**

This is not `CHAT_ACCEPT`, because there is no implementation result to accept.
This is not a product-code FAIL.
It is a bounded assignment/recovery outcome.

## Root cause

**CHAT assignment-binding defect.**

The handoff incorrectly used one SHA for two different concepts:
1. accepted immutable **product source baseline**; and
2. **execution starting HEAD** after task/prompt/PreExec evidence publication.

Git-first PreExec necessarily advances the task branch after the product baseline, so an executable prompt must not require current HEAD to equal the older product baseline.

## Verdict

`REWORK — ASSIGNMENT_BINDING_DEFECT / CONSUMED_SAFE_STOP / NO_PRODUCT_CHANGE`

Historical A01 remains consumed and must never be replayed.

## Required correction for the fresh attempt

The new immutable assignment must separate:

- `PRODUCT_SOURCE_BASE=b065a468279cbf63ae4bbfad7a0efaad1e6046e4`;
- `EXECUTION_START_HEAD=Dispatch.runtime_contract.base_sha`.

Agent start gate:
- exact branch must match;
- current HEAD must equal the fresh Dispatch runtime base;
- product baseline must be an ancestor;
- pre-execution administrative/task/prompt/receipt commits after the product baseline must be independently bounded and must not be mistaken for product-code drift;
- no requirement may simultaneously assert HEAD equals the old product baseline.

A fresh task/prompt/PreExec/Dispatch identity is required. A01 Dispatch `...001` is permanently consumed.

## NEXT_SAFE_ACTION

Prepare fresh A02 assignment under the same Whole-WP with corrected dual-source semantics. Do not start Agent execution until fresh A02 task/prompt publication and route-specific PreExec PASS are remote-read and a new max-runs=1 Dispatch is published.
