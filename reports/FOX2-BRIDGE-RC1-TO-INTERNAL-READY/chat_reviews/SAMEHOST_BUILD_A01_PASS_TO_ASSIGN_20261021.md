# FOX2 — CHAT Preflight Intake — Same-Host BUILD A01 PASS_TO_ASSIGN

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-SAMEHOST-BUILD-A01`
Stage: BUILD
Action class: AGENT_EXECUTION admission only

## Source / task lock

- Governance Registry release branch head observed: `d34da1e3b4918a902646621b487ca8ad3e05b0e0`.
- Policy 2.0.0: `96175ac4f39197794a04e695f0046fa7ef9321fe`, SHA-256 `281bcd61bb8c2fb7929ac474f218adbd004bbca6bc21e5311944a0e590723e1e`.
- Dictionary 1.3: `b25f7f728de67cf8595bf24f22fcbd79ef50babc`, SHA-256 `8a64771916d9e3d447f560658e20b307b5945a5d6b3820ea61cd0298636abe1d`.
- Git-first Protocol 12: `f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa`.
- Dispatch Schema v3 current release compatibility accepts versioned Dictionary paths; release manifest records compatibility source `759d0e324838c7d34a1d74f7b5aa1fb2d5696470` and hosted migration compatibility PASS.
- Immutable task/prompt source lock: `600f8ceb6943d1f1ecf341ff06072bf31c1babe0`.
- Task path: `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/samehost/task.md`.
- Task raw SHA-256: `71c4e1c0401c429878fabb95859f64c568c43dbe02f2ffab7b8c0de41b0837fa`.
- Prompt path: `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/samehost/prompt.md`.
- Prompt blob SHA-1: `f9a60988fd5e13158cd898492910e92dfbbed253`.
- Prompt raw SHA-256: `2b67241b343989b2da6dd17c6927fc5ace6c75678f28efbfa4934e717875f5d9`.

## PreExec evidence

Metadata PreExec:
- receipt commit `f60ab169baaf8c3e0f644adbf850021cea9ebf7d`;
- receipt blob `340ea3401d8ea94b86ae85bd8f067d17ddb44bb8`;
- CHAT verdict: metadata PASS only.

Live pinned-route admission:
- recovered/delivered commit `0962ec74617613ff01a629926e64b7ae8b122979`;
- evidence blob `2c24f03f7a970692178d220f7a15455288b838b0`;
- evidence type `FOX2_CODEX_LIVE_ADMISSION_PROBE`;
- status `PASS`;
- model `gpt-6.1-sol`;
- reasoning `high`;
- sandbox `read-only`;
- probe exit `0`;
- marker `FOX2_ADMISSION_OK` matched;
- temp working directory only;
- project files accessed by probe: false;
- task Agent execution started: false;
- Dispatch consumed: false;
- host policy mutation: false.

The raw CRLF local artifact was normalized to LF before delivery; canonical JSON semantic SHA-256 was unchanged. The delivered remote evidence was independently read back by CHAT.

## R0–R7 / assignment gates

- POLICY_CHECK: **PASS**
- TASK_STATE_CHECK: **PASS** — A01 implementation not started/consumed.
- SOURCE_BINDING_CHECK: **PASS**
- ROUTING_R0_R7: **PASS**
- ASSIGNMENT_CHECK: **PASS**
- MATERIAL_CAPABILITY_CHECK: **PASS** — pinned CODEX route live-probed successfully.
- One writer / dedicated worktree: **PASS** at PreExec/admission observation; launcher must recheck immediately before start.
- Role: CODEX primary implementation.
- Model: `gpt-6.1-sol`.
- Thinking: `high`.
- Permission profile: `FULL_ACCESS` within task allowlist only.
- Execution path: `MANUAL_LOCAL`.
- Delivery owner: `AGENT`.
- Max implementation runs: 1.

## Owner / scope authorization basis

This is continuation of the already-issued Whole-WP A01 same-host BUILD task under the Owner-directed FOX2 continuation and physical-host-only target decision recorded at `438169d5728a4b5b5da19b737e79db3fc6515ce0`. The immutable task itself contains the bounded FULL_ACCESS code/build/test permission and explicit forbidden host/release actions. This intake does not expand that scope.

No main/PR/merge/deploy/provider/broker/LIVE authority is granted.

## Verdict

**PASS_TO_ASSIGN**

Protocol v12 still requires a fresh executable Dispatch publication after this verdict and before implementation Agent start.

NEXT_SAFE_ACTION:
1. publish one new Dispatch v3 on `work/FOX2-DISPATCH-chat`;
2. bind Dictionary 1.3, Policy 2.0.0, immutable task/prompt, current task branch base/evidence, CODEX `gpt-6.1-sol/high/FULL_ACCESS`, MANUAL_LOCAL, one run;
3. remote-readback exact Dispatch commit/blob;
4. only then provide Owner-visible PowerShell 7 launcher for one CODEX implementation attempt.

Historical Dispatches and G2/G3/Canary attempts remain immutable and are not replayed.
