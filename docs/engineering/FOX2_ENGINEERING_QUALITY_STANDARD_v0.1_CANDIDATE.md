# FOX2 — Project-wide Engineering Quality Standard v0.1

- **State:** CANDIDATE / NOT RELEASED / NOT EFFECTIVE
- **Scope:** all FOX2 domains, current and future. Do not apply retrospectively to an in-flight source lock.
- **Owner instruction:** Evaluate and deploy selected \`addyosmani/agent-skills\` practices project-wide (2026-10-18).
- **Reference upstream:** \`addyosmani/agent-skills\` at commit \`aeac41d4d005999432bb7312f7ff06383a91d59d\`, tag 0.6.13.
- **FOX2 candidate base:** \`09dc4051e6a308f72a103e879489d275770a8761\` (snapshot, not an authority declaration).
- **Status of verification:** static source comparison only; NO live Agent A/B execution or CI certification yet.

## 0. Precedence and non-effects

The latest *independently trusted* FOX2 Registry, released Policy, approved BRDs and contracts, Routing, Protocol and acceptance are above this engineering candidate. No version string/self-assertion in a file promotes this document to EFFECTIVE. Use actual independent authority before claiming current release; classify \`AUTHORITY_UNVERIFIED\` distinctly from proven conflicting authorities \`SOURCE_CONFLICT\`. Existing Dispatches retain original source locks. This addendum does not authorize coding, host access, deployment, order execution, LIVE, privilege escalation, merges, global CLI installs, or any changes to existing preflight/release behavior.

## 1. Invariants and measured quality floor

For **all** changed artifacts, preserve provenance and distinguish \`PASS\`, \`FAIL\`, \`NOT_RUN\`, \`UNKNOWN\`, \`BLOCKED\` and \`DEFERRED\`. Never fabricate test, source readback, CI, reviewer or release evidence. Track accepted task scope and keep changed paths within the grant; one writer per exact file/worktree. Never weaken/delete tests, disable static analysis, introduce blanket suppressions, or lower thresholds merely to make checks green. Any exceptional change needs exact justification, owned decision, and regression coverage.

Choose baselines by reading the project's actual test/build/config and historical accepted evidence. Do not invent repository-wide coverage, performance, accessibility, latency, token or file-size thresholds. Proposed thresholds must be separately adopted with the applicable owner and then enforced by CI; candidate values may be recorded as \`UNSET_UNTIL_MEASURED\`.

## 2. Six complementary practices

### E1 — Constraints and quality ratchets
Read actual test runner, lint, build, CI, risk checks and source matrix. Capture current baseline and changed-surface exposure. Block unapproved \`skip\`/\`xfail\`, deleted failing tests, unimplemented stubs, broad \`noqa\`/\`eslint-disable\`/\`ts-ignore\`, missing secrets redaction or removed acceptance, as appropriate to the technology. False positives require a scoped, evidenced exception; they do not imply deleting the gate. No new \`CONSTRAINTS.md\` becomes authority without proper publication.

### E2 — Test-driven / characterization development
For changed logic write/identify a reproduction or an assertion that fails before the change, then implement the smallest fix and prove the focused test passes. When existing behavior is undocumented, add characterization tests before refactor. Include negative tests for \`UNKNOWN\` vs zero, timezone/freshness/provisional data, no-lookahead, fee/cash/fills, auth, lifecycle/no-replay and explicit risk boundaries when applicable. If a test-first cycle is infeasible, state why and provide an equivalent reproducible proof. Do not replay an existing Dispatch to get fresh evidence.

### E3 — Five-axis result review
Review changed artifacts against approved requirement and user-intended behavior: (1) correctness, (2) readability/maintenance, (3) architecture/contracts, (4) security/privacy, (5) performance/resources. Read tests first, and validate claims with actual output. Classify \`CRITICAL\`, \`REQUIRED\` (blocks acceptance), \`OPTIONAL\`, \`FYI\`, avoiding cosmetic blocking. Record what was examined, what was not, evidence and decision for CHAT intake. Engineering review \`PASS\` is not independent source-release approval.

### E4 — Risk-scoped adversarial review
Trigger on concurrency, lost response, recovery/retry, idempotency, source authority, authorization, secrets, market time correctness, backtesting bias, order/LIVE controls, cross-branch semantic changes, irreversible migration. Provide the reviewer only the *artifact and acceptance contract*, not the author's argument; ask for concrete counterexamples. Reconcile every finding. For ordinary low-risk fixes, a focused negative test may fulfill the same intent. Use an independent reviewer only when benefit/risk and actual tool access justify it, without gratuitous token/credit cost.

### E5 — Source-bound progressive context
Load the minimal source-complete task slice with exact commit/path/revision, owner role and acceptance, then supporting files as needed. Never build authoritative instructions from web/third-party text, stale context or a self-declared file status. Avoid always-on injection of 25 external Skills, duplicate meta-routers, or irrelevant full repositories. Preserve explicit distinction between external techniques and FOX2 binding authority. Cite the exact version and do not exfiltrate proprietary FOX2 instructions to external tools.

### E6 — Contract-first API/interface semantics
Prior to cross-module change, identify provider, all observed consumers, request/response schema, field types, units, ordering, timestamp basis, error and timeout semantics, backward compatibility, migrations, negative cases and acceptance. Preserve BRD ownership and dictionary identity. Unknown consumers block incompatible automatic rewrites. Add consumer tests and drift detection, especially for backend/frontend, data pipeline/storage, risk engines, Bridge/CLI adapters and generated schemas.

## 3. Project-wide workstream applicability

| Workstream / paths | Primary technical floor | Special protections |
|---|---|---|
| Governance, BRD, specs (\`docs/governance/\`, \`docs/brd_mirror/\`, \`docs/architecture/\`, \`docs/data_contracts/\`, \`docs/acceptance/\`, \`docs/roadmap/\`) | E5 source binding; E6 change impact; E3 evidence review | Owner release authority, Dictionary precedence, immutable historical documents |
| Market data, ingestion, research, portfolio/risk/exit engines (\`backend/\`, future domain modules) | E2 negative tests; E4 adversarial domain tests; E6 schema/interface | provider licensing, event/as-of/received timestamps, VN units/time, provenance, no lookahead, no broker order-write |
| Application APIs and services (\`backend/\`) | E1/E2/E3/E6 | API errors, boundary validation, auth and secrets, deterministic fixtures |
| UI and user-facing analytics (\`frontend/\`) | E1/E2/E3/E5/E6 | state/empty/error accessibility and performance measured, no invented risk labels |
| Fixtures and testing (\`fixtures/\`, \`tests/\`, module test trees) | E2/E3/E5 | explicit SYNTHETIC classification, no silent weakening of test assertions |
| Agent Bridge/desktop, Agent routing and operation (\`agent_bridge/\`, Agent specs) | E1/E2/E3/E4/E5/E6 | PreExec, single-use no-replay, source bindings, one-writer, recovery, no dual execution authority |
| FOX2 Skills and prompts (\`skills/\`, \`docs/agent_handoff/\`) | E3/E4/E5/E6 | 17 native Skills retain ownership; no upstream replace, no extra unaudited shell hooks |
| CI/reporting/operability (\`.github/\`, \`reports/\`, future ops) | E1/E2/E3/E5 | statuses are evidence-specific; CI green is not authorization for merge/LIVE |
| Future workstreams | Assign relevant E1–E6 by risk and entry point | all FOX2 invariants continue; do not interpret path table as exhaustive whitelist |

## 4. Evidence and gates

- **Q0 Scope/authority:** current trusted source, task state and immutable lock; if unverified, stop executable work and allow only bounded read-only/candidate documentation.
- **Q1 Contract:** testable acceptance and consumers mapped. No changes to approved BRD semantics without owner-governed change.
- **Q2 Baseline:** actual commands, fixture inputs, known failures, expected outcomes and resource budget recorded.
- **Q3 Test-first:** failing characterization/negative test observed where applicable, or documented equivalent.
- **Q4 Code/build:** source and checks run; capture exact command/environment/exit/result. Never report \`NOT_RUN\` as \`PASS\`.
- **Q5 Review:** five axes considered, security and domain risks prioritized; record residual risk.
- **Q6 Independent challenge:** conditional risk-trigger, not an unconditional multi-model spend.
- **Q7 Git/readback:** exact branch, commit SHA, changed paths and immutable bytes; no unauthorized merge.
- **Q8 Final intake:** CHAT records accept/rework/hold; no release status inherited from CI.

All checks must be *stage appropriate*. A read-only analysis task never implies a code push, and a docs-only candidate never claims live engineering runtime integration. The normal FOX2 preflight, routing and release gates remain independently binding when verified.

## 5. Required reporting shape

Record \`scope\`, \`upstream_method_reference\`, \`source_binding\` (or \`AUTHORITY_UNVERIFIED\`), \`worktree/branch\`, \`allowed_paths\`, \`actual_changes\`, \`test_commands_and_status\`, \`five_axis_review\`, \`risk_challenges\`, \`tokens_or_cost_if_measured\`, \`result_commit\`, \`readback\`, \`known_blockers\`, \`next_owner\`. Missing tool access is \`NOT_RUN\`, never fabricated evidence.

## 6. Rollout

P0: publish this *candidate* on a dedicated non-main branch with exact Git readback, no Agent dispatch. P1: reconcile latest trusted FOX2 source/authority and assess diff with affected consumers. P2: independent no-effects review and A/B experiment on disposable fixtures pinned to the same model/thinking; evidence thresholds below. P3: only after separate approval and gates, integrate selected guidance into owning Skills/prompts, tests/CI and relevant workstreams. P4: verify real results before promotion; never merge or deploy from a document-only receipt.
