# FOX2 — CHAT Result Review — G2 Integrated F1 Build A01

Date: 2026-10-21  
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`  
Task: `FOX2-BRIDGE-RC1-G2-A01`  
Reviewer: CHAT  
Skill: `fox2-result-review` + `fox2-feature-certification`

## Immutable chain

- Owner G2 coding lift: `fe926ad24d89231e5cf80f0f48ea44eb36887834`.
- Task publication: `653e49fc0d0f15981bf230995925c89d6994723d`.
- Prompt publication: `eec25e64a66fed7afc3f45b4d490e6a944e8fe6c`.
- Task-specific PreExec source: `ca684b09b3eaea7fa2ce7fc7983f890384202296`.
- PreExec PASS receipt: `94c936b1d93bbfcee5818db24dd75bd9bb32733f`.
- Recovered Agent code commit: `66e8f0a8b3a93140b5f908628b55ac965e15b96e`, direct child of receipt.
- Recovered immutable result/evidence commit: `ac1d1184255945b2c4304641360a1e661ff2d7bd`, direct child of code commit.
- Remote branch readback equals result commit.

No replay occurred. A01 is the sole consumed implementation attempt.

## Route / provenance

PreExec and source-readback evidence bind CODEX / `gpt-6.1-sol` / HIGH / FULL_ACCESS / MANUAL_LOCAL, one writer, task branch and exact immutable task. The Git commit author metadata is `Copilot`, but this is treated as local Git identity metadata rather than execution-route evidence because:
1. task-specific PreExec observed CODEX exact route;
2. active session evidence records `gpt-6.1-sol/high/danger-full-access/approval=never`;
3. command inventory records the source commit inside that same A01 session;
4. no second G2 writer was observed.

No Agent substitution is established by the commit author string alone.

## Scope / K1

Code commit changes 24 product/test paths; result commit changes 35 report/evidence paths. All observed paths are inside the task allowlist.

K1: `UNEXPLAINED=0`. Material hunks are classified REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED. No governance, BRD, TechSpec, main, release or unrelated engine path changed.

## Test chronology

Historical failures are preserved and are not converted to PASS:
- `regression-01`: FAIL, 7 failed / 193 passed — Windows MAX_PATH fixture path.
- `regression-02`: FAIL, 1 failed / 199 passed — PowerShell AuthorizationManager on extended-path script execution.
- `full-01`: FAIL, 26 failed / 518 passed — includes unchanged PreExec fixture Git path-length failures plus inventory-helper module-import issue.

The failures were followed by bounded corrective test-fixture/environment changes, not by hiding/removing tests. Final evidence:
- focused F1: **61 PASS**;
- affected regression: **200 PASS** (final `regression-06`);
- full `agent_bridge/tests`: **557 PASS** (final `full-03`);
- static/package contract: **PASS**, allowlist/diff/syntax PASS, 40 wheel-source modules checked, no effective-policy mutation, no service install/start;
- native non-elevated Windows F1 tests: **3 PASS**;
- Desktop Release build: **PASS**, 0 warning / 0 error.

Command inventory shows the final test sequence completed before the source commit, with no observed source mutation between final checks and commit.

## G2 acceptance matrix

| Gate | Verdict | Boundary |
|---|---|---|
| Service/AppIDSvc/policy/SCM/runtime drift => DENY | PASS_G2 | source/native test; not G3 enforcement |
| Forged request/caller/task/source/package/nonce/epoch => DENY | PASS_G2 | focused authority/protocol tests |
| Global same-dispatch one-consumed result | PASS_G2 | concurrent source test + broker store |
| Restart/revoke/lease/clock/no replay | PASS_G2 | source/store tests |
| Installed consumer convergence to service gate | PASS_G2 | code + consumer/regression tests |
| Copied legacy/current AppLocker identity model | PASS_G2 | hash/SID model only; effective policy NOT_RUN_G3 |
| No broad user-writable path trust | PASS_G2 | policy model rejects path trust |
| Reconciliation ambiguity remains HOLD/DENY | PASS_G2 | regression suite |
| Frozen F0 negatives remain green | PASS_G2 | full suite |
| Full Bridge regression | PASS | 557/557 final |
| Package/service/policy support does not activate host policy | PASS_G2_SCOPED | static/package contract; full offline package archive build remains NOT_RUN |
| Rollback returns DENY and preserves tombstones | PASS_G2 | source fixture |
| No host mutation/elevation/Canary | PASS | static/result evidence |
| K1 / scope discipline | PASS | UNEXPLAINED=0 |

## Required NOT_RUN boundaries

- `G3_HOST`: NOT_RUN — effective AppLocker deployment, SCM install/start/reboot, LocalSystem positive spawn, real protected-root attack tests, service crash/lifetime, Owner-host adoption.
- `OFFLINE_USER_PACKAGE`: NOT_RUN — no provisioned isolated full package build environment. This is not treated as G3 PASS. For this G2 task, static package-module contract and changed-script/package tests satisfy the explicit build-task packaging/static check requirement; an actual deployable package remains a later gate.

## Direct security review

CHAT inspected the security-sensitive source:
- installed/runtime ledger paths cannot use local positive claim authority;
- installed E2E delegates to `f1_client` before local worktree/claim/adapter execution;
- client verifies SCM server PID, LocalSystem identity, protected expected image and has no fallback;
- named-pipe peer SID/session/token/PID come from Windows impersonation; caller-supplied identity is not authority;
- global claim persists before one-use spawn intent and OS process creation;
- child is created suspended under authenticated user token, assigned to kill-on-close Job, then policy/source/lease are rechecked before resume;
- service boot increments epoch and revokes old leases;
- revocation tombstones the adoption-plan digest and closes service-owned Jobs;
- policy artifact uses enforcing Exe/Script/MSI/Dll hash rules and rejects path-only trust;
- G2 source contains no service install/start or effective AppLocker mutation path.

No G2-blocking security bypass was found in this review. This does not certify real Windows enforcement.

## Result-contract observations

Result Schema v2 validation and evidence SHA checks passed. The committed manifest/report retain `LOCAL_ONLY` wording because they were assembled before delivery recovery. Independent remote readback proves the two commits are now published on the authorized non-main branch. This stale delivery label is retained as historical truth-at-assembly and is not rewritten after the fact.

## CHAT verdict

**CHAT_ACCEPT — G2 BUILD ONLY**

Accepted:
- G2 source/build implementation at `66e8f0a8b3a93140b5f908628b55ac965e15b96e`;
- immutable result/evidence delivery at `ac1d1184255945b2c4304641360a1e661ff2d7bd`;
- BUILD exit evidence sufficient to move the F1 feature into the next TEST/host-enforcement stage.

Not accepted / not authorized:
- G3/G4 host enforcement;
- installed positive F1 authority;
- full offline release package;
- merge/main;
- deployment;
- provider/trading broker;
- Canary/LIVE;
- `INTERNAL_FOX2_BRIDGE_READY`.

Current runtime semantics remain **F1 positive authority DENY / Canary HOLD / INTERNAL_FOX2_BRIDGE_READY NOT_ATTESTED**.

NEXT_SAFE_ACTION: prepare G3 host-enforcement/test entry and its exact privileged-operation gates. Do not install/start the service or apply AppLocker until separate G3 authority and host PreExec are established.
