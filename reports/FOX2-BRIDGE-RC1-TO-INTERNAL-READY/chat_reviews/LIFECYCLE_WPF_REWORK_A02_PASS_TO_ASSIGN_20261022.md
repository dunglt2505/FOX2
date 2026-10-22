# FOX2 — CHAT PASS_TO_ASSIGN — Lifecycle/WPF Contract Rework A02

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02`
Stage: BUILD rework / recovery continuation

## Verdict

**PASS_TO_ASSIGN — CODEX BUILD REWORK A02 ONLY**

This verdict authorizes publication of exactly one fresh executable CODEX Dispatch for A02 after the verified task-specific PreExec REV3. It does not certify A02 implementation, real host lifecycle, G3/G4, Canary, provider, broker, main, merge or LIVE.

Attempt A01 remains permanently consumed and MUST NOT be replayed.

## Recovery / task state

Historical consumed Dispatch:

`FOX2-DISPATCH-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A01-CODEX-001`

- commit: `b7894655bb53ac302279439d024de7822139abe5`
- state: `EXITED_CONSUMED`
- exit: `1`
- result delivery: `NEEDS_RECONCILIATION`
- Agent result: absent
- replay: forbidden

Immutable salvage snapshot:

`1a11fa0b232a69f0c26a0b4029c331ee2a8c840f`

Recovery parent:

`e7d5acf51dddcbc95324a992ad6be2773e61285f`

Recovery snapshot is salvage input only; it is not an Agent result and is not CHAT-accepted.

## A02 immutable task/prompt

Branch:

`work/FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02-20261022`

Task:
- commit: `f796306ca4e79b9ab61cd436cf69a5f28ede4faf`
- blob: `3beb3bf2f3c2a76dcd8b10308f3670da98e70424`
- SHA-256: `7bfe425ad18f372960fb0440cd8694fb1a2a86edd7bd10cac5b105817f73d58c`

Prompt:
- commit: `56e4c1eeb9341062fdb8ec52110e4e5c44c329e2`
- blob: `faef3f5cf4b6d286d7a30cb4200c6b6526ed55b2`
- bytes: `10270`
- corrected raw SHA-256: `a9b07516ce8f5b31ffb7b404f993407855cb1449f28be244011902630df5f201`

The prior CHAT-only prompt hash `454423ec...` was invalid because of a hashing-helper state bug. Prompt bytes never changed. Feature Status correction was published at `12c5de7f18027db5a122ebc91bdf0372b78aee94`.

## PreExec REV3

Owner-host PreExec result: **PASS**

Local receipt SHA-256:

`0d265137e1567a2b47999e99716cacca9c6121bb2ac606688b949b4f88aa6c2f`

Published receipt:
- commit: `4504bf95dd2baf474b30f896b23365c52fe10c9f`
- blob: `827fb02b57a49483b8a5be7589170d38cbb9df59`
- path: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/lifecycle_wpf_contract_rework_a02_preflight.json`
- remote SHA-256: `0d265137e1567a2b47999e99716cacca9c6121bb2ac606688b949b4f88aa6c2f`
- exact byte readback: PASS
- blockers: `[]`

Material evidence:
- exact recovery/task/prompt binding PASS;
- current Governance source bytes PASS;
- dedicated worktree clean;
- competing writer: NONE_OBSERVED;
- CODEX CLI: `codex-cli 0.162.1`;
- pinned `gpt-6.1-sol`;
- reasoning `high`;
- FULL_ACCESS capability present;
- read-only CODEX current probe PASS;
- authentication/capacity PASS;
- `eligible_agent_route=PASS`;
- A02 executable Dispatch absent at PreExec;
- Agent implementation not started;
- real host lifecycle mutation false;
- Worker/F1 false;
- G3 false.

## Current Governance source resolution

- Policy 2.0.0: `96175ac4f39197794a04e695f0046fa7ef9321fe`
- Dictionary 1.3: `b25f7f728de67cf8595bf24f22fcbd79ef50babc`
- Routing Index 1.4.0: `bcd008983b61349646a5198ff243069f81484fae`
- Git-first Protocol v12: `f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa`
- Governance release branch observed head: `d34da1e3b4918a902646621b487ca8ad3e05b0e0`

Effective Dispatch schema v3 source on that Governance release branch:
- blob: `1692061941e2bef498515cd0e96b9b3046119ebb`

The older schema copy `a53956cad7809cc53f92ecdc5d91a1ff2119b421` on historical task/control ancestry hard-codes the obsolete v1 Dictionary path and is not used as authority for the new Dispatch. No schema file is modified by A02.

Bridge TechSpec v0.7 REV10 remains `CANDIDATE_NO_PROMOTION`.

## R0–R7

- R0 task/evidence: PASS — A01 consumed state reconciled; immutable recovery snapshot exists; A02 is a fresh assignment identity.
- R1 stage: PASS — BUILD correction only; real-host TEST remains separate.
- R2 source/authority/risk: PASS — current Governance resolved; immutable recovery/task/prompt binding verified.
- R3 route/capability: PASS — CODEX `gpt-6.1-sol/high`, current auth/capacity and CLI route observed PASS.
- R4 actor/cost: PASS — CODEX remains the pinned implementation route; WORK not required.
- R5 writer/WIP: PASS at PreExec — dedicated A02 worktree clean, one writer.
- R6 Git/delivery: PASS — non-main branch, bounded code/report paths, Agent push followed by CHAT result review.
- R7 assignment: PASS — exact role/model/thinking/scope/STOP/result contract frozen.

## Authorized paths

Allowed code:
- `agent_bridge/scripts/certify_user_lifecycle.py`
- `agent_bridge/tests/test_rc1_package.py`
- `agent_bridge/tests/test_rc1_launcher.py`
- `agent_bridge/tests/test_lifecycle_wpf_contract.py`

Allowed result:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/lifecycle_wpf_contract_rework/**`

Recovery provenance `recovery_codex001_snapshot.json` must remain byte-identical.

## Prohibited

No launcher/F1/WPF production architecture change, installation.py change, certify_rc1_ui.ps1 change, real installed lifecycle mutation, Worker/F1 start, AppLocker/AppIDSvc/service/ACL/reboot, G3/G4/Canary, main/PR/merge/provider/broker/LIVE.

## Assignment decision

CHAT may now publish one new schema-v3 Dispatch:

`FOX2-DISPATCH-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02-CODEX-001`

with:
- target CODEX;
- pinned model `gpt-6.1-sol`;
- reasoning `high`;
- permission `FULL_ACCESS`;
- execution path `MANUAL_LOCAL`;
- delivery owner `AGENT`;
- runtime base = A02 PreExec receipt commit `4504bf95dd2baf474b30f896b23365c52fe10c9f`;
- source/salvage input = `1a11fa0b232a69f0c26a0b4029c331ee2a8c840f`;
- max_runs = 1;
- explicit A01 no-replay.

Agent completion state is at most `PUSHED_UNREVIEWED` until CHAT result-review.
