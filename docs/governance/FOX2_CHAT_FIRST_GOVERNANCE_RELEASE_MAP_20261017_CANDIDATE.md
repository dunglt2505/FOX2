# FOX2 CHAT-FIRST Governance Release Map
State: CANDIDATE; Git candidate publication is not canonical effective release
Scope: all FOX2 governance operations, not only Skills
Owner authorization: explicit 2026-10-17 CHAT-FIRST delegation in CHAT conversation
Git branch: work/FOX2-CHAT-FIRST-SKILLS-CANDIDATE-20261017

| Family | Historical source | Proposed successor |
| --- | --- | --- |
| Project Dictionary | FOX2_PROJECT_DICTIONARY_v1.json, v1.2 | FOX2_PROJECT_DICTIONARY_v1.3_CANDIDATE.json |
| Policy | FOX2_POLICY_V1.8.9.md | FOX2_POLICY_V1.9.0_CANDIDATE.md |
| Routing | FOX2_AGENT_PROMPT_POLICY_V1_3_0_EFFECTIVE_ROUTING_INDEX_20261014.md | FOX2_AGENT_PROMPT_ROUTING_INDEX_V1_4_0_CANDIDATE_20261017.md |
| Git-first Protocol | FOX2_GIT_FIRST_TASK_RESULT_PROTOCOL_v12.md | FOX2_GIT_FIRST_TASK_RESULT_PROTOCOL_v13_CANDIDATE.md |
| PreExec | FOX2_PREEXEC_EVIDENCE_PROTOCOL_v1.1.md | FOX2_PREEXEC_EVIDENCE_PROTOCOL_v1.2_CANDIDATE.md |
| CHAT Preflight Intake | FOX2_CHAT_PREFLIGHT_INTAKE_CHECKLIST_v1.1.md | FOX2_CHAT_PREFLIGHT_INTAKE_CHECKLIST_v1.2_CANDIDATE.md |
| CHAT Result Intake | FOX2_CHAT_RESULT_INTAKE_CHECKLIST_v9.md | FOX2_CHAT_RESULT_INTAKE_CHECKLIST_v10_CANDIDATE.md |
| Master Plan | FOX2_MASTER_EXECUTION_PLAN_20261014.md | FOX2_MASTER_EXECUTION_PLAN_CHAT_FIRST_ADDENDUM_20261017_CANDIDATE.md |
| Agent Skills | installed FOX2 Skills 17, old shared guidance | skills/fox2-skills-integrated/*/SKILL.md Candidate + package manifest |

## Affected but no semantic changes
BRD-00/06/08 released; BRD-09 candidate; M1 Tech Spec; Market Data Contract; M1 Acceptance; Bridge Technical Spec; Dispatch Schema v3; Result Schema v2; Preflight Receipt Schema v1; Bridge/source branches and worktree ownership. They remain unchanged because routing ownership change does not create business requirements or alter dispatch payload semantics.

## Migration requirements
- Do not mutate immutable released bytes in-place. Produce new versioned sources, release manifest with source commit and exact file SHA-256/blob SHA, and independently trusted Owner authorization.
- Compare old/new to verify intended routing/operational semantics only. Preserve frozen in-flight source bindings; no automatic rebind of consumed dispatch.
- Align Dictionary pointers and generated bindings only after publication and any required host tests. Candidate Dictionary is never current executable identity.
- Publish/mirror authorized sources to /Trading/FOX2 paths with exact-byte readback; plugin cloud package must be updated separately by its publisher.
- Await independently verified trusted host evidence from native_registry.bind and ReleaseChainVerifier when available, before claiming certified EFFECTIVE. Missing provider is AUTHORITY_UNVERIFIED.
- Do not infer release authorization from an ordinary Git commit, self-declared status, Skills output or branch name.

## Test fixtures
Direct source read -> CHAT completes; policy/BRD drafting -> CHAT executes draft; authorized non-main Git documentation update -> CHAT writes + readback; unsafe conflict -> affected path HOLD without blocking other safe paths; pinned runtime engineering -> CODEX with PreExec; independent audit required -> WORK; unknown authority -> prepare conditional material, hold EFFECTIVE; consumed dispatch -> no replay.

## Git latest-at-execution — Phase A prospective candidate integration

Status: CANDIDATE_NOT_EFFECTIVE. Applies prospectively only after the required authority and compatibility gates; this amendment grants no runtime/DEV, merge, release or LIVE permission.

1. **Historical references remain valid.** Old version numbers in BRDs, Policy, Specs, Protocols, templates and reports are historical references, not execution pins. Do not rewrite them in bulk merely because a newer version exists.
2. **Refresh live Git before every execution.** At CHAT direct actionable admission, Agent PreExec and dequeue before first claim, automatically contact authenticated GitHub at the authorized Registry location; read current Registry, manifests, publication and supersession metadata and newly published versions. Record observation time, Registry ref/commit and all relevant candidates. If the trusted Registry location or live access is unavailable, record SOURCE_UNVERIFIED / AUTHORITY_UNVERIFIED / GIT_UNAVAILABLE and HOLD dependent execution; cache or Library must never silently substitute.
3. **Choose newest applicable.** Evaluate scope, owning authority, release approval, compatibility and target environment; distinguish LATEST_GIT_OBSERVED from LATEST_APPLICABLE. Record selected and rejected versions with reasons. A newer unqualified version is LATEST_PRESENT_BUT_BLOCKED and goes through the applicable gate; do not silently promote it or downgrade to the version in authored text. A qualified older source requires an explicit, evidenced applicability decision under the gate.
4. **Lock before claim/effect.** Recheck material Registry/source-head drift immediately before first claim or side effect. Drift invalidates affected stale PreExec/routing and requires permitted revalidation before start. Freeze repository, Registry and manifest commits, source path/commit, Git blob and SHA-256 of exact bytes, scope/compatibility verdict and approval evidence into the attempt source lock. Refresh/lock is not a release approval.
5. **Preserve running Dispatches.** Consumed/started Dispatches retain their original immutable source locks; no hot-swap, mutation or automatic replay. Newer sources affect subsequent work or explicit governed stop/reconciliation. Queued unstarted work refreshes and rebinds only before claim, within existing permissions.

Evidence must distinguish REFRESH_PASS, APPLICABILITY_PASS, RELEASE_AUTHORITY_PASS, EXECUTION_PASS and EFFECTIVE_RELEASE_PASS. Static document verification proves none of the runtime or release claims. CHAT result intake compares actual execution to its frozen lock; live discovery for follow-up does not retroactively rebind that execution.

Normative candidate detail: `docs/governance/FOX2_GIT_LATEST_AT_EXECUTION_CONTRACT_v1_CANDIDATE.md`. Source commit/hash must be resolved at execution; this path/reference is not proof that this Candidate is EFFECTIVE.
