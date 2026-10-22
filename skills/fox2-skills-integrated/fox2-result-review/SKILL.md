---
name: fox2-result-review
description: Review immutable Agent output, code diff, tests and receipts.
---

# fox2-result-review

## Agile Lite Owner-approved precedence

Policy v2.1.0 and `../shared/operating_rules.md` govern ordinary internal project work. Use one Kanban task with real output, proportionate checks and CHAT acceptance. Historical R0-R7, PreExec receipts, source-locked Dispatch and extra review apply only when the chosen technical transport or consequential action requires them. Preserve specialized analysis, real permissions, historical evidence and no-replay; do not propagate version changes without material consumer impact.

## Activate when
An Agent delivered code/docs/results requiring CHAT intake.

## Work to perform
Verify exact Dispatch identity, immutable base/result commits and Git readback, source lock, path/one-writer rules, test logs and negative cases. Evaluate Standards and Spec separately plus correctness/security/performance. For code diffs, label hunks REQUESTED/NECESSARY_DEPENDENCY/JUSTIFIED_GENERATED/UNEXPLAINED/NOT_VERIFIED; missing diff => HOLD, unrelated changes => REWORK. Check excluded tests/fixtures; never let green tests override unauthorized edits.

## Completion / stop
CHAT_ACCEPT/REWORK/HOLD with cited evidence and uncovered surfaces; never call PUSHED_UNREVIEWED released or audited.


Completion is governed by the **Execution Contract v0.3.6** below; apply conditional obligations only when triggered, report bounded HOLD otherwise.

## Execution Contract v0.3.6 — observable completion
- **TRIGGER:** Agent result return or request to accept code/docs/evidence for an existing immutable task.
- **PRECONDITIONS:** Original task/prompt/source SHA, Git result pointer and scope/allowed paths; no NEW assignment generated for normal return.
- **REQUIRED_ACTIONS:** Remote-readback result commit, report/evidence, diff/test logs, writer/permissions and K1 classifications; issue CHAT-owned verdict.
- **REQUIRED_EVIDENCE:** Actual Git result SHA and committed `report.md`/`evidence_manifest.json`, ancestry/diff/tests and proof/unknown boundaries.
- **DELIVERABLES:** Independent `CHAT_ACCEPT`/`REWORK`/`HOLD` receipt with uncovered surfaces and NEXT_SAFE_ACTION.
- **VALIDATION:** Compare result to immutable task/acceptance; no inference from green tests or Agent DONE without real Git.
- **FAILURE_STATE:** `DELIVERY_BLOCKED` / `NEEDS_RECONCILIATION` / `RESULT_REVIEW_HOLD` when delivery or provenance absent.
- **COMPLETION_GATE:** CHAT acceptance only after all applicable evidence verified, or bounded REWORK/HOLD; Git pushed is still PUSHED_UNREVIEWED otherwise.
## Mandatory Git-first closed loop
Start from original Git-published immutable task/prompt/Dispatch source identity; fetch prompt commit/blob SHA-1/SHA-256, approved source set and Owner scope. Fetch actual Agent pushed result commit from its authorized non-main branch; compare ancestry, changed paths, one-writer, report.md + evidence_manifest.json against Dictionary-resolved result contract, real logs/tests, K1 diff and secrets. The Agent must supply observed remote commit SHA OUTSIDE committed report (avoid impossible self-reference); CHAT independently remote-readbacks it. Missing prompt/result/evidence = HOLD / DELIVERY_BLOCKED / NEEDS_RECONCILIATION, not ACCEPT. Record CHAT_ACCEPT/REWORK/HOLD as **separate CHAT-owned review receipt**, then issue next Git-first task if necessary; `PUSHED_UNREVIEWED` is not acceptance.

## Intake-to-next-action ownership
CHAT directly fetches Git code, report, evidence and tests when connectors permit, records ACCEPT/REWORK/HOLD, and performs the next *authorized safe* step without asking Owner to repeat the original task. After REWORK, prepare only the bounded correction and reissue via a new eligible Git-first task if gates permit; never replay the consumed attempt. HOLD only the blocked operation and state the exact missing evidence; routine result review alone never requires WORK.

## Audit result delivery and stage update (v0.3.5)
For any WORK/CODEX/Copilot result, verify the original Git task/prompt SHA, actual result branch+commit, `reports/<WP_ID>/report.md`, `reports/<WP_ID>/evidence_manifest.json`, contract-specific test/audit evidence, Git remote readback and independent CHAT-owned receipt. For read-only WORK audit: code diff/tests are `NOT_APPLICABLE` only with justified audit scope, not synthetic PASS. Report-only Git commit is allowed where authorized. If WORK lacked push access, obtain real file bytes by authorized channel, record WORK as author and CHAT as publisher and verify resulting remote Git SHA before `CHAT_ACCEPT`; missing artifact => `DELIVERY_BLOCKED`/HOLD rather than a chat-only pass. A returned report isn't a new assignment; Prompt Builder applies only if CHAT issues a fresh bounded REWORK/task under material gates.
Once accepted, check whether an opened feature's Stage/Status/Evidence changed; update lazy feature status only with supported evidence and authorized write, not just WORK opinion. Continue `NEXT_SAFE_ACTION` without redundant Owner approval.


## v0.3.7 — Domain-specific bounded recovery
Deliver `DEFECT_SLICE`: first failure, affected paths/consumers, earlier still-applicable PASS, later NOT_RUN, minimum patch, focused tests and independently mandatory gates. One downstream FAIL does not retrospectively erase accepted build; old PASS does not certify new source. CHAT result verdict remains separately required.


## v0.3.7 — Project-wide focused correction and PASS preservation
FOX2 all stages: earliest causal divergence. Accepted PASS is REUSE_VERIFIED by default; no blanket recheck. Retest only changed fact→affected gate or mandatory gates. CONSUMED Attempt cannot replay; accepted PASS evidence from it is reusable. NOT_RUN/UNKNOWN remain scoped.
