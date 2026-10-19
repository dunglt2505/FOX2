# FOX2 — POLICY V2.0.0 | OWNER SUPREMACY · CODE-FIRST · CHAT-FIRST · RISK-PROPORTIONATE GOVERNANCE

**Document ID:** `FOX2-POLICY-V1` (same Policy family, major version 2)  
**Version:** `2.0.0`  
**Project:** `FOX2 ONLY`  
**Owner decision date:** `2026-10-19`  
**Publication classification:** `OWNER_APPROVED_POLICY_SOURCE / GIT_LIBRARY_RELEASE_AND_MACHINE_POINTER_TO_BE_ATTESTED_SEPARATELY`  
**Semantic predecessor:** `docs/governance/FOX2_POLICY_V1.8.9.md` (released Policy v1.8.9)  
**Companion authority:** Owner's explicit 2026-10-19 directives: (1) CODE-FIRST, CHAT-FIRST, no default WORK; (2) Owner is supreme project authority entitled to decide and authorize bypass of internal FOX2 governance blockers; (3) CHAT tasked to aggregate and publish a new Policy.  
**Operational direction:** This Owner instruction supersedes any conflicting earlier *project planning and internal approval* position from its date; the Git file alone does not assert Dictionary migration, a cryptographic Owner signature or completed runtime execution.

> **Governing principle.** Coding is the default when its task, permissions and development environment are sufficiently controlled. Governance supports safe product delivery, not a self-perpetuating administrative workstream. The Owner is the final decision authority on FOX2 internal rules and may expressly approve their exception/waiver/bypass. A waiver changes permission for a future action; it never changes what physically happened, fabricates a test PASS, supplies unavailable technology, grants third-party rights or erases durable records.

## 1. Authority hierarchy and Owner Override

1. The **Owner** is FOX2's **highest internal decision, approval, priority, exception and release authority**. CHAT is the delegated governance coordinator, source/routing/acceptance owner and default direct executor of non-host work; CODEX/Copilot are implementation agents; WORK is an independent reviewer only when required. No Agent, Bridge worker, previous task document or release checklist may countermand a later sufficiently specific Owner decision within FOX2.
2. The Owner may **approve, reject, waive, bypass, narrow or replace any FOX2-internal gate**, including routing order, pre-execution checks, review/admission sequence, work packaging, a temporary HOLD, independent audit requirement or delivery method. This may be one-off or a documented standing exception for a **defined class of work**. The scope and effective time of the decision govern; it must not be silently generalized to unrelated tasks or destructive actions.
3. A statement that the Owner *has* override authority is **not itself a command to execute all currently BLOCKED actions**. The Owner may specify `OVERRIDE_APPROVED` for named blockers or set a standing lower-risk DEV exception. CHAT must apply an explicit Owner-approved scope immediately without soliciting duplicate approval. If the exact action is not inferable, CHAT may prepare the safe portions but must not invent the omitted irreversible operation.
4. An Owner Override is a **decision authorization, not technical evidence**: `OVERRIDDEN_FOR_EXECUTION` and `TECHNICALLY_PASS` are separate fields. A past `FAIL`, `BLOCKED`, `NOT_RUN`, consumed identity, failed test or missing legal right MUST NOT be relabeled `PASS`. Existing immutable Git evidence remains intact.
5. Owner authority governs **FOX2 internal decisions**, not external contracts/laws, platform access, brokerage/provider entitlements, machine impossibilities, or actions prohibited by higher-level system safety and security requirements. A user-requested risk acceptance does not grant permissions at an external provider or eliminate real-money side effects.
6. A specific, current Owner override takes precedence over older FOX2-internal Policy or task STOP language **to the extent of the expressly covered action**. CHAT records the interpretation and ensures residual safety controls are visible. A global Dictionary/Registry version pointer changes only by its real publication process; source bytes and authorization must never be conflated.

## 2. Required minimal override record (fast, same-WP; not a new micro-WP)

When invoking an Owner exception, CHAT records in the existing WP/owner directive or concise append-only receipt:

```text
OVERRIDE_ID            unique within FOX2
OWNER_AUTHORITY        exact directive or source-ref + date
WP / ACTION            exact Whole-WP, operation and permitted scope
GATE_OVERRIDDEN        exact named rule/STOP/blocker and its historical status
REASON                 delivery benefit, risk acceptance and alternative safeguard
ACTOR / MODEL          CHAT, CODEX/Copilot or host (if relevant)
PATHS / ENVIRONMENT    bounded files, branch/worktree, sandbox/offline or installed runtime
DURATION / REUSE       once, stated period, or defined standing low-risk class
NO_FALSE_EVIDENCE      historical failure/test/dispatch truth preserved
CHECKPOINT             required review/result/source readback after action
```

The Owner's exact instruction in the active conversation may be the primary approval evidence. The record is prepared by CHAT as a faithful transcription, **not a fabricated cryptographic signature**; publishing a JSON/Markdown file does not by itself prove external signer authentication. Avoid duplicative Owner prompts and elaborate approval bureaucracy for the same bounded scope.

**Override lifecycle:** `REQUESTED -> OWNER_APPROVED -> RECORDED -> ACTION_ATTEMPTED -> RESULT_VERIFIED | FAILED | UNKNOWN`. The state `OWNER_APPROVED` must not be confused with `ACTION_COMPLETED`.

## 3. CODE-FIRST product priority and stage-specific gates

**P0 — Product:** finish existing `FOX2-M1-A-APP-BATCH-B` into a runnable localhost offline React/backend product: UI/typecheck/build/API/watchlist/negative/security/acceptance. The prior `BRIDGE_FIRST -> APP_WAIT_BRIDGE_READY` scheduling requirement is superseded by Owner on 2026-10-19; keep the original directive as historical evidence.

**P1 — Bridge:** consolidate `MANUAL_LOCAL`, paused/stop controls, singleton, recovery and installation into the existing Bridge infrastructure Whole-WP. A Bridge-only blocker must not automatically stop unrelated offline coding.

**P2 — Integration/Release:** certify tested product and installed Bridge/Canary only at the relevant checkpoint. Provider/broker/LIVE remain separate technical/entitlement/risk decisions, not implied by `FULL_ACCESS`.

The three material gate families are:
- **DEV:** correct task/code rights, scoped non-main source/worktree, a single material writer, usable Agent/toolchain and result delivery; only capabilities actually used by the chosen route are material. Apply project-wide PreExec v1.1 unless a specific Owner Override waives/modifies that internal requirement. For a truly independent native CLI DEV route, installed Bridge worker PAUSED/singleton is **not** a material prerequisite. Do not claim a route has been implemented without source/host proof.
- **INTEGRATION:** actual build/test/API/UI negative and security evidence, source/fixtures, CHAT result/diff review. Owner may accept defined unrun cases as `OWNER_WAIVED`, not `PASS`; report coverage honestly.
- **OPERATIONAL/RELEASE:** installed runtime ownership, durable claim/no-replay, recovery, pre-Canary independent review when required, actual provider rights and release evidence. Owner may approve exceptions to internal review or sequencing explicitly; retain evidence of technical risks and side-effect exposure.

## 4. CHAT-FIRST execution and WORK exception policy

CHAT must do directly, with available authorized connectors and readback:
- current Git/source and release manifest inspection, hash/byte verification, Dictionary/Policy/BRD/Tech Spec and source-impact analysis;
- architecture and requirements, Whole-WP plan/roadmap updates, bounded prompt/handoff design, owner decisions, conflicts, code scope and candidate/release publication;
- source/Library sync where the actual connector permits, release status reconciliation and ordinary report/test/diff review;
- routing R0–R7/PreExec intake (or authorized override interpretation), acceptance `ACCEPT/REWORK/HOLD`, project status and next action.

Do not assign WORK just because the task is long, has many files, involves static checks, reports, manifests, a Registry, an ordinary code review, a planning document or an available connector operation.

WORK is exceptional for **substantive independent judgment** (critical concurrency/race/recovery and real financial safety, genuinely contested independent source authority, or a pre-Canary/release independent checkpoint). The assignment MUST name the precise independent question, source, deliverable, non-duplicated evidence and acceptance criterion. Do not use WORK as a replacement for Windows host operations or as a proxy for CHAT. The Owner can approve an explicit audit bypass with recorded residual risk.

CODEX/Copilot or a properly authorized host perform code implementation, build/tests, Windows process/installer and installed runtime work where CHAT cannot execute them. CHAT finishes its own feasible portion before handing over the residual host/code actions.

## 5. Whole-WP continuity, credit efficiency, progress

1. Preserve existing `APP-BATCH-B` and Bridge Whole-WPs. Never create an Owner-facing micro-WP just to fix metadata, evidence formatting, a transient preflight observation, an already known control defect or an administrative HOLD.
2. Fix a real systemic defect once, with the minimum justified code change and regression tests. Record `REQUESTED` / `NECESSARY_DEPENDENCY` / `JUSTIFIED_GENERATED` for material diff hunks; reject drive-by unrelated edits.
3. Optimize costs/tokens **after** correctness and safety: reuse verified immutable evidence, no redundant marker probes, repeated generic audits or unnecessary transfers across CHAT→WORK→CHAT.
4. Track product output as code implemented, real tests run, functional offline startup and accepted results. Do not present document counts or Dispatch publication as product delivery.

## 6. Project Dictionary / sources / machine compatibility

The Project Dictionary v1.2 continues to be the controlling machine identity registry **until a newer Dictionary revision is genuinely published and its generated bindings/consumers validated**. A new human Policy text alone does not update runtime pointers.

For new machine bindings:
- retain canonical current/supported legacy Dispatch schemas, control branches, Git-first paths and machine enums from the active Dictionary; never hard-code a competing "current" value;
- a Policy version transition is `SEMANTIC_SOURCE_CHANGE` with a Dictionary identity pointer update, manifest/hash update and generated binding drift checks for affected runtime consumers; do not silently bump business BRDs with no semantic change;
- unsupported execution path/schema is a technical limitation, not a rationale to lie in evidence. Owner may authorize a **different explicit, legitimate native DEV workflow** after host validation rather than mislabeling the original installed Bridge route;
- preserve immutable earlier candidate/receipt/Dispatch SHA histories and release/supersession mapping.

## 7. Agent selection, permission and Git delivery

1. CHAT routes the least-cost capable actor based on material complexity and current evidence. Prefer Copilot Native Auto for well-specified routine implementation where currently usable; Codex pinned Medium for complex work; High only for risk/concurrency/security/broker semantics. Preserve exact pinned tuple unless CHAT/Owner explicitly changes it.
2. Default `FULL_ACCESS` maps to the current actual CLI's fully permissive development sandbox. It is a **technical capability** and never automatically grants external provider entitlements, Git main/merge, broker orders or production deployment.
3. Every non-overridden executable handoff binds exact WP/Owner scope, source/task commit, model/effort/permission, execution path, delivery owner, worktree, allowed code/report files, `max_runs=1`, tests, failure policy and Git destination.
4. Ordinary DEV code may be pushed to its authorized non-main branch by the selected Agent; CHAT remote-reads code/diff/results, verifies tests and accepts/reworks. Do not select `delivery_owner=BRIDGE` for a genuinely Bridge-independent local run merely to satisfy a historical transport rule.
5. Parallel material coding lanes are limited by the effective Dictionary (currently 2) and must use independent worktrees and disjoint writable files. The Owner can modify internal sequencing/concurrency policy explicitly with an appropriately scoped alternative protection plan.

## 8. PreExec, gate failure and Owner Override

**Default:** shared FOX2 PreExec v1.1 produces a schema-valid durable task-specific receipt before final executable Agent assignment. `PASS` proves only scoped host readiness; `BLOCKED` means one or more current material prerequisites failed; `INFRA_FAILED` means evidence machinery failed. Readback and capability classification must be truthful.

**Override:** the Owner may explicitly authorize an execution **despite** a prior internal `BLOCKED`/PreExec failure/NOT_RUN gate or may waive a named nonmaterial check for a defined offline DEV class. CHAT records `OWNER_OVERRIDDEN_GATE`, the original receipt, exact risk, separate controls, scope and outcome; it MUST NOT publish `PASS` for an unpassed check or impersonate the former source version. The resulting execution status is `AUTHORIZED_BY_OWNER_OVERRIDE`, not `PASS_TO_ASSIGN` unless normal PASS was actually achieved.

**PreExec versus Route:** if the selected native offline DEV workflow does not use installed Bridge, no Bridge-specific lock/PAUSED probe may be made a DEV material prerequisite solely because another Bridge task is blocked. Conversely, a Bridge `e2e-once` run still depends on actual Bridge admission unless Owner authorizes a different real execution architecture.

**No invented bypass:** an Owner Override can waive an *internal decision gate* but cannot force a CLI binary to exist, repair wrong source code, atomically acquire an OS lock which is held by another process, or erase a prior executed Agent call. A host that cannot truthfully execute an approved exception reports `TECHNICALLY_UNAVAILABLE` with a minimal remediation.

## 9. Durable claim, one-writer, post-start recovery

- Preserve the historical consumed/unconsumed identity of every Dispatch. Never relabel a consumed `Dispatch001` or `Canary009` as unused and never modify its immutable source by pretending an Override rewrites history.
- Prior to a high-risk or once-only Agent start, use a source-proven durable claim/attempt identity and compatible singleton/writer protection, or an expressly Owner-approved alternative with the concrete duplicate/side-effect risk recorded. New authorized **attempt** identity is distinct from automatic replay of an old consumed Dispatch.
- After ambiguous launch, timeout, worker crash or report loss: status `NEEDS_RECONCILIATION`; inspect actual outputs/ledgers/branches before taking a new action. An explicit Owner risk decision can authorize a new attempt only after stating what was observed/unknown; never silently repeat live/broker/order side effects.
- Any waiver of review, preflight, publication sequencing or writer coordination is scoped and traceable. The unperformed check remains `WAIVED` / `NOT_RUN`, never `PASS`.

## 10. Release and external effects

1. **Source publication:** Git commit/branch + exact byte/hash verification; Library publication requires actual destination bytes and readback. A Git push is not a Library sync receipt; a Library upload is not a version identity promotion.
2. **Policy effectivity:** require Owner-approved source content, publish/readback, and an unambiguous release manifest/source authority for the intended scope. Global machine effectivity requires the actual Dictionary/Registry and generated runtime pointers to be updated or a documented compatible transition. Until then this version is an Owner-approved published policy *source* with a not-yet-adopted machine pointer.
3. **Owner override of internal release sequence:** possible with explicit scope/risk and honest notation `RELEASE_BY_OWNER_EXCEPTION`; it never forges the independent audit or unrun test or external licenses. Do not silently publish a globally `EFFECTIVE` machine version from a self-described label.
4. Main/merge/deploy/real provider access/broker write/LIVE are separate consequential actions, requiring **specific explicit Owner instruction** and actual technical/external permission. This general declaration of Owner supremacy is not itself a production order or unrestricted provider right.
5. A change to governing documentation must not alter already executed immutably bound WP semantics retrospectively. Historical evidence stays available.

## 11. Current 2026-10-19 disposition and first execution priorities

- APP-BATCH-B source branch `work/FOX2-M1-A-APP-BATCH-B` @ `51a97bfa7420efa0a0e0ea9a1f35f77d2e823613`; the Owner has approved the offline APP product priority/code scope. Native DEV implementation not yet observed after this directive.
- Master Plan Code-First amendment is on `work/FOX2-CODE-FIRST-CHAT-FIRST-chat-20261019`; its semantic order supersedes 2026-10-17 BRIDGE_FIRST scheduling.
- Manual Admission infrastructure WP `work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019` has historical BLOCKED preflight @ `1ce109b9a4c538b255c6d8ffc6be8b4dccecf65d` from Bridge bootstrap controls. CODEX probe PASS for that WP only.
- Original compatibility Dispatch001 `work/FOX2-DISPATCH-chat` @ `3f885b2d24cb131b5e96dfdb67a44677599197e2`: PUBLISHED/HOLD. Canary009 `work/FOX2-BRIDGE-FINAL-CANARY-009` @ `501822a33ef08c7365154913bbc677544856eee5`: HOLD. This policy does not silently activate either.
- Immediate delivery sequence: CHAT chooses controlled native APP DEV, resolves current source/Owner path scope and uses project-wide preflight or an **expressly authorized Owner Override of a named internal gate**; CODEX implements and tests the existing product WP; CHAT accepts actual Git result. Bridge defect work may proceed separately only with a verified independent path or a specifically recorded Owner Override.
- WORK is NOT_NEEDED for normal planning, Git/Library checks or routine acceptance; use only at a material independent checkpoint or by Owner request.

## 12. Source/release compatibility and supersession record

**Supersession claim:** Policy v2.0.0 replaces the **human-level operating direction** of v1.8.9 where they conflict, after this explicit Owner approval. It does not silently rewrite the Dictionary v1.2 `current.policy=1.8.9`, generated `project_dictionary.py` or immutable RC1 trust bundle. These are tracked compatibility dependencies for machine adoption, not reasons to suspend unrelated authorized offline product work.

**Explicit non-effects:** No hidden implementation run, no installed runtime replacement, no source hash rewrite, no fabricated past PASS, no audit impersonation, no actual main/merge/provider/broker/LIVE execution and no implicit dispatch replay.

```text
POLICY_ID=FOX2-POLICY-V1
POLICY_VERSION=2.0.0
OWNER_SUPREMACY=APPROVED
OWNER_OVERRIDE_AUTHORITY=ALL_FOX2_INTERNAL_GATES_WITH_EXPLICIT_SCOPE
CODE_FIRST=YES
CHAT_FIRST=YES
WORK=INDEPENDENT_AUDIT_EXCEPTION_ONLY
WHOLE_WP_CONTINUITY=YES
DEV_BRIDGE_DEPENDENCY=ROUTE_SPECIFIC_NOT_GLOBAL
HISTORICAL_BLOCKED_REMAINS_BLOCKED=YES
OVERRIDE_EXECUTION_STATE=SEPARATE_FROM_TECHNICAL_PASS
MACHINE_DICTIONARY_CURRENT_POLICY=1.8.9_UNTIL_UPDATED
EXTERNAL_RIGHTS_AND_REAL_WORLD_EFFECTS=NOT_IMPLIED
```
