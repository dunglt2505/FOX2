# FOX2 — Agent Prompt Policy V1.2.3 — CHAT-FIRST Effective Routing & Latest-Release Handoff Index

**Document ID:** `FOX2-AGENT-PROMPT-ROUTING-INDEX`  
**Revision:** `V1.2.3` · **Date:** 2026-10-13 (Asia/Ho_Chi_Minh)  
**Status:** `EFFECTIVE_DERIVATIVE_ROUTING_INDEX / NOT_SEPARATE_POLICY / NO_DEV_GRANT` after verified Library publication + exact raw-byte readback + Git reference manifest  
**Supersedes for NEW prompts:** `FOX2_AGENT_PROMPT_POLICY_V1_2_2_EFFECTIVE_ROUTING_INDEX_20261013.md` (historical provenance only).  
**Sole normative Policy:** `/Trading/FOX2/00_Governance/FOX2_POLICY_V1.8.3.md` — `RELEASED_EFFECTIVE`, exact Library raw SHA-256 `892a44f414c8deb3754782b0d1c9998a88fa1116da33e76048ac8756005dee82`; Git source `0ecce9f732e64742ca1309bbd7da6fe6cad4d137:docs/governance/FOX2_POLICY_V1.8.3.md`, blob `96304b16cfa6437a540a68c14ee1a284a17ea195`; Release Manifest Library `/Trading/FOX2/00_Governance/FOX2_POLICY_V1.8.3_RELEASE_MANIFEST_20261013.json`, Git `80d873bb29ab9d77fee782e1ae345fa03dc1dffc:docs/governance/FOX2_POLICY_V1.8.3_RELEASE_MANIFEST_20261013.json`, blob `91cf9ab9507750c61392c894e446a2a45d8093d6`. This routing index implements FOX2 Policy A1, C1A/C1B, C2A.7 CHAT-FIRST, C4A, C5/C5A and C6F; it does not replace the single FOX2 Policy family.
**Owner decision:** CHAT performs GitHub/Library/source/Issue work directly when its actual authenticated tools suffice; Copilot/Codex are only for genuine local-host or coding deltas. New work handed to Copilot/Codex/Bridge must bind the **newest demonstrably RELEASED_EFFECTIVE** applicable source, not a previously pinned older Technical Spec or a newer-but-unreleased Candidate. Do not repeat approvals for unchanged Owner decisions; preserve prior accepted work.  
**Scope:** FOX2 only. This index does not authorize Bridge automatic dispatch, local source import, Git code push, merge, provider, broker or LIVE.

## 1. Defect and disposition

The historical V1.2.1 routing index cited Policy V1.8.1 and did not expressly require a fresh **latest-effective-release resolution** before a new handoff. In addition, the initial BRG-003 prompt identified Bridge v0.3 RELEASED_EFFECTIVE and v0.4 CANDIDATE; after v0.4 was actually released, that static prompt became stale. Citing a valid *old* immutable SHA does **not** establish that the handoff uses the currently effective document.

**Fix (retained from V1.2.2):** resolve the applicable released *family head* before issuing each **new** WP/prompt; pin its exact immutable Library release + manifest + Git mirror; re-evaluate when there is a later relevant release or a material gap before dispatch. Preserve a prior WP's original immutable source receipt for history; do not automatically redo already accepted work.

## 2. Normative authority separation and version choice

1. **Authority order:** applicable external restrictions → attributable latest FOX2 Owner decision → released FOX2 Policy → released BRD/Data Contract/Acceptance for owned requirements → latest applicable **released** Technical Specification for implementation → Candidates/drafts/references. A source's filename, version number or Git commit does not alone prove release effectivity.
2. **Active Policy:** FOX2 Policy V1.8.3, unless CHAT verifies a newer FOX2 Policy `RELEASED_EFFECTIVE` release with its Library manifest and authoritative scope. Prior version strings embedded in older released documents can be historical; do not use them as a runtime version selector.
3. **Bridge technical document at this 2026-10-13 checkpoint:** v0.4 `RELEASED_EFFECTIVE`, Library path `/Trading/FOX2/02_Architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.4.md`, raw SHA-256 `8a7d5e55239c07fb32834f856fbe59b33cbc90d92768a7804c9a70236907cd9e`, 59,353 bytes. Its Library release manifest is `/Trading/FOX2/02_Architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.4_RELEASE_MANIFEST_20261013.json`, raw SHA-256 `3ceb1f5ea1ca55dd17a1060fe36a12a317e4e3738481fca2a3456eb04abc6493`. Git mirror: `dunglt2505/FOX2`, commit `36e4249d10d82e258626e3e49d796d8a8f498b8d`, path `docs/architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.4.md`, blob SHA `e74402d294c713a07a08b2c4e68b6caafbe2ad48`; manifest mirrored at commit `5b17d4a3947679b60403d95c558536b1af5b8e48` and Git blob `52306026977bd649427e9ddb7b7000fb446609af`.
4. **Historical Bridge v0.3** remains immutable and is `SUPERSEDED_FOR_NEW_BRIDGE_TASKS`; v0.4 Candidate is superseded by released v0.4. A newer Candidate cannot displace released v0.4 until the newer release has been published and independently read back. If a newer released v0.5 or newer relevant Policy exists at handoff time, the hardcoded v0.4 example above is historical and MUST be replaced after verification.
5. **Standing Git authority distinct:** Owner's Bridge one-branch review-event standing grant is recorded at `bcd78aabeaf7817b7d9b682a0180445293061f41:docs/agent_handoff/BRIDGE/FOX2_BRIDGE_STANDING_GIT_BRANCH_GRANT_20261013.md`, blob `ca2d414c0daacda1ba5a20ed963e1eb314e7cc7b`. It never grants BRG-003 source-code import. No repeated Owner grant is needed for authorized, validated review-event metadata operations on `work/FOX2-REVIEW-EVENTS-bridge`; actual local credentials, allowed paths, branch writer safety and remote SHA still require checks. Gate A automated remains `BLOCKED_CAPABILITY_UNAVAILABLE` until real trust enforcement is demonstrated.

## 3. REQUIRED SOURCE_FRESHNESS_PRECHECK (CHAT owns the decision)

Before the first prompt for each **new** WP, and again before an automated dispatch when source could have changed. **Perform C2A.7 CHAT-first remote work directly before even considering Agent delegation**:

1. Enumerate the **applicable family** (Policy, BRD/Data Contract/Acceptance, Technical Spec, relevant grants/Source Manifest) rather than asking the Agent to guess by file name. Verify the newest applicable `RELEASED_EFFECTIVE` from the authorized Library publication, exact bytes and release manifest; record time and scope of the check. Search/list must be complete enough to rule out another relevant effective release; `next_cursor` or other pagination must be exhausted when applicable.
2. Compare supersession/effectivity and material relevance. **Latest released applicable** wins for new WPs, not simply largest text version. Owner-approved scope can explicitly freeze a revision for a particular WP; that exception must be identified, attributable, current and consistent with Policy/real-world restrictions. A Candidate is not released merely because it was uploaded or mirrored to Git.
3. Verify exact Library file/revision and raw SHA-256; independently read back pinned Git full commit:path and blob/hash for the *same released bytes* (or label Git sync `SOURCE_PENDING` and do not issue an executable Git-first dispatch). Record any split if a manifest and Git source are at distinct immutable commits.
4. First check whether CHAT can do the actual remaining work through connected GitHub/Library tools; if yes perform it and record `CHAT_DIRECTLY_COMPLETED`. Delegate only real `LOCAL_ONLY_DELEGATED` or `CODE_WORK_PACKAGE_DELEGATED` work, with why CHAT cannot do it. Check that task/Owner permission, actual role/model/quota if visible, allowed paths, WIP/writer and branch still satisfy R0–R7; previously accepted evidence is reused without reruns. An approved standing report/event grant is not a code/DEV grant.
5. Construct a single **SOURCE_LOCK** in the new prompt/handoff. Do not leave older `v0.3 current` or Candidate-current instructions elsewhere in the same prompt, prior linked prompts, issue commentary or templates. An immutable prompt from an older release is **superseded for new use**; do not silently send it unchanged.
6. Receiver (Copilot/Codex/WORK/Bridge) independently opens the exact authorized commit:path and checks the specified identity/receipt when technically accessible; reports limitations as `LATEST_LIBRARY_STATUS=CHAT_ATTESTED_NOT_INDEPENDENT` rather than pretending the Agent has Library access. The Agent must not promote Candidate, choose a superseded version or substitute model/Agent itself.
7. On any known newer released document, missing/contradictory manifest, mismatch in Library/Git SHA, untrusted issue text, or incomplete family-head resolution: `BLOCKED_SOURCE_VERSION` and STOP the affected **new handoff**, return to CHAT for a source-lock refresh. `READ_ONLY` inspection can return its blocker without writing. No automatic downgrade to an older valid SHA.
8. If source changed after assignment but before operation, retain original source evidence, classify **relevance/materiality**, and re-route only the affected portion; don't retroactively mark historical accepted WPs stale unless new requirements expressly demand action.

## 4. Minimum SOURCE_LOCK fields for new Copilot prompts

```yaml
source_lock:
  verified_at_local: <actual-timestamp>
  project: FOX2
  policy:
    version: <newest-released-effective-or-BLOCKED_SOURCE_VERSION>
    library_path: <authoritative-path>
    library_raw_sha256: <measured>
    git_full_commit_path: <full-SHA:path>
    git_blob_sha: <observed>
  requirements:
    released_brd_data_contract_acceptance: <explicit-per-WP-source-set-or-NOT_APPLICABLE>
    source_manifest_sha256: <observed-or-SOURCE_PENDING>
  technical:
    document_family: <e.g.-FOX2-LOCAL-AGENT-BRIDGE-SPEC>
    latest_effective_version: <verified-version>
    status: RELEASED_EFFECTIVE
    library_path: <authoritative-path>
    library_raw_sha256: <measured>
    release_manifest_path_sha256: <verified-pair>
    git_full_commit_path: <full-SHA:path>
    git_blob_sha: <observed>
    supersedes: <prior-released-version>
  owner_grants:
    decisions_and_scopes: <exact-source-or-NONE>
    code_allowed: <YES-only-on-independent-grant-else-NO>
    report_write_push: <actual-standing/task-grant-and-runtime-verification>
  handoff:
    task_id: <id>
    wp_id: <id>
    phase: READ_ONLY|DESIGN_ONLY|AUTHORIZED_MATERIAL_DEV
    chat_first_disposition: CHAT_DIRECTLY_COMPLETED|LOCAL_ONLY_DELEGATED|CODE_WORK_PACKAGE_DELEGATED|BLOCKED_CAPABILITY
    chat_direct_evidence: <commit:blob/Library-receipt/Issue-or-NOT_APPLICABLE>
    delegation_reason: <local-host/programming-required-or-NONE>
    source_version_check: PASS|BLOCKED_SOURCE_VERSION
    library_head_check_method: <observed-method-or-CHAT_ATTESTED>
    allowed_paths: <exact-list>
    forbidden_paths: <exact-list>
    git_source_ready: YES|NO
    worktree_writer: <observed-or-UNKNOWN>
    stop_if: [BLOCKED_SOURCE_VERSION, SOURCE_PENDING, SHA_MISMATCH,
              AUTHORITY_UNKNOWN, WIP_COLLISION, UNTRUSTED_PROVENANCE]
```

**Important:** source-lock check does not replace the rest of the required C5/C5A handoff (model/Thinking/cost/acceptance/result receipt etc.). Missing actual host quota or access must be `UNKNOWN`, not invented. Frozen old tasks retain original locks for traceability.

## 5. Execution Routing Selector — unchanged Owner-confirmation semantics

1. CHAT executes the one-time decision chain `POLICY_CHECK → TASK_STATE_CHECK → ROUTING_R0_R7 → ASSIGNMENT_CHECK`. `SOURCE_FRESHNESS_PRECHECK` is a mandatory **input** to the existing policy/source gate, not a second round of routing or Owner approval.
2. Only at actual `PROMPT_READY_TO_DISPATCH` for a fully authorized executable WP does Screen 1 present `MANUAL_VSCODE` or `CONFIGURE_AUTOMATED_AGENT`. Manual choice ends Bridge dispatch processing.
3. Only after `CONFIGURE_AUTOMATED_AGENT` does Screen 2 show Agent/Model/Thinking/Optimize choices, truthful availability and minimum-sufficient cost; require explicit Owner selection, not a preselected default. Do not invent Copilot Thinking capability.
4. Only after Screen 2 confirmation does Screen 3 present `DISPATCH_VIA_LOCAL_BRIDGE`, `BACK_TO_AGENT_CONFIGURATION`, `CANCEL_EXECUTION`. No `SAVE_PROMPT_ONLY`/`SAVE_CONFIGURATION_ONLY` actions in this automated selector.
5. Native controls are used only if exposed by the current client. Text/number fallback retains the same affirmative confirmation sequence. Prompt may be supplied for an Owner-chosen manual VS Code step without claiming automated-Bridge execution.
6. On confirmed `DISPATCH_VIA_LOCAL_BRIDGE`, CHAT publishes one source-pinned immutable schema-v1.1 dispatch to `docs/agent_handoff/<WP_ID>/dispatch/<DISPATCH_ID>.json` only after applicable source, trust and technical capability gates, including effective Gate A, are satisfied. Bridge checks runtime facts and does not repeat Owner Policy/R0–R7 decisions or substitute the configuration.
7. One `DISPATCH_ID` is single use (`max_runs=1`); mismatch `LOCAL_RUNTIME_BLOCKED`, duplicate `DISPATCH_DUPLICATE_IGNORED`. The result contract, independent CHAT review and acceptance boundaries remain unchanged. A dispatch is not an approval to merge or LIVE.

## 6. Negative tests and acceptance evidence for this routing index

| ID | Scenario | Required outcome |
|---|---|---|
| APIX-01 | Older v0.3 Git commit valid, but latest Bridge v0.4 actually released | Reject v0.3 as active for NEW WP; bind verified v0.4 |
| APIX-02 | v0.5 Candidate exists without a published manifest | v0.4 remains effective; don't promote candidate |
| APIX-03 | Newer RELEASED_EFFECTIVE document appears after prompt authored | STOP old handoff, CHAT refreshes source lock before execution |
| APIX-04 | Technical v0.4 remains released after Policy v1.8.3 enters effect | Use Policy v1.8.3 + Technical v0.4; independent versioning |
| APIX-05 | Copilot has Git access but no Trading Library | Use CHAT's verified source lock; mark own Library freshness verification unavailable |
| APIX-06 | Git artifact found without matching Library release/readback | SOURCE_PENDING or BLOCKED_SOURCE_VERSION, no executable dispatch |
| APIX-07 | Release manifest and raw byte hash disagree | BLOCKED_SOURCE_VERSION; no fallback |
| APIX-08 | Old WP accepted under original immutable source | Preserve acceptance, no default rework |
| APIX-09 | Standing Bridge review-event branch exists | No DEV/GIT_CODE_PUSH inference |
| APIX-10 | New WP asks Copilot under Gate A still BLOCKED | Manual READ_ONLY possible if independently scoped; no autonomous Bridge dispatch |
| APIX-11 | A file listing has `next_cursor` or incomplete scope | Continue inventory or mark CURRENT_RELEASE_UNKNOWN, fail closed |
| APIX-12 | Prompt refers both v0.3 as effective and v0.4 as effective | Fail consistency check, correct prompt before handoff |

**Acceptance status of tests:** design-only negative test matrix; no operational Agent/Bridge test execution or Gate A verification is claimed by this index.

## 7. Release and transition notes

- V1.2.2 and V1.2.1 remain historical quick-references, **superseded for NEW FOX2 Agent prompts** by this V1.2.3 index. The substantive governance owner is released FOX2 Policy V1.8.3; there is no newly invented parallel Policy or CODE_ALLOWED grant.
- BRG-003 initial prompt is historical and superseded by `FOX2_BRG003_COPILOT_PRECOMMIT_PROMPT_20261013_REV2.md`, Git `92178766f3609e5c4c7f9be8a5eb584e988b8a0d`, under released Bridge v0.4. Any future prompt uses the then-current release, not this static example forever.
- This document is a decision-routing quick-reference and latest-release source-lock implementation guide. If a future change truly alters FOX2 Policy invariants rather than the mechanics of applying A1/C5/C5B, a new FOX2 Policy version requires its own proper release/publication.

## 8. Owner CHAT-FIRST allocation gate — V1.2.3

Mandatory source: released FOX2 Policy V1.8.3 §C2A.7 + Owner's Shared Governance directive `/Trading/00_Governance/TRADING_CHAT_FIRST_AGENT_ALLOCATION_OWNER_DIRECTIVE_20261013.md`. For every new or re-scoped Agent prompt, CHAT must first complete independently available remote GitHub/Library/Issue/commit/blob/manifest/Policy work. An Agent must not be assigned a remote repository metadata task merely to echo information available to CHAT via authenticated connectors. An existing local-Agent source-check of *received immutable bytes* and own-branch Git push as part of authorized programming remain valid distinct requirements.

**Handoff STOP examples (design only):** `CFH-01` Agent prompt asks Copilot to search remote GitHub Issues/Policy even though CHAT has already verified exact refs → ROUTE_BACK_TO_CHAT; `CFH-02` CHAT tool blocked by safety and prompt tries Agent as workaround → BLOCK; `CFH-03` Windows-only worktree collision check → COPILOT/CODEX if eligible; `CFH-04` actual authorized code/test with own-branch Git push → eligible CODEX/COPILOT; `CFH-05` Agent claims ChatGPT Library release independently without Library access → BLOCKED_SOURCE_ATTESTATION; `CFH-06` old v1.8.2 pinned prompt starts new task when Policy v1.8.3 already released → BLOCKED_SOURCE_VERSION. Tests are NOT_RUN.

This derivative index is document-only and does not grant BRG-003 import, any additional scoped DEV, Git code push, branch protection, merge, auto-dispatch or LIVE. Do not version-bump Bridge v0.4, SFR Candidate v0.1 or unrelated BRDs just to reflect a CHAT routing rule; update each future Agent handoff's exact source lock instead.
