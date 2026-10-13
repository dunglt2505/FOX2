# FOX2 — M1-P2-01 DELIVERY-ONLY REBIND

**Date:** 2026-10-13  
**Project:** FOX2  
**WP:** `FOX2-M1-P2-01`  
**Status:** `DELIVERY_REBOUND / IMPLEMENTATION_SCOPE_UNCHANGED / REPORT_PATHS_AUTHORIZED`

## 1. Purpose

Resolve only the result-delivery allowlist conflict observed after the existing P2-01 implementation run.

This record does **not** re-scope implementation, change requirements, change the Agent assignment, recreate the worktree, change the task branch, modify Policy/BRD/Contract/Acceptance sources, or authorize merge/deployment/LIVE.

The existing implementation prompt and code scope remain authoritative except where this delivery-only addendum explicitly authorizes the canonical Result Contract paths below.

## 2. Bound source / execution identity

- Effective Policy: **FOX2 Policy V1.8.4 RELEASED_EFFECTIVE**
  - Library SHA-256: `481790b2512ea1cd4891fe1b03258175d68d9bfae71158d19283bd003c560f5a`
  - Git blob: `483a74ff39339e653bbd7bbfba0feaf7b1c003e9`
- Effective Routing Index: **V1.2.5 EFFECTIVE_DERIVATIVE**
  - Git blob: `3ea18c06af93cd059b7e29c6f09914ac4a0298a7`
- Original P2-01 rebind:
  - `588da7b1c1a642ddfd935ff6372af83a35acaa2f:docs/agent_handoff/M1/P2-01/FOX2_M1_P2_01_PREDEV_REBIND_V184_20261013.md`
  - Blob: `031c02fc420f9156e809a6f0e77b864b6ad09c23`
- Conditional DEV authorization:
  - `docs/agent_handoff/M1/P2-01/FOX2_M1_P2_01_CONDITIONAL_DEV_AUTH_20261013.md`
  - Blob: `8b0ec8670457da76a02f8e9d9c5f0a0013f8d4f7`
- Executable CODEX prompt:
  - `docs/agent_handoff/M1/P2-01/FOX2_M1_P2_01_CODEX_EXECUTE_PARALLEL_20261013.md`
  - Blob: `182d5600843d19ad5f64af67eadc7149f7c55c13`
- Task branch: `work/FOX2-M1-P2-01-foundation-codex`
- Expected unchanged remote HEAD before delivery reconciliation:
  - `588da7b1c1a642ddfd935ff6372af83a35acaa2f`
- Existing worktree to reuse:
  - `C:\Projects\FOX2-worktrees\FOX2-M1-P2-01-CODEX`

## 3. Scope preserved exactly

### Allowed implementation/code paths — unchanged

- `backend/**`
- `tests/p2_01/**`

No other application-code path is authorized by this rebind.

### Existing implementation exclusions — unchanged

Still denied unless separately re-scoped:

- `agent_bridge/**`
- `source_freshness/**`
- `frontend/**`
- `docs/**` other than this CHAT-authored handoff record
- `.github/**`
- root `tests/**` outside `tests/p2_01/**`
- P2-02 store/migrations
- P2-03 DSM implementation
- P2-04 integration beyond the already-authorized P2-01 minimal foundation/health boundary
- DNSE/provider network
- account/order/broker code
- main push, merge, deployment, Production or LIVE

## 4. Delivery-only permission correction

The canonical Result Contract requires task-result delivery under `reports/<WP_ID>/`.

For this WP only, add/confirm the following **report paths** independently from `allowed_code_paths`:

```text
allowed_report_paths:
- reports/FOX2-M1-P2-01/report.md
- reports/FOX2-M1-P2-01/evidence_manifest.json
- reports/FOX2-M1-P2-01/evidence/**
```

Permissions for these canonical result paths:

```text
GIT_REPORT_WRITE = YES
GIT_REPORT_PUSH = YES
REPORT_BRANCH = work/FOX2-M1-P2-01-foundation-codex
```

Existing code-push authority is **preserved, not broadened**:

```text
GIT_CODE_PUSH = preserve the already-activated task-bound grant only
CODE_PATHS = backend/** + tests/p2_01/**
```

If the current runtime cannot establish that the existing P2-01 code-push grant is active for this same branch/worktree/source scope, STOP and return that single remaining blocker. This rebind must not manufacture a broader code grant.

## 5. Delivery reconciliation instructions

CODEX shall resume from the existing worktree/WIP and **must not** redo the implementation merely because delivery was blocked.

1. Reuse:
   - `C:\Projects\FOX2-worktrees\FOX2-M1-P2-01-CODEX`
   - `work/FOX2-M1-P2-01-foundation-codex`
2. Preserve the existing local WIP. Do not reset, clean, stash, rebase or recreate the worktree.
3. Keep all implementation mutations inside:
   - `backend/**`
   - `tests/p2_01/**`
4. Convert/copy the useful human-result content currently held at:
   - `tests/p2_01/P2_01_RESULT.md`
   into:
   - `reports/FOX2-M1-P2-01/report.md`
5. Create:
   - `reports/FOX2-M1-P2-01/evidence_manifest.json`
   conforming to the currently bound Agent Result Contract/schema.
6. Optional sanitized evidence attachments may be written only under:
   - `reports/FOX2-M1-P2-01/evidence/**`
7. Prior test evidence may be cited as prior evidence, but before the final task-result commit/push, rerun the required current P2-01 suite/acceptance checks against the current worktree bytes.
8. Preserve truthful acceptance status. In particular, any canonical/integrated scenario previously marked `PARTIAL` stays `PARTIAL` unless newly executed evidence actually closes it.
9. Before staging:
   - run the required P2-01 tests;
   - run safe syntax/import/static checks already available;
   - run `git diff --check`;
   - inspect `git status`;
   - verify every staged path is inside either `allowed_code_paths` or `allowed_report_paths`;
   - run secret/evidence redaction checks.
10. Stage only:
    - authorized P2-01 code/test paths; and
    - the canonical report/evidence paths above.
11. Commit only on:
    - `work/FOX2-M1-P2-01-foundation-codex`
12. Push only that non-main task branch.
13. Independently read back the full remote commit SHA.
14. Final Agent submission state may be only:
    - `PUSHED_UNREVIEWED`
15. CHAT performs the independent immutable-SHA review before any acceptance decision.

## 6. Explicit non-effects

This delivery rebind does **not**:

- change Policy V1.8.4;
- change Routing Index V1.2.5;
- change M1 Technical Spec;
- change P2 WP Plan;
- change Market Data Contract/schema;
- change the frozen acceptance source/subset;
- change Agent selection;
- change model/thinking/quota requirements;
- authorize another Agent writer;
- authorize PR creation unless separately granted;
- authorize main push/merge;
- authorize Production/provider network;
- authorize broker/account/order writes;
- authorize LIVE.

## 7. STOP conditions

STOP and preserve WIP if any of the following occurs:

- source/Policy/task binding drifts;
- branch/worktree identity changes unexpectedly;
- writer collision appears;
- actual staged path falls outside `allowed_code_paths + allowed_report_paths`;
- report-push permission is unavailable;
- existing task-bound code-push grant cannot be verified where code files must be committed;
- required current tests fail;
- secret/private account/licensed raw feed exposure is detected;
- push fails or remote SHA cannot be verified;
- any safety/platform refusal occurs.

## 8. Required final return

Return:

```text
FOX2 M1-P2-01 DELIVERY RESULT

DELIVERY_REBIND_READBACK:
POLICY_READBACK:
ROUTING_INDEX_READBACK:
SOURCE_BINDING:
WORKTREE:
BRANCH:
INITIAL_REMOTE_HEAD:
FINAL_LOCAL_HEAD:
REMOTE_HEAD:

CODE_PATHS_STAGED:
REPORT_PATHS_STAGED:
TESTS:
TEST_RESULT:
ACCEPTANCE_SUMMARY:
SECRET_SCAN:

COMMIT:
PUSH:
RESULT_REPORT:
EVIDENCE_MANIFEST:

EXECUTION_STATE:
  PUSHED_UNREVIEWED
  | BLOCKED_SOURCE
  | BLOCKED_SCOPE
  | BLOCKED_TEST
  | BLOCKED_PUSH
  | BLOCKED_OTHER

OPEN_GATES:
STOP_REASON:
```

**Owner/CHAT decision:** delivery mismatch is resolved only by the report-path authorization above. No implementation rescope is approved.
