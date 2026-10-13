# FOX2 — SFR-001 / COPILOT — Source-Freshness Runtime Readiness

**WP:** FOX2-SFR-001 · **Change:** `FOX2-SFR-P0-20261013` · **Stage:** PRE-DEV, READ_ONLY · **Priority:** P0 · **Agent:** GitHub Copilot in VS Code on authorized Windows machine only if actual host access observed. **Model/Mode/Quota:** report observed or UNKNOWN; choose minimum sufficient mode; do not run paid probes.

## Authority and exact references

1. FOX2 Policy V1.8.2 RELEASED_EFFECTIVE — Library SHA256 `552d36d910a020de4475b1994975d09a30dd09a138476b03a4a2250d543181dc`, Git `c9dc41b97ca8bc58f06cc2f3701832ba083422e3:docs/governance/FOX2_POLICY_V1.8.2.md`, blob `0783c024d19f96a0b87ab770dad80bab449fa21f`.
2. Agent Prompt Routing Index V1.2.2 EFFECTIVE DERIVATIVE — Git `e24d4b56f1bc8c0b649f30da0e460cf2dcefeafc:docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_2_2_EFFECTIVE_ROUTING_INDEX_20261013.md`, blob `7d697a8db00a0ebbbb6eb68285fbf5ed2eade5ab`.
3. Bridge Technical Spec v0.4 RELEASED_EFFECTIVE — Git `36e4249d10d82e258626e3e49d796d8a8f498b8d:docs/architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.4.md`, blob `e74402d294c713a07a08b2c4e68b6caafbe2ad48`.
4. CHAT design **Candidate only** `FOX2_SOURCE_FRESHNESS_REGISTRY_RESOLVER_SPEC_v0.1_CANDIDATE.md`, and bootstrap data `FOX2_ACTIVE_SOURCE_REGISTRY_BOOTSTRAP_20261013.json` from the immutable Git full commit specified by CHAT. These documents are NOT a DEV grant or current released authority.
5. GitHub Issue #10 https://github.com/dunglt2505/FOX2/issues/10. BRG-001/002 were already inspected; reuse prior host inventory (20 source INCLUDE/3 review/55 excludes); DO NOT rerun tests, full inventory or P1.

**Mandatory flow:** `POLICY_CHECK → TASK_STATE_CHECK → ROUTING_R0_R7 → ASSIGNMENT_CHECK → RESPONSE`. R0 reuse verified prior work. R1 SFR-001 capability inspection, not coding. R2 source authority and Gate A: no auto dispatch, no DEV. R3 record actual host/model/quota/permissions or UNKNOWN. R4 compare available CHAT/COPILOT/CODEX/WORK; here inspect only, do not choose next DEV. R5 verify worktree/current processes/writer with READ_ONLY methods. R6 report source/credential/API capabilities without exposing credentials or generating output files. R7 STOP on any mutation.

## Perform narrowly, READ_ONLY

1. Check whether existing Bridge code in `C:\Projects\FOX2-AgentBridge` already implements any `SourceRegistry`, `ReleaseManifestReader`, `LatestPolicyResolver`, or `SOURCE_LOCK` validator. Record exact relative file/symbol and evidence, no assumptions from feature names.
2. Check whether a **working authenticated Library reader** and automatic Library publication event/hook are technically exposed to the local host. Distinguish `CHAT_CONNECTED_LIBRARY` from `WINDOWS_BRIDGE_CAN_READ_LIBRARY`. No auth/login/push/token display, no paid or destructive probes.
3. Inspect repository worktree + source-file preservation status since BRG-002; determine source import progress and which source revisions are in an immutable remote Git commit, with exact SHA readback if present; never infer it from local report.
4. Check GitHub Actions/webhook/event possibilities only as potential transport; a Git-only event does not prove a Library release. Record actual identity, grant, allowed branch scope and platform protection limitations without probing private credentials or writing.
5. Prepare **one complete SFR-010 task grant proposal**: implementation paths (new resolver package and offline fixtures), dedicated non-main Git branch and isolated worktree, base SHA, one-writer lane, expected tests, STOP and immutable result destination. Note gaps rather than fabricating permission/model/quota.
6. Classify 18 SFR-T scenarios by OFFLINE_TESTABLE vs HOST_INTEGRATION_REQUIRED vs EXTERNAL_CAPABILITY_BLOCKED. No tests run or Agent launch.

**Forbidden:** modifying files, opening SQLite (the earlier `mode=ro` created sidecars), starting processes, installing tools, creating worktrees/branches, staging, committing/pushing, scanning secrets by printing matches, changing tokens/credentials, fetching into owner's working tree, PR/merge, automatic Agent execution, code edits, provider/broker/LIVE.

## Required result: `FOX2-SFR-001 SOURCE FRESHNESS CAPABILITY REPORT`

Include Policy/latest-release lock with full commit/path/hash, host/CLI capability and evidence/UNKNOWN, exact existing component inventory (delta only), Library API/event capability status, result of source-baseline inspection, candid Git/publication constraints, 18-test feasibility classification, one-time SFR-010 scope/grant proposal, error/STOP cases. Final verdict `READY_FOR_CHAT_REVIEW` / `BLOCKED` / `INCOMPLETE_EVIDENCE`. Output **in Copilot Chat only**, no local file writes. Source mismatch or newer effective release: `BLOCKED_SOURCE_VERSION` and STOP for CHAT. A valid old SHA does not prove it is latest. No automatic dispatch Gate A PASS based on this preflight.
