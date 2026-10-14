# FOX2 — CHAT Agent Result Intake & Review (Guide v8 / Policy V1.8.6)

**Authority:** released FOX2 Policy V1.8.6 + Routing Index V1.2.7. This is an operational checklist, not a second Policy and not a merge/DEV grant.

## Intake ordering

1. **Locate immutable remote submission:** verify repo, WP, branch, full remote SHA and ancestry. Review that commit, not a moving branch.
2. **Read required result files at the same SHA:** `report.md`, `evidence_manifest.json`, and material referenced evidence.
3. **Validate source + dispatch binding:** Policy V1.8.6, Routing V1.2.7, exact task/source lock, Agent/model/permission, execution path, delivery owner, branch/base, allowed paths and Git grants.
4. **Validate publication ownership:** ensure only the dispatch-authorized owner published the result. Agent-owned delivery requires `git_code_push=YES + delivery_owner=AGENT`; Bridge-owned delivery requires `git_code_push=YES + delivery_owner=BRIDGE`. Duplicate publication path -> `REWORK/BLOCKED`.
5. **Independently diff exact base -> result SHA:** reconcile all ADD/MODIFY/DELETE paths with allowlists and report.
6. **Validate each material claim:** tests/evidence IDs must resolve to real bytes; NOT_RUN cannot become PASS.
7. **Apply Material Tool Compatibility Rule:** version mismatch alone is not failure. Verify task-material capabilities and required tests. Non-material deviation may remain recorded; missing/unknown material capability blocks/holds.
8. **Check permission evidence:** requested Full Access or other bound profile must match effective execution evidence when material. Silent downgrade -> `REWORK/BLOCKED`.
9. **Check runtime failure semantics:** a post-start uncertain non-zero must not have been blindly replayed or silently substituted.
10. **Check security/domain restrictions:** secrets, private data, licensed/raw feeds, unauthorized Production/provider/broker/LIVE activity remain blocking.
11. **Issue independent CHAT decision:** `ACCEPTED`, `ACCEPTED_PARTIAL`, `REWORK`, or `BLOCKED`, with next actor/gate.

## Decision rules

- `ACCEPTED`: all in-scope required acceptance evidence verified; no unresolved blocking risk.
- `ACCEPTED_PARTIAL`: accepted sub-results are explicit; WP remains open where required.
- `REWORK`: credible repairable discrepancy in implementation/evidence/contract.
- `BLOCKED`: authority/source/security/scope/remote-verification conflict.
- `PUSHED_UNREVIEWED`: delivery state only.

## Anti-fragmentation review rule

Do not create a new Owner-facing corrective WP merely for:

- staging/index cleanup;
- rerunning a validator;
- a non-material tool/runtime version difference;
- local metadata reconciliation;
- one regenerated evidence file when the shared pipeline is already scheduled for a consolidated systemic fix.

Open a separate corrective WP only for a genuine ownership/dependency/authority/safety/architecture boundary or when isolating the defect is necessary for correctness.

## Git delivery validation

```text
delivery_owner=AGENT
=> verify Agent-owned commit/push is within exact grant and scope

delivery_owner=BRIDGE
=> verify Bridge-owned commit/push is within exact grant and scope
```

CHAT must not publish a second copy of an already valid delivered result.

## Non-circular proof

The manifest inside the commit does not embed its own containing commit SHA. CHAT uses the external immutable remote SHA after push.

## Efficiency

Read report + manifest first. Fetch only evidence material to acceptance, negative controls and residual risk. Reuse still-valid evidence on identical bytes. Do not demand unnecessary transcript dumps.

## Final intake marker

`CHAT_INTAKE_GUIDE=V8 / POLICY=V1.8.6 / ROUTING=V1.2.7 / DELIVERY_OWNER_CHECK=REQUIRED / MATERIAL_TOOL_COMPATIBILITY=REQUIRED`
