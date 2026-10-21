# FOX2 — CHAT PASS_TO_ASSIGN — Lifecycle/WPF Contract Rework A01

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A01`
Stage: BUILD rework

## Verdict

**PASS_TO_ASSIGN — CODEX BUILD REWORK ONLY**

This PASS_TO_ASSIGN authorizes one fresh CODEX implementation attempt for the bounded lifecycle/WPF contract rework. It does not certify the real host lifecycle and does not authorize G3/G4/Canary.

## Policy / task / source resolution

Live governance readback:
- governance release branch head: `d34da1e3b4918a902646621b487ca8ad3e05b0e0`;
- Policy 2.0.0: `96175ac4f39197794a04e695f0046fa7ef9321fe`, SHA-256 `281bcd61bb8c2fb7929ac474f218adbd004bbca6bc21e5311944a0e590723e1e`;
- Dictionary 1.3: `b25f7f728de67cf8595bf24f22fcbd79ef50babc`, SHA-256 `8a64771916d9e3d447f560658e20b307b5945a5d6b3820ea61cd0298636abe1d`;
- Routing 1.4.0: `bcd008983b61349646a5198ff243069f81484fae`;
- Git-first Protocol v12: `f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa`;
- Dispatch schema: v3;
- Result Contract: schema v2 / template v4 / CHAT intake v9.

Bridge TechSpec v0.7 REV10 remains `CANDIDATE_NO_PROMOTION` and is not used to override accepted implementation semantics.

## Immutable task chain

Failed host lifecycle result / rework source base:
`9dd91becf47d934183baf147d0a4f03f4bf5933d`

Unchanged accepted product source under that result:
`2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb`

Task:
- commit `aabe81fad8a465ea12a763fd4cccc54670dd707f`;
- path `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/lifecycle_wpf_contract_rework/task.md`;
- blob `e6503c2a817450f270ab674ce1cd723019961dce`;
- SHA-256 `50bf03fc9fdb149dd7b4d0a3edf4bd2acbc26ec0000f39208b17b9d2f7bc2b01`.

Prompt:
- commit `de3f6768fa01b1396b6686f3c06c103669bcd24d`;
- path `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/lifecycle_wpf_contract_rework/prompt.md`;
- blob `5bd037b3536592d31e68b3b5e5929b84fb48d50f`;
- SHA-256 `88359fad2607aeb7669f3678966390a118c131d9849697c24a8505e3d9932dd9`.

PreExec v1:
- `544c1a39861966b3d589f692bb8e0b27c6f329c3`;
- blob `ef329ab0bc5ecf88048734012c0d66e292f84f43`;
- **PUBLISHED_INVALID_NOT_EXECUTABLE**;
- Owner execution NOT_RUN;
- rejection receipt `6db4755e2f652377a9c0a74250a76823397467c7`.

PreExec v2 publication:
`7207a3c455b40bd24b71e0cd94c5f42d7e348bd0`

PreExec v2 script blob:
`68db0d3f0d867bd18aaa8dee6174791f31b36f9b`

PreExec v2 PASS receipt:
- commit `e7d5acf51dddcbc95324a992ad6be2773e61285f`;
- blob `66fc3c02a35ad05b40faed578ecd0355472111ee`;
- status `PASS`;
- blockers `[]`.

Remote task branch head equals the PASS receipt commit.

The PreExec receipt commit is exactly one commit after the v2 publication and adds only:
`reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/lifecycle_wpf_contract_rework_a01.json`.

No product source changed in the PreExec chain.

## Material route evidence

Observed PASS:
- PowerShell 7.6.7;
- Python 3.13.15;
- Git;
- .NET 8.0.426;
- CODEX login;
- CODEX CLI contract;
- CODEX live route probe;
- pinned `gpt-6.1-sol`;
- reasoning `high`;
- permission profile `FULL_ACCESS`;
- dedicated clean worktree;
- one writer;
- exact task/prompt binding.

PreExec explicitly records:
- implementation Agent not started;
- Dispatch not published;
- Dispatch not consumed;
- real host lifecycle mutation false;
- G3 mutation false.

## R0–R7

- R0 task/evidence: PASS — fresh rework task and truthful failed A01 evidence.
- R1 stage: PASS — BUILD source correction; TEST host lifecycle remains pending.
- R2 source/authority/risk: PASS — current governance resolved; product source/failure base immutable; candidate Bridge TechSpec not promoted.
- R3 route/capability: PASS — CODEX `gpt-6.1-sol / high / FULL_ACCESS / MANUAL_LOCAL` verified by task-specific PreExec.
- R4 cost/actor: PASS — host-only coding/testing is residual work; CHAT completed all Git/source/review work directly; WORK not required.
- R5 writer/WIP: PASS at PreExec; must be rechecked immediately before Agent spawn.
- R6 Git source/delivery: PASS — non-main task branch; AGENT code/report push; CHAT result review required.
- R7 assignment: PASS — exact role/model/thinking/scope/STOP/result contract frozen in prompt.

## Skill coverage

- `fox2-governance-preflight`: REQUIRED / APPLIED.
- `fox2-agent-route-runtime`: REQUIRED / APPLIED.
- `fox2-agent-prompt-builder`: REQUIRED / APPLIED.
- `fox2-result-review`: NOT_APPLICABLE until Agent result return.
- `fox2-execution-recovery`: NOT_APPLICABLE unless consumed attempt becomes interrupted/non-normal.

## Authorized implementation scope

Allowed code paths:
- `agent_bridge/scripts/certify_user_lifecycle.py`;
- `agent_bridge/tests/test_rc1_package.py`;
- `agent_bridge/tests/test_rc1_launcher.py`;
- at most one focused new lifecycle/WPF test file under `agent_bridge/tests/`.

Allowed result paths:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/lifecycle_wpf_contract_rework/**`.

Forbidden:
- launcher/F1/WPF production architecture changes;
- installation.py or certify_rc1_ui.ps1 changes;
- real installed Bridge lifecycle mutation;
- Worker/F1 start;
- AppLocker/AppIDSvc/service/ACL/reboot;
- G3/G4/Canary;
- main/PR/merge/provider/broker/LIVE.

## Assignment decision

A fresh schema-v3 Dispatch may now be published with:
- target CODEX;
- model `gpt-6.1-sol`;
- reasoning `high`;
- FULL_ACCESS;
- MANUAL_LOCAL;
- AGENT delivery;
- code/report push allowed only within bounded paths;
- max_runs = 1;
- runtime base = `e7d5acf51dddcbc95324a992ad6be2773e61285f`;
- no replay.

The consumed host lifecycle A01 Dispatch remains historical and must never be reused.

## Next

Publish and remote-read a fresh executable Dispatch. Only then may the Owner run the complete PowerShell 7 launcher exactly once.
