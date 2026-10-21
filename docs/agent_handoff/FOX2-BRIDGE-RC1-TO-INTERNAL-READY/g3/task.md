# FOX2 — G3 Isolated Host Enforcement Test Task

Task ID: `FOX2-BRIDGE-RC1-G3-HOST-A01`
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION`
Stage: TEST
Execution owner: OWNER_MANUAL_HOST under CHAT governance
Execution path: MANUAL_LOCAL / PowerShell 7+
Agent assignment: NONE
Dispatch: NONE

## Owner authority

Exact Owner directive: `làm tiếp đi`.

Authority receipt:
- path: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/owner_directives/G3_PRIVILEGED_ISOLATED_HOST_AUTHORITY_20261021.md`
- commit: `3dfefb9f18b5634252c9f6da6a795069ea262ce6`
- scope: bounded G3 privileged isolated-host testing only.

This authority does not grant G4 Owner-host adoption, Canary, main/merge, provider/trading broker or LIVE.

## Accepted predecessor

- G2 code: `66e8f0a8b3a93140b5f908628b55ac965e15b96e`
- G2 result/evidence: `ac1d1184255945b2c4304641360a1e661ff2d7bd`
- CHAT G2 review: `dcf42dd76c8f22e155d469d356e1f1219f3d7b14`
- G2 verdict: `CHAT_ACCEPT — G2 BUILD ONLY`
- G3 entry contract: `docs/architecture/FOX2_BRIDGE_F1_G3_HOST_ENFORCEMENT_TEST_ENTRY_CANDIDATE_20261021.md` @ `f0fcc1bfefa682701f3d9a9f8e0a24d2ab33b071`.

G2 A01 is consumed/closed. No replay.

## Governance/source set

Live governance resolution was re-read on 2026-10-21 from:
`work/FOX2-POLICY-V200-OWNER-OVERRIDE-RELEASE-20261019` @ `d34da1e3b4918a902646621b487ca8ad3e05b0e0`.

Bound governance:
- Registry: `docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json`, source commit `1f04d62fb7039646c9a213f04a1f1eb17e0f2cc5`, blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`.
- Policy 2.0.0: source commit `96175ac4f39197794a04e695f0046fa7ef9321fe`, SHA-256 `281bcd61bb8c2fb7929ac474f218adbd004bbca6bc21e5311944a0e590723e1e`.
- Dictionary 1.3: source commit `b25f7f728de67cf8595bf24f22fcbd79ef50babc`, SHA-256 `8a64771916d9e3d447f560658e20b307b5945a5d6b3820ea61cd0298636abe1d`.
- Routing 1.4.0: source commit `bcd008983b61349646a5198ff243069f81484fae`, SHA-256 `5759b9a8d63ef165ef63c60ecc601198e39296518c5a1eb91db54555ccd07205`.
- Git-first Protocol 12: source commit `f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa`.
- PreExec Protocol 1.1 / Receipt Schema 1 / CHAT Preflight Intake 1.1 remain the current machine pre-execution contract.
- BRD-09 v0.1 REV3 and Bridge TechSpec v0.7 REV10 remain globally CANDIDATE; task-specific G1/G2 acceptance is not global promotion.

Source axes:
- governance source bytes: VERIFIED;
- scoped Owner G3 authority: VERIFIED by direct current-context directive + Git receipt;
- installed F1 runtime enforcement: NOT_RUN until this G3 task succeeds.

## Target boundary

G3 must run on an isolated/disposable Windows test target. The Owner daily-use Bridge host is not a valid G3 target under this task unless separately admitted as an isolated test target by a new explicit authority.

Task-specific PreExec must identify the exact target and prove:
- Windows 11 Pro-compatible AppLocker capability;
- elevated Administrator token;
- virtual/isolated target evidence;
- rollback/pre-change AppLocker/AppIDSvc/service snapshot;
- clean exact G3 Git worktree;
- no competing material writer;
- no existing FOX2 F1 production/adoption collision;
- task/source identities.

No privileged mutation may occur before the durable G3 PreExec receipt is PASS and CHAT performs remote intake.

## Authorized privileged operations after PASS_TO_EXECUTE

Only on the admitted isolated G3 target:

1. create/ACL-protect `%ProgramData%\FOX2\F1Authority` test authority root;
2. construct the accepted G2-derived offline package in an isolated build environment;
3. provision protected runtime, broker store and sealed G3 test adoption plan;
4. apply/replace the test target's AppLocker policy required by G3 and operate AppIDSvc;
5. install/configure/start/stop/delete service `FOX2F1Authority`;
6. run negative service/policy/source/package/caller/replay tests;
7. after all mandatory negatives PASS, run one bounded authenticated positive service-owned child fixture;
8. run restart/revoke/policy-loss/service-loss/clock/rollback tests;
9. restore pre-G3 AppLocker/AppIDSvc/service state and end with F1 positive authority DENY.

## Mandatory execution order

`SNAPSHOT → PACKAGE → PROTECTED_STATE → APPLOCKER → SERVICE → NEGATIVES → SINGLE_POSITIVE → LIFECYCLE → ROLLBACK`

Do not reorder positive execution ahead of negative gates.

## Required G3 evidence

Write bounded, secret-safe evidence under:
`reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g3/`

Required final summary:
`reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/g3/report.md`

Minimum gate evidence:
- E1 protected root owner/DACL/reparse closure;
- E2 SCM LocalSystem exact service config/image/singleton;
- E3 AppLocker Enforce digest + AppIDSvc running;
- E4 real copied/alternate-root legacy executable/script/interpreter blocks;
- E5 authenticated pipe peer and untrusted peer/server denial;
- E6 one real service-owned positive CreateProcessAsUser fixture;
- E7 same-dispatch concurrency gives exactly one creation/global consumption;
- E8 restart/revoke/policy-loss/service-loss/clock rollback no replay;
- E9 task/source/package/adoption-plan drift DENY;
- E10 rollback restores host controls and final authority DENY.

Every FAIL/BLOCKED/NOT_RUN remains factual.

## Acceptance

G3 PASS requires all E1–E10 material gates PASS on the admitted isolated host plus rollback evidence. Partial success is not G3 PASS.

Even G3 PASS does not authorize:
- G4 Owner-host adoption;
- Canary009;
- `INTERNAL_FOX2_BRIDGE_READY`;
- main/merge;
- provider/trading broker/LIVE.

## STOP

STOP before mutation if:
- PreExec is not PASS_TO_EXECUTE after CHAT intake;
- target is not proven isolated;
- admin/AppLocker/AppIDSvc/SCM/rollback capability is missing or unknown;
- branch/source/task drift;
- worktree has unrelated WIP or competing writer;
- effective policy cannot be exported/restored;
- target contains an unknown existing FOX2 F1 authority/service/adoption state;
- any planned operation exceeds this task.

During execution, any material negative-gate failure prevents the positive fixture. Roll back and publish evidence; do not improvise broader host changes.

