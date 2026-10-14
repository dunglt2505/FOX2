# FOX2 — CHAT Preflight Intake Checklist v1.1

**Status:** RELEASED_EFFECTIVE  
**Scope:** all new/re-scoped executable FOX2 WPs  
**Source resolution:** Project Dictionary v1.2 -> Policy V1.8.9 -> Routing V1.3.0 -> PreExec Evidence Protocol v1.1.

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
