# FOX2 — Project-wide Engineering Agent Guidance (CANDIDATE)

> Status: \`CANDIDATE / NOT EFFECTIVE\`. Applies as an engineering **proposal** to the entire FOX2 repository if adopted through approved source governance. This branch does not confer execution, merge, release, deployment or LIVE authority.

## Scope
All FOX2 workstreams: Governance/BRD/architecture/contracts; backend, frontend, fixtures, tests, market data and risk/exit/profit-protection engines; Agent Bridge and desktop; agent prompts/Skills; CI/reports/operations. Do not import any other Trading project.

## Authority and routing
1. Resolve current authoritative FOX2 Dictionary/Registry, Policy, Routing, Protocol, BRD/Technical/Data Contracts and source lock at the **required execution gate**. Historical paths or filenames, even ones labeled EFFECTIVE, are not independent proof of current release authority. If the independent release chain is unavailable, report \`AUTHORITY_UNVERIFIED\` and hold dependent executable actions, without inventing \`SOURCE_CONFLICT\`.
2. Preserve existing in-flight Dispatch identities, WIP, receipts, and one-writer rules. No retry, reset, rebase, branch changes, close, merge, release, agent launch, or other side effect merely from this file.
3. CHAT owns task interpretation, source conflict resolution, requirements, routing and final intake. Copilot/Codex execute only an assigned, source-bound, preflight-cleared task. WORK provides independent audit when required by a real gate or scoped request.
4. Before a new material implementation assignment: \`POLICY_CHECK → TASK_STATE_CHECK → SOURCE_BINDING_CHECK → ROUTING_R0_R7 → PREEXEC_REQUIREMENTS_BIND → MATERIAL_PREFLIGHT_RUN → PREFLIGHT_EVIDENCE_CHECK → ASSIGNMENT_CHECK\`. If any required gate is unverified, STOP affected execution and report exact blocker. Do not require synthetic preflight for CHAT-only analysis or authorized candidate documentation work.
5. Follow the current verified FOX2 rule if any instruction here conflicts. Upstream Addy Agent Skills are *reference methods*, not FOX2 governance or authority.

## Six targeted engineering practices (only when task-relevant)
- **Constraint-driven:** preserve existing checks; no hiding errors with suppressions, deleted/skipped tests or weakened thresholds without explicit approval and evidence; compare against measured baseline rather than invented quotas.
- **TDD / characterization:** for behavior change, write a failing/characterization test before fix where practicable; run targeted tests and applicable regression; avoid generating tests merely to pass a quota.
- **Five-axis review:** correctness, readability, architecture, security, performance; validate tests and changed paths; label blocking defects and residual uncertainty distinctly.
- **Adversarial doubt:** for safety/concurrency/auth/recovery/irreversible claims, isolate artifact + contract and attempt falsification with fresh context when justified by risk/cost; never turn a discretionary review into fabricated release approval.
- **Context engineering:** use minimal, exact, source-bound context and on-demand references; do not preload unrelated Skills or duplicate the native Agent router; retain provenance and omit private secrets.
- **Contract-first interfaces:** identify producer/consumers, validation, units/time semantics, errors, compatibility and test evidence before changing API, data model or cross-module boundary. Do not change BRD semantics via implementation.

## Completion evidence
Return exact task/Dispatch identity where applicable; branch/base and immutable result SHA; allowed changed files; tests commands and outcomes with unrun tests \`NOT_RUN\`; negative/safety cases; source evidence; unresolved blockers and recommended next owner. \`PUSHED_UNREVIEWED\` does not mean \`CHAT_ACCEPTED\`, \`AUDIT_PASS\`, \`RELEASED\` or \`LIVE\`.

## Project-wide adoption files
- [Engineering quality standard](docs/engineering/FOX2_ENGINEERING_QUALITY_STANDARD_v0.1_CANDIDATE.md)
- [6-skill/17-FOX2-skill adoption matrix](docs/engineering/FOX2_AGENT_SKILLS_ADOPTION_v0.1_CANDIDATE.md)
- [A/B evidence protocol and fixtures](docs/engineering/FOX2_ENGINEERING_SKILLS_EVAL_v0.1_CANDIDATE.md)

No upstream scripts, lifecycle hooks, npm install, CLI plugin enablement, cross-model API spending or release process is authorized by this candidate.
