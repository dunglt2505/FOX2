"""Single Batch A acceptance cycle with canonical, hashed evidence."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'agent_bridge/src'))
from fox2_agent_bridge.artifacts import write_json, write_text, text_hygiene
from fox2_agent_bridge.agent_policy import help_text, permission_arguments, policy_arguments, version_text

REPORT = ROOT / 'reports/BRIDGE-DESKTOP-BATCH-A'
BASE = 'ef9f290e73c4f4500900528656212c38acf43a4f'
START = '9224b144f704964907162e77ebec520aa9b09f77'
BRANCH = 'work/FOX2-BRIDGE-DESKTOP-BATCH-A-codex'
ALLOW = ('agent_bridge/', 'reports/BRIDGE-DESKTOP-BATCH-A/')
SUPPORT = {
    'PROJECT_DICTIONARY_BINDING': ['test_project_dictionary_binding_deterministic_drift'],
    'PROJECT_DICTIONARY_DRIFT_CHECK': ['test_project_dictionary_binding_deterministic_drift'],
    'DISPATCH_V3_RUNTIME_COMPATIBILITY': ['test_dictionary_schema_exact_normalized_tuple', 'test_dictionary_v3_fails_closed', 'test_dictionary_non_bridge_never_spawned'],
    'V2_COMPATIBILITY': ['test_dictionary_schema_exact_normalized_tuple', 'test_dictionary_filename_and_legacy_bound_policy'],
    'V06_COMPATIBILITY': ['test_dispatch_validation_accepts_minimal_canary', 'test_dictionary_schema_exact_normalized_tuple'],
    'STABLE_DISPATCH_PATH': ['test_dictionary_stable_dispatch_discovery'],
    'CONTROL_BRANCH_REGISTRY': ['test_dictionary_control_branch_registry'],
    'SINGLE_NORMALIZED_EXECUTION_PATH': ['test_batch_real_git_delivery_has_one_publication_path', 'test_batch_post_start_zero_exit_capacity_never_publishes'],
    'WORKER_RECOVERY': ['test_restart_stages_never_replay', 'test_backoff_bounded_and_resets',
                        'test_controls_work_while_singleton_owned', 'test_idle_pause_resume_check_now_durable'],
    'CODEX_EXACT_CONFIG': ['test_batch_exact_policies_and_material_compatibility', 'test_codex_adapter_passes_model_and_keeps_safety'],
    'COPILOT_EXACT_POLICY': ['test_batch_exact_policies_and_material_compatibility'],
    'USAGE_PERSISTENCE': ['test_batch_immutable_tuple_and_usage_survive_restart', 'test_batch_streamed_telemetry_survives_output_tail'],
    'POST_START_QUOTA_RECONCILIATION': ['test_batch_post_start_zero_exit_capacity_never_publishes', 'test_nonzero_after_agent_start_needs_reconciliation'],
    'NO_REPLAY': ['test_batch_claim_race_consumes_once', 'test_restart_stages_never_replay', 'test_batch_real_git_delivery_has_one_publication_path'],
    'NO_AGENT_SUBSTITUTION': ['test_full_runner_exact_routing_and_failure_no_fallback', 'test_batch_post_start_zero_exit_capacity_never_publishes'],
    'GIT_DELIVERY_POLICY_ALIGNED': ['test_batch_real_git_delivery_has_one_publication_path'],
    'NO_DUPLICATE_PUBLICATION_PATH': ['test_batch_real_git_delivery_has_one_publication_path'],
    'FULL_ACCESS_CODEX': ['test_codex_exec_uses_full_access_and_never_approval', 'test_batch_streamed_telemetry_survives_output_tail'],
    'FULL_ACCESS_COPILOT': ['test_batch_streamed_telemetry_survives_output_tail'],
    'PERMISSION_PREFLIGHT': ['test_batch_full_access_preflight_blocks_before_spawn', 'test_batch_dispatch_permission_and_owner_fail_closed'],
    'MATERIAL_TOOL_COMPATIBILITY': ['test_batch_exact_policies_and_material_compatibility'],
    'NON_MATERIAL_VERSION_MISMATCH_CONTINUES': ['test_batch_exact_policies_and_material_compatibility'],
    'MATERIAL_CAPABILITY_MISSING_BLOCKS': ['test_batch_full_access_preflight_blocks_before_spawn', 'test_batch_exact_policies_and_material_compatibility'],
    'CANONICAL_GENERATED_ARTIFACT_PIPELINE': ['test_batch_canonical_artifacts_and_logs'],
    'TRAY_READ_ONLY_USAGE_DISPLAY': ['test_batch_tray_usage_controls_are_read_only', 'test_powershell_scripts_parse_and_startup_mock_is_idempotent'],
}
PATTERNS = [r'\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b',
            r'\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b', r'(?i)\bBearer\s+[^\s\\]+',
            r'-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----']


def git(*args):
    result = subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True, check=True)
    return result.stdout.decode('utf-8')


def changed_paths():
    paths = set(filter(None, git('diff', START, '--name-only', '-z').split('\0')))
    paths.update(filter(None, git('ls-files', '--others', '--exclude-standard', '-z').split('\0')))
    assert all(path.startswith(ALLOW) for path in paths), 'changed path outside allowed scope'
    return sorted(paths)


def scan(paths):
    for name in paths:
        path = ROOT / name
        if path.is_file():
            content = path.read_text(encoding='utf-8')
            assert not any(re.search(pattern, content) for pattern in PATTERNS), f'secret scan failed: {name}'


def verify_outputs():
    paths = changed_paths()
    assert git('branch', '--show-current').strip() == BRANCH, 'wrong task branch'
    git('merge-base', '--is-ancestor', BASE, 'HEAD')
    git('diff', '--check'); git('diff', '--cached', '--check')
    for path in REPORT.rglob('*'):
        if path.is_file():
            text_hygiene(path)
    scan(paths)
    manifest = json.loads((REPORT / 'evidence_manifest.json').read_text(encoding='utf-8'))
    for entry in manifest['files']:
        assert hashlib.sha256((ROOT / entry['path']).read_bytes()).hexdigest() == entry['sha256'], f"hash mismatch: {entry['path']}"
    assert all(value == 'PASS' for value in manifest['acceptance'].values())
    return paths, manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    assert git('branch', '--show-current').strip() == BRANCH, 'wrong branch'
    git('merge-base', '--is-ancestor', BASE, 'HEAD')
    if args.verify_only:
        paths, manifest = verify_outputs()
        print(json.dumps({'status': 'PASS', 'tests': manifest['pytest']['tests'], 'changed_paths': len(paths), 'manifest_hashes': 'PASS'}))
        return
    assert git('rev-parse', 'HEAD').strip() == START, 'unexpected start HEAD'
    changed_paths()
    evidence = REPORT / 'evidence'
    evidence.mkdir(parents=True, exist_ok=True)
    environment = {**os.environ, 'PYTHONPATH': str(ROOT / 'agent_bridge/src')}
    focused = subprocess.run([sys.executable, '-m', 'pytest',
        str(ROOT / 'agent_bridge/tests/test_project_dictionary.py'),
        str(ROOT / 'agent_bridge/tests/test_batch_a.py'), '-q',
        '--junitxml=' + str(evidence / 'focused_pytest.xml')], cwd=ROOT, env=environment,
        capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=300)
    write_text(evidence / 'focused_pytest.txt', focused.stdout + focused.stderr)
    assert focused.returncode == 0, 'focused Dictionary/runtime regressions failed'
    write_text(evidence / 'focused_pytest.xml', (evidence / 'focused_pytest.xml').read_text(encoding='utf-8'))
    result = subprocess.run([sys.executable, '-m', 'pytest', str(ROOT / 'agent_bridge/tests'), '-q',
        '--junitxml=' + str(evidence / 'pytest.xml')], cwd=ROOT, env=environment, capture_output=True,
        text=True, encoding='utf-8', errors='replace', timeout=300)
    write_text(evidence / 'pytest.txt', result.stdout + result.stderr)
    assert result.returncode == 0, 'full Bridge tests failed; see evidence/pytest.txt'
    write_text(evidence / 'pytest.xml', (evidence / 'pytest.xml').read_text(encoding='utf-8'))
    suite = ET.parse(evidence / 'pytest.xml').getroot().find('testsuite')
    assert suite is not None
    summary = {key: int(suite.attrib[key]) for key in ('tests', 'failures', 'errors', 'skipped')}
    assert summary['tests'] >= 164 and summary['failures'] == summary['errors'] == summary['skipped'] == 0
    cases = [case.attrib['name'].split('[')[0] for case in suite.findall('testcase')]
    for required in SUPPORT.values():
        assert all(name in cases for name in required), 'acceptance test evidence missing'
    live_tools = {}
    for product in ('CODEX', 'COPILOT'):
        path = shutil.which(product.lower())
        assert path, 'material CLI missing'
        executable = Path(path)
        cli_help = help_text(executable, 'exec') if product == 'CODEX' else help_text(executable)
        permissions, applied = permission_arguments({'product': product}, cli_help + '\n' + help_text(executable))
        selection = ({'product': product, 'model_policy': 'PINNED', 'model': 'gpt-6.1-sol', 'reasoning_effort': 'high'}
                     if product == 'CODEX' else {'product': product, 'auto_tier': 'balance'})
        arguments, metadata = policy_arguments(selection, cli_help)
        write_text(evidence / (product.lower() + '_help.txt'), cli_help)
        live_tools[product] = {'executable': str(executable), 'version': version_text(executable),
            'capability_preflight': 'PASS', 'permission_arguments': permissions, 'applied_intent': applied,
            'selection_arguments': arguments, 'paid_execution': 'NOT_RUN', 'observed_model': None, 'observed_quota': None}
    write_json(evidence / 'cli_capabilities.json', live_tools)
    acceptance = {name: 'PASS' for name in SUPPORT}
    acceptance.update({name: 'PASS' for name in ('TEXT_ARTIFACT_HYGIENE', 'FULL_BRIDGE_TESTS', 'SECRET_SCAN', 'CHANGED_PATH_ALLOWLIST', 'GIT_DIFF_CHECK')})
    rows = '\n'.join(f'- {key}=PASS' for key in acceptance)
    report = f'''# BRIDGE-DESKTOP-BATCH-A

Implemented as one work package on `{BRANCH}`, based on accepted FIX-01 `{BASE}`.
Execution start HEAD: `{START}`. Delivery owner: AGENT.
State: VALIDATED_FOR_AGENT_PUBLICATION_UNREVIEWED.

Final full-suite outcome: **{summary['tests']} passed** on Python {sys.version.split()[0]}.

The background Worker retains its Git durable mailbox, pause/resume/check-now,
bounded backoff and singleton. Recovery requires an explicit zero exit and valid
recorded configuration; it only verifies remote results. Consumed claims survive
restart, races and quota failures without replay or Agent substitution.

Exact adapters persist the immutable tuple and requested/applied/observed model,
reasoning, permission, usage and capacity metadata in SQLite checkpoints, runtime
reports and Tray status. Structured counters survive stdout truncation. Codex uses
danger-full-access/never. Copilot uses allow-all tools/paths/URLs and task-local
Native Auto tier. Missing material capabilities and permission mismatch block
before launch. Versions are recorded without equality gates.

Dispatch delivery_owner selects AGENT verification or one BRIDGE publication.
Four real local Git regressions cover both owners and both products, proving one
result commit, remote SHA equality and replay rejection. Existing schema 0.6
legacy dispatches retain BRIDGE ownership when delivery_owner is absent.

Generated text uses a shared atomic UTF-8/LF helper, deterministic JSON, trailing
whitespace removal and post-write hygiene. Runtime logs use the shared canonical
text routine. Tray model/permission/usage/capacity entries are disabled read-only
items. Fixed controls and per-user startup remain covered by headless PowerShell.

{rows}

Evidence: evidence/pytest.xml, evidence/pytest.txt, evidence/cli_capabilities.json,
evidence/verification.json and SHA-256 entries in evidence_manifest.json.

Tests use fake Agents, real local child failure fixtures and actual local Git
publication; CLI help/version probes are real and harmless. Startup is mocked in
PowerShell; no paid Agent invocation, manual Tray interaction, real Windows logon,
PR/main/merge/deploy/provider/broker/LIVE was performed. Actual live model, usage
and quota remain unknown; fixture observations are not live account telemetry.

Project Dictionary rollup follows the exact CHAT same-WP plan. The deterministic
binding is generated from exact bytes at
`28866ee6a61bde3fc3837ebd999c7b470afc7486:docs/governance/FOX2_PROJECT_DICTIONARY_v1.json`.
A byte drift gate checks identity, versions, paths and registry identifiers before
publication. Default polling selects the Dictionary current control branch;
explicit legacy selection remains supported, with one branch per profile.

Discovery uses the Dictionary canonical DISPATCH path and its two legacy patterns.
External v3 and v2 shapes normalize into the existing common validator and execution
engine. Current v3 binds Dictionary hash/version/path/commit and current Policy;
immutable v2 records retain their own Policy identity. Non-BRIDGE execution paths,
invalid routing, protected authority expansion and malformed runtime identities
fail closed before spawn. Required capabilities/tests and exact owners are preserved.
Legacy 0.6 retains its historical missing-owner default. Publication/replay and
quota/auth/capacity reconciliation run against all three schemas, both Agents and
both owners through the same engine. Focused evidence is in focused_pytest.xml/txt.
The Dictionary contains machine identity only; no Policy/BRD semantics were moved.
The pinned release names a v3 schema path whose file is absent at that commit;
v3 follows the CHAT plan's Dictionary block over the bound external dispatch shape.

Agent will publish only allowed paths to this task branch and verify the remote
SHA after commit. This pre-publication manifest excludes its own hash and does
not claim a post-commit SHA before Git creates it.
'''
    write_text(REPORT / 'report.md', report)
    write_json(evidence / 'verification.json', {'status': 'PASS', 'work_package': 'BRIDGE-DESKTOP-BATCH-A',
        'accepted_base_sha': BASE, 'start_head': START, 'branch': BRANCH, 'python': sys.version.split()[0],
        'pytest': summary, 'acceptance': acceptance, 'support_tests': SUPPORT,
        'evidence_classes': {'agent_execution': 'FAKE_CLI_AND_REAL_LOCAL_CHILD',
            'git_publication': 'REAL_LOCAL_BARE_REMOTE', 'desktop': 'REAL_HEADLESS_POWERSHELL_AND_MOCKED_STARTUP',
            'cli_capabilities': 'REAL_HELP_AND_VERSION_WITHOUT_AGENT_EXECUTION'}})
    paths = changed_paths()
    scan(paths)
    for path in REPORT.rglob('*'):
        if path.is_file():
            text_hygiene(path)
    git('diff', '--check'); git('diff', '--cached', '--check')
    prior_manifest = json.loads(git('show', START + ':reports/BRIDGE-DESKTOP-BATCH-A/evidence_manifest.json'))
    evidence_paths = sorted(set(paths) | {entry['path'] for entry in prior_manifest['files']})
    assert all(name.startswith(ALLOW) for name in evidence_paths)
    files = [{'path': name, 'sha256': hashlib.sha256((ROOT / name).read_bytes()).hexdigest()} for name in evidence_paths
             if (ROOT / name).is_file() and name != 'reports/BRIDGE-DESKTOP-BATCH-A/evidence_manifest.json']
    write_json(REPORT / 'evidence_manifest.json', {'schema_version': 1, 'work_package': 'BRIDGE-DESKTOP-BATCH-A',
        'delivery_status': 'VALIDATED_FOR_AGENT_PUBLICATION_UNREVIEWED', 'delivery_owner': 'AGENT',
        'base_sha': BASE, 'start_head': START, 'branch': BRANCH,
        'allowed_scope': ['agent_bridge/**', 'reports/BRIDGE-DESKTOP-BATCH-A/**'],
        'pytest': summary, 'acceptance': acceptance, 'files': files, 'manifest_self_hash': 'EXCLUDED',
        'live_model_and_quota_observations': 'NOT_EXPOSED', 'manual_paid_execution': 'NOT_RUN'})
    paths, manifest = verify_outputs()
    print(json.dumps({'status': 'PASS', 'tests': summary['tests'], 'changed_paths': len(paths),
        'secret_scan': 'PASS', 'text_hygiene': 'PASS', 'manifest_hashes': 'PASS', 'diff_check': 'PASS'}))


if __name__ == '__main__':
    main()
