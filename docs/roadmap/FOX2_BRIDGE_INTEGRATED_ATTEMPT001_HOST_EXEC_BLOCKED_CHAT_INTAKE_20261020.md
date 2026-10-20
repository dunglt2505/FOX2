# FOX2 — CHAT intake of integrated Attempt-001 Windows CODEX host-exec failure

**Date observed:** 2026-10-20T15:48:39.857046Z. **Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`. **Opened feature:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION` (BUILD/BLOCKED). **Source/task:** integrated Attempt-001 `work/FOX2-BRIDGE-RC1-INTEGRATED-RECOVERY-20261020`, published prompt HEAD `b50dc1ec1ddce4e2f3b772e0244b64338c172663`, task blob `d4a46a8568a53716ff9758d6a1d45624881a0168`, prompt blob `82c7283a6bc3b875f9d201c279a4a7521e515944`, prompt SHA256 `91e799d7dbe9e482768bf7edb74dc7205f2a9e77bca8bd90cbeee8bdd323a473`.

## Actual Owner-reported terminal output, scoped independent conclusion

The Owner ran the corrected PowerShell 7 CODEX launcher after the earlier false-positive `Get-Process codex` global check had been removed. The launcher proceeded to Stage 3, **created an attempt-used marker before invoking CODEX** and invoked the pinned CODEX CLI for Attempt-001. CODEX returned a shell tool failure at its first actual command: `Failed to create unified exec process: helper_unknown_error: setup refresh had errors`, with `exit -1` for the attempted read of two FOX2 Skills. This demonstrates failure at CODEX's Windows unified-exec/sandbox bootstrap before a source/test/process command, **not** failure of Bridge application logic.

CODEX self-reported only local sanitized failure files:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`, local reported SHA256 `66316ac94afe5187bd7051f2bbfed61b29bff41ff8abaa353835eddc09229cb8`.
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`, local reported SHA256 `ed02675173c6cfe07cf5beb5f79212119f99258052790c6c70691758c9e75346`.
- The manifest was reported to contain a sanitized failure receipt hash. **Actual file bytes not yet independently remote-read; these hashes are Agent self-report, not CHAT-certified.**

The Owner's resulting script reported `FOX2_BRIDGE_INTEGRATED_RECOVERY_EXECUTION_V2`, `codex_exit_code=0`, `git_initial_sha=git_local_result_sha=git_remote_result_sha=b50dc1ec1ddce4e2f3b772e0244b64338c172663`, `report_file_exists=true`, `manifest_file_exists=true`, `worktree_has_uncommitted_changes=true`, `result_delivery=LOCAL_RESULT_NEEDS_RECONCILIATION`, `attempt_replay=PROHIBITED`, `chat_acceptance=PENDING`, `installed_adoption=NOT_RUN`, `canary=HOLD`. The CLI process exit code ZERO does **not** mean BUILD/TEST succeeded, since its own narrative states blocked before code mutation.

CHAT direct GitHub readback on 2026-10-20: branch HEAD still `b50dc1ec1ddce4e2f3b772e0244b64338c172663`; task/prompt bytes unchanged; both report and manifest **absent on remote**. No claim is made about all local filesystem state beyond Owner console output. Implementation/tests/packaging/remote results `NOT_RUN/NOT_DELIVERED`; installed Bridge/Canary `HOLD`.

## Safety and recovery verdict

- `ATTEMPT001=CONSUMED_AT_CODEX_INVOCATION`. No rerun of same attempt even though code execution did not start. Do not erase `*.started` marker or change the attempt identity to replay.
- `ACTUAL_ROOT_CAUSE=WINDOWS_CODEX_SANDBOX_SETUP_FAILURE_CLASS`, internal subcause `UNVERIFIED` pending read-only sandbox log (`$HOME/.codex/.sandbox/setup_error.json`, relevant `sandbox*.log`). Similar `helper_unknown_error` reports exist upstream but are **not** a diagnosis of this host.
- `RESULT_DELIVERY=LOCAL_RESULT_NEEDS_RECONCILIATION`. **Immediate next safe action** is **report-only existing local artifact delivery** (report, manifest, sanitized receipt under the exact existing WP report subtree) with strict SHA and Git source/branch/no-scope-change checks. This is completion of *result delivery*, **not** Agent replay or a new attempt.
- After actual Git commit/push/readback, CHAT reviews file contents, evidence manifest, hashes and diff and records `HOLD_TOOLING_BOOTSTRAP` outcome. No code/test improvement claimed.
- Subsequent new CODEX coding attempt **requires fresh identity, fresh source-bound task/prompt, route-specific confirmed Windows sandbox-exec repair and preflight**. A common cause of this error in public upstream issues is sandbox helper setup/permissions/sharing; no OS ACL changes, reset, reinstall or CODEX process termination are authorized by this receipt.
- Preserve Owner standing directive to finish Bridge as the Whole-WP. No splitting into micro-WP. Do not grant positive claim, startup/worker changes, Canary, release, broker/provider/LIVE.

## Governance and skill disposition

Scoped Owner governance: Registry blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`, human Policy v2.0.0, Dictionary v1.3; installed enforcement NOT_ATTESTED. `POLICY_CHECK=SCOPED_OWNER_GOAL` → `TASK_STATE_CHECK=ATTEMPT001_CONSUMED` → `SOURCE_RESOLUTION=F0_611EC26_AND_PROMPT_b50dc1` → `ROUTING_R0_R7=CHAT_DIRECT_READONLY_AGENT_RESULT_INTAKE_GIT_ONLY` → `ASSIGNMENT_CHECK=NOT_APPLICABLE` (no new Agent). Applied read Skills: `fox2-result-review`, `fox2-execution-recovery`, `fox2-governance-preflight`, `fox2-agent-route-runtime`, `fox2-source-resolver`, `fox2-status-roadmap`, `fox2-feature-certification`, `fox2-document-publication`. No full Agent Result v2 acceptance without remote files. **STOP:** no retry, host ACL repair, installed mutation, task replay, main merge, Canary or LIVE.
