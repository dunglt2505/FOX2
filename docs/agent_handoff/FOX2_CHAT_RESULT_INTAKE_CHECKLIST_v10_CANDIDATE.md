# FOX2 — CHAT Result Intake Checklist v10 CANDIDATE — Dictionary-Bound

**Proposed source resolution:** Project Dictionary v1.3 CANDIDATE -> Policy V1.9.0 CANDIDATE -> Routing V1.4.0 CANDIDATE -> Protocol v13 CANDIDATE. In-flight Agent receipts retain frozen historical bindings.

For every new/re-scoped result intake:

1. **Dictionary identity**
   - read exact Dictionary path/commit/hash bound by dispatch;
   - verify dispatch schema/control/path identity is declared current/supported;
   - verify Policy/Protocol identities match Dictionary.

2. **Immutable delivery**
   - exact repository;
   - exact task branch;
   - full remote result SHA;
   - expected parent/base ancestry;
   - no unexpected history rewrite.

3. **Scope**
   - changed paths inside authorized code/report paths;
   - no frozen semantic source changed without authority.

4. **Execution tuple**
   - Agent Product;
   - model policy/tier/model/reasoning;
   - permission profile;
   - execution path;
   - delivery owner;
   - no silent substitution/downgrade.

5. **Git publication**
   - exactly one publication owner;
   - remote SHA readback equals delivered SHA;
   - no main/PR/merge/deploy unless separately authorized.

6. **Validation**
   - required tests actually PASS;
   - task-material capability checks PASS;
   - evidence resolves all material claims;
   - canonical artifact/text hygiene where applicable.

7. **Failure/replay**
   - post-start uncertainty is not falsely marked success;
   - consumed dispatch not replayed;
   - no Agent substitution.

8. **Semantic boundaries**
   - Dictionary used only for identity/compatibility;
   - Policy/BRD/Contract/Technical semantics remain consistent;
   - no provider/broker/LIVE expansion.

9. **Verdict**
   - ACCEPTED;
   - ACCEPTED_PARTIAL;
   - REWORK;
   - BLOCKED.

A stale in-commit wording such as UNREVIEWED may be non-material when immutable remote evidence proves final delivery state; do not create micro-fix WPs solely for such wording.

`CHAT_INTAKE_V9=DICTIONARY_BOUND / REMOTE_READBACK_REQUIRED / SELF_ACCEPTANCE=NO`


## CHAT direct execution evidence and next routing — candidate

For tasks completed directly by CHAT, collect actual operation authorization, input provenance, before/after destination identity, exact remote commit/byte digest and conflict guard. Do not fabricate an Agent result receipt or trigger any consumed dispatch. For Agent results, CHAT remains independent recipient/intake owner; actual tests and runtime facts remain required, never merely source claims. After review, CHAT itself performs all authorized next safe work before considering another Agent or independent WORK review. `CHAT_DIRECT_COMPLETED` is a work-result classification, not certified release authority.

## Git latest-at-execution — Phase A prospective candidate integration

Status: CANDIDATE_NOT_EFFECTIVE. Applies prospectively only after the required authority and compatibility gates; this amendment grants no runtime/DEV, merge, release or LIVE permission.

1. **Historical references remain valid.** Old version numbers in BRDs, Policy, Specs, Protocols, templates and reports are historical references, not execution pins. Do not rewrite them in bulk merely because a newer version exists.
2. **Refresh live Git before every execution.** At CHAT direct actionable admission, Agent PreExec and dequeue before first claim, automatically contact authenticated GitHub at the authorized Registry location; read current Registry, manifests, publication and supersession metadata and newly published versions. Record observation time, Registry ref/commit and all relevant candidates. If the trusted Registry location or live access is unavailable, record SOURCE_UNVERIFIED / AUTHORITY_UNVERIFIED / GIT_UNAVAILABLE and HOLD dependent execution; cache or Library must never silently substitute.
3. **Choose newest applicable.** Evaluate scope, owning authority, release approval, compatibility and target environment; distinguish LATEST_GIT_OBSERVED from LATEST_APPLICABLE. Record selected and rejected versions with reasons. A newer unqualified version is LATEST_PRESENT_BUT_BLOCKED and goes through the applicable gate; do not silently promote it or downgrade to the version in authored text. A qualified older source requires an explicit, evidenced applicability decision under the gate.
4. **Lock before claim/effect.** Recheck material Registry/source-head drift immediately before first claim or side effect. Drift invalidates affected stale PreExec/routing and requires permitted revalidation before start. Freeze repository, Registry and manifest commits, source path/commit, Git blob and SHA-256 of exact bytes, scope/compatibility verdict and approval evidence into the attempt source lock. Refresh/lock is not a release approval.
5. **Preserve running Dispatches.** Consumed/started Dispatches retain their original immutable source locks; no hot-swap, mutation or automatic replay. Newer sources affect subsequent work or explicit governed stop/reconciliation. Queued unstarted work refreshes and rebinds only before claim, within existing permissions.

Evidence must distinguish REFRESH_PASS, APPLICABILITY_PASS, RELEASE_AUTHORITY_PASS, EXECUTION_PASS and EFFECTIVE_RELEASE_PASS. Static document verification proves none of the runtime or release claims. CHAT result intake compares actual execution to its frozen lock; live discovery for follow-up does not retroactively rebind that execution.

Normative candidate detail: `docs/governance/FOX2_GIT_LATEST_AT_EXECUTION_CONTRACT_v1_CANDIDATE.md`. Source commit/hash must be resolved at execution; this path/reference is not proof that this Candidate is EFFECTIVE.
