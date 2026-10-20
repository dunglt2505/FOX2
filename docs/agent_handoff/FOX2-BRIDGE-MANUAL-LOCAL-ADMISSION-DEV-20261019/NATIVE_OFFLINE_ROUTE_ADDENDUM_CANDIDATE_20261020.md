# FOX2 — Manual Local Admission: Candidate Native Offline Route Addendum

**Scope:** existing `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019` within Whole-WP `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`.  
**Date:** 2026-10-20. **Author:** CHAT.  
**State:** `ROUTE_CANDIDATE_ONLY / NON_EXECUTABLE / PREEXEC_NOT_RUN / CODEX_NOT_ASSIGNED`.  
**Original task:** `docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/task.md` at initial immutable task commit `482d26d71c5c95f028f9b4110349e4d318bcb342`. Original task bytes, its previously proposed BRIDGE bootstrap, and receipt `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/preflight_receipt.json` at `1ce109b9a4c538b255c6d8ffc6be8b4dccecf65d` remain unchanged. That original route's `CHECK_BRIDGE_BOOTSTRAP_CONTROLS=FAIL` and overall `BLOCKED` are not overwritten or waived.

## Decision provenance

- Current scoped human policy: `docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json` at `d34da1e3b4918a902646621b487ca8ad3e05b0e0` selects Owner-approved Policy 2.0.0 and Routing 1.4.0 for new/re-scoped human work, CODE-FIRST/CHAT-FIRST. This is NOT installed machine adoption. In-flight original Bridge tasks retain their old immutable Policy 1.8.9/Dictionary 1.2 source bindings.
- Infrastructure code-rights Owner grant: `c23d28bd56d9d06d64561dcf255b2d94227f6acc:docs/governance/releases/FOX2_MANUAL_LOCAL_ADMISSION_OWNER_EXECUTION_AUTHORIZATION_20261019.json` (`OWNER_APPROVED_SCOPED_END_TO_END_MANUAL_LOCAL_ADMISSION_INFRASTRUCTURE`). Allows the six primary implementation/test files and exact K1-supported shared dependencies; no wildcard, no automatic machine launch.
- Frozen engineering input: `work/FOX2-BRIDGE-DESKTOP-BATCH-B@f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`. Source-impact and safety: `060beb6fdfb741d99a6ec8730f6e76ad2d873fd7:docs/roadmap/FOX2_BRIDGE_RC1_Q1_SELECTIVE_ADMISSION_SOURCE_IMPACT_CANDIDATE_20261020.md`. Route separation: `2c130ce37f15ad32f987d5616ada561fed076f1d:docs/roadmap/FOX2_BRIDGE_OFFLINE_DEV_ROUTE_DECISION_20261020.md`. Candidate documents are not Effective Policy/TechSpec.
- Owner's read-only 2026-10-20 host result `FOX2_NATIVE_OFFLINE_PRECHECK_20261020T020939778Z.json`, reported SHA-256 `ADE3EF2CB0D10A24DCE645E00630499BE77E6D626AD717DB2B8E444CFF35C754`, had source/branch/remote match, zero worktree changes and zero candidate writer processes **at that snapshot**. CHAT independently confirmed the Git HEAD `1ce109...`; CHAT did not receive original Windows file bytes. CODEX CLI 0.162.1 supports flags `--sandbox`, `--model`.
- Separate read-only `codex login status` executed 2026-10-20T02:18:10.5485373Z by Owner yielded exit code 0 / `CLI_REPORTED_SUCCESS`. **Pinned exact model availability and quota remain NOT_ATTESTED**, no AI marker/executable coding attempt observed in this check.

## Prospective DEV route — PREPARATION, NOT EXECUTION

**Actor:** CODEX only after valid new-route preflight and CHAT `PASS_TO_ASSIGN`. **Engine/model:** PINNED `gpt-6.1-sol`; **Thinking:** Medium; **Permission:** FULL_ACCESS for authorized offline developer worktree, subject to task path/sandbox review and output controls. **Execution path:** proposed `NATIVE_LOCAL_CODEX_CLI_OFFLINE_DEV`, not a v3 `BRIDGE` Dispatch, not the existing immutable COMPAT001 `MANUAL_LOCAL` attempt. **Delivery owner:** AGENT using exact authorized non-main Git result branch; CHAT independently accepts. **Worktree:** `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`; `branch=work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`. This addendum's own commit becomes the **new source HEAD for any prospective native-only task-specific PreExec**, not a retroactive rebind of the previous BLOCKED Bridge receipt.

**Core code allowlist proposal (exact, not wildcard):**
1. `agent_bridge/src/fox2_agent_bridge/dispatch_normalizer.py`
2. `agent_bridge/src/fox2_agent_bridge/e2e_runner.py`
3. `agent_bridge/src/fox2_agent_bridge/app.py`
4. `agent_bridge/src/fox2_agent_bridge/__main__.py`
5. `agent_bridge/tests/test_project_dictionary.py`
6. `agent_bridge/tests/test_e2e_runner.py`

`ledger.py` shared transaction semantics are a CONDITIONAL DEPENDENCY and require K1 consumer demonstration and exact bound scope before editing. `desktop.py` is excluded from the initial offline implementation: Worker `PAUSED` denies new launch/claim, and selective Worker admission while still paused would change safety semantics without a separately justified explicit maintenance state/authorization. `ops_runner.py`, `process_lock.py`, `dispatch_poller.py`, `project_dictionary.py`, schema/generated Registry and all other paths are excluded unless CHAT documents additional material impact. No code execution, real DB, Worker control, installed runtime or synthetic `PASS` permitted.

## Route-specific PreExec requirements and safety decision

**Fresh receipt destination:** `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/native_offline_preflight_20261020.json` on this branch, **different from the original immutable BLOCKED receipt**. Use the real task-specific shared v1.1 `PreExec(Requirements(...))` engine under the inspected source, not canned `scripts/preexec.py --profile bridge` which hardcodes Batch-B and its material Bridge checks. Do not perform a custom ad-hoc check and call it an official PASS.

Material checks for a future **genuinely offline** coding attempt: (1) matching exact current branch and immutable task/addendum SHA plus current remote HEAD, (2) clean owned worktree and single writer, including PreExec's own bounded lock, (3) no reused or consumed attempt and no unrelated result/WIP, (4) credible pinned CODEX CLI model/medium/FULL_ACCESS/approval policy, usable authentication/capacity, (5) `git`, `pwsh`, Python, `pytest`, `jsonschema`, (6) Owner grant and changed-path/rights review, (7) authorized Git result delivery and abort-on-drift. A stock model-probe `agent_probe` **does invoke a small CODEX AI request**, hence it is not “zero Agent execution”: run only after exact source/path/safety checks are met, and record observed result honestly. CLI login success is not proof of the model/quota. If the active route cannot prove all task-material capabilities, record truthful `BLOCKED`/`INFRA_FAILED` and STOP; never issue coding prompt as PASS.

Do NOT use installed Bridge for native coding preflight, and do not substitute `bridge_bootstrap_controls=PASS` or relabel the old `BLOCKED`; installed Bridge ownership, continuous singleton lock and paused state remain operational/Canary gates only. No claim of current Windows writer ownership after the host snapshot; PreExec and the eventual assignment require fresh checks at execution time.

**No Agent task issued yet:** No exact `prompt.md` has been published for this route; `fox2-agent-prompt-builder` must bind a new attempt's task/prompt/PreExec/permissions/STOP/result contract and publish/read back the exact immutable prompt **after** the route-specific receipt supports assignment. Never invoke a reused Dispatch identity. Preserve `COMPAT001=PUBLISHED_HOLD`, `CANARY009=HOLD`, `INTERNAL_READY=NOT_ATTESTED`. No main, merge, install, runtime mutation, provider/broker or LIVE.

**NEXT_SAFE_ACTION:** verify this addendum's remote SHA/blob and exact task branch, then on FOXLE-PC fast-forward only the *clean* task worktree to this new addendum commit, and execute one task-scoped, actual native/offline PreExec with recorded outcome; do not execute implementation Agent until CHAT has remote-read the receipt and returned explicit assignment verdict.
