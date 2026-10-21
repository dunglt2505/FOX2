# FOX2 — CHAT Preflight Intake — Package Lifecycle A01 PASS_TO_ASSIGN

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-A01`
Stage: BUILD / TEST-HARNESS CORRECTION
Actor: CODEX
Route: `gpt-6.1-sol / high / FULL_ACCESS / MANUAL_LOCAL`

## Immutable chain

- Accepted product/source code base: `b065a468279cbf63ae4bbfad7a0efaad1e6046e4`.
- Task commit: `31caeb95ceb6d50644722527252f714a4406ab97`.
- Task blob: `4fa3356f3d6a362a8af8cbc7340288a13a451835`.
- Task SHA-256: `c2270f33db37b39f6296abeac86dd3e572309258918bab5d878454895a034811`.
- Prompt commit: `56f3a8058d5e2083e6190b180ff0181b97e259bb`.
- Prompt blob: `b208ece6eb9bb9fa667b6afd906320b8e1a9882d`.
- Prompt SHA-256: `a26cf973ef4f7e7066f0b48057b7018eafc4d8d8848baf6a33d0c730342c1616`.
- Final PreExec publication head: `d55c0c79349f3f7e1e42cd6f60a942b5934de9e1`.
- Recovered/delivered PreExec PASS receipt commit: `b224f029bc911c0a131342b8ac142fdd4952a96f`.
- Receipt blob: `450dc8cd35f6236beabda51617d06f7896e17770`.

Historical PreExec tooling failures remain preserved and are not relabeled PASS.

## Remote receipt intake

CHAT remote-read the committed receipt and verified:

- status: `PASS`;
- blockers: none;
- task/prompt identities: exact;
- route actor: CODEX;
- model: `gpt-6.1-sol`;
- reasoning: `high`;
- permission profile: `FULL_ACCESS`;
- execution path: `MANUAL_LOCAL`;
- pwsh7/python/git/login/CLI/one-writer/task-prompt/clean-worktree/live-route capabilities: PASS;
- live probe: PASS, exit 0, exact marker `FOX2_PACKAGE_LIFECYCLE_ADMISSION_OK`;
- live probe working directory: empty temp directory;
- live probe sandbox: read-only;
- project files accessed by live probe: false;
- implementation Agent started: false;
- Dispatch published: false;
- Dispatch consumed: false;
- host lifecycle mutation: false.

Receipt delivery recovery normalized CRLF to LF only; canonical JSON semantic SHA-256 was unchanged. The delivered receipt blob was read back remotely.

## Assignment gates

- POLICY_CHECK: **PASS**
- TASK_STATE_CHECK: **PASS**
- SOURCE_BINDING_CHECK: **PASS**
- ROUTING_R0_R7: **PASS**
- ASSIGNMENT_CHECK: **PASS**
- MATERIAL_CAPABILITY_CHECK: **PASS**
- TASK-SPECIFIC_PREEXEC: **PASS**
- ONE_WRITER: **PASS at PreExec observation; launcher must recheck immediately before Agent start**

## Scope

Authorized coding scope is the immutable A01 task only:
- fix lifecycle certification to invoke stable external `uninstall.ps1`;
- retain bounded sanitized exit/stdout/stderr evidence;
- add regression coverage;
- preserve product self-delete fail-closed guard;
- run offline/unit/full Bridge tests and Result Contract delivery.

Forbidden:
- real install/update/uninstall/reinstall on Owner host during coding task;
- AppLocker/AppIDSvc/service/ACL mutation;
- G3/G4/Canary/main/PR/merge/provider/broker/LIVE.

## Verdict

**PASS_TO_ASSIGN**

Next safe action:
1. publish one fresh Dispatch v3 on `work/FOX2-DISPATCH-chat`;
2. bind source code base `b065a468…`, runtime task branch head `b224f029…`, exact task/prompt and PASS receipt;
3. remote-readback Dispatch identity;
4. Owner launches exactly one CODEX implementation attempt through complete PowerShell 7 launcher with durable no-replay claim;
5. CHAT performs immutable result review.
