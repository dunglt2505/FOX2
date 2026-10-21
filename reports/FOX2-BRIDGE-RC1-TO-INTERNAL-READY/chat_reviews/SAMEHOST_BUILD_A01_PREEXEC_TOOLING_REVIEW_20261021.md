# FOX2 — CHAT Review — Same-Host BUILD A01 PreExec Tooling

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-SAMEHOST-BUILD-A01`
Reviewer: CHAT
Skills: `fox2-result-review`, `fox2-execution-recovery`, `fox2-status-roadmap`

## Immutable source and publication

- Task/prompt source lock: `600f8ceb6943d1f1ecf341ff06072bf31c1babe0`.
- PreExec tooling publication commit: `f3a0e86515c5285715730ff86781eb71c62c7ab0`.
- Publication parent: exactly `600f8ceb6943d1f1ecf341ff06072bf31c1babe0`.
- Publication branch: `work/FOX2-BRIDGE-F1-SAME-HOST-POLICY-BUILD-20261021`.
- Published file: `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/samehost/samehost_build_a01_preexec.ps1`.
- Published blob SHA-1: `eb7d42028ead630ad58fb2ea392c5570ff1d6b65`.

Remote branch readback equals the publication commit.

## Diff / K1

Compare `600f8ceb...` -> `f3a0e865...`:
- ahead: 1;
- behind: 0;
- changed paths: exactly 1;
- only added path: the PreExec script above;
- 232 additions / 0 deletions.

K1 classification: **REQUESTED**. `UNEXPLAINED=0`.

No task.md, prompt.md, product code, governance, AppLocker policy, service state or host ACL was changed by this publication.

## Script review

CHAT independently read the complete published script and Receipt Schema v1.

Verified design properties:
- original task/prompt source lock remains `600f8ceb...`;
- publication head must be the single script-only child;
- script verifies its own Git blob identity before continuing;
- raw task/prompt identities are verified from Git bytes, not checkout re-encoding;
- one-worktree + task-scoped CODEX writer checks are fail-closed;
- CODEX calls are metadata/help/login only; no `exec`, `resume` or implementation launch;
- no AppLocker/service/ACL/install/deploy action exists in the PreExec flow;
- historical receipt/WIP is not deleted/reset/stashed/replayed;
- receipt is validated against `FOX2_PREFLIGHT_RECEIPT_SCHEMA_v1.json`;
- only the exact receipt path may be staged/committed;
- receipt commit must have publication head as parent;
- remote readback and remote receipt blob are verified after push;
- PASS/BLOCKED is emitted from actual receipt state;
- a child PowerShell process exits without terminating the Owner shell.

Receipt Schema v1 requires only `status` inside each capability object; the script's capability shape is schema-compatible.

## Test claim boundary

The returned result reports **11/11 simulated checks PASS**, but no committed simulation test artifact was included in the tooling publication. CHAT therefore records:

`SIMULATED_11_OF_11 = NOT_VERIFIED_BY_CHAT`

This does not block accepting the publication as PreExec tooling because CHAT independently reviewed the actual Git diff/script/schema. It does mean the 11/11 statement is not used as execution evidence.

## Verdict

**CHAT_ACCEPT — PREEXEC TOOLING ONLY**

Accepted:
- script-only publication at `f3a0e86515c5285715730ff86781eb71c62c7ab0`;
- immutable blob `eb7d42028ead630ad58fb2ea392c5570ff1d6b65`;
- safe to invoke as the next same-host BUILD PreExec mechanism.

Not accepted / still NOT_RUN:
- real Owner-host PreExec;
- CODEX model/quota/live execution readiness;
- CODEX implementation start;
- same-host BUILD result;
- AppLocker/AppIDSvc/service/ACL host mutation;
- G3 physical-host enforcement;
- G4/Canary/LIVE.

NEXT_SAFE_ACTION: run this exact versioned PreExec file from the dedicated same-host worktree. CHAT must remote-intake the resulting receipt before CODEX implementation may start.
