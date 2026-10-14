"""Read-only Batch B launch checks; persist sanitized evidence in report scope."""
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys

import jsonschema

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'reports/BRIDGE-DESKTOP-BATCH-B'
CONTROL = '801a68beaeae8db8e8841ef53b009fc064ed9fc1'
BASE = 'fd84006c4152fa8f0cda7c5df7c0b4c56ac7d48b'
BRANCH = 'work/FOX2-BRIDGE-DESKTOP-BATCH-B'
DISPATCH_PATH = 'docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-001.json'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, indent=2, sort_keys=True) + '\n'
    path.write_bytes(text.encode('utf-8'))


dispatch_bytes = git('show', CONTROL + ':' + DISPATCH_PATH)
dispatch = json.loads(dispatch_bytes)
schema_path = 'docs/agent_handoff/FOX2_LOCAL_AGENT_DISPATCH_SCHEMA_v3.json'
schema_bytes = git('show', BASE + ':' + schema_path)
schema = json.loads(schema_bytes)
jsonschema.Draft202012Validator.check_schema(schema)
validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
errors = sorted(error.message for error in validator.iter_errors(dispatch))
bindings = {}
for key, commit_key, path_key in [
    ('dictionary', 'git_commit_sha', 'git_path'),
    ('policy', 'git_commit_sha', 'git_path'),
    ('task', 'commit_sha', 'path'),
    ('prompt', 'git_commit', 'path'),
]:
    binding = dispatch[key]
    raw = git('show', binding[commit_key] + ':' + binding[path_key])
    actual = hashlib.sha256(raw).hexdigest()
    bindings[key] = {
        'commit': binding[commit_key], 'path': binding[path_key],
        'expected_sha256': binding['sha256'], 'actual_sha256': actual,
        'hash_match': actual == binding['sha256'],
        'worktree_canonical_bytes_match': (ROOT / binding[path_key]).read_bytes().replace(b'\r\n', b'\n') == raw,
    }
bindings['prompt']['blob_sha1_match'] = git('rev-parse', dispatch['prompt']['git_commit'] + ':' + dispatch['prompt']['path']).decode().strip() == dispatch['prompt']['git_blob_sha1']

tools = {name: bool(shutil.which(name)) for name in [
    'git', 'python', 'pwsh', 'schtasks.exe', 'codex',
    'iscc', 'makensis', 'msbuild', 'dotnet', 'iexpress.exe', 'tar.exe',
]}
modules = {name: importlib.util.find_spec(name) is not None for name in [
    'setuptools', 'wheel', 'build', 'PyInstaller', 'jsonschema', 'pytest',
]}
import tomllib
project = tomllib.loads((ROOT / 'agent_bridge/pyproject.toml').read_text(encoding='utf-8'))
ledger_observations = []
for runtime in [Path(os.environ['LOCALAPPDATA']) / 'FOX2/AgentBridge',
                Path(os.environ['LOCALAPPDATA']) / 'AgentBridge',
                Path('C:/Projects/FOX2-AgentBridge')]:
    for path in runtime.rglob('*') if runtime.exists() else []:
        if path.suffix not in {'.db', '.sqlite', '.sqlite3'}:
            continue
        db = sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)
        counts = {}
        for (table,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'"):
            if not table.replace('_', '').isalnum():
                continue
            columns = [row[1] for row in db.execute('PRAGMA table_info(' + table + ')')]
            if 'dispatch_id' in columns:
                counts[table] = db.execute('SELECT COUNT(*) FROM ' + table + ' WHERE dispatch_id=?', (dispatch['dispatch_id'],)).fetchone()[0]
        db.close()
        ledger_observations.append({'runtime': runtime.name, 'ledger': path.name, 'matching_dispatch_row_counts': counts})

precheck = {
    'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'BLOCKED_PREEXEC', 'dispatch_id': dispatch['dispatch_id'],
    'control_commit': CONTROL, 'dispatch_sha256': hashlib.sha256(dispatch_bytes).hexdigest(),
    'schema': {'path': schema_path, 'sha256': hashlib.sha256(schema_bytes).hexdigest(), 'full_draft_2020_12_validation': 'PASS' if not errors else 'FAIL', 'errors': errors},
    'bindings': bindings,
    'head': git('rev-parse', 'HEAD').decode().strip(),
    'branch': git('branch', '--show-current').decode().strip(),
    'approved_base': BASE,
    'python_version': sys.version.split()[0], 'tools_on_path': tools, 'python_modules': modules,
    'declared_build_system': project['build-system'],
    'packaging_gate': {
        'status': 'MISSING', 'material': True,
        'missing': ['setuptools>=80,<90'],
        'reason': 'The declared Python package build backend is not installed. No package build or installer implementation is attempted after this mandatory launch gate fails.',
        'native_archive_tools_available': True,
        'native_archive_tools_note': 'IExpress and tar availability does not establish the declared Python build backend or a certified deterministic installed runtime. Optional bundler absence alone is not the blocker.',
        'dependencies_installed_by_this_attempt': False,
    },
    'existing_ledger_observations': ledger_observations,
    'lifecycle': {
        'implementation_started': False, 'installed_certification_started': False,
        'dispatch_claimed_by_this_attempt': False, 'dispatch_consumed_by_this_attempt': False,
        'existing_consumption': 'NONE_OBSERVED_IN_KNOWN_RUNTIME_LEDGERS',
        'auto_retry': False, 'dispatch_replayed': False,
        'next_action': 'Return blocker evidence to CHAT; do not automatically start or replay this dispatch.',
    },
    'writer_observation': {
        'initial_task_worktree_clean': True,
        'competing_writer': 'NONE_OBSERVED',
        'method': 'Registered worktree inventory, clean task status, sanitized Windows process inspection; no Bridge Worker or second Batch B implementation process observed.',
        'limitation': 'Observation is not an acquired execution lock; implementation was stopped before claim.',
    },
    'launch_configuration': {
        'requested': dispatch['routing'], 'process_model': 'gpt-6.1-sol',
        'process_reasoning_effort': 'medium', 'process_sandbox': 'danger-full-access',
        'session_approval_policy': 'never',
        'sources': ['Sanitized current Codex launch process inspection', 'Session permissions instructions'],
        'installed_runtime_attestation': 'NOT_RUN',
    },
}
assert not errors
assert all(binding['hash_match'] and binding['worktree_canonical_bytes_match'] for binding in bindings.values())
assert precheck['head'] == BASE and precheck['branch'] == BRANCH
assert not modules['setuptools']
assert all(count == 0 for entry in ledger_observations for count in entry['matching_dispatch_row_counts'].values())
write(OUT / 'evidence/preexecution.json', precheck)
gates = [{'gate': name, 'status': 'NOT_RUN', 'reason': 'Mandatory packaging launch gate failed; implementation and installed-runtime certification stopped.'} for name in dispatch['required_tests']]
write(OUT / 'evidence/acceptance_gates.json', {'count': len(gates), 'gates': gates, 'no_installed_runtime_pass_claimed': True})
report = '''# FOX2 Bridge Desktop Batch B: stopped at launch gate

Status: BLOCKED_PREEXEC. Whole-WP implementation and installed certification did not start.

The host Python environment lacks `setuptools>=80,<90`, the build requirement declared by `agent_bridge/pyproject.toml` for `setuptools.build_meta`. The required installer/package launch capability is therefore not established. No dependency installation, package build, installer change, or accepted Batch A rewrite was performed. Windows native IExpress/tar tools are available; their presence does not supply the declared Python build backend. Optional PyInstaller/build/wheel and common installer tools are also absent, but those optional absences are not independently classified as mandatory failures.

The controlling instruction requires STOP for a missing material packaging dependency. This attempt stops at that gate and publishes only bounded report evidence.

Pre-execution evidence:

- Full Dispatch Schema v3 validation, including date-time format and additional-property constraints: PASS.
- Exact Dictionary, Policy, Task, Prompt SHA-256 and Prompt Git blob binding: PASS.
- Initial branch and approved base: exact match; initial worktree clean.
- Control remote SHA: 801a68beaeae8db8e8841ef53b009fc064ed9fc1.
- Task remote SHA before this report: fd84006c4152fa8f0cda7c5df7c0b4c56ac7d48b.
- Current Codex process: gpt-6.1-sol / medium / danger-full-access; session approval policy never.
- Known runtime ledger: zero matching dispatch rows; no installed AgentBridge runtime found in the two inspected LocalAppData locations.
- Competing material writer: none observed. No execution lock was claimed after the failed prerequisite.

Read sources: immutable dispatch at control commit, pinned task, Dictionary v1.2, Policy V1.8.9, Dispatch Schema v3, Git-first Protocol v12, PreExec Evidence Protocol v1.1, Bridge Technical Spec v0.7 Candidate REV10, and Usage/Routing Contract Candidate REV5.

All 24 acceptance gates are recorded individually in `evidence/acceptance_gates.json`. Installed runtime, real eligible canary, runtime routing enforcement, usage, restart/no-replay, and full Bridge tests are NOT_RUN. Source/schema prechecks do not discharge the six carried Batch A certification obligations. No application readiness or Windows runtime PASS is asserted.

Lifecycle: no implementation, installation, Agent certification launch, Bridge claim, consumption, replay, or substitution occurred in this attempt. The existing ledger was opened read-only. This durable blocked record does not authorize automatic retry. Return the missing packaging capability to CHAT for reconciliation before any further execution.

Only reports/BRIDGE-DESKTOP-BATCH-B was written. Report-only publication is on the authorized task branch; no main, PR, merge, release, deploy, provider, broker, or LIVE operation is performed. Publication/readback evidence is recorded separately from installed-runtime acceptance.

FOX2_BRIDGE_DESKTOP_BATCH_B_PUSHED_UNREVIEWED is not earned by a blocked report. INTERNAL_FOX2_BRIDGE_READY remains an independently accepted CHAT target.
'''
(OUT / 'report.md').write_bytes(report.encode('utf-8'))
write(OUT / 'evidence_manifest.json', {
    'status': 'BLOCKED_PREEXEC', 'dispatch_id': dispatch['dispatch_id'],
    'control_commit': CONTROL, 'approved_base': BASE,
    'files': [{'path': p.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size}
              for p in sorted(OUT.rglob('*')) if p.is_file() and p.name != 'evidence_manifest.json'],
    'manifest_self_hash': 'Excluded to avoid recursive hashing; exact bytes verified through Git readback.',
    'acceptance': '24 NOT_RUN; mandatory packaging launch failure',
})
print(json.dumps({'status': 'BLOCKED_PREEXEC', 'schema': 'PASS', 'binding_hashes': 'PASS', 'missing_build_backend': 'setuptools>=80,<90', 'acceptance_gate_count': len(gates)}))
