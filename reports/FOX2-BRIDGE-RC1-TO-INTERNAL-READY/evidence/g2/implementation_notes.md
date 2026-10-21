# G2 implementation boundary and review notes

This is engineering evidence for G2 A01, not a host adoption receipt. No service or effective policy was installed/started/applied. Installed F1 runtime remains DENY pending independent G3/G4 evidence.

## Trusted entry and process ownership

The only production constructor is `f1_service` under SCM and LocalSystem. It uses the OS ProgramData known-folder API rather than a requester-controlled environment variable. It requires an existing reconciled `broker.sqlite` and protected `adoption.json`; startup does not bootstrap either file or create host policy. Root protection, trusted owners, access rules, reparse paths, runtime file inventory, raw file digests, SCM PID/account/type/start mode/command, AppIDSvc status, effective policy identity, source Git HEAD/branch/cleanliness and local PAUSE/STOP controls are checked before creation/resumption.

The SCM binary binding is the fully quoted fixed `runtime/Scripts/python.exe` followed by `-I -B -m fox2_agent_bridge.f1_service --scm`. There is no install/start CLI. A protected global mutex rejects a second authority instance. The service holds a first-instance local named pipe throughout its lifetime, with an explicit DACL and remote-client rejection. It derives SID, session, PID and a primary token from Windows pipe impersonation, then reverts impersonation before acting. Client-side observations additionally check pipe server PID against SCM, LocalSystem identity and the protected image path. Untrusted or absent service means DENY; there is no fallback spawn.

`Authority` is a deliberately injectable source-test engine, not an OS trust anchor. Constructing it, a `Peer`, a broker store, or a reconciliation snapshot in ordinary Python grants no installed authority. The installed ledger and launcher cannot select those offline APIs as a positive path.

## State and no-replay

Boot increments a durable authority epoch and revokes all prior leases before staging. Service revocation also tombstones the sealed adoption-plan digest in the same transaction; restart or rollback cannot reactivate that unchanged plan. A separately administered new plan is required after shutdown/revocation. Reconciliation runs against the sealed inventory and requires every historical identity to already exist in the global consumed set. The original WAL/SHM/missing-root/duplicate/manual-overlap HOLD rules are unchanged. Provisioning/importing histories is a separate privileged G3 preparation step, never exposed through interactive IPC.

An authenticated request must exactly match the staged version/dispatch/task/source/package/actor/nonce/epoch tuple and OS peer. Claims commit before a second durable one-use spawn intent. The Windows spawner creates under the duplicated caller token with explicit application/arguments, a filtered user-profile environment, no inherited handles, a suspended primary thread and a kill-on-close Job. The authority rechecks policy, source, control, time and lease before resuming. Ambiguous creation, failed resumption and all uncertain claims stay consumed. No lease/token is returned to the requester. User outcomes are idempotent information and cannot unconsume an identity.

The service serializes claim/creation/revoke, checks leases at resumption, and monitors policy/time/lifetime between bounded IPC requests. Leases currently last at most 60 seconds and cannot outlive the sealed task/epoch expiry. G3 must exercise lifetime timing and suitability for the intended Agent workload. Shutdown/revocation closes service-owned Jobs even if storage revocation fails; memory stays denied and the next boot fences the old epoch. Heartbeat time floors survive restart. The two-second wall-versus-monotonic tolerance is explicit; backward wall movement below the previous observed second is always rejected.

## Administrative adoption-plan input (G3/G4 only)

`load_authority` accepts only the protected fixed-root plan. It is not generated or installed by this attempt. Its fields are:

- `adoption`: independent G3/G4 verification disposition; the service requires the exact verified disposition. G2 creates no such receipt.
- `service_start_type`: exact SCM mode; `runtime_bindings`: absolute file path to raw SHA-256 for the complete service runtime and trusted Git executable; `git_executable`: that absolute executable.
- `policy_digest`: canonical effective-policy identity; `source_commit`: immutable Git commit; `package_digest` and `package_path`: exact package bytes; `expires_at`: service/epoch UTC deadline.
- `historical_roots`, `manual_consumed`, `inventory_complete`, `inventory_sha256`: reviewed complete historical snapshot, independently quiesced/fenced before adoption. A boolean alone is never adequate host evidence.
- `tasks`: per-dispatch sealed objects with `request`, `caller_sid`, `caller_session`, `expires_at`, `argv`, `worktree`, `branch`, `controls_db`, `bindings`, `task_path`, and `dispatch_digest`. The service replaces the request epoch with its current boot epoch. Source digest is SHA-256 of compact sorted JSON of `bindings`; task/package hashes must appear in that map. The raw dispatch digest selects a descriptor for the matching OS caller. Neither a descriptor nor its nonce is a bearer authorization.

Task authority stays external: CHAT/Git approval and the independently administered protected plan must agree. No user IPC method stages tasks, changes inventory, imports consumption or activates an epoch. Interactive operations are non-granting inspection, claim-and-spawn, informational outcome and administrator-only revocation.

## Policy artifact and interpreter limits

`f1_policy` generates deterministic hash rules for EXE/Script/MSI/DLL, all enforcing. EXE/DLL extensions include service and system-code settings. It accepts exact SID scopes, enabling a service-only interpreter allow with a caller-SID interpreter deny. Duplicate/conflicting same-principal identities are rejected. Paths confer no execution trust. Canonical policy identity binds the reviewed rules to source/package provenance through deterministic rule IDs.

AppLocker file hashes come from the native file-information/policy-construction cmdlets; raw SHA-256 is recorded separately. `f1_inventory.ps1` is read-only and explicitly imports Windows modules to avoid inherited module-search drift. Unsupported surfaces fail: `.py` cannot be represented as an AppLocker Script hash. G3 must inventory/fence the interpreter executable and prove that copied/imported code cannot escape through an allowed interpreter, shell, DLL loader or shared hash. The generated fixture policy is not a complete Windows baseline and is never applied. Exact current fixtures and copied legacy identity decisions are source/policy-model tests, not host enforcement results.

## Consumer convergence and packaging

Launcher starts only the interactive desktop and observes service status. Installed or runtime-marked E2E calls delegate to the service before worktree creation, local claiming or adapters. Ops, DesktopWorker and BridgeApp share that runner; installed smoke is denied without a staged task. Installed module/interpreter identity also fences alternate databases with forged SINGLE_ROOT metadata. The tray startup route stays current-user UX. There is no privileged tray conversion.

Package generation includes F1 Python modules and the read-only inventory script, declares `DENY_PENDING_G3_G4`, and does not register SCM or deploy policy. No product dependency was added. Static checks verify source-module byte inclusion using a synthetic wheel contract; this is explicitly not a newly built release package. A complete offline user-package build is NOT_RUN because the selected host has no provisioned isolated setuptools/build/wheel environment. Source/package fixture tests and a Windows desktop build are recorded separately.

## G3-only tests (all NOT_RUN_G3 here)

Isolated elevated SCM installation/start/stop/reboot; LocalSystem positive creation under an authenticated interactive token; effective AppLocker deployment; copied legacy executable/script/interpreter bypass probes; full OS/native dependency allow inventory; lease/process-tree behavior during service crash and AppIDSvc/policy changes; protected-root ACL mutation attempts; rollback/reinstall preserving global tombstones; interactive credential usability; Owner-host adoption/G4. No Git push establishes any of these facts.

## Primary API references consulted

- [Pipe impersonation](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-impersonatenamedpipeclient)
- [Process creation under a user token](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasuserw)
- [Job objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- [Nonblocking pipe connection states](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-connectnamedpipe)
- [Disconnect and unread pipe data](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-disconnectnamedpipe)
- [AppLocker service/system collection extensions](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/rule-collection-extensions)
