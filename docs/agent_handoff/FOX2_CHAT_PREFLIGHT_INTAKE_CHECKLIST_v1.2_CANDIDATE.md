# FOX2 — CHAT Preflight Intake Checklist v1.2 CANDIDATE

**Status:** CANDIDATE / NOT EFFECTIVE  
**Scope:** all new/re-scoped executable FOX2 WPs  
**Source resolution:** Project Dictionary v1.3 CANDIDATE -> Policy V1.9.0 CANDIDATE -> Routing V1.4.0 CANDIDATE -> PreExec v1.2 CANDIDATE.

CHAT performs this intake **before final executable assignment/Dispatch publication**.

1. **Identity**
   - exact repository/WP/task branch;
   - receipt schema is Dictionary-resolved current schema;
   - exact source/task head matches the task being routed.

2. **Remote publication**
   - receipt exists on exact non-main task branch;
   - exact remote SHA is readable;
   - no `RECEIPT_PUSHED` claim without commit/push/readback evidence.

3. **Worktree/writer**
   - expected worktree identity;
   - no competing material writer;
   - any cleanup was limited to objectively stale preflight evidence.

4. **Capabilities**
   - every task-material prerequisite is PASS;
   - MISSING/FAIL for a material prerequisite -> BLOCKED;
   - UNKNOWN material capability -> HOLD;
   - non-material version mismatch alone does not block.

5. **Agent readiness / route materiality**
   - candidate Agent/product/model policy/tier/reasoning/permission is supported by the Dictionary;
   - individual alternative candidate probes are normally NON_MATERIAL routing evidence;
   - one MATERIAL aggregate capability such as `eligible_agent_route` must PASS;
   - aggregate PASS requires at least one allowed candidate probe PASS;
   - a failed preferred candidate is recorded but does not block if another allowed candidate passes;
   - if the immutable task pins a specific Agent as material, that candidate itself must PASS;
   - successful probe demonstrates execution availability without product-code mutation;
   - probe failure does not silently trigger Agent substitution; CHAT alone selects the final route.

6. **Sanitization/hygiene**
   - no secret/token/credential-bearing URL/raw unrestricted CLI output;
   - canonical UTF-8/LF;
   - receipt shape matches schema.

7. **Dispatch state**
   - `executable_dispatch_published=false`;
   - `dispatch_consumed=false`;
   - `agent_execution_started=false`.

8. **Verdict**
   - `PASS_TO_ASSIGN`: R3/R5 evidence sufficient; CHAT may finalize assignment and publish executable Dispatch;
   - `BLOCKED`: resolve same-WP material blocker; no executable Dispatch;
   - `HOLD_UNKNOWN`: material fact remains unknown;
   - `INFRA_FAILED`: evidence mechanism failed and must be repaired before routing continues.

Preflight intake is distinct from `FOX2_CHAT_RESULT_INTAKE_CHECKLIST_v9.md`, which applies after Agent result publication.

`FOX2_CHAT_PREFLIGHT_INTAKE_V1_1=RELEASED_EFFECTIVE / PRE_DISPATCH=YES / AGENT_ROUTE_MATERIALITY=AGGREGATE / REMOTE_READBACK_REQUIRED=YES / AGENT_RESULT=NO`


## Prior routing question — candidate

Before this checklist, CHAT must record `DIRECT_CHAT_FEASIBILITY`: tool actually available, permission grant, source binding, destination conflict/readback, and any mandatory host or independent-assurance reason. If supported and authorized, CHAT performs the work directly; this Agent preflight checklist is not invoked. If remaining executable work is delegated, existing mandatory PreExec Receipt intake remains exact and non-skippable. Result verdict PASS_TO_ASSIGN is not an authorization to release protected sources.

## Git latest-at-execution — Phase A prospective candidate integration

Status: CANDIDATE_NOT_EFFECTIVE. Applies prospectively only after the required authority and compatibility gates; this amendment grants no runtime/DEV, merge, release or LIVE permission.

1. **Historical references remain valid.** Old version numbers in BRDs, Policy, Specs, Protocols, templates and reports are historical references, not execution pins. Do not rewrite them in bulk merely because a newer version exists.
2. **Refresh live Git before every execution.** At CHAT direct actionable admission, Agent PreExec and dequeue before first claim, automatically contact authenticated GitHub at the authorized Registry location; read current Registry, manifests, publication and supersession metadata and newly published versions. Record observation time, Registry ref/commit and all relevant candidates. If the trusted Registry location or live access is unavailable, record SOURCE_UNVERIFIED / AUTHORITY_UNVERIFIED / GIT_UNAVAILABLE and HOLD dependent execution; cache or Library must never silently substitute.
3. **Choose newest applicable.** Evaluate scope, owning authority, release approval, compatibility and target environment; distinguish LATEST_GIT_OBSERVED from LATEST_APPLICABLE. Record selected and rejected versions with reasons. A newer unqualified version is LATEST_PRESENT_BUT_BLOCKED and goes through the applicable gate; do not silently promote it or downgrade to the version in authored text. A qualified older source requires an explicit, evidenced applicability decision under the gate.
4. **Lock before claim/effect.** Recheck material Registry/source-head drift immediately before first claim or side effect. Drift invalidates affected stale PreExec/routing and requires permitted revalidation before start. Freeze repository, Registry and manifest commits, source path/commit, Git blob and SHA-256 of exact bytes, scope/compatibility verdict and approval evidence into the attempt source lock. Refresh/lock is not a release approval.
5. **Preserve running Dispatches.** Consumed/started Dispatches retain their original immutable source locks; no hot-swap, mutation or automatic replay. Newer sources affect subsequent work or explicit governed stop/reconciliation. Queued unstarted work refreshes and rebinds only before claim, within existing permissions.

Evidence must distinguish REFRESH_PASS, APPLICABILITY_PASS, RELEASE_AUTHORITY_PASS, EXECUTION_PASS and EFFECTIVE_RELEASE_PASS. Static document verification proves none of the runtime or release claims. CHAT result intake compares actual execution to its frozen lock; live discovery for follow-up does not retroactively rebind that execution.

Normative candidate detail: `docs/governance/FOX2_GIT_LATEST_AT_EXECUTION_CONTRACT_v1_CANDIDATE.md`. Source commit/hash must be resolved at execution; this path/reference is not proof that this Candidate is EFFECTIVE.
