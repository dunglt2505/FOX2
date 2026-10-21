# FOX2 Package Lifecycle A03 — BUILD result

Task: `FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-A03`
Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-PACKAGE-LIFECYCLE-A03-CODEX-001`
Delivery: `PUSHED_UNREVIEWED` on the authorized task branch; independent CHAT review pending. The observed remote result SHA is returned outside this report after push/readback.

## Change and boundary

The certification harness now invokes the stable `BridgeRoot/uninstall.ps1` once, synchronously, using the fixed PowerShell 7 executable with `cwd=BridgeRoot`. It rejects a supervisor or parent interpreter inside `versions`. Installed Python remains available for the existing control/setup/status operations.

Before reinstall, the harness checkpoints supervisor kind/path/content SHA-256, actual exit code (null when no exit is observed), sanitized stdout/stderr limited to 4096 characters each, current-pointer/version absence and durable config/database/manual-consumption checks. Redaction happens before truncation. Nonzero exit, timeout, launch failure or failed postconditions persists evidence and raises without retry or reinstall.

Only `agent_bridge/scripts/certify_user_lifecycle.py` and `agent_bridge/tests/test_rc1_package.py` changed in the implementation commit. The product `installation.py` and `__main__.py` are unchanged. No product uninstall redesign was needed.

## Binding and implementation

- Product source baseline: `b065a468279cbf63ae4bbfad7a0efaad1e6046e4`.
- Execution starting HEAD: `e052082afd7279f21611d76669dc8e761c003e79`; exact launcher-supplied Dispatch runtime base, not the product baseline.
- Dispatch commit: `9ddb2154d87fc88ccbdfd4c3e9550574f0bb6a66`, blob `bfa449e8b9050b0f524ac5c8552e95eb3bccb7e4`; fetched from origin and matched to inherited launcher identity.
- Task: `ac12501e1b3c94a0e75b72adc7dc78743d18e660`; prompt: `39d6a8f36dd573a4fb9e61a5d4102a15e9b3a80f`; hashes and task-specific PreExec PASS verified.
- Entry branch/worktree clean; product baseline ancestor; only 12 handoff/PreExec/receipt files before execution, with no product-code drift. One task-scoped CODEX writer observed, PID 21216, requested model/high/full-access route verified from its process; no subagents.
- Implementation commit: `fab3642b818415428ae3f67965430e3ea0b11401`.
- A01 was not replayed; neither A02 Dispatch was executed. This is one A03 Agent attempt, with no Agent retry or model substitution.

`source_binding.json` separates verified Git bytes and task-scoped Owner/CHAT authority from global runtime or release claims. Dictionary 1.3 resolves Result Contract v2 and Protocol 12. Prior accepted report/manifest remain available at product baseline `b065a468...`; this report describes A03 only.

## Validation

| Check | Observed result | Evidence |
|---|---|---|
| Initial focused lifecycle regressions | 8 PASS before three additional cases | focused.log / focused.xml |
| Final lifecycle regressions | 11 PASS, included in final package and full suite | installation_package.xml / test_summary.json |
| Installation/package | 62 PASS | installation_package.log / .xml |
| Full suite, initial environment | 592 PASS / 25 FAIL | full_initial.log / .xml |
| Full suite, corrected process environment | 617 PASS, no failures/errors/skips | full.log / full.xml |
| Python syntax and stable supervisor PowerShell parse | PASS; PowerShell 7, zero parse errors | static_checks.json |
| Allowlist, diff check, bounded secret scan | PASS | static_checks.json / verify.py |
| K1 material hunks and result artifacts | UNEXPLAINED=0 | k1.json / implementation.diff |
| Result Contract v2, hashes, references and changed-path coverage | PASS before result commit | evidence_manifest.json / verify.py |
| Real Owner-host install/update/uninstall/reinstall | NOT_RUN | source_binding.json / static_checks.json |

The first full run failed only in unchanged `test_preexec.py`: Git for Windows reported `Filename too long` for a nested fixture's `git show <sha>:<routing-path>`. Read-only reproduction returned exit 128; the same command with `core.longpaths=true` read the exact 4920-byte object. The second full run appended that setting through child-process `GIT_CONFIG_COUNT/KEY/VALUE` and passed. No persistent Git config or test/product source change was needed. Both runs are retained.

Commands: `python -m pytest agent_bridge/tests/test_rc1_package.py -k lifecycle -q`; `python -m pytest agent_bridge/tests/test_installation.py agent_bridge/tests/test_rc1_package.py -q`; `python -m pytest agent_bridge/tests -q`. Each run used the source `agent_bridge/src` import path and the committed JUnit/log destinations. The final full command also used process-only `core.longpaths=true`. `python reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/package_lifecycle_fix/verify.py` repeats static checks; add `--result` for schema/hash/reference validation.

Evidence logs/XML use canonical LF text, workspace/hostname aliases and redacted artificial secret parameters. `evidence_normalization.json` preserves original and sanitized hashes. The bounded scan excludes only two exact artificial sanitizer literals in source/diff; no actual credential was found. Evidence assembly corrections are recorded in `validation_history.json`.

## Remaining limits and next owner

Historical Batch-B `UNINSTALL_PATH=FAIL` remains factual and unchanged. This source BUILD correction and fixture-based tests do not demonstrate a successful real host lifecycle. Real lifecycle certification, G3/G4, Canary, AppLocker/AppIDSvc/service/ACL changes, reboot, main/PR/merge, provider/broker/LIVE and global product release were not performed.

CHAT owns independent review of the pushed result. There is no CHAT acceptance claim in this submission.
