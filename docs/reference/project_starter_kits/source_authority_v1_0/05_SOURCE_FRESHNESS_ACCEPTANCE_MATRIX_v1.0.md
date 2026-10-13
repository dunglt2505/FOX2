# Trading — Source Freshness Starter Kit Acceptance Matrix v1.0

**Status:** REUSABLE_TEST_DESIGN / NOT_EXECUTED_IN_ANY_NEW_PROJECT. The starter JSON Schema validates structural fields, **not** actual Library/Git authority, release ordering, GitHub permissions, webhook delivery or Owner decisions. Per-project implementation must run and provide evidence for every applicable test below. Neither this file nor a JSON-valid registry authorizes any agent execution.

| ID | Scenario | Required behavior | Layer |
|---|---|---|---|
| SRT-01 | Valid old SHA remains in Git, but newer Policy was effectively released | STOP `BLOCKED_SOURCE_VERSION`; do not use old prompt | Resolver/Handoff |
| SRT-02 | Higher numbered Candidate exists, current release unchanged | Retain latest issued effective source, Candidate never auto-promoted | Resolver |
| SRT-03 | Listing paginated, `next_cursor` not exhausted | No current-head PASS; `SOURCE_ACCESS_UNKNOWN` / incomplete inventory | Library reader |
| SRT-04 | New Policy released while prompt prepared but not dispatched | Recheck and stop/reissue on material drift | Handoff |
| SRT-05 | Immutable prior WP accepted against historic source lock | Keep accepted evidence, no automatic rerun | Governance |
| SRT-06 | Library bytes differ from release-manifest digest | STOP `DIVERGED` | Publication/Resolver |
| SRT-07 | Correct Library SHA, Git blob changed | STOP `DIVERGED` / Git mirror blocked | Git verifier |
| SRT-08 | Library release complete, Git mirror missing or delayed | `SOURCE_PENDING`; prevent Git-first executable dispatch | Publisher/Handoff |
| SRT-09 | Git-only higher version exists; Library release absent | No release promotion; report Git-only candidate | Resolver |
| SRT-10 | Two active heads without explicit supersession or valid Owner resolution | `AMBIGUOUS_ACTIVE_HEAD` and STOP | Resolver |
| SRT-11 | Out-of-order publication events or duplicate event ID | CAS/dedup; preserve verified head and immutable receipt | Registry trigger |
| SRT-12 | Crash after Library publication but before Git mirror | Recovery states `SOURCE_PENDING`, no false `COMPLETE` | Recovery |
| SRT-13 | Library read API unavailable from local Bridge | CHAT attestation/manual fallback; **no automatic freshness PASS** | Capability |
| SRT-14 | Prompt's task-grant boolean `CODE_ALLOWED=true` with no external receipt | Reject; not an authority grant | Handoff |
| SRT-15 | Correct source lock, wrong project / repo / writer worktree | STOP, no checkout/exec | Isolation |
| SRT-16 | Project copied kit and claims it is globally effective | Reject missing project Owner decision and release | Bootstrap |
| SRT-17 | Same service identity pushes to different branch or unauthorized file path | Block; preserve evidence; do not infer server-side ACL without observed enforcement | Git writer |
| SRT-18 | Publisher discloses secrets or licensed raw feed in registry | Quarantine; prevent Git publication | Privacy |
| SRT-19 | New Library release discovered by polling before new handoff (no webhook) | Correct fresh decision, label MANUAL/PULL not push-triggered auto | Fallback |
| SRT-20 | Unsupported webhook / unverified Library event access | Do not claim unattended real-time automation | Capability |
| SRT-21 | New technical spec release but unchanged Policy release | Only applicable technical family head changes; independent versioning | Applicability |
| SRT-22 | Valid new owner supersession intentionally changes applicability | Select by authenticated owner/scope; reject lexical/max-version shortcuts | Authority |
| SRT-23 | Registry cache says current, authoritative Library now newer | Resolver re-queries and stops stale; cache alone never PASS | Resolver |
| SRT-24 | Agent correct checkout Git bytes but no evidence of latest Library | Agent reports `LATEST_LIBRARY_STATUS=CHAT_ATTESTED_NOT_INDEPENDENT`; cannot claim global freshness | Checkout |
| SRT-25 | Bootstrap first-ever project checkout no approved DEV yet | Allow only separately scoped safe PREPARE_CHECKOUT; no code edits | Bootstrap |
| SRT-26 | Offline schema validation PASS but no runtime service installed | State `STRUCTURE_PASS/AUTO_ENFORCEMENT_NOT_IMPLEMENTED` | Honesty |
| SRT-27 | Current repo lacks enforced protected ref on private personal plan | Keep `GATE_A=BLOCKED_CAPABILITY_UNAVAILABLE` even with fresh registry | Trust |
| SRT-28 | Change source just before execution (TOCTOU) | Recheck authoritative head and materiality; stop affected launch | Dispatch |

## Project adoption evidence matrix

| Gate | Needed proof | Status for this generic kit |
|---|---|---|
| G1: Policy publication | Owner decision + actual Library release + immutable bytes + manifest | NOT_APPLICABLE; no new project exists |
| G2: Source Registry bootstrap | Instantiated project profile, schema validation, current-family source receipts | TEMPLATE_ONLY |
| G3: Release trigger | Authenticated publisher hook or effective event subscription, race/retry tested | NOT_IMPLEMENTED |
| G4: Resolver | Latest Library-head selection, Git mirror re-verification, negative tests | NOT_IMPLEMENTED |
| G5: CHAT handoff enforcement | New prompt blocked on stale release; source lock receipt | NOT_IMPLEMENTED |
| G6: Agent checkout | Exact worktree HEAD + source hashes + task grant/writer | NOT_VERIFIED |
| G7: Unattended dispatch | Trust publisher, replay protection, real client capability and required gates | NOT_AUTHORIZED |

**Operational proof minimum:** A controlled test publishes an actually effective Policy revision after a baseline, shows complete Library listing, verifies manifest and raw bytes, proves Resolver picks new head, makes the *old prompt fail*, rebuilds `SOURCE_LOCK` for an allowed NEW task, and demonstrates no escalation to DEV/merge/LIVE. Candidate-only and outage/rollback/concurrency cases must also pass. Do not run such a test by altering a real project's published Policy unless the project Owner separately authorizes a sandbox release.
