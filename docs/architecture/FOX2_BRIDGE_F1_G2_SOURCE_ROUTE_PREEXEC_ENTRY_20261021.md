# FOX2 Bridge F1 — G2 source / route / PreExec entry review
Date: 2026-10-21
Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY
Feature: FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION
Class: CHAT READ-ONLY/CANDIDATE ENTRY REVIEW — NO EXECUTABLE TASK
Design-branch base: 382fce8458862c6ac8bbebcca7ffaad12e0e1ced

## 1. Governance source resolution
Resolved from the explicitly selected non-main Governance release chain, not from this design branch or filename ordering.

| Source | State for G2 preparation | Immutable identity |
|---|---|---|
| Projectwide Governance Registry | GOVERNANCE_EFFECTIVE_OWNER_AUTHORIZED_IN_SCOPE | commit 1f04d62fb7039646c9a213f04a1f1eb17e0f2cc5; blob 1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35 |
| Current Source Resolution | GOVERNANCE_EFFECTIVE_OWNER_APPROVED; machine installed adoption NOT_ATTESTED | commit b04ded4b9d7fb241dc69ad25097eb474807cf68c; blob 186fdbc72dc1b22e97330895142d68600591ac21 |
| Policy 2.0.0 | OWNER_APPROVED_EFFECTIVE_FOR_NEW_AND_RESCOPED_CHAT_WORK | commit 96175ac4f39197794a04e695f0046fa7ef9321fe; blob 2d373f374f906bf7959062050bbeae5350b0c482; sha256 281bcd61bb8c2fb7929ac474f218adbd004bbca6bc21e5311944a0e590723e1e |
| Project Dictionary 1.3 | GOVERNANCE_EFFECTIVE_BY_SCOPED_RELEASE_RECORD; machine adoption separate | commit b25f7f728de67cf8595bf24f22fcbd79ef50babc; blob 6c8f30e2e6b07f2e65e45c14faab99672d036083; sha256 8a64771916d9e3d447f560658e20b307b5945a5d6b3820ea61cd0298636abe1d |
| Routing 1.4.0 | GOVERNANCE_EFFECTIVE_BY_SCOPED_RELEASE_RECORD | commit bcd008983b61349646a5198ff243069f81484fae; blob 14d2e95e419cc67c3e0cf851cc806a96cf885b7e; sha256 5759b9a8d63ef165ef63c60ecc601198e39296518c5a1eb91db54555ccd07205 |
| Git-first Protocol 12 | RELEASED_UNCHANGED / current for new-re-scoped work | commit f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa; blob d34a022f2bda39a167a404c8530e57b30f337cb9 |

Source verdict: SOURCE_BYTES_VERIFIED for the identities above. Governance human-operating authority is VERIFIED_IN_OWNER_SCOPE by the projectwide release record. Installed/machine enforcement remains NOT_ATTESTED and is not reclassified.

## 2. Bridge semantic/design source resolution
| Source | State | Immutable identity | Role |
|---|---|---|---|
| BRD-09 v0.1 REV3 | CANDIDATE / NO_DEV_GRANT | commit e13820c05ec0c7e97853daa61f6f5fb6b73391cc; blob 99971d65ccb90874e75ace54e6a4f8ec21ba0188 | Product/UX requirements input; not globally promoted |
| Bridge TechSpec v0.7 REV10 | CANDIDATE | commit e13820c05ec0c7e97853daa61f6f5fb6b73391cc; blob 5a82bd74b30f71f7b46652f67a70cd7768f68143 | Existing technical baseline; not globally promoted |
| G1 Design Acceptance | CHAT_ACCEPTED_DESIGN | commit 9c27e7c7104facdb7f083350f38d2451939b6c2a; path docs/architecture/FOX2_BRIDGE_F1_G1_DESIGN_ACCEPTANCE_20261021.md | Task-specific accepted F1 delta over candidate BRD/TechSpec |
| G2 Integrated Build Scope | CANDIDATE / NON_EXECUTABLE | commit 9410edb0d88631c33ffda8494b238ec9f4446dc1; path docs/architecture/FOX2_BRIDGE_F1_G2_INTEGRATED_BUILD_SCOPE_CANDIDATE_20261021.md | Single Whole-WP build envelope |

Binding rule: G2 implementation may not claim BRD-09 or TechSpec v0.7 globally EFFECTIVE. The executable task, if later authorized, must state that G1 acceptance is the task-specific accepted design authority for the F1 delta while preserving candidate/global publication status.

## 3. Task state / no-replay
- Whole-WP remains FOX2-BRIDGE-RC1-TO-INTERNAL-READY; no micro-WP is created.
- G1 is ACCEPTED DESIGN ONLY.
- G2 has no executable task.md, prompt.md or Dispatch.
- Historical Attempt06 remains consumed / RESULT_V2_NOT_DELIVERED / NO_REPLAY.
- Dispatch001 and Canary009 are not rebound or replayed.

## 4. Route decision
Task class: BUILD with security, Windows service identity, IPC authentication, global atomic claim, lease/revocation, replay prevention and process-spawn concurrency.

Preferred executable route IF separately authorized:
- Role: CODEX implementation agent.
- Model: preserve Owner-pinned GPT-6.1 Sol.
- Thinking: HIGH because the material work is security/concurrency/recovery-sensitive.
- Execution path: MANUAL_LOCAL/native CLI in a dedicated non-main G2 worktree; do not use installed Bridge to modify/certify itself.
- Permission profile: Dictionary-resolved coding profile only after real PreExec; main/merge/deploy/provider/broker/LIVE remain forbidden.
- Delivery: Agent pushes exact authorized non-main code/report scope; CHAT remote-readbacks and applies fox2-result-review.

Copilot is not selected as the primary candidate for this integrated F1 scope because the critical path is privileged-service security/concurrency rather than routine isolated editing. WORK is NOT_NEEDED for implementation; independent review may be revisited only at G5 or another explicitly required checkpoint.

ROUTE_STATUS=ROUTE_NOT_VERIFIED. Model/CLI/auth/capacity/worktree capability has not been probed for a G2 executable task.

## 5. Required route-specific PreExec before assignment
PreExec v1.1 must produce a durable task-specific receipt after coding authority exists and before Prompt Builder issues an executable task.

Material checks:
1. exact G2 implementation branch/worktree exists, non-main and clean;
2. unique material writer / no competing writer;
3. exact source head and source-set match this entry plus any later authorized supersession;
4. Codex CLI exists and supports the pinned GPT-6.1 Sol + required High reasoning/permission mode, or returns an honest material capability failure;
5. Codex authentication/capacity is usable for one bounded attempt;
6. Python/PowerShell/Git toolchain required for Bridge source/tests is available;
7. allowed paths and Git push rights are bounded to G2 implementation/result scope;
8. no old Dispatch identity is reused;
9. result schema/template/intake identities are re-resolved from Dictionary 1.3 and bound before issue;
10. executable task/prompt publication remains NOT_RUN until PreExec PASS or a specific Owner override.

## 6. Current Owner coding decision
Preserved exact operational record: OWNER_EXPLICIT_KEEP_GPT_6_1_SOL_HOLD_CODING; exact reply recorded in Feature Status: `Giữ gpt-6.1-sol; HOLD coding`.

`Làm tiếp đi` is applied to CHAT-safe source/routing/preparation work only and is not treated as an implicit repeal of that explicit coding HOLD.

Therefore:
- coding_authority=HOLD;
- PreExec execution probe=NOT_RUN;
- task.md=NOT_PUBLISHED;
- prompt.md=NOT_PUBLISHED;
- Dispatch=NOT_CREATED;
- Agent=NOT_STARTED.

## 7. Entry verdict
STAGE=BUILD
STATUS=BLOCKED
EVIDENCE=G1_ACCEPTED + GOVERNANCE_SOURCE_RESOLVED + SEMANTIC_SOURCE_CLASSIFIED + ROUTE_SELECTED_CANDIDATE
EXIT_GATE=CODING_HOLD_LIFTED_OR_SPECIFIC_OVERRIDE + TASK-SPECIFIC_PREEXEC_PASS + ONE_WRITER + IMMUTABLE TASK/PROMPT READBACK
BLOCKER=OWNER_EXPLICIT_GPT_6_1_SOL_HOLD_CODING
NEXT_SAFE_ACTION=No further executable action. On a later explicit lift/override, run only the G2 task-specific PreExec, then use fox2-agent-prompt-builder to publish one integrated task/prompt and launch at most one authorized attempt.

F1 runtime DENY; G3/G4 NOT_RUN; Canary009 HOLD; INTERNAL_FOX2_BRIDGE_READY NOT_ATTESTED.
