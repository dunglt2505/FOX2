# FOX2 — CHAT Preflight Intake — Package Lifecycle A02 PASS_TO_ASSIGN

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-A02`
Stage: BUILD / TEST-HARNESS CORRECTION
Actor: CODEX
Route: `gpt-6.1-sol / high / FULL_ACCESS / MANUAL_LOCAL`

## Immutable chain

- Product source baseline: `b065a468279cbf63ae4bbfad7a0efaad1e6046e4`.
- Task commit: `fc03d7b130f0d987c94ecd6bb636ca482d9f637e`.
- Task blob: `4fc6c4eb80cf362ea2b9e4fc2082cc8f2e5e68dc`.
- Task SHA-256: `3e9aca6b43485f9dcecf3ee72749e8c8c1b8ae4c4e31ef41eff5df5306acf4fd`.
- Prompt commit: `3321d69a998e3279782476c9d52f7224095fb2d8`.
- Prompt blob: `23c821c9c27d2e46855539a1b2314b48a1abd1d2`.
- Prompt SHA-256: `3271f23f8eecc308899fb5f2200d3bb274562eefaf5d13d9d49248767b089852`.
- PreExec publication head: `a9a7a327cd293c0450a073f92c98e3c7d09d3bff`.
- PreExec PASS receipt commit: `036de99a6d649bfcf9a427aa914809a9d53592c3`.
- PreExec receipt blob: `ce4cd89b718a44ff2398e33aa1872df4009f3dce`.

A01 remains permanently consumed and is not part of A02 execution.

## Remote receipt intake

CHAT independently remote-read the committed receipt and verified:

- `status=PASS`;
- no blockers;
- exact A02 task/prompt identities;
- route actor CODEX;
- model `gpt-6.1-sol`;
- reasoning `high`;
- permission profile `FULL_ACCESS`;
- execution path `MANUAL_LOCAL`;
- pwsh7/python/git/login/CLI/one-writer/task-prompt/clean-worktree/live-route capabilities all PASS;
- live probe PASS, exit 0, exact marker `FOX2_PACKAGE_LIFECYCLE_A02_ADMISSION_OK`;
- live probe ran in empty temp directory, read-only, no project files accessed;
- implementation Agent started false;
- Dispatch published false;
- Dispatch consumed false;
- host lifecycle mutation false.

Receipt commit ancestry was independently verified:
`a9a7a327...` → `036de99a...`, exactly one commit adding only the A02 receipt.

## Corrected execution identity

A02 explicitly separates:
- `PRODUCT_SOURCE_BASE=b065a468...`;
- `EXECUTION_START_HEAD=fresh Dispatch.runtime_contract.base_sha`.

The executable Dispatch must bind:
`runtime_contract.base_sha=036de99a6d649bfcf9a427aa914809a9d53592c3`.

The Agent must NOT require current HEAD to equal the older product baseline.

## Gates

- POLICY_CHECK: **PASS**
- TASK_STATE_CHECK: **PASS**
- SOURCE_BINDING_CHECK: **PASS**
- ROUTING_R0_R7: **PASS**
- ASSIGNMENT_CHECK: **PASS**
- MATERIAL_CAPABILITY_CHECK: **PASS**
- TASK-SPECIFIC_PREEXEC: **PASS**
- ONE_WRITER: **PASS at PreExec observation; launcher must recheck immediately before Agent start**
- A01 NO-REPLAY: **PASS / preserved**

## Verdict

**PASS_TO_ASSIGN**

Next safe action:
1. publish one fresh A02 Dispatch with max_runs=1;
2. bind runtime base `036de99a...`, product source baseline `b065a468...`, exact A02 task/prompt and PASS receipt;
3. remote-readback Dispatch identity;
4. Owner launches exactly one CODEX implementation attempt with durable no-replay claim;
5. CHAT reviews actual Git result via `fox2-result-review`.
