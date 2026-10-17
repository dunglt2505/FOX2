# FOX2 — Git Latest-at-Execution Source Resolution Contract v1 (CANDIDATE)

Status: OWNER-DIRECTED CHANGE / CANDIDATE / NOT GOVERNANCE EFFECTIVE
Date: 2026-10-17
Scope: FOX2 only
Authoritative user requirement: Static files may reference historical versions; when work is actually executed, resolve fresh latest Git versions and apply the admissible source set. Do not require rewriting static documents solely because old version numbers remain.

## 1. Distinguish text references from execution authority

- Documentation, READMEs, previous reports, templates and historical receipts MAY mention old Policy, Dictionary, Routing or Protocol versions; this is not a release or execution blocker by itself.
- `STATIC_VERSION_REFERENCE` is informational and historical unless an exact immutable commit/hash is deliberately bound to an already-started execution.
- Never infer execution-current from text `Policy vX`, local package labels, filenames, cached Memory, Library mirror or Git main alone.
- New/queued unstarted work MUST use the most recent Git-discovered applicable sources at the actual execution admission boundary, not whichever version its authored text happened to mention.

## 2. Mandatory automatic execution-time Git refresh

At every execution admission (CHAT direct actionable operation, new/re-scoped WP, Agent PreExec and Bridge dequeue before first claim):

1. Contact authenticated live Git for the current authorized Registry discovery location/refs. Enumerate recently published governance versions/manifests, including newer Candidate versions; record `LATEST_GIT_OBSERVED` with immutable commit, Git path, blob/SHA-256, status and supersession.
2. Resolve the newest **applicable** version for the requested execution scope and source family using actual authoritative Git metadata, compatibility, required release/owner gates and target environment. `LATEST_GIT_OBSERVED` is not by itself `LATEST_APPLICABLE`.
3. If a newer Git version exists, do not silently reuse the version that static documents reference. Bind the fresh applicable version, or return `LATEST_PRESENT_BUT_BLOCKED` when authority/compatibility for the newest version is not proven. Never silently downgrade solely to avoid such a blocker.
4. Carry out source/permission/routing/preflight checks against that just-refreshed bundle. Record `GIT_REFRESH_AT`, Registry HEAD, version candidates considered, selected version and rejection reasons, immutable source identity and before-run compatibility verdict.
5. After approval and immediately before first dispatch claim/side effect, verify no material Registry/source-head drift (or repeat refresh and routing). Lock the exact immutable source set for the attempt, then execute. Fail closed if live Git is unavailable or sources are conflicting/unverifiable. Never substitute cached Library content as current Git.
6. Publish proof of refresh/selected source or bounded blocker in result evidence; distinguish `REFRESH_PASS`, `APPLICABILITY_PASS`, `RELEASE_AUTHORITY_PASS`, `EXECUTION_PASS` and `EFFECTIVE_RELEASE_PASS`.

## 3. In-flight immutability / no replay

- If a Dispatch has started/been consumed, preserve its immutable source snapshot and no-replay semantics. Do not silently hot-swap source during that attempt or replay it.
- For queued/not-yet-started work, refresh before claim; when materially newer source changes execution contract, regenerate/rebind relevant preflight or dispatch **before** starting, with legitimate permissions.
- A newer version appearing mid-run is handled by subsequent work/intake or a governed stop/reconciliation if safety requires; it does not mutate the consumed dispatch's history.
- A frozen, signed/hashed release artifact remains immutable evidence, not a permanent instruction to ignore live Git for new executions.

## 4. Enforced tests (not yet implemented in runtime)

- OLD_REFERENCE_ALLOWED: a static file referencing prior Policy/Dictionary versions cannot fail a gate solely for being old.
- NEW_GIT_VERSION_SEEN: a newer eligible source published before first execution is selected despite old static references.
- NEW_GIT_VERSION_BLOCKED: a newer Git candidate lacking required authority is surfaced as a blocked newer source, never silently treated as approved or simply ignored.
- GIT_REFRESH_FAILURE: network/authority failure is explicit; no stale fallback.
- RACE_BEFORE_CLAIM: source update between preflight and claim triggers drift check and safe reconciliation.
- IN_FLIGHT_PINNED: an already-consumed Dispatch remains bound to its original immutable bytes and is never replayed.
- SCHEMA_AND_RUNTIME_COMPATIBILITY: new governance versions are not pushed into generated runtime constants unless required compatibility/preexec checks pass.

## 5. Release and work boundary

This contract records the Owner's corrected intended operating semantics. It does **not** assert that the installed Bridge/Skills currently enforce the full algorithm, does not retroactively change previously consumed dispatches, and does not create an EFFECTIVE release, merge, DEV or LIVE grant.

Current candidate path is non-main and reviewable. Governed promotion needs source/authority/compatibility evidence and independent verification when required.
