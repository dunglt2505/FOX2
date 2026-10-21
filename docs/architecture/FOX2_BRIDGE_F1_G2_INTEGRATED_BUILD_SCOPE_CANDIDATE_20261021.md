# FOX2 Bridge F1 — G2 integrated build scope candidate
Date: 2026-10-21
Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY
Class: CHAT READ-ONLY BUILD ENTRY REVIEW / NON-EXECUTABLE CANDIDATE
Code snapshot inspected: ba65ad77270924e0b5f966ae0104c7dc317d0df6
G1 acceptance: 9c27e7c7104facdb7f083350f38d2451939b6c2a

## Entry governance
POLICY_CHECK: scoped human Policy/Dictionary/Routing/Protocol source set already resolved in G1; no new executable source lock is minted by this document.
TASK_STATE_CHECK: Whole-WP remains FOX2-BRIDGE-RC1-TO-INTERNAL-READY. No G2 executable task/Dispatch exists. Historical Attempt06 remains consumed/no-replay.
SOURCE_RESOLUTION: G1 design is accepted; executable G2 binding must re-resolve Registry/Dictionary/BRD/TechSpec/Protocol/acceptance immediately before assignment.
ROUTING_R0_R7: safe CHAT direct inspection is allowed; executable coder route is not admitted here.
ASSIGNMENT_CHECK: HOLD_EXECUTABLE. Existing Owner decision `OWNER_EXPLICIT_KEEP_GPT_6_1_SOL_HOLD_CODING` is preserved. No coding model/actor substitution, task.md, prompt.md or Dispatch is created.

## Current code reality at inspected snapshot
- f1_broker_store.py is an offline storage core and explicitly states it is not wired into desktop/ledger/e2e_runner. It already contains atomic consumed IDs, epoch, lease, revocation and trusted-time-floor primitives.
- f1_reconcile.py is read-only/offline and refuses ambiguous roots/WAL/SHM/incomplete inventory. It is not an authority grant.
- ledger.py deliberately denies installed-root direct claim_dispatch regardless of local metadata. This F0 fail-closed behavior must remain until the trusted-service path owns positive authority.
- launcher.py directly spawns the installed Worker and Desktop today. G2 must remove direct installed Worker spawn authority from this unprivileged path.
- startup.py manages current-user logon startup. User-facing startup/tray semantics can remain, but startup must request/observe the trusted service rather than create the Worker authority itself.
- installation.py is user-root package lifecycle code. G2 may add package/service/policy artifacts and offline validation, but actual privileged installation/policy changes are G3/G4-host actions under separate authorization.

## One integrated G2 build scope — not micro-WPs
### A. Trusted authority service and IPC
Implement a Windows-only F1 service boundary and authenticated local IPC. Candidate internal modules may be added under agent_bridge/src/fox2_agent_bridge/ for service lifecycle, IPC, policy observation and service-owned spawn; exact filenames are implementation details, not separate WPs.

Required properties:
- service principal LocalSystem or separately justified dedicated service principal;
- ProgramData-protected broker store owned by service/Administrators;
- named-pipe DACL and server-derived caller token/session identity;
- versioned request contract from G1;
- no client bearer capability that can independently spawn an Agent;
- service-owned atomic claim_and_spawn with bounded lease;
- restart creates new authority epoch and revokes prior leases;
- policy/AppIDSvc/source/package/epoch/clock drift => DENY.

### B. AppLocker policy artifact support
Build deterministic, source/package-bound AppLocker policy generation/validation support for the G1 baseline. G2 does NOT apply policy to the Owner host.

Required properties:
- explicit Enforce rules mode for relied-upon collections;
- executable + script closure mandatory; installer/DLL collections included when inventory/tests require them;
- copied legacy binaries/scripts blocked by publisher/hash identity, not path-only logic;
- current approved package/source identity represented without broad user-writable path trust;
- policy identity/digest exposed to trusted service for exact binding;
- Application Identity service absence/stopped/drift represented as DENY at runtime;
- service/non-user enforcement support when required by service-spawn topology.

### C. Consumer convergence
Change all installed positive paths so there is one authority:
- ledger.py: installed root remains unable to positive-claim directly;
- launcher.py: no direct Worker creation; request/observe F1 service-controlled lifecycle;
- desktop.py / app.py: requester/status surface only, no positive bypass;
- ops_runner.py / e2e_runner.py: same service gate for installed execution;
- f1_broker_store.py / f1_reconcile.py: preserve offline safety semantics while exposing service-internal integration only;
- installation.py / startup.py and scripts: package service/policy artifacts and fail-closed lifecycle support without auto-deploy in tests.

### D. Service-owned spawn and interactive identity
Service must own the authorization decision and process creation. To preserve user Agent credentials/environment, implementation may duplicate the authenticated interactive caller token and create the child under that token while the service remains the controlling creator and Job owner. If this cannot be implemented safely, positive spawn remains DENY; do not fall back to caller Popen.

### E. Test and evidence scope
G2 build acceptance requires source-level and Windows-CI evidence only; it must not claim host enforcement.

Minimum G2 tests:
1. service unavailable / AppIDSvc not enforcing / policy identity mismatch => all installed claims/spawns deny;
2. forged caller identity, task/source/package, nonce and epoch deny;
3. same dispatch concurrency through service produces one consumed identity;
4. service restart/revocation/clock rollback invalidates leases without replay;
5. launcher/desktop/ops/e2e installed paths cannot bypass service;
6. copied legacy hash/publisher fixtures match generated AppLocker deny/allow contract;
7. exact current package fixture is allowed by policy model while unrelated system allow baseline remains explicit;
8. reconciliation ambiguity, WAL/SHM, missing root or manual overlap stays HOLD/DENY;
9. F0 frozen cross-root negatives remain green;
10. full existing Bridge regression suite remains green;
11. service-install/policy-deploy scripts are static-reviewed for no implicit activation during package build/tests;
12. rollback fixture returns to DENY and preserves consumed/tombstone state.

## Candidate changed-path envelope
Expected existing consumers:
- agent_bridge/src/fox2_agent_bridge/{f1_broker_store.py,f1_reconcile.py,ledger.py,launcher.py,desktop.py,app.py,ops_runner.py,e2e_runner.py,installation.py,startup.py}
- agent_bridge/scripts/** only where service/policy packaging/lifecycle support is required;
- agent_bridge/tests/** for F1 service/policy/consumer/regression coverage.

New F1-specific source/test files under those directories are permitted only in a future executable task with an exact allowlist. Governance docs, unrelated FOX2 engines, main branch, Canary, provider/broker/LIVE remain out of scope.

## G2 entry verdict
STAGE=BUILD
STATUS=BLOCKED
EVIDENCE=G1_ACCEPTED_PLUS_CODE_TREE_INSPECTED
EXIT_GATE=NEW_EXECUTABLE_TASK_SOURCE_LOCK + CODING_AUTHORITY + VERIFIED_ROUTE/PREEXEC + ONE_WRITER + GIT task/prompt readback
BLOCKER=OWNER_EXPLICIT_GPT_6_1_SOL_HOLD_CODING; NO_G2_EXECUTABLE_TASK; ROUTE_PREEXEC_NOT_RUN
NEXT_SAFE_ACTION=HOLD executable assignment. If coding is separately authorized, CHAT re-resolves sources and route, applies fox2-agent-prompt-builder, publishes one integrated task/prompt to non-main Git, then accepts only real Git results.

F1 runtime remains DENY; G3/G4 NOT_RUN; Canary009 HOLD.
