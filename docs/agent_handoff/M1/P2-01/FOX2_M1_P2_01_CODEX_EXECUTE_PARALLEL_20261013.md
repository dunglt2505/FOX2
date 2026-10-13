# FOX2 — CODEX EXECUTION PROMPT — M1-P2-01 FOUNDATION
Date: 2026-10-13
Execution mode: MANUAL_LOCAL_START / AUTONOMOUS_BOUNDED_EXECUTION / STOP_AT_PUSHED_UNREVIEWED
Agent lane: CODEX / M1 APPLICATION
Issues: https://github.com/dunglt2505/FOX2/issues/8 and /9

## 0. CHAT routing decision
This prompt is the executable handoff for FOX2-M1-P2-01 under FOX2 Policy V1.8.4 and Routing Index V1.2.5.

Routing result:
- target architecture: localhost modular FastAPI backend with typed contracts/validators, later Store -> DSM -> API sequence
- actual stage: PRE-DEV -> executable P2-01
- execution path class: TARGET_PATH
- P2-01 has no material technical dependency on Bridge Gate A or SFR-010
- Agent choice: CODEX
- reason: coding spec is frozen enough, isolated branch/worktree is available, file scope is disjoint from COPILOT Bridge lane
- COPILOT: forbidden from this P2-01 writer lane during this run
- WORK: not required before code; independent review only at a material later checkpoint
- CHAT: owns source/readback/acceptance
- OWNER_SCOPE_APPROVED=YES
- CHAT_ASSIGNMENT_CHECK=PASS_CONDITIONAL_ON_IMMEDIATE_LOCAL_RUNTIME_CHECK

If the local runtime check below PASSes, this prompt activates:
`CODE_ALLOWED=YES_FOR_FOX2_M1_P2_01_ONLY`
`GIT_CODE_PUSH=YES_OWN_TASK_BRANCH_ONLY`

No further Owner approval is required inside this WP.

## 1. Authoritative sources
### Policy
- FOX2 V1.8.4 RELEASED_EFFECTIVE
- SHA256 `481790b2512ea1cd4891fe1b03258175d68d9bfae71158d19283bd003c560f5a`
- Git `a366f509899cec97f64316cb111b29a3849325b5:docs/governance/FOX2_POLICY_V1.8.4.md`
- Blob `483a74ff39339e653bbd7bbfba0feaf7b1c003e9`

### Routing Index
- V1.2.5 EFFECTIVE_DERIVATIVE
- Git `7b6e30e0712071da3a576e1ebda2dce364aa7dff:docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_2_5_EFFECTIVE_ROUTING_INDEX_20261013.md`
- Blob `3ea18c06af93cd059b7e29c6f09914ac4a0298a7`

### P2-01 rebind
- Git `588da7b1c1a642ddfd935ff6372af83a35acaa2f:docs/agent_handoff/M1/P2-01/FOX2_M1_P2_01_PREDEV_REBIND_V184_20261013.md`
- Blob `031c02fc420f9156e809a6f0e77b864b6ad09c23`

### M1 Technical
- `FOX2_M1_TECHNICAL_SPEC_v0.1.md` — RELEASED_EFFECTIVE
- use latest released exact Git copy visible from the P2 source set; do not use Candidate copies

### P2 Work-Package Plan
- Git source commit `282fe0654de13e8d9c679e171e7ac81f29a545ca`
- `docs/roadmap/FOX2_M1_P2_WP_PLAN_v0.1.md`
- Blob `6612f7d05b4724be396214e5446eb685e58979c9`

### Market contract / acceptance
Frozen M1 source commit:
`955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`

At minimum bind:
- `docs/data_contracts/FOX2_MARKET_DATA_CONTRACT_v0.4.md`
- `docs/data_contracts/FOX2_MARKET_DATA_v0.4.schema.json`
- `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv`
- `docs/acceptance/FOX2_M1_V04_CHANGE_CONTRACT_AND_REQUIREMENT_MAP.md`

Acceptance subset for this WP:
- FOX2-00-T01/T02/T03/T04
- FOX2-06-T05/T13/T14/T16/T18
- FOX2-N1-T01/T02/T03/T04/T12

Do not claim integrated/provider acceptance outside P2-01 as PASS.

## 2. Exact writer destination
Remote branch:
`work/FOX2-M1-P2-01-foundation-codex`

Expected initial remote HEAD:
`588da7b1c1a642ddfd935ff6372af83a35acaa2f`

Preferred local worktree:
`C:\Projects\FOX2-worktrees\FOX2-M1-P2-01-CODEX`

Writer lease:
- CODEX ONLY for this exact worktree/branch
- COPILOT and other Agents MUST NOT write here

Allowed paths for this run:
- `backend/**`
- `tests/p2_01/**`

Denied:
- `agent_bridge/**`
- `source_freshness/**`
- `frontend/**`
- `docs/**`
- `.github/**`
- root `tests/**` outside `tests/p2_01/**`
- P2-02 store/migrations
- P2-03 DSM implementation
- P2-04 application/API integration beyond P2-01 minimal health/foundation boundary
- DNSE/provider network
- account/order/broker code
- main/merge/LIVE

## 3. Immediate local runtime check
Do this first and keep it minimal.

1. verify repository/origin
2. verify remote task branch exists at expected initial HEAD
3. inspect registered worktrees
4. if preferred worktree does NOT exist and branch is not attached elsewhere, create:
   `C:\Projects\FOX2-worktrees\FOX2-M1-P2-01-CODEX`
   attached to the exact task branch
5. verify branch/HEAD/clean status
6. verify no `index.lock`, no writer collision/WIP
7. observe Python, pip, pytest, FastAPI and Pydantic already installed
8. do NOT install packages and do NOT use network
9. observe actual Codex model/thinking/quota only if exposed; use `NOT_EXPOSED` truthfully

STOP if:
- branch/base mismatch;
- target path/branch already owned by another writer;
- dirty unexpected WIP;
- Python/pytest/FastAPI/Pydantic required for this WP are unavailable;
- source readback mismatch;
- any safety/platform refusal.

If all checks PASS, continue automatically into implementation. Do not return for another CHAT approval.

## 4. Implement P2-01 only
Use the frozen package direction. Preferred paths already contemplated by the accepted source manifest:

- `backend/pyproject.toml`
- `backend/src/fox2/__init__.py`
- `backend/src/fox2/main.py`
- `backend/src/fox2/config.py`
- `backend/src/fox2/contracts/__init__.py`
- `backend/src/fox2/contracts/market.py`
- `backend/src/fox2/contracts/health.py`
- `backend/src/fox2/contracts/instruments.py`
- `backend/src/fox2/contracts/watchlist.py`
- `backend/src/fox2/validation/__init__.py`
- `backend/src/fox2/validation/schema.py`
- `backend/src/fox2/validation/semantics.py`
- `backend/src/fox2/ports/__init__.py`
- `backend/src/fox2/ports/store.py`
- `backend/src/fox2/ports/dsm.py`
- `backend/src/fox2/ports/preferences.py`
- `backend/src/fox2/api/__init__.py`
- `backend/src/fox2/api/health.py`
- `tests/p2_01/test_contract_schema.py`
- `tests/p2_01/test_semantics.py`
- `tests/p2_01/test_offline_startup.py`
- `tests/p2_01/test_security_boundary.py`

You may add additional files only under `backend/**` or `tests/p2_01/**` when technically necessary for P2-01. Report them explicitly.

### Required implementation semantics

#### DTO families
Keep separate DTO families:
- `MarketDataEnvelope` v0.4: `{contract_version, request_id, generated_at, data}`
- market observation DTOs from the published Contract
- `ProcessHealth`
- `SourceHealth`
- `InstrumentSearchResult`
- `WatchlistPreference`

Do NOT apply market-observation schema to health/search/watchlist payloads.
Do NOT invent a new contract version.

#### Validation boundary
Keep shape/schema and semantic validation separate.

Required conceptual interface:
- `MarketValidator.validate_shape(payload, kind) -> ValidationResult`
- `MarketValidator.validate_semantics(observation, capability_context) -> SemanticVerdict`

Semantic validation must cover where applicable:
- positive quote price;
- OHLC bounds/ordering;
- event/observation timestamp ordering;
- real zero volume vs missing;
- observation/available timestamps;
- unit/basis/rights/freshness classifications.

JSON-schema PASS must never be reported as semantic PASS.
`generated_at` is response creation time, not market-event time.

#### Ports
Freeze lightweight interfaces only; do not implement downstream persistence/DSM behavior:
- `StoreReadPort.get_observation(instrument_id, capability, at_or_before)`
- `StoreWritePort.append_and_promote(candidate, ingest_audit)` — interface only
- `DSMSelectPort.select(capability, instrument_id, use_context)` — interface only
- `PreferenceRepositoryPort.replace_if_version(expected_version, items)` — interface only

Domain/contracts/validators MUST NOT import:
- FastAPI
- SQLite
- DSM implementation
- provider SDK
- runtime fixture modules

#### Configuration / network safety
Default configuration:
- provider disabled
- no provider transport construction
- no background retry/scheduler/backfill
- loopback/local-only host defaults
- no external network requirement

#### Health diagnostics
Minimal P2-01 health diagnostics may expose configuration/runtime foundation status only.
Before real DSM/provider/store wiring:
- use `UNKNOWN` / `UNAVAILABLE` truthfully;
- never fabricate `READY`, LIVE market data or source success.

No market route implementation beyond what is minimally needed for P2-01 foundation/offline startup and health boundary.
Do not implement P2-04 API integration early.

## 5. Tests
Create and run offline tests under `tests/p2_01/**`.

At minimum prove:
1. DTO/schema happy paths for P2-01-owned families;
2. invalid contract version / missing required fields / malformed payloads are rejected according to source contract;
3. schema PASS and semantic FAIL are distinguishable;
4. positive price and OHLC semantic negative cases;
5. timestamp semantics are not replaced by `generated_at`;
6. health/search/watchlist do not incorrectly use market schema;
7. provider disabled causes zero provider/network construction;
8. startup works offline on loopback settings;
9. diagnostics use UNKNOWN/UNAVAILABLE before integration;
10. no account/order/broker endpoints exist;
11. imports respect dependency direction.

Network must remain disabled. If a test tries to access network, fix the test/code or STOP.

Use already-installed tooling only.
No package download/install.

## 6. Quality checks
Before commit:
- run P2-01 test suite;
- run any safe static/syntax/import checks available without installation;
- `git diff --check`;
- inspect `git status`;
- verify all modified/untracked files are inside allowed paths;
- scan changed content for obvious secrets/credentials;
- ensure no generated DB/cache/log/venv artifacts are staged.

If defects are within P2-01 scope, fix and rerun tests autonomously.
If a fix requires P2-02/03/04 or a forbidden path, STOP and report.

## 7. Result evidence
Create:
`tests/p2_01/P2_01_RESULT.md`

Include:
- exact source/readback identities;
- worktree/branch/initial HEAD;
- file inventory;
- design choices;
- acceptance subset mapping;
- tests and results;
- explicit NOT_RUN items;
- actual model/thinking/quota if exposed;
- final status/STOP reason.

Do not include secrets.

## 8. Commit and push
Only after required tests PASS:
1. stage only `backend/**` and `tests/p2_01/**`
2. commit with a P2-01-specific message
3. push ONLY:
   `work/FOX2-M1-P2-01-foundation-codex`
4. read back remote head if possible

Do NOT:
- push main
- merge
- create provider credentials
- access DNSE Production
- touch broker/account/order systems
- implement P2-02/03/04
- open PR unless CHAT later requests it

## 9. Final response format
Return exactly:

```text
FOX2 M1-P2-01 CODEX RESULT

POLICY_READBACK:
ROUTING_INDEX_READBACK:
P2_REBIND_READBACK:
M1_TECH_READBACK:
P2_PLAN_READBACK:
CONTRACT_READBACK:
ACCEPTANCE_READBACK:

ACTUAL_CODEX_MODEL:
ACTUAL_THINKING:
QUOTA_STATUS:

WORKTREE:
WORKTREE_CREATED_THIS_RUN:
BRANCH:
INITIAL_HEAD:
FINAL_LOCAL_HEAD:
REMOTE_HEAD:
CLEAN_BEFORE:
CLEAN_AFTER:
WRITER_COLLISION:

FILES_CHANGED:
IMPLEMENTATION_SUMMARY:
ACCEPTANCE_MAPPING:

TESTS:
TEST_RESULT:
NETWORK_ACTIVITY:
SECRET_SCAN:

COMMIT:
PUSH:
RESULT_REPORT:

EXECUTION_STATE:
  PUSHED_UNREVIEWED
  | BLOCKED_SOURCE
  | BLOCKED_BRANCH
  | BLOCKED_WORKTREE
  | BLOCKED_COLLISION
  | BLOCKED_TOOLCHAIN
  | BLOCKED_TEST
  | BLOCKED_SCOPE
  | BLOCKED_PUSH
  | BLOCKED_OTHER

OPEN_GATES:
STOP_REASON:
```

STOP at `PUSHED_UNREVIEWED`. CHAT performs remote independent acceptance before P2-02.
