# FOX2 — CHAT Preflight Intake — Package Lifecycle A03 PASS_TO_ASSIGN

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-A03`
Stage: BUILD / TEST-HARNESS CORRECTION
Actor: CODEX
Route: `gpt-6.1-sol / high / FULL_ACCESS / MANUAL_LOCAL`

## Immutable chain

- Product source baseline: `b065a468279cbf63ae4bbfad7a0efaad1e6046e4`.
- Task commit: `ac12501e1b3c94a0e75b72adc7dc78743d18e660`.
- Task blob: `264c1bb54e985d8cd3a73df21072b04271b79d6c`.
- Task SHA-256: `b6bbe42d781939a1b05b1dd2aa3fd985677d970b783ab8c2a30b11e9ada85c7e`.
- Prompt commit: `39d6a8f36dd573a4fb9e61a5d4102a15e9b3a80f`.
- Prompt blob: `23e562253b1d61f413ed6378a218ba903f87d92e`.
- Prompt SHA-256: `25ff86531e9841a9cc8cde6259f0fc9512fe8949c98a57457d689c61bcabce77`.
- PreExec publication head: `52686a5f573dd177341adb72d4feef4cc929a4be`.
- PreExec PASS receipt commit: `e052082afd7279f21611d76669dc8e761c003e79`.
- PreExec receipt blob: `6a08ac2bcd3ca60556f1a0bd7f7ffdc37d5bfa49`.

## Prior attempt boundaries

- A01 implementation Dispatch: consumed safe-stop, no product change, no replay.
- A02 Dispatch001: schema-invalid, not executable, not consumed.
- A02 Dispatch002: schema-valid but immutable-prompt identity mismatch, not executable, not consumed.
- A03 is a fresh assignment identity and is not a replay.

## Remote receipt intake

CHAT independently remote-read A03 receipt and verified:
- status PASS, blockers empty;
- exact A03 task/prompt commit/blob/SHA-256;
- CODEX / gpt-6.1-sol / high / FULL_ACCESS / MANUAL_LOCAL;
- pwsh7/python/git/login/CLI/one-writer/task-prompt/clean-worktree/live-route capabilities PASS;
- live probe PASS, exit 0, exact A03 marker;
- empty temp working directory, read-only sandbox, no project-file access;
- implementation Agent started false;
- Dispatch published false;
- Dispatch consumed false;
- host lifecycle mutation false.

Receipt ancestry:
`52686a5f...` → `e052082a...`, exactly one receipt-only commit.

## Product-baseline / runtime-head separation

`b065a468...` is the merge base / ancestor of `e052082a...`.

CHAT compared `b065a468... → e052082a...` and observed only bounded handoff / PreExec / receipt artifacts. No `agent_bridge/**` product-code path changed before A03 execution.

Executable starting HEAD must be the future schema-valid Dispatch:
`runtime_contract.base_sha=e052082afd7279f21611d76669dc8e761c003e79`.

The immutable A03 prompt intentionally does not hard-code a future Dispatch sequence number.

## Gates

- POLICY_CHECK: PASS
- TASK_STATE_CHECK: PASS
- SOURCE_BINDING_CHECK: PASS
- ROUTING_R0_R7: PASS
- ASSIGNMENT_CHECK: PASS
- MATERIAL_CAPABILITY_CHECK: PASS
- TASK-SPECIFIC_PREEXEC: PASS
- ONE_WRITER: PASS at PreExec observation; launcher must recheck immediately before start
- A01 NO-REPLAY: preserved
- A02 NON-EXECUTABLE identities: preserved

## Verdict

**PASS_TO_ASSIGN**

Next safe action:
1. publish one fresh schema-valid A03 Dispatch with max_runs=1;
2. bind source.commit_sha to product baseline `b065a468...`;
3. bind runtime_contract.base_sha to `e052082a...`;
4. remote-readback and validate Dispatch v3 exactly;
5. Owner launches exactly one CODEX implementation attempt with durable claim;
6. CHAT remote-reviews actual result.
