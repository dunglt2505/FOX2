# FOX2 — CHAT Preflight Intake Checklist v1

**Status:** RELEASED_EFFECTIVE  
**Scope:** all new/re-scoped executable FOX2 WPs  
**Source resolution:** Project Dictionary v1.1 -> Policy V1.8.8 -> Routing V1.2.9 -> PreExec Evidence Protocol v1.

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

5. **Agent readiness**
   - candidate Agent/product/model policy/tier/reasoning/permission is supported by the Dictionary;
   - successful probe demonstrates execution availability without product-code mutation;
   - probe failure does not silently trigger Agent substitution.

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

`FOX2_CHAT_PREFLIGHT_INTAKE_V1=RELEASED_EFFECTIVE / PRE_DISPATCH=YES / REMOTE_READBACK_REQUIRED=YES / AGENT_RESULT=NO`
