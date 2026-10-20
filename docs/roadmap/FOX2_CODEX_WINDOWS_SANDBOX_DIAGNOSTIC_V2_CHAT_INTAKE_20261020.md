# FOX2 — CODEX Windows sandbox diagnostic V2: CHAT scoped intake

**Owner-provided observation:** `2026-10-20T16:05:19.5994113Z` (2026-10-20 23:05 ICT). **Context:** existing Whole-WP `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`, integrated Attempt-001 consumed, Git Result `947cf9a33585a286a2447aa27c35328b146b2fbd` delivered and CHAT review completed as `ACCEPT_BLOCKED_REPORT / HOLD_BUILD_TEST` at `446089625885488366b11fd63bea357fb14ba987`.

## Actual bounded evidence

Owner pasted JSON `schema=FOX2_CODEX_SANDBOX_DIAGNOSTIC_V2`, `mode=READ_ONLY_NO_CODEX_EXECUTION`; `setup_file_status=NOT_FOUND`, `setup_error_code=null`, `recent_log_count=1`, `logs_examined=1`, `log_read_errors=0`, `detected_signatures=["FILE_SHARING_CONFLICT","ACL_OR_OWNERSHIP_FAILURE","SANDBOX_SETUP_FAILURE"]`. Output labels `actual_root_cause=NOT_CERTIFIED`, `attempt001=CONSUMED_NO_REPLAY`, `bridge_installed=UNTOUCHED`.

**Independent CHAT verdict:** `ACCEPT_SCOPED_SANITIZED_SIGNATURE_DISCOVERY` only. This is a **single log tail scanned with three broad regular expressions**: matching all three categories does not establish event chronology, the first failing syscall, a particular locked binary, or that error 5 and error 32 occurred in the same attempt. Setup file absence is NOT proof the CODEX sandbox succeeded; diagnostic lacks exact current pinned executable version and path/config binding. The already observed `helper_unknown_error: setup refresh had errors` remains operationally blocking code execution. No source tests or bridge changes performed.

## External issue confirmation, applicability boundary

Public `openai/codex` issue `#54325` includes a maintainer comment dated 2026-10-16 stating sharing-violation/runtime ACL setup defect fixed in **CLI 0.163.0** by PR `#51822`. Issue `#54635` describes stale `CODEX_CLI_PATH` in Codex config/plugin MCP configuration still pinning an older CLI despite installing newer software. These are public third-party issue comments, **not machine diagnosis**. There are unrelated Windows access-control failures sharing generic strings; do not reset ACLs, disable sandbox, delete runtime directories, kill CODEX/VS Code sessions, change windows.sandbox or force reinstall on this evidence. Official repository `openai/codex` documents CLI install/update paths, but actual user install method and active command binding have not been established.

## Targeted single-step repair decision

1. Non-mutating Windows PowerShell 7 verify **which exact CLI is invoked** (Get-Command, actual `codex --version`), whether it is **0.163.0 or newer**, whether configured `CODEX_CLI_PATH` is stale, and which Windows sandbox mode is configured, without printing raw paths or credential configuration. This does not run an Agent.
2. If invoked CLI older than 0.163.0 or stale version pointer is evidenced, resolve through vendor-supported update/selection of current signed CLI, preserve original configuration and verify correct executable binding. Updating Codex itself is a **separate Owner-controlled host action**, not authorized via Git-only receipt. If already 0.163.0 or later and problem persists, inspect precise failed file/operation in the single log privately; no speculative ACL resets.
3. After host repair, ONE **harmless sandbox execution smoke** in a neutral temporary non-FOX2 directory using exact supported CLI sandbox command; no Agent prompt, no Git checkout, no Bridge/legacy process or ledger touched. Capture explicit `SANDBOX_OK`, version and sandbox mode. Passing does NOT authorize a new coding attempt on its own.
4. Only after separate pinned model/quota/host capability, clean Git source, one-writer, permissions and route-specific PreExec PASS, open **new** attempt identity/task/prompt through Prompt Builder; preserve Attempt-001 consumed and do not reuse its marker/branch to relaunch. Installed Bridge F1, legacy retirement, Canary and LIVE remain HOLD.

**Status:** `HOST_SANDBOX_SIGNATURES_OBSERVED / EXACT_CAUSE_UNVERIFIED / INSTALLED_AND_BUILD_HOLD`. Owner command to finish Bridge remains in force, but no protected execution gate is waived.

Governance: human Registry blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`, Policy 2.0.0/Dictionary 1.3 scoped; installed enforcement NOT_ATTESTED. `POLICY_CHECK=SCOPED_REVIEW`, `TASK_STATE_CHECK=ATTEMPT001_CONSUMED`, `SOURCE_RESOLUTION=GIT_REPORT_947cf9a_AND_OWNER_REPORTED_LOG_CLASSIFICATION`, `R0–R7=CHAT_DIRECT_READONLY_RESULT_INTAKE_NONMAIN_PUBLIC_SANITIZED_RECEIPT`, `ASSIGNMENT_CHECK=NOT_APPLICABLE`. Skills source-resolver, execution-recovery, result-review, status-roadmap, governance-preflight, agent-route-runtime applied. STOP: no Agent replay/new task or Windows mutation from this receipt.

## Owner correction — 2026-10-20: FUNCTIONAL_EXECUTION_FIRST, no CLI version floor

The Owner expressly rejected using a high/low CODEX CLI version as an execution-governance prerequisite. The earlier conditional `UPDATE_CODEX_TO_AT_LEAST_0_163_0` is **SUPERSEDED for operational routing**. The Owner-observed installed `codex-cli 0.162.1` and `cli_path_pin_suspected=true` are environment context, **not an automatic hard failure** or instruction to update/clear pins. A version fix mentioned in an upstream issue cannot prove the user's exact host is incompatible or justify replacing working tooling.

**Correct acceptance criterion:** with actual invoked pinned CLI/model `gpt-6.1-sol` / medium and a sandbox restriction meeting task policy, a **new neutral and isolated** functional test must show that CODEX can actually invoke its shell tool, execute a harmless real command, produce a verified exit code/output (not just an agent statement or CLI top-level exit code), and not modify FOX2 worktree or installed Bridge. If the installed 0.162.1 achieves this, no upgrade is required. A newer CLI that fails the same functional test is still BLOCKED. Standalone `codex sandbox ... echo` is a useful bounded subtest, not proof the agent's own `exec_command` works; both can differ in practice. This applies prospectively; the consumed Attempt-001 outcome remains unchanged.

If default elevated sandbox cannot run a neutral smoke, a separately scoped read-only comparison using the vendor-supported `windows.sandbox="unelevated"` option **may be evaluated** for compatibility, but **do not silently modify global configuration, disable sandbox, or assume a less privileged mode meets the engineering task security requirements**; any use for a new CODEX code task needs policy/source/host PreExec, Owner permission, a new attempt, and objective proof. No arbitrary ACL reset, process termination or forced CLI upgrade.

`NEXT_SAFE_ACTION`: check **functional Codex shell execution**, not version ranking, in a disposable non-FOX2 location; preserve sanitized event evidence and verify non-write; then, only if complete, prepare ONE new offline Bridge source-bound attempt through Prompt Builder and required PreExec. Avoid another generic source inventory or CODEX version hunt. Existing installed/Canary gates still HOLD.

**Disposition:** `OWNER_CORRECTION_APPLIED_CANDIDATE`; no direct Windows command, Agent invocation or installed mutation carried out by CHAT.
