# BRIDGE-DESKTOP-01-02-FIX-01 corrective delivery

FIX-01 corrects CHAT review findings in the already-authorized Desktop-01+02
implementation: post-launch non-zero/quota classification, diff hygiene, incomplete
local evidence, and stale delivery lineage. This is a local, uncommitted delivery.
Bridge owns publication; CHAT owns subsequent immutable-SHA review. No future
remote FIX-01 commit SHA is claimed.

## Identity and scope

- Work package: `BRIDGE-DESKTOP-01-02-FIX-01`.
- Exact worktree: `C:ProjectsFOX2-worktreesFOX2-BRIDGE-DESKTOP-01-02-FIX-01-CODEX`.
- Exact branch: `work/FOX2-BRIDGE-DESKTOP-01-02-FIX-01-codex`.
- Exact base and unchanged local HEAD: `ceeb2bb2db3e09c2c2ad485a82a70c4f446e8e6a`.
- Parent recovery publication SHA: `3497356d5fc74785ab3377c1a49ea5330c0dab13`.
- Source/design lock blob: `6683781beb03a9c7deea9260c2d6553798e298ad`.
- Initial worktree status: clean. Task index remains unstaged.
- Only allowed writes: `agent_bridge/**` and `reports/BRIDGE-DESKTOP-01-02/**`.

The source/design lock, governance, BRD, Technical source, docs, and application
backend/frontend were not modified. Bridge architecture and the existing
single-use claim/recovery model were preserved.

## Corrective behavior

Both CODEX and COPILOT now persist AGENT_EXITED evidence before checking a returned
exit code: stdout, stderr, exit code, metadata, immutable payload, original branch,
worktree, and pre-execution HEAD. A non-zero exit after launch sets both dispatch
and execution state to NEEDS_RECONCILIATION. Partial work and the consumed dispatch
identity remain available for reconciliation. No automatic replay, publication,
or alternate Agent substitution occurs.

Restart recovery also refuses to promote a recorded non-zero exit to
PUSHED_UNREVIEWED, including the interruption window after the exit checkpoint.
Older successful checkpoints without an exit-code field retain their existing
strict result-verification path.

Proven pre-spawn failures remain terminal/actionable FAILED with the original
claim retained. Missing exact tools and unsupported capabilities still fail
closed. Popen OSError now uses the existing AgentNotStarted error because process
creation failed; errors after process creation remain conservative. A pre-launch
restart checkpoint still uses SAFE_NOT_STARTED, without releasing the claim.

Four deterministic regressions exercise real local Python child processes through
the actual selected adapters: both products, exit 1 and exit 75 with a simulated
quota diagnostic. Each child observes the ledger in RUNNING, writes partial-result
evidence with its real PID/execution identity, then returns non-zero. Tests verify
final state, retained result/checkpoint/runtime report, a rejected second claim,
ReplayBlocked on a second runner invocation, no substitution, and no publication.
Six additional cases cover missing tool, unsupported capability and failed process
creation for both products. Four restart cases cover non-zero AGENT_EXITED and
PUBLISHING checkpoints. These are fake-Agent/local-process tests; no paid Agent
or real provider/quota invocation is implied.

README EOF and pytest text CR/trailing whitespace were corrected. The validator
was updated for the exact FIX-01 branch/base/work package and parent publication.
It retains source-lock identity, allowlist, unstaged-index, diff, test, secret-scan
and evidence gates, and additionally requires all 14 FIX-01 regression cases,
full-suite evidence and consistent report identity/count.

## Final local evidence

Final full-suite outcome: **134 passed** in **40.59 seconds**, with **0 failures,
0 errors, 0 skips**. The exact final result is recorded in `evidence/pytest.txt`
and `evidence/pytest.xml`. The focused runner run also passed all 21 cases.

Validator result: PASS (exit 0; 134 tests, secret scan PASS, diff check PASS).
Git diff --check result: PASS (exit 0, no output); checked again after evidence
completion. `evidence/verification.json` and `evidence_manifest.json` record the
validator checks and SHA-256 hashes of delivery files, including required report,
JUnit and verification evidence. The manifest excludes its own hash.

| Required check | Final state |
| --- | --- |
| FULL_TESTS | PASS |
| NONZERO_AFTER_AGENT_START | NEEDS_RECONCILIATION |
| DISPATCH_REPLAY_AFTER_NONZERO | BLOCKED |
| NO_AGENT_SUBSTITUTION | PASS |
| PRESPAWN_FAILURE_SEMANTICS | PASS |
| GIT_DIFF_CHECK | PASS |
| DELIVERY_VALIDATOR | PASS |
| EVIDENCE_MANIFEST | PRESENT_VALID |
| VERIFICATION_JSON | PRESENT_VALID |
| REPORT_STATE | CONSISTENT |
| OUT_OF_SCOPE_CHANGES | 0 |

### Execution environment and limits

The normal shell tool failed before creating a process. The local Node tool ran
PowerShell and commands in the exact worktree instead. The existing Bridge venv
could not launch its Python 3.13.15 base executable because this session cannot
access that executable. Tests ran on the already-installed cached Python 3.12.14,
with pytest 8.4.2 and its pure-Python dependencies read-only from the Bridge venv.
No package was installed and the declared Python >=3.13 requirement was unchanged.
**Declared Python 3.13 runtime validation remains NOT_RUN**; the final results
certify the recorded local test environment, not that inaccessible runtime.

The first full run had 132 passes and two environmental failures: Git rejected
read-only status checks of the owner checkout under the sandbox account. That
output is retained in `evidence/pytest-preliminary.txt`. The final full run used an
exact-path safe.directory entry for C:/Projects/FOX2 in the test process environment
only. No global/local Git configuration, permissions, source files or test
assertions were changed for this setup. Test repositories/history and SQLite are
real; poller remote transport and publication verification remain simulated. No
GitHub/network canary was run.

Reproduce the recorded final environment with the existing runtimes:

```powershell
$env:PATH = 'C:UsersFox Le.cachecodex-runtimescodex-primary-runtimedependenciespython;' + $env:PATH
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPATH = Join-Path $PWD 'agent_bridge/src'
$env:PYTHONPATH += ';C:ProjectsFOX2-AgentBridge.venvLibsite-packages'
$gitConfigSlot = if ($env:GIT_CONFIG_COUNT) { [int]$env:GIT_CONFIG_COUNT } else { 0 }
[Environment]::SetEnvironmentVariable("GIT_CONFIG_KEY_$gitConfigSlot", 'safe.directory', 'Process')
[Environment]::SetEnvironmentVariable("GIT_CONFIG_VALUE_$gitConfigSlot", 'C:/Projects/FOX2', 'Process')
$env:GIT_CONFIG_COUNT = [string]($gitConfigSlot + 1)
python -m pytest agent_bridge/tests -q -p no:cacheprovider --junitxml reports/BRIDGE-DESKTOP-01-02/evidence/pytest.xml
python agent_bridge/scripts/validate_desktop_delivery.py
git diff --check
```

## Acceptance and publication boundary

Real Windows logon/startup, manual Tray interaction, normal hidden-launch usability,
manual paid Agent canaries and actual CLI Auto/model/tier/credit canaries remain
**NOT_RUN**. Headless PowerShell/.NET checks and mocked scheduler tests passed as
part of the local suite; they do not certify those manual/paid obligations.

Desktop-03, packaging/setup/install/update/uninstall, community extraction and
release remain out of scope. Batch-A, Usage Telemetry and Full Access feature work
were not added.

No git add, git commit, git push, PR creation, merge, main modification, deploy,
provider access, broker access or LIVE operation occurred. The owner checkout was
read-only during its non-mutation tests. No remote FIX-01 publication happened;
Bridge performs publication after local verification.
