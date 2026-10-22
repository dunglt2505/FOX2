---
name: fox2-source-resolver
description: Discover source claims and verify Git bytes separately from governance authority.
---

# fox2-source-resolver

## Agile Lite Owner-approved precedence

Policy v2.1.0 and `../shared/operating_rules.md` govern ordinary internal project work. Use one Kanban task with real output, proportionate checks and CHAT acceptance. Historical R0-R7, PreExec receipts, source-locked Dispatch and extra review apply only when the chosen technical transport or consequential action requires them. Preserve specialized analysis, real permissions, historical evidence and no-replay; do not propagate version changes without material consumer impact.

## Activate when
Any new or materially changed FOX2 task/source binding, or query about Policy/Registry/Dictionary/BRD provenance and effective status.

## Work to perform
Locate authorized Registry anchor (not chosen by file name), manifest, immutable Git SHA/path, file digest and supersession; independently validate signer/approval via actual trust root. `shared/git_resolver.py` only verifies Git source claim, not owning authority; if unavailable use connector read-only comparison and disclose limits. A self-declared authority label is not an approval.

## Completion / stop
Separate SOURCE_BYTES_VERIFIED, AUTHORITY_VERIFIED and EFFECTIVE; else AUTHORITY_UNVERIFIED or proven SOURCE_CONFLICT, never fabricate release.


Completion is governed by the **Execution Contract v0.3.6** below; apply conditional obligations only when triggered, report bounded HOLD otherwise.

## Execution Contract v0.3.6 — observable completion
- **TRIGGER:** Any new/re-scoped task source binding or question about Policy/Dictionary/BRD/Registry authority/effectivity.
- **PRECONDITIONS:** Exact scope, available independent Owner approvals and Registry/Dictionary/release chain.
- **REQUIRED_ACTIONS:** Resolve precedence/supersession/identity before immutable SHA; distinguish human operating approval, published effectivity and installed enforcement.
- **REQUIRED_EVIDENCE:** Actual Git path/commit/blob SHA-256, authority provenance and any competing source claims.
- **DELIVERABLES:** Source selection with SHA/source-set and separate `SOURCE_BYTES_VERIFIED`/`AUTHORITY_VERIFIED`/`EFFECTIVE` verdicts.
- **VALIDATION:** Validate selected source against approval and release manifests; absent independent authority is UNKNOWN, not conflict.
- **FAILURE_STATE:** `AUTHORITY_UNVERIFIED` / `SOURCE_BYTES_UNVERIFIED` / proven `SOURCE_CONFLICT` as distinct outcomes.
- **COMPLETION_GATE:** Exactly scoped source-binding verdict with evidence; no promoted EFFECTIVE without independently validated release chain.
## Dictionary-first source resolution
For each new/re-scoped WP resolve authorized Registry → Dictionary identity and release manifest → semantic BRD/TechSpec/Policy/Contract/Protocol versions/paths. Latest filename or branch HEAD is not authority. Verify immutable SHA-256 and independent Owner/trust chain; only then freeze a source-set for the specific task and record compatible generator/schema/normalizer consumers. Preserve original lock on in-flight Dispatch. Missing trust root => `AUTHORITY_UNVERIFIED` and honest bounded preparation, not a fabricated current EFFECTIVE label.

## New Task Source Binding (R2, selection → immutable lock)
At each *new or materially re-scoped* task, separate **human operating policy selection** from **machine source-contract adoption**:
1. Read the current trusted Registry/Dictionary and release/supersession manifests; also read later explicit Owner directives and scoped human source resolution, checking dates, scope, provenance and affected consumers. Registry lookup is not a veto of a newer, valid Owner decision for planning when the Registry machine pointer is stale.
2. Select newest *authorized and in-scope* source by owner scope/precedence + lineage, not maximum version/filename or branch main. Treat Policy v2.0.0 (Owner-approved 2026-10-19) as `OWNER_APPROVED_PRINCIPLE` for prospective FOX2 human CODE-FIRST/CHAT-FIRST planning even if machine Registry still points v1.8.9; preserve v1.8.9 as historical/machine source until actual adoption. Do not pretend approval applies outside its scope.
3. Report separate status axes: `OWNER_APPROVED_PRINCIPLE` (scoped human operating), `PUBLISHED_EFFECTIVE` (actual document + release/Registry evidence for defined scope), `RUNTIME_ENFORCED` (installed runtime/Bridge compatibility independently tested). An old Bridge pointer does not silently revert Owner human decisions, and an Owner directive does not fake machine capability.
4. For an authorized executable NEW task, after actual stage/route checks and without borrowing a previous Dispatch identity, bind exact Policy/Dictionary/BRD/TechSpec/Protocol/Acceptance path+immutable Git commit+SHA-256 and owner directive evidence. If immutable source set or task authority required by chosen route is missing, `HOLD_EXECUTABLE_BINDING`; continue safe planning only.
5. Keep every existing in-flight task/Dispatch on its original immutable source lock; re-scope only via separate authorized new binding. If multiple files self-claim EFFECTIVE, inspect authority evidence and supersession; only declare `SOURCE_CONFLICT` on proven competing authorities, otherwise `AUTHORITY_UNVERIFIED` or scoped release pending.
**Case anchor:** `docs/governance/releases/FOX2_CURRENT_SOURCE_RESOLUTION_20261019.json` at Git `7c6eb6102faa91149baf3a30bb5d823dcf30cad7` records human Owner-approved Policy 2.0.0, but global machine registry and Windows runtime not attested. Re-resolve live; this pinned anchor is historical evidence, NOT a forever-current registry.


## v0.3.7 — Domain-specific bounded recovery
A code/host/delivery failure is not a source conflict. Reuse exact verified source SHA when unchanged; never silently rebind old Dispatch.


## v0.3.7 — Project-wide focused correction and PASS preservation
FOX2 all stages: earliest causal divergence. Accepted PASS is REUSE_VERIFIED by default; no blanket recheck. Retest only changed fact→affected gate or mandatory gates. CONSUMED Attempt cannot replay; accepted PASS evidence from it is reusable. NOT_RUN/UNKNOWN remain scoped.
