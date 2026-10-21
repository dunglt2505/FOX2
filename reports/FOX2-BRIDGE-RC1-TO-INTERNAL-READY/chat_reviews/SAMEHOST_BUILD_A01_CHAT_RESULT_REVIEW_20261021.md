# FOX2 — CHAT Result Review — Same-Host BUILD A01

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-SAMEHOST-BUILD-A01`
Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-SAMEHOST-BUILD-A01-CODEX-001`
Reviewer: CHAT
Skill: `fox2-result-review` + `fox2-feature-certification`

## Immutable execution chain

- Task/prompt source lock: `600f8ceb6943d1f1ecf341ff06072bf31c1babe0`.
- Metadata PreExec PASS: `f60ab169baaf8c3e0f644adbf850021cea9ebf7d`.
- Live route admission PASS evidence: `0962ec74617613ff01a629926e64b7ae8b122979`.
- CHAT PASS_TO_ASSIGN: `2c7c233d4afeda5462241f4126a16f075840157e`.
- Executable Dispatch: `7efb5d98d8b51a26c8e3de1a0b808a0f48b3885c`, blob `b7461f9273d5a1e0a6cdbc38e787070bdd650e8e`, max_runs=1.
- Durable local claim was created once; initial launcher stopped before Agent start, then CHAT reconciled `CLAIMED_NOT_STARTED`, clean worktree, unchanged remote, exact prompt temp and zero task-scoped CODEX processes.
- Same attempt resumed without new claim/Dispatch/PreExec. CODEX exited 0, worktree clean and remote result read back.
- Entry/result diff base: `0962ec74617613ff01a629926e64b7ae8b122979`.
- Implementation commit: `be883bb8106ca1c058b2b34765e55c2529fe883f`, direct child of entry base.
- Result/evidence commit: `b065a468279cbf63ae4bbfad7a0efaad1e6046e4`, direct child of implementation commit.
- Remote task branch readback equals result commit.

No replay occurred. Dispatch is consumed exactly once.

## Scope / diff / K1

Implementation commit changes exactly five product/test files:
- `agent_bridge/scripts/f1_policy_artifact.py`
- `agent_bridge/src/fox2_agent_bridge/f1_policy.py`
- `agent_bridge/src/fox2_agent_bridge/f1_service.py`
- `agent_bridge/tests/test_f1_host_fence.py`
- `agent_bridge/tests/test_f1_policy.py`

Result commit adds bounded `evidence/samehost/**` material and updates the required report/manifest. No governance/BRD/TechSpec/global-roadmap/main/release path is touched.

K1 remote readback:
- REQUESTED: 6 paths;
- NECESSARY_DEPENDENCY: 2 paths;
- JUSTIFIED_GENERATED: 10 paths;
- UNEXPLAINED: 0.

All paths are within the immutable task allowlist.

## Independent evidence integrity

CHAT remote-read the Result Contract files and all manifest-referenced same-host evidence. SHA-256 was independently recomputed from the GitHub-readback UTF-8/LF content:
- 11 evidence files checked;
- 11/11 match the committed manifest SHA-256;
- mismatches: 0.

`delivery_checks.json` reports Result Schema v2, evidence hashes, changed hashes, K1, source blobs, diff check, bounded secret scan and allowlist PASS. CHAT separately verified ancestry, changed paths, task/prompt/admission identities and evidence bytes rather than treating that self-check as acceptance.

## Security / contract review

The same-host rework implements the accepted contract:

1. **Composite policy**
   - requires an explicit reviewed baseline;
   - supports exact hash, exact publisher and restricted Windows/SystemApps/Program Files path rules;
   - rejects broad/user-writable/ambiguous paths, unsupported XML/rule shapes, duplicate IDs and baseline rules that conflict with explicit F1 denies.

2. **Collection semantics**
   - Exe and Script are mandatory `Enabled` in the final positive contract;
   - Msi/Dll default to `NotConfigured` and require explicit reviewed mode preservation;
   - package DLL/MSI presence no longer silently forces enforcement.

3. **Dual identities**
   - `effective_policy_digest` binds the complete expected effective policy;
   - `f1_control_digest` binds a sealed deterministic F1 rule selector including principals/actions/hashes, modes and relied-on extensions.

4. **HostFence**
   - positive authority denies on full effective-policy drift;
   - positive authority independently denies on F1-control drift;
   - missing legacy single-digest fields or malformed selector/XML fail closed as `POLICY_CONTRACT`.

5. **Audit/rollback source support**
   - transition artifacts bind pre-enforcement local/effective snapshots, audit XML, final identities and rollback artifact identity;
   - artifacts explicitly carry `NOT_RUN_G3`, `host_mutation=false`, `adoption_authority=false`;
   - no AppLocker/AppIDSvc/service/ProgramData ACL mutation path was executed.

No BUILD-blocking security contradiction was found. Physical path DACL/reparse-point compatibility and actual AppLocker enforcement remain G3 responsibilities.

## Test chronology

Historical failures are preserved:
- focused-01: FAIL, 2 failed / 136 passed — denial-reason handling defect;
- assembly-01: FAIL — evidence enumeration/CRLF/code-page assembly defects.

Those failures were corrected within the same single Agent attempt; they are not relabeled PASS.

Final evidence:
- focused same-host/F1: **142 PASS**;
- full `agent_bridge/tests`: **606 PASS**;
- static/package source contract: **PASS** — 3 PowerShell scripts parsed, 40 wheel source modules checked;
- final delivery checks: **PASS**;
- secret scan / changed-path allowlist / diff check: **PASS**.

Required boundaries remain:
- physical G3 enforcement/compatibility/rollback: **NOT_RUN**;
- G4 installed adoption: **NOT_RUN**;
- complete release-package build: **NOT_RUN**.

## Acceptance matrix

All immutable task acceptance items 1–15 are satisfied for BUILD scope:
- safe baseline parser/canonicalizer;
- broad user-writable rejection;
- deterministic F1/effective digests;
- baseline/full-digest and F1/subset drift behavior;
- mandatory Exe/Script;
- conditional Msi/Dll;
- no BUILD host mutation;
- preserved protected-root/runtime/source/package/no-replay regressions;
- focused/full tests;
- allowlist/secret/diff checks;
- Result Contract publication;
- historical evidence preservation.

## CHAT verdict

**CHAT_ACCEPT — SAME-HOST BUILD ONLY**

Accepted:
- same-host implementation commit `be883bb8106ca1c058b2b34765e55c2529fe883f`;
- result/evidence commit `b065a468279cbf63ae4bbfad7a0efaad1e6046e4`;
- BUILD exit sufficient to proceed to current package lifecycle/rollback closure.

Not accepted / not authorized:
- physical G3 AppLocker/service enforcement;
- installed F1 positive authority;
- G4 adoption;
- complete release package;
- old Canary009 replay or current Canary acceptance;
- main/merge/provider/broker/LIVE;
- `INTERNAL_FOX2_BRIDGE_READY`.

Runtime remains **F1 positive authority DENY / RUNTIME_ENFORCED NOT_ATTESTED / INTERNAL_FOX2_BRIDGE_READY NOT_ATTESTED**.

NEXT_SAFE_ACTION: Phase 2 current package lifecycle and rollback analysis. Reconcile the historical Batch-B uninstall failure against the current accepted same-host source; preserve the old FAIL. If a current code defect is proven, issue one new Git-first bounded correction task. Otherwise run a fresh current-package lifecycle certification before any physical-host G3 enforcement.
