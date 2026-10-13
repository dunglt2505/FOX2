# BRG-003 Sanitized Source Baseline Result

## Authority and source identity

- Policy: FOX2 V1.8.4 RELEASED_EFFECTIVE; Git `a366f509899cec97f64316cb111b29a3849325b5`, blob `483a74ff39339e653bbd7bbfba0feaf7b1c003e9`, Library SHA256 `481790b2512ea1cd4891fe1b03258175d68d9bfae71158d19283bd003c560f5a`.
- Routing Index: V1.2.5 EFFECTIVE_DERIVATIVE; Git `7b6e30e0712071da3a576e1ebda2dce364aa7dff`, blob `3ea18c06af93cd059b7e29c6f09914ac4a0298a7`.
- Bridge Technical Spec: v0.5 RELEASED_EFFECTIVE; Git `8010a121e1d8b3f244da7dd856931b1bce41da21`, blob `1ce788e84628764f1b58459e93aecd5c7fde641e`, Library SHA256 `2d182972b5edd6ccfd72c83b07d97907fa7fb63ed6eaa4de68b03b7e5165740a`.
- Accepted source manifest: Git `8c217d122f171de5bfef9b2c7cca6c823cd32eaa:docs/agent_handoff/BRIDGE/FOX2_BRG003_20FILE_HASH_RECONCILIATION_20261013.json`, blob `3ef8852964214c99161ed9ff4e463cb677af51cd`.
- Direct local comparison: all 20 source paths, sizes, and SHA256 values matched the accepted manifest before import; the source files were rechecked unchanged after import.

## Runtime

- Worktree: `C:\Projects\FOX2-worktrees\FOX2-BRG-003`
- Branch: `work/FOX2-BRG-003-SOURCE-BASELINE-copilot`
- Initial HEAD: `c8a0d517b8655868053e4923f5947c12975a5865`
- Remote branch pointed to the expected initial HEAD before the first write.
- Initial worktree status: clean; no untracked WIP.
- Writer check: no index lock, matching external process, or other active session for this worktree was observed.
- Model, mode, and quota: NOT_EXPOSED by the local runtime surfaces.
- Python toolchain: system Python 3.13.15; preinstalled pytest. No dependencies were installed.

## Imported inventory

Twenty manifest-listed files were imported, preserving their relative paths:

- `pyproject.toml`, `README.md`
- `src/fox2_agent_bridge/__init__.py`
- `src/fox2_agent_bridge/__main__.py`
- `src/fox2_agent_bridge/app.py`
- `src/fox2_agent_bridge/config.py`
- `src/fox2_agent_bridge/dispatch_poller.py`
- `src/fox2_agent_bridge/errors.py`
- `src/fox2_agent_bridge/hashing.py`
- `src/fox2_agent_bridge/ledger.py`
- `src/fox2_agent_bridge/logging_config.py`
- `src/fox2_agent_bridge/models.py`
- `src/fox2_agent_bridge/paths.py`
- `src/fox2_agent_bridge/process_lock.py`
- `src/fox2_agent_bridge/runtime_tools.py`
- `tests/conftest.py`
- `tests/test_config_paths.py`
- `tests/test_dispatch_poller.py`
- `tests/test_lock_logging_health.py`
- `tests/test_runtime_ledger.py`

Also added `.gitignore` and this result report. The ignore rules cover virtual environments, Python/test caches, environment files, SQLite DB/SHM/WAL files, logs, and temporary output.

Excluded by design: `config/bridge.example.toml`, `reports/BRG-010.md`, `reports/BRG-020.md`, runtime DB/sidecars, `.venv`, logs, caches, generated metadata, and all files outside the accepted manifest.

## Sanitization and security

Four copied source files were intentionally sanitized; the source project was not modified:

- `src/fox2_agent_bridge/config.py`: replaced literal user-profile tool paths with paths derived from `Path.home()`.
- `tests/test_config_paths.py`: replaced host-specific expected paths with exported path constants and `Path.home()`-based tool-path expectations.
- `tests/test_dispatch_poller.py`: constructed OAuth-token and credentialed-URL fixtures from clearly synthetic components at runtime; replaced the query-token fixture with a synthetic value.
- `tests/test_lock_logging_health.py`: constructed the OAuth-token and private-key redaction fixtures at runtime from synthetic components.

`bridge-test@example.invalid` remains as the local Git fixture identity; it is a reserved non-routable example address required by the local commit test. A pre-redacted asterisk-only URL fixture is retained as a negative parser case. The credentialed URL test now also uses a well-formed synthetic URI.

Secret scan: no literal user-profile paths, provider/AWS token patterns, private-key material, or real credentials were found in the imported target content. The credentialed-URL check was manually reviewed; its only static candidate was the pre-redacted asterisk-only fixture. No provider, broker, production, or external HTTP calls were made.

## Validation and Git result

- `python -m compileall -q src tests`: PASS.
- `PYTHONPATH=src python -m pytest -q`: PASS, 60 tests.
- The initial bare pytest invocation could not resolve the `src`-layout package; setting `PYTHONPATH=src` resolved the import without installing anything.
- `git diff --cached --check`: PASS.
- Staged scope: only `agent_bridge/**`.
- Final local status: clean after commit and push verification.
- Final local/remote HEAD: this report is included in the BRG-003 result commit; its exact object ID is provided in the execution response because a commit cannot embed its own object ID.

Execution stops at `PUSHED_UNREVIEWED`; independent CHAT readback and acceptance remain open.
