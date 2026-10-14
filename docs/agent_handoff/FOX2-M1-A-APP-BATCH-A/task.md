# FOX2-M1-A-APP-BATCH-A — Executable Task

**Status:** EXECUTABLE / WHOLE-WP / OWNER-AUTHORIZED
**Governance:** FOX2 Policy V1.8.6 + Routing Index V1.2.7
**Protocol:** Dispatch Schema v2 + Git-first Protocol v9
**Execution path:** MANUAL_LOCAL
**Delivery owner:** AGENT

## Source binding

- Accepted application base: `d90987afd861a41aef01059d95ca039509ede09c`
- P2-03 implementation: `7478e09bcae1f890058fd134e79fd6f7013103c6`
- P2-02 accepted upstream: `f70f0237356c4f27afb0e6760b01870228ba3739`
- P2-01 accepted upstream: `4bbbdf02387727e7d3c6900f163d7b1eedc5e2b3`
- Policy V1.8.6 source commit: `116c362b9c6243ebaa23ad17df3104d9f07c50d5`
- Routing V1.2.7 source commit: `c8474b059f372bb37cfe4989f44b92f346a7146d`
- Master execution plan: `cc7fa95ea7ff5613b3fdb33c26245834089050ca:docs/roadmap/FOX2_MASTER_EXECUTION_PLAN_20261014.md`
- Existing M1 Roadmap v0.4 / P2 Plan v0.1 / Market Data Contract v0.4 / schema / acceptance matrix remain business/contract sources unless materially superseded.
- Source authority is CHAT-verified. Agent MUST NOT redo governance/source-release discovery.

## Role / Agent

- Role: M1-A backend integration implementation Agent
- Agent: CODEX CLI
- Model policy: PINNED
- Model: `gpt-6.1-sol`
- Reasoning: `medium`
- Permission profile: `FULL_ACCESS`
- Git delivery: Agent-owned on exact task branch

Latest explicit repository evidence records Copilot quota exhaustion and no newer verified reset/availability snapshot. Codex is the proven available execution route. This is a routing decision, not a permanent Copilot exclusion.

## Whole-WP objective

Absorb historical P2-04 into one implementation round. Deliver a runnable offline M1-A backend service by wiring already accepted Foundation + Store + DSM without redesigning their frozen contracts.

Implement together:

1. application/runtime composition for accepted P2-01/P2-02/P2-03 components;
2. approved read-only market API endpoints:
   - GET `/api/health`
   - GET `/api/data-sources/health`
   - GET `/api/market/overview`
   - GET `/api/stocks`
   - GET `/api/stocks/{symbol}`
   - GET `/api/stocks/{symbol}/bars`
   - GET/PUT `/api/watchlist`;
3. watchlist service using existing SQLite preference repository/CAS semantics;
4. explicit UNKNOWN/UNAVAILABLE responses when data/rights/mapping/freshness are insufficient;
5. localhost Host/Origin/content-type guards and sanitized errors;
6. integrated regression/negative tests across P2-01/P2-02/P2-03 + this batch;
7. one final result/evidence package.

No synthetic investor quote/price fallback. Provider transport remains disabled/unimplemented in this batch.

## Writable scope

Allowed code:
- `backend/src/fox2/api/**`
- `backend/src/fox2/application/**`
- `backend/src/fox2/runtime/**`
- `backend/src/fox2/main.py`
- `backend/src/fox2/config.py`
- `tests/app_batch_a/**`

Allowed report:
- `reports/FOX2-M1-A-APP-BATCH-A/**`

Everything else is READ-ONLY, including:
- `backend/src/fox2/contracts/**`
- `backend/src/fox2/ports/**`
- `backend/src/fox2/store/**`
- `backend/src/fox2/dsm/**`
- existing `tests/p2_01/**`, `tests/p2_02/**`, `tests/p2_03/**`
- governance/roadmap/source documents
- frontend
- agent_bridge.

If a frozen interface genuinely prevents correct integration, STOP with one material blocker rather than editing it.

## Required behavior

- No provider network construction/call in default offline runtime.
- No account/order/broker/private endpoint.
- No history-to-quote fallback.
- No fabricated market values.
- Watchlist PUT is local preference only; no provider/broker side effect.
- Unknown symbol vs unavailable data vs invalid request vs unsafe store must remain distinguishable with sanitized HTTP behavior.
- Preserve atomic watchlist CAS; stale version -> 409 without lost update.
- Invalid/duplicate/>100/unverified items -> 422 or bound safe error semantics.
- Store failure -> sanitized 503 with prior data/version preserved.
- API remains loopback-only.
- Browser/frontend work is not part of this batch.

## Required validation

Run the batch tests plus full relevant upstream regressions. Superseded stage-boundary assertions that merely assert later modules do not exist may be deselected only when explicitly documented; do not weaken functional/security assertions.

Minimum gates:
- APP_BATCH_A_TESTS=PASS
- P2_01_FUNCTIONAL_REGRESSION=PASS
- P2_02_FUNCTIONAL_REGRESSION=PASS
- P2_03_FUNCTIONAL_REGRESSION=PASS
- OFFLINE_NO_NETWORK=PASS
- NO_SYNTHETIC_INVESTOR_VALUES=PASS
- WATCHLIST_CAS=PASS
- LOOPBACK_SECURITY=PASS
- API_ERROR_SANITIZATION=PASS
- CHANGED_PATH_ALLOWLIST=PASS
- SECRET_SCAN=PASS
- GIT_DIFF_CHECK=PASS
- RESULT_EVIDENCE=PASS

Record exact commands, environment and any justified deselections.

## Git authority

`git_code_push=YES`, `delivery_owner=AGENT`.

Agent may:
- stage only allowed paths;
- commit exact task branch;
- push exact non-main task branch;
- remote-readback its own SHA.

Agent MUST NOT:
- push main;
- create PR;
- merge;
- rebase/reset/stash unrelated WIP;
- modify frozen upstream modules;
- deploy;
- access DNSE Production/provider transport;
- access broker/private account/order channels;
- enable LIVE.

## STOP

Stop only for material conditions:
- wrong branch/base/task;
- competing writer on same writable paths;
- frozen interface must materially change;
- required test/security failure;
- actual quota/capacity failure;
- denied required Full Access capability;
- out-of-scope write required;
- secret/private/licensed-data exposure;
- push/readback failure.

Do not stop solely for non-material runtime/version mismatch or missing numeric quota telemetry while the Agent can execute.

## Delivery

Create:
- `reports/FOX2-M1-A-APP-BATCH-A/report.md`
- `reports/FOX2-M1-A-APP-BATCH-A/evidence_manifest.json`
- material evidence under `reports/FOX2-M1-A-APP-BATCH-A/evidence/**`

Then commit/push exact branch and return:
`FOX2_M1_A_APP_BATCH_A_PUSHED_UNREVIEWED`
