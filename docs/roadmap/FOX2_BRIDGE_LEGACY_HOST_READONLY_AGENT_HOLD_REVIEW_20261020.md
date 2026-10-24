# FOX2 — CHAT Result Review: Legacy Lifecycle Host Read-Only Attempt (2026-10-20)

**Verdict:** `CHAT_HOLD / INVENTORY_NOT_RUN / RESULT_NOT_DELIVERED / HOST_MARKER_NEEDS_RECONCILIATION / NO_REPLAY`. No manual-local BUILD acceptance, host evidence, retirement/fencing attestation or installed runtime permission.
**Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`. **Existing WP:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`. This is the returned result for the existing read-only inventory assignment, **not a new task**.

## Immutable originals

- Task `45a50c6cdca27faaf3e24f71abd7b032214178ec:docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/HOST_LEGACY_LIFECYCLE_READONLY_20261020/task.md`, blob `b093b7b01c6e97cd221781fb5d4e91c61baac78f`, SHA-256 `8af4e53145b64765b1a1225ab7606b9785284f7ffafaec1b4e07850bc85283fd`.
- Prompt `a0122041ba594ee59b6069cfcb26f035f9eb62a9:.../prompt.md`, blob `50f8b1894e5a337cb413acb77d6d2206526d842a`, SHA-256 `0232d5804ec0da12157b98c2e25cdda79643159d0dff27213c1470b9ce2191d3`.
- Conditional prospective CHAT admission `b9f273f1c71b59f20f543680a0b196caab130422:.../chat_conditional_admission.json`, blob `0c5d491026c94352474b0e43a494c83ae8a802c3`, SHA-256 `a880b67290b00ac38f69a6e9afeea325fa86fc3251aab586861f0ff5b7b9fd37`. Admission status `HOST_PREFLIGHT_REQUIRED_BEFORE_AGENT`, not a live host writer certificate.
- Dedicated result branch `work/FOX2-BRIDGE-LEGACY-LIFECYCLE-READONLY-RESULT-20261020` remains at initial `3167d8502588dd106f9a4cea8ef931e9148040ff`, independently fetched on CHAT intake. Both expected report paths `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md` and `evidence_manifest.json` are **ABSENT**. No remote result commit beyond original start source, no diff/tests/secret-scan evidence to accept.

## Return and failure classification

Owner supplied actual CODEX terminal result `HOLD — inventory NOT_RUN`; CODEX checked task/prompt, read-only Git source and conditional admission, then stopped before host inspection because the atomic one-shot marker reservation could not be independently verified from its supplied preflight payload. CODEX reported no writes in **its own worktree**, no commit/push and no installed Bridge runtime mutation. `CODEX_EXIT_CODE=0` denotes CLI process exit, not acceptance.

The prior CHAT-authored PowerShell launcher puts an on-disk one-shot `FileMode.CreateNew` marker before the actual CODEX CLI invocation, then supplies only generic text `fresh one-shot marker reserved`, **not** an exact trusted readback of the marker's content/path/record SHA to the Agent. Thus the successful CODEX invocation is consistent with marker creation, but CHAT has **not independently observed local marker bytes**. `HOST_AUDIT_MARKER` path in terminal output is a string/pointer, not a readback. The launcher wrote or reserved a durable marker before invoking CODEX under normal control flow; exact current host state remains `NOT_VERIFIED`. Preserve the marker and last-message; never delete, reuse or silently mark its state PASS. Agent STOP was consistent with fail-closed instructions.

This is an **assignment/orchestration evidence bug** rather than proof of a retired legacy launcher or a source conflict. The earlier inability to prove durable cross-root no-replay remains unresolved. No raw host inventory evidence was produced.

## CHAT review decision and NEXT_SAFE_ACTION

- `CHAT_HOLD` for Agent result delivery and task goal. `NO_REPLAY_STOP` for the just-consumed/possibly reserved one-shot host audit identity. Historical coding Attempts01–03 remain consumed and protected.
- **First perform NEW host-only READ-ONLY reconciliation, without invoking any Agent:** exact file presence/byte validity of `%LOCALAPPDATA%\FOX2\NativeOfflineClaims\FOX2-LEGACY-LIFECYCLE-READONLY-20261020.json`, JSON schema/task identity/source SHA/creation timestamp/expected owner-readable marker, last-message presence and metadata, current repo branch/readback and whether relevant CODEX process remains running. Avoid raw sensitive data; do not upload marker contents to public Git. Unknown stays UNKNOWN.
- If marker exists, record `ATTEMPT_CONSUMED`, preserve it and issue only a **NEW** distinct read-only host inventory assignment (new one-shot identity, corrected prompt-builder proof contract) after full R0–R7/PreExec/host checks; do not reuse old result branch/marker identity or re-run current launcher.
- Future corrected launcher must write atomic durable marker, immediately close and validate exact bytes and task/source identity, pass a minimal **verified marker evidence record and SHA-256** to CODEX; CODEX checks read-only marker status without inventing runtime telemetry. If receipt cannot be verified, STOP before agent spawn. A named Windows mutex covers cooperating launchers only; do not claim global one-writer.
- If CHAT can collect sufficient sanitized host evidence directly using a read-only host procedure after a proven host route, prefer that to a needless extra CODEX invocation. Never disable/stop/start/uninstall Worker or legacy services or read SQLite payload. Public repo should contain only bounded privacy-safe review decision; raw host identity stays private.
- `BUILD/BLOCKED`, `CANARY009/HOLD`, `COMPAT001/PUBLISHED_HOLD`, `INTERNAL_READY/NOT_ATTESTED`. No main/merge/install/provider/broker/LIVE.
- **Applied Skills:** `fox2-result-review` REQUIRED/APPLIED (no Git Result to accept), `fox2-execution-recovery` REQUIRED/APPLIED, `fox2-governance-preflight` REQUIRED/APPLIED scoped STOP, `fox2-source-resolver` REQUIRED/APPLIED historic immutable task/prompt readback, `fox2-agent-prompt-builder` NOT_APPLICABLE for an Agent *return*; mandatory only if a **new** task is issued.

**GOAL_MET:** no (host inventory remains NOT_RUN). **REAL_BLOCKER:** unverified atomic marker-readback binding and now-consumed one-shot identity. **NEXT_SAFE_ACTION:** read-only host marker reconciliation; no coding or Agent attempt.
