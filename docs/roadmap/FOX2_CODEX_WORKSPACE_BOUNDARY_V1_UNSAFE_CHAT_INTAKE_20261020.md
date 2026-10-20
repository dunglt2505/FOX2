# FOX2 — CODEX Windows unelevated workspace boundary UNSAFE (Owner V1 test)

**Observed UTC:** `2026-10-20T16:35:23.4240514Z`. **Scope:** existing Whole-WP `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`; `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION` BUILD/BLOCKED. **Mode:** CHAT read-only intake and governed non-main status update. **Source:** Owner-pasted JSON `FOX2_CODEX_WORKSPACE_BOUNDARY_V1`. No actual host operations by CHAT.

## Observed scoped facts

Owner's test used `codex-cli 0.162.1`, command mode `windows.sandbox="unelevated"` with `sandbox_mode="workspace-write"` in a disposable non-FOX2 workspace and a separate outside-workspace fixture. Model-free direct CODEX sandbox commands were run. The JSON reported:

```json
{
  "mode": "MODEL_FREE_TEMPORARY_UNELEVATED",
  "inside_exit": 0,
  "inside_write_pass": true,
  "outside_exit": 0,
  "outside_write_created": true,
  "outside_write_denied": false,
  "cleanup": "COMPLETE",
  "verdict": "UNSAFE_OUTSIDE_WRITE_ALLOWED",
  "agent_workspace_write": "NOT_YET_ATTESTED",
  "coding_authorization": "NOT_GRANTED",
  "attempt001": "CONSUMED_NO_REPLAY",
  "installed_bridge": "UNTOUCHED"
}
```

**Review disposition:** `ACCEPT_NEGATIVE_BOUNDARY_EVIDENCE` for the tested direct sandbox route; **`NO_GO_CODEX_UNELEVATED_WORKSPACE_WRITE` for FOX2 source editing on this host**. The outside fixture was writable, so no assertion that this invocation confines writes to its worktree is acceptable. An outside path under the user's local-app-data could be treated specially by an implementation; even if so, it is outside this task's allowed code scope. This one experiment does not prove that all Codex sandbox modes or other host isolation mechanisms are unsafe. Cleanup reported COMPLETE and is not positive sandbox evidence.

Prior read-only shell smoke with the same unelevated mode was `PASS_NEUTRAL_FUNCTIONAL_EXECUTION`; this is not the same as source-write confinement. The default read-only sandbox had failed CODEX exec setup (`helper_unknown_error: setup refresh had errors`); the underlying Windows sandbox helper repair remains unresolved. **Do not bypass that by using an unverified weaker mode for the production FOX2 source worktree.**

## Decision and one integrated recovery route

1. **Stop repeated unelevated local write probes and do not use `danger-full-access` or an implicit `full-access` bypass.** Do not change global Codex config or blanket ACLs; do not kill other Codex/VS Code processes merely to overcome the bug. Version `0.162.1` is not itself a release gate and has already passed a neutral shell smoke.
2. To resume code work, prefer a **real isolation boundary outside the Windows host's original sensitive files** — e.g., an independently provisioned and **verified** disposable VM or container/WSL2 environment, with an isolated Git worktree and only explicit source/result export, or restore a working elevated sandbox with verified workspace write-denial semantics. Neither environment capability nor workspace scope is verified by this record. A fallback coding Actor/host may be selected only after genuine route permissions/model/PreExec, never by assuming Copilot/workstation safe or disabling sandbox.
3. Verify a **new isolated host/source write boundary** (inside allowed source/test fixture succeeds, attempted write to dedicated outside guard fails, no unexpected files, one-writer, no installed Bridge/data available) and CODEX pinned model `gpt-6.1-sol`/medium behavior before one fresh CODEX coding attempt. No new Agent task until actual host capability and scope are proven; future formal assignment uses `fox2-agent-prompt-builder` and a fresh immutable Git task/prompt/result contract, not a replay or a rebind of Attempt-001.
4. Preserve already certified F0 offline source and all consumed task/result identities. Installed Bridge pre-F0 module identity, legacy retirement/one-writer, F1 implementation and Canary remain HOLD. No operations on installed worker, local ledger, `main`, dispatch, provider, broker or LIVE.

**Required/Applied Skills:** `fox2-governance-preflight`, `fox2-agent-route-runtime`, `fox2-execution-recovery`, `fox2-source-resolver`, `fox2-status-roadmap`, `fox2-feature-certification`, `fox2-document-publication`. `fox2-agent-prompt-builder` READ / NOT_APPLICABLE to passive failed-gate intake (REQUIRED for new Agent task). **Policy:** Owner Registry blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`, human Policy v2.0.0/Dictionary v1.3, installed enforcement NOT_ATTESTED; `TASK_STATE_CHECK=ATTEMPT001_CLOSED_CONSUMED`, `SOURCE_RESOLUTION=PRIOR_F0_ACCEPTED_PLUS_OWNER_NEGATIVE_HOST_PROBE`, `ROUTING_R0-R7=CHAT_DOC_ONLY`, `ASSIGNMENT_CHECK=NOT_APPLICABLE`.

**NEXT_SAFE_ACTION:** identify an actually available, isolated code execution host or repair an enforceable elevated sandbox; do not re-run the same unsafe mode. If none exists, leave coding BLOCKED instead of repeating ineffective diagnostics.
