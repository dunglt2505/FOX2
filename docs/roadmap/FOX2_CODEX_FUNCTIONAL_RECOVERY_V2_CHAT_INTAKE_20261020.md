# FOX2 — CODEX Windows functional recovery V2: actual shell PASS, write-scope UNKNOWN

**Observation:** Owner-host PowerShell 7 output `FOX2_CODEX_FUNCTIONAL_RECOVERY_V2` at `2026-10-20T16:28:42.6971614Z` (2026-10-20 23:28 ICT). **Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`, feature `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION` BUILD/BLOCKED. **Mode:** CHAT direct read-only intake and non-main Git report; no Agent assignment or host file mutation from CHAT.

## Evidence accepted in exact scope

Owner supplied a neutral disposable host test with `codex-cli 0.162.1` using **per-command** `windows.sandbox="unelevated"`, pinned model `gpt-6.1-sol` / medium, and an Agent shell invocation. Snapshot:

```json
{
  "direct_sandbox_exit": 0,
  "direct_sandbox_error": false,
  "direct_sandbox_pass": true,
  "agent_cli_exit": 0,
  "agent_command_events": 1,
  "agent_successful_events": 1,
  "marker_observed": true,
  "turn_completed": true,
  "setup_failure_detected": false,
  "scratch_files_created": 0,
  "functional_verdict": "PASS_NEUTRAL_FUNCTIONAL_EXECUTION",
  "coding_permission": "NOT_GRANTED_BY_SMOKE",
  "attempt001": "CONSUMED_NO_REPLAY",
  "bridge_runtime": "UNTOUCHED",
  "canary": "HOLD"
}
```

**CHAT verdict:** `PASS_OWNER_REPORTED_NEUTRAL_SHELL_EXECUTION_IN_UNELEVATED_READ_ONLY_MODE`. This overturns the earlier narrower `SHELL_BOOTSTRAP_BLOCKED` status **only for this tested sandbox mode and this harmless operation**; it does not retroactively change Attempt-001, whose sandbox setup failed and BLOCKED report was already delivered/accepted. Current CLI version is not a release gate; Owner explicitly requested functional-first.

**What is not proven:** (i) actual effective `workspace-write` policy, (ii) ability to write inside one allowed workspace, (iii) denial of writes outside that workspace (especially with temp special writable roots), (iv) installed Bridge Worker source/authority, (v) CLI sandbox invariance on repeat or when CODEX modifies a real source tree, (vi) pinned Codex model running privileged engineering task with route-specific permissions. **CODEX coding remains not authorized by this neutral smoke alone.**

## Next safe action and decision

1. Perform **one scoped, disposable, bounded** write-permission experiment in a purpose-created isolated work directory, with independently created sibling/guard fixtures outside the work directory, **never** target FOX2, installed Bridge, actual Git credentials/config, or live SQLite. Test `workspace-write` actual write inside and rejection outside; independently inspect and clean up only the exact created fixture files. A weaker sandbox or an LLM simply reporting `sandbox enforced` is not an acceptable proof.
2. Explicit verdict:
   - `PASS_ISOLATED_WORKSPACE_BOUNDARY` only when actual inside write succeeds, outside write fails and no other unexpected files or actions occur.
   - `UNSAFE_OUTSIDE_WRITE_ALLOWED` if an outside dedicated fixture is writable, even if inside write succeeds. No source coding in this mode.
   - `BLOCKED_WORKSPACE_WRITE` when inside write fails. Resolve capability without escalating to full access.
   - `UNKNOWN` for ambiguous tool results or lack of independent OS-file evidence. No source coding.
3. If boundary fails, prefer a secure alternative route, isolated host/Windows capability or correctly enforced elevated sandbox; do **not** silently disable sandbox, loosen machine ACL, change global Codex config, or merge bypass into existing F0 code.
4. After boundary **plus** source/task/model/one-writer/permissions/quota/PreExec verified, use `fox2-agent-prompt-builder` to issue one fresh immutable **new** integrated BUILD attempt. No replay of consumed Attempt-001, whose result SHA remains `947cf9a33585a286a2447aa27c35328b146b2fbd`.
5. Existing Bridge F0 offline accepted is not installed source attestation; F1 source/build/Windows durable legacy retirement/one-writer/Canary all HOLD.

**Public ecosystem caveat:** `openai/codex` issues `#32855`, `#34961` and `#27889` contain examples of Windows `unelevated` functioning for shell but write-scope or effective policy remaining uncertain. They are not host-specific proof. Owner's instruction supersedes any hard `CLI >=0.163.0` gate.

**Governance:** Registry `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`, human Policy v2.0.0 / Dictionary v1.3 scope, installed effectivity NOT_ATTESTED. `POLICY_CHECK`, `TASK_STATE_CHECK`, `SOURCE_RESOLUTION`, `R0–R7` completed for CHAT read-only intake/non-main status; `ASSIGNMENT_CHECK=NOT_APPLICABLE`. Applied actual Skills: `fox2-agent-route-runtime`, `fox2-governance-preflight`, `fox2-execution-recovery`, `fox2-result-review`, `fox2-status-roadmap`, `fox2-source-resolver`, `fox2-document-publication`; Prompt Builder READ/NOT_APPLICABLE to this passive review (required later for new Agent assignment). No host action performed in Git result review.
