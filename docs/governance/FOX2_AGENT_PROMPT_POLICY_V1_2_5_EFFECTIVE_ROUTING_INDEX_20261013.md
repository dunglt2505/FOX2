# FOX2 — Agent Prompt Policy V1.2.5 — Architecture–Stage Aligned Routing & Latest-Release Handoff Index

**Document ID:** `FOX2-AGENT-PROMPT-ROUTING-INDEX`  
**Revision:** `V1.2.5` · **Date:** 2026-10-13 (Asia/Ho_Chi_Minh)  
**Status:** `EFFECTIVE_DERIVATIVE_ROUTING_INDEX / NOT_SEPARATE_POLICY / NO_DEV_GRANT` after verified Library publication + exact raw-byte readback + Git reference manifest  
**Supersedes for NEW/re-scoped prompts:** `FOX2_AGENT_PROMPT_POLICY_V1_2_4_EFFECTIVE_ROUTING_INDEX_20261013.md` (historical provenance only).  
**Sole normative Policy:** `/Trading/FOX2/00_Governance/FOX2_POLICY_V1.8.4.md` — `RELEASED_EFFECTIVE`, exact Library raw SHA-256 `481790b2512ea1cd4891fe1b03258175d68d9bfae71158d19283bd003c560f5a`; Library file `file_0000000008e08211b685c8e280ee8ca7`; Git mirror `a366f509899cec97f64316cb111b29a3849325b5:docs/governance/FOX2_POLICY_V1.8.4.md`, blob `483a74ff39339e653bbd7bbfba0feaf7b1c003e9`; Release Manifest Library `/Trading/FOX2/00_Governance/FOX2_POLICY_V1.8.4_RELEASE_MANIFEST_20261013.json`, SHA-256 `ee3a49cf06645e4e2409987caa140c60c68980338710b719bd174b51c4a9f10c`; Git `a70ae6f310003457b770b385b7205715debdc90d:docs/governance/FOX2_POLICY_V1.8.4_RELEASE_MANIFEST_20261013.json`, blob `0eb4f3145f8497906e46351f1dc402fe9e6355d0`. This routing index implements FOX2 Policy A1, C1/C1.2/C1A/C1B, C2A.7, C4A, C5/C5B and C6F; it does not replace the single FOX2 Policy family.
**Owner decision:** Before choosing any Agent or execution path, CHAT must reconcile the **released target architecture, actual implementation stage, material dependency/gates and path class**. CHAT still performs GitHub/Library/source/Issue work directly when its authenticated tools suffice; Copilot/Codex are for genuine local-host or coding deltas. New/re-scoped work binds the newest applicable RELEASED_EFFECTIVE source; bootstrap/fallback paths stay explicitly temporary and cannot silently replace the target architecture.  
**Scope:** FOX2 only. This index does not authorize Bridge automatic dispatch, local source import, Git code push, merge, provider, broker or LIVE.

## 1. Defect and disposition

V1.2.3 correctly enforced latest-effective source resolution and CHAT-FIRST allocation, but it did not make **architecture/stage alignment a first-class routing gate**. A technically valid fallback (for example a manual execution path) could therefore be selected before reconciling whether the project was in bootstrap, partial-operation or target-operation stage, creating a mismatch between the released Technical architecture and the route presented to the Owner.

**V1.2.5 update:** retain the V1.2.4 Architecture–Stage Alignment gate and bind new Bridge handoffs to released Technical Spec v0.5. For the current FOX2 build stage, `BOOTSTRAP_TRUST` may use authenticated CHAT publication to the exact control branch plus immutable commit/hash/decision/replay validation; dedicated GitHub App + enforced control-ref provenance is a later `HARDENED_TRUST` requirement, not a bootstrap blocker. This does not relax DEV/merge/Production/LIVE gates.

## 2. Normative authority separation and version choice

1. **Authority order:** applicable external restrictions → attributable latest FOX2 Owner decision → released FOX2 Policy → released BRD/Data Contract/Acceptance for owned requirements → latest applicable **released** Technical Specification for implementation → Candidates/drafts/references. A source's filename, version number or Git commit does not alone prove release effectivity.
2. **Active Policy:** FOX2 Policy V1.8.4, unless CHAT verifies a newer FOX2 Policy `RELEASED_EFFECTIVE` release with its Library manifest and authoritative scope. Prior version strings embedded in older released documents can be historical; do not use them as a runtime version selector.
3. **Bridge technical document at this 2026-10-13 checkpoint:** v0.5 `RELEASED_EFFECTIVE / BOOTSTRAP_TRUST_ENABLED / HARDENED_TRUST_DEFERRED`, Library path `/Trading/FOX2/02_Architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.5.md`, raw SHA-256 `2d182972b5edd6ccfd72c83b07d97907fa7fb63ed6eaa4de68b03b7e5165740a`, 13,380 bytes. Its Library release manifest is `/Trading/FOX2/02_Architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.5_RELEASE_MANIFEST_20261013.json`, raw SHA-256 `a8569e8e5f75a37201c4bc88145c60875cf15d7261f86db85f8bfdb620f89198`. Git mirror: `dunglt2505/FOX2`, commit `8010a121e1d8b3f244da7dd856931b1bce41da21`, path `docs/architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.5.md`, blob SHA `1ce788e84628764f1b58459e93aecd5c7fde641e`; manifest mirrored at commit `030ea086c70cb9feb38d777edf76bdef5124dc2c` and Git blob `55a4be069639f342ebab24baf624477764d72493`.
4. **Historical Bridge v0.3/v0.4** remain immutable and are `SUPERSEDED_FOR_NEW_BRIDGE_TASKS` after v0.5 verified release. v0.5 supersedes only the trust-mode/Gate-A/readiness portions it explicitly names; all other v0.4 mechanics remain incorporated by reference. A newer Candidate cannot displace released v0.5 until actually released and read back.
5. **Standing Git authority distinct:** Owner's Bridge one-branch review-event standing grant is recorded at `bcd78aabeaf7817b7d9b682a0180445293061f41:docs/agent_handoff/BRIDGE/FOX2_BRIDGE_STANDING_GIT_BRANCH_GRANT_20261013.md`, blob `ca2d414c0daacda1ba5a20ed963e1eb314e7cc7b`. It never grants BRG-003 source-code import. During current public build stage, Bridge may target `BOOTSTRAP_GATE_A` under v0.5 using the exact control ref + immutable commit/hash/decision/replay controls. `HARDENED_GATE_A` remains separate and mandatory before confidential/private/Production-LIVE operation.

## 2A. Bridge v0.5 stage-specific trust routing

For current FOX2 public bootstrap:

```text
trust_mode = BOOTSTRAP_PINNED_GIT
BOOTSTRAP_GATE_A = the required Gate A for Bridge launch readiness
HARDENED_GATE_A = deferred, not a bootstrap blocker
```

`BOOTSTRAP_PINNED_GIT` requires exact repository/ref, immutable dispatch commit, task/prompt/Policy/Technical/source hashes, Owner decision binding, single-use replay protection and runtime revalidation. It does **not** require GitHub App-specific publisher proof or ruleset bypass proof. The current misconfigured Ruleset 24990489 is non-authoritative for bootstrap.

Before confidential/proprietary/private or Production/LIVE operation, route to `HARDENED_PUBLISHER` and require `HARDENED_GATE_A=PASS` under Bridge v0.5 or a later released equivalent.

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

## 4. REQUIRED ARCHITECTURE_STAGE_ALIGNMENT_PRECHECK (FOX2-wide)

Perform after latest-effective source resolution and **before** selecting CHAT/COPILOT/CODEX/WORK or presenting any execution selector.

Required order:

`TARGET_ARCHITECTURE → ACTUAL_STAGE → OBSERVED_CAPABILITY → MATERIAL_DEPENDENCY/GATE → PATH_CLASS → AGENT_COMPARISON`.

Required record:

```yaml
architecture_stage_alignment:
  technical_source: <latest-applicable-released-Technical-Spec-or-NOT_APPLICABLE>
  target_architecture: <authoritative-end-state>
  actual_stage: PLANNING|BOOTSTRAP|PARTIAL_OPERATIONAL|OPERATIONAL|CLOSED_LOOP|OTHER_OBSERVED
  observed_capabilities: [<facts>]
  unmet_dependencies_or_gates: [<material-only>]
  execution_path_class: TARGET_PATH|BOOTSTRAP_PATH|FALLBACK_PATH
  path_reason: <why-stage-aligned>
  target_transition: <next-gate/milestone>
  fallback_retirement_condition: <condition-or-NOT_APPLICABLE>
  alignment_verdict: PASS_TARGET|PASS_BOOTSTRAP|PASS_FALLBACK|BLOCKED_ARCHITECTURE_UNKNOWN|BLOCKED_STAGE_MISMATCH
```

Rules:

1. Never equate a documented target architecture with a capability that is already operational.
2. A WP that builds missing enabling infrastructure is a **bootstrap task**; do not circularly require that infrastructure to be operational before it may be built. Use the smallest authorized bootstrap path and name the exit gate.
3. Manual/degraded/alternate handling is a `FALLBACK_PATH`, not the FOX2 default architecture. It must have a retirement condition and cannot broaden authority.
4. After the target path objectively passes its required gates, use it for new equivalent WPs unless a new material blocker is observed.
5. Read the applicable released Technical Spec whenever it owns transport/topology/lifecycle/isolation/dependency mechanics. Read BRD/Data Contract/Acceptance when the WP implements their business requirements; pure infrastructure may record them `NOT_APPLICABLE`.
6. Unknown/NOT_EXPOSED facts block only if material to the requested operation; real documented gates cannot be ignored because a fallback looks easier.
7. Agent selection is last. Do not choose an Agent first and bend scope/architecture around it.
8. Parallelism is allowed only across dependency-safe, interface-frozen, writer-isolated paths; priority is not blanket serialization.

This precheck does not grant DEV, Git write, Bridge dispatch, merge, Production or LIVE.

## 5. Minimum SOURCE_LOCK fields for new Copilot/Codex prompts

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
    architecture_stage_alignment: <record-from-section-4>
    execution_path_class: <TARGET_PATH|BOOTSTRAP_PATH|FALLBACK_PATH>
    target_transition: <next-gate-or-milestone>
    fallback_retirement_condition: <condition-or-NOT_APPLICABLE>
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

## 6. Execution Routing Selector — architecture-stage constrained Owner-confirmation semantics

**Architecture/stage constraint:** the selector is subordinate to the V1.8.4 C1.2 result. It presents only execution options valid for the recorded current stage/path class. A bootstrap/fallback option must remain labeled temporary and cannot be described as the FOX2 target architecture.

1. CHAT executes the one-time decision chain `POLICY_CHECK → TASK_STATE_CHECK → ROUTING_R0_R7 → ASSIGNMENT_CHECK`. `SOURCE_FRESHNESS_PRECHECK` is a mandatory **input** to the existing policy/source gate, not a second round of routing or Owner approval.
2. Only at actual `PROMPT_READY_TO_DISPATCH` for a fully authorized executable WP does Screen 1 present `MANUAL_VSCODE` or `CONFIGURE_AUTOMATED_AGENT`. Manual choice ends Bridge dispatch processing.
3. Only after `CONFIGURE_AUTOMATED_AGENT` does Screen 2 show Agent/Model/Thinking/Optimize choices, truthful availability and minimum-sufficient cost; require explicit Owner selection, not a preselected default. Do not invent Copilot Thinking capability.
4. Only after Screen 2 confirmation does Screen 3 present `DISPATCH_VIA_LOCAL_BRIDGE`, `BACK_TO_AGENT_CONFIGURATION`, `CANCEL_EXECUTION`. No `SAVE_PROMPT_ONLY`/`SAVE_CONFIGURATION_ONLY` actions in this automated selector.
5. Native controls are used only if exposed by the current client. Text/number fallback retains the same affirmative confirmation sequence. Prompt may be supplied for an Owner-chosen manual VS Code step without claiming automated-Bridge execution.
6. On confirmed `DISPATCH_VIA_LOCAL_BRIDGE`, CHAT publishes one source-pinned immutable schema-v1.1 dispatch to `docs/agent_handoff/<WP_ID>/dispatch/<DISPATCH_ID>.json` only after applicable source, trust and technical capability gates, including the stage-appropriate effective Gate A (`BOOTSTRAP_GATE_A` for the current public build stage; `HARDENED_GATE_A` when required by v0.5), are satisfied. Bridge checks runtime facts and does not repeat Owner Policy/R0–R7 decisions or substitute the configuration.
7. One `DISPATCH_ID` is single use (`max_runs=1`); mismatch `LOCAL_RUNTIME_BLOCKED`, duplicate `DISPATCH_DUPLICATE_IGNORED`. The result contract, independent CHAT review and acceptance boundaries remain unchanged. A dispatch is not an approval to merge or LIVE.

## 7. Negative tests and acceptance evidence for this routing index

| ID | Scenario | Required outcome |
|---|---|---|
| APIX-01 | Older v0.4 Git commit valid, but Bridge v0.5 actually released | Reject v0.4 as active for NEW Bridge WP; bind verified v0.5 |
| APIX-02 | v0.6 Candidate exists without a published manifest | v0.5 remains effective; don't promote candidate |
| APIX-03 | Newer RELEASED_EFFECTIVE document appears after prompt authored | STOP old handoff, CHAT refreshes source lock before execution |
| APIX-04 | Policy v1.8.4 remains effective while Bridge v0.5 releases | Use Policy v1.8.4 + Technical v0.5; independent versioning |
| APIX-05 | Copilot has Git access but no Trading Library | Use CHAT's verified source lock; mark own Library freshness verification unavailable |
| APIX-06 | Git artifact found without matching Library release/readback | SOURCE_PENDING or BLOCKED_SOURCE_VERSION, no executable dispatch |
| APIX-07 | Release manifest and raw byte hash disagree | BLOCKED_SOURCE_VERSION; no fallback |
| APIX-08 | Old WP accepted under original immutable source | Preserve acceptance, no default rework |
| APIX-09 | Standing Bridge review-event branch exists | No DEV/GIT_CODE_PUSH inference |
| APIX-10 | Current public bootstrap WP has v0.5 but BOOTSTRAP_GATE_A runtime tests are NOT_RUN | No Agent launch yet; complete BRG-010..040 validation first |
| APIX-11 | A file listing has `next_cursor` or incomplete scope | Continue inventory or mark CURRENT_RELEASE_UNKNOWN, fail closed |
| APIX-12 | Prompt refers both v0.4 and v0.5 as current Bridge baseline | Fail consistency check; v0.5 wins for new Bridge handoff |


Additional architecture-stage checks:

| ID | Scenario | Required outcome |
|---|---|---|
| `ASX-01` | Technical source defines automated target, capability not yet built, CHAT presents manual fallback as project default | REJECT; classify BOOTSTRAP/FALLBACK and retain target transition |
| `ASX-02` | WP builds the missing infrastructure but routing requires that infrastructure to execute itself | REJECT circular gate; bounded BOOTSTRAP_PATH allowed if independently authorized |
| `ASX-03` | Target gate is already PASS but new equivalent WP keeps historical fallback without new blocker | REJECT STALE_FALLBACK |
| `ASX-04` | Unrelated missing gate blocks an isolated WP | REJECT OVERBLOCKING; evaluate materiality |
| `ASX-05` | Applicable Technical Spec not resolved before mechanism choice | BLOCKED_ARCHITECTURE_UNKNOWN |
| `ASX-06` | Agent chosen first, task reshaped afterward to fit Agent | REJECT ROUTING_ORDER |
| `ASX-07` | Material target/dependency changes after assignment | Preserve unaffected evidence; rerun stage alignment for affected WP |
| `ASX-08` | Fallback attempts to bypass safety/access/merge/LIVE restriction | BLOCK |

**Acceptance status of tests:** design-only negative test matrix; no operational Agent/Bridge test execution or Gate A verification is claimed by this index.

## 8. Release and transition notes

- V1.2.5 supersedes V1.2.4 for **NEW/re-scoped FOX2 prompts**. V1.2.4 remains immutable history.
- New mandatory routing input: `ARCHITECTURE_STAGE_ALIGNMENT_PRECHECK` from Policy V1.8.4 C1.2. Latest-source freshness and CHAT-FIRST remain mandatory and are not replaced.
- Existing accepted immutable results retain their original source/routing history. Open/non-executed WPs use V1.8.4/V1.2.5 at their next executable handoff.
- Bridge Technical v0.5 is separately released because trust/Gate-A execution mechanics changed. SFR-010 Technical Spec, BRDs/Data Contract/Acceptance and M1 technical/roadmap sources remain unchanged.
- The index creates no BRG-003/SFR/P2 DEV permission, no Git code push, no automated Bridge dispatch, no merge and no LIVE.

## 9. Owner CHAT-FIRST allocation gate — V1.2.5

Mandatory source: released FOX2 Policy V1.8.4 §C1.2/§C2A.7 + Owner's Shared Governance directive `/Trading/00_Governance/TRADING_CHAT_FIRST_AGENT_ALLOCATION_OWNER_DIRECTIVE_20261013.md`. For every new or re-scoped Agent prompt, CHAT must first complete independently available remote GitHub/Library/Issue/commit/blob/manifest/Policy work. An Agent must not be assigned a remote repository metadata task merely to echo information available to CHAT via authenticated connectors. An existing local-Agent source-check of *received immutable bytes* and own-branch Git push as part of authorized programming remain valid distinct requirements.

**Handoff STOP examples (design only):** `CFH-01` Agent prompt asks Copilot to search remote GitHub Issues/Policy even though CHAT has already verified exact refs → ROUTE_BACK_TO_CHAT; `CFH-02` CHAT tool blocked by safety and prompt tries Agent as workaround → BLOCK; `CFH-03` Windows-only worktree collision check → COPILOT/CODEX if eligible; `CFH-04` actual authorized code/test with own-branch Git push → eligible CODEX/COPILOT; `CFH-05` Agent claims ChatGPT Library release independently without Library access → BLOCKED_SOURCE_ATTESTATION; `CFH-06` old/superseded Policy pinned prompt starts a new task when V1.8.4 is already released → BLOCKED_SOURCE_VERSION. Tests are NOT_RUN.

This derivative index is document-only and does not grant BRG-003 import, SFR/P2 DEV, Git code push, branch protection, merge, auto-dispatch or LIVE. Do not version-bump unrelated SFR/BRD/M1 sources merely because Bridge v0.5 changed. Each future Agent handoff must bind the exact applicable source lock and architecture-stage record.
