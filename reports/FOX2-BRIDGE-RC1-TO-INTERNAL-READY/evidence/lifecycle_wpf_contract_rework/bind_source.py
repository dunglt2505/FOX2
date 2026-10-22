"""Bind A02 to immutable Dispatch, PreExec, source and the running launcher claim."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
BASE = '4504bf95dd2baf474b30f896b23365c52fe10c9f'
SNAPSHOT = '1a11fa0b232a69f0c26a0b4029c331ee2a8c840f'
CONTROL = '126e8d857e7e4964fe05a47d558215763779535f'
BRANCH = 'work/FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02-20261022'
git = lambda *a: subprocess.check_output(['git', '-C', str(ROOT), *a])
sha = lambda b: hashlib.sha256(b).hexdigest()
claim_dir = Path(git('rev-parse', '--absolute-git-dir').decode().strip()) / 'fox2-attempts'
claims = list(claim_dir.glob('*.claim.json'))
assert len(claims) == 1
claim = json.loads(claims[0].read_text())
assert claim['state'] == 'RUNNING_CONSUMED' and claim['dispatch_consumed'] is True
assert claim['runtime_base'] == BASE and claim['recovery_snapshot'] == SNAPSHOT
assert (claim['model'], claim['reasoning'], claim['permission_profile']) == ('gpt-6.1-sol', 'high', 'FULL_ACCESS')
assert git('rev-parse', 'HEAD').decode().strip() == BASE
assert git('branch', '--show-current').decode().strip() == BRANCH
remote = lambda b: git('ls-remote', '--refs', 'origin', 'refs/heads/' + b).decode().split()[0]
assert remote(BRANCH) == BASE
assert remote('work/FOX2-DISPATCH-chat') == CONTROL == claim['dispatch_commit']
subprocess.run(['git', 'merge-base', '--is-ancestor', SNAPSHOT, BASE], check=True)
setup = git('diff', '--name-only', SNAPSHOT, BASE).decode().splitlines()
assert set(setup) == {
    'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/lifecycle_wpf_contract_rework_a02/' + n + '.md'
    for n in ['task', 'prompt']
} | {'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/lifecycle_wpf_contract_rework_a02_preflight.json'}
assert not git('diff', '--name-only', SNAPSHOT, BASE, '--', 'agent_bridge').strip()
dispatch_path = 'docs/agent_handoff/DISPATCH/' + claim['dispatch_id'] + '.json'
raw = git('show', CONTROL + ':' + dispatch_path)
dispatch = json.loads(raw)
assert git('rev-parse', CONTROL + ':' + dispatch_path).decode().strip() == claim['dispatch_blob']
assert dispatch['runtime_contract']['base_sha'] == BASE
assert dispatch['runtime_contract']['branch'] == BRANCH
assert Path(dispatch['runtime_contract']['worktree']).resolve() == ROOT.resolve()
assert dispatch['max_runs'] == 1 and dispatch['delivery_owner'] == 'AGENT'
bindings = []
for name, commit, path, expected in [
    ('task', dispatch['task']['commit_sha'], dispatch['task']['path'], dispatch['task']['sha256']),
    ('prompt', dispatch['prompt']['git_commit'], dispatch['prompt']['path'], dispatch['prompt']['sha256']),
    ('policy', dispatch['policy']['git_commit_sha'], dispatch['policy']['git_path'], dispatch['policy']['sha256']),
    ('dictionary', dispatch['dictionary']['git_commit_sha'], dispatch['dictionary']['git_path'], dispatch['dictionary']['sha256']),
    ('routing', 'bcd008983b61349646a5198ff243069f81484fae', 'docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_4_0_OWNER_OVERRIDE_ROUTING_INDEX_20261019.md', '5759b9a8d63ef165ef63c60ecc601198e39296518c5a1eb91db54555ccd07205'),
    ('preexec', BASE, 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/lifecycle_wpf_contract_rework_a02_preflight.json', '0d265137e1567a2b47999e99716cacca9c6121bb2ac606688b949b4f88aa6c2f'),
]:
    content = git('show', commit + ':' + path)
    assert sha(content) == expected, name
    if name in ['task', 'prompt', 'preexec']:
        assert content == (ROOT / path).read_bytes()
    bindings.append({'name': name, 'commit': commit, 'path': path, 'blob': git('rev-parse', commit + ':' + path).decode().strip(), 'sha256': expected})
    if name == 'dictionary':
        dictionary = json.loads(content)
    if name == 'preexec':
        receipt = json.loads(content)
assert receipt['status'] == 'PASS' and not receipt['blockers']
for capability in ['codex_current_probe', 'codex_auth_capacity', 'one_writer', 'worktree_clean']:
    assert receipt['capabilities'][capability]['status'] == 'PASS'
protocol_path = dictionary['current']['git_first_protocol']['path']
protocol_commit = 'f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa'
assert git('rev-parse', protocol_commit + ':' + protocol_path).decode().strip() == 'd34a022f2bda39a167a404c8530e57b30f337cb9'
bindings.append({'name': 'protocol', 'commit': protocol_commit, 'path': protocol_path, 'sha256': sha(git('show', protocol_commit + ':' + protocol_path))})
governance = 'd34da1e3b4918a902646621b487ca8ad3e05b0e0'
assert git('rev-parse', governance + ':' + dictionary['current']['dispatch_schema']['path']).decode().strip() == '1692061941e2bef498515cd0e96b9b3046119ebb'
import jsonschema
schema = json.loads(git('show', governance + ':' + dictionary['current']['dispatch_schema']['path']))
jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(dispatch)
review_path = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/LIFECYCLE_WPF_REWORK_A02_PASS_TO_ASSIGN_20261022.md'
review_commit = '61b75156bb4b241b88a26c0c11cb8af79f79a94b'
assert 'PASS_TO_ASSIGN' in git('show', review_commit + ':' + review_path).decode()
provenance_path = OUT.relative_to(ROOT).as_posix() + '/recovery_codex001_snapshot.json'
provenance_raw = git('show', SNAPSHOT + ':' + provenance_path)
assert (ROOT / provenance_path).read_bytes() == provenance_raw
provenance = json.loads(provenance_raw)
assert (provenance['source_attempt_state'], provenance['source_attempt_exit_code'], provenance['failure_class']) == ('EXITED_CONSUMED', 1, 'CODEX_USAGE_LIMIT')
assert provenance['source_attempt_delivery'] == 'NEEDS_RECONCILIATION'
assert not provenance['replay_allowed'] and not provenance['chat_accepted'] and not provenance['snapshot_is_agent_result']
# Inventory only Agent command lines. No credentials, Bridge data or lifecycle are read.
command = "Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'codex.exe' -and $_.CommandLine -match ' exec ' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -AsArray -Compress"
processes = json.loads(subprocess.check_output(['pwsh', '-NoProfile', '-Command', command], text=True))
assert len(processes) == 1 and processes[0]['ProcessId'] == claim['process_id'], processes
cli_version = subprocess.check_output([receipt['capabilities']['codex_cli']['executable'], '--version'], text=True).strip()
assert cli_version == 'codex-cli 0.162.1'
value = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS', 'stage': 'OFFLINE_BUILD_CORRECTION_A02',
    'claim': claim, 'dispatch_path': dispatch_path, 'dispatch_sha256': sha(raw), 'bindings': bindings,
    'remote_task_head_at_entry': BASE, 'remote_control_head': CONTROL,
    'pre_start_setup_paths': setup, 'pre_start_product_drift': [],
    'entry_worktree': 'CLEAN observed by git status --porcelain before any source/evidence writes',
    'one_writer': {'status': 'PASS', 'processes': processes, 'subagents': 0, 'cli_version': cli_version},
    'auth_capacity': 'PreExec REV3 authenticated service probe PASS; current pinned execution active; no numeric quota inferred',
    'source_bytes': 'SOURCE_BYTES_VERIFIED',
    'scoped_authority': 'Owner task plus fresh CHAT PASS_TO_ASSIGN and Dispatch; AUTHORITY_VERIFIED for bounded offline BUILD only',
    'global_effectivity_or_runtime_promotion': 'NOT_CLAIMED; TechSpec REV10 CANDIDATE_NO_PROMOTION',
    'chat_intake': {'commit': review_commit, 'path': review_path, 'sha256': sha(git('show', review_commit + ':' + review_path))},
    'governance_commit_for_schemas': governance, 'result_schema_path': dictionary['current']['result_schema']['path'],
    'a01_no_replay': provenance, 'recovery_provenance_sha256': sha(provenance_raw),
    'real_host_lifecycle': 'NOT_RUN', 'worker_f1_g3_g4_canary_mutation': 'NOT_RUN',
    'skill_coverage': {'source-resolver': 'APPLIED', 'governance-preflight': 'APPLIED', 'agent-route-runtime': 'APPLIED: existing pinned route', 'result-review': 'N_A: independent CHAT intake follows delivery', 'feature-certification': 'N_A: offline BUILD verification only; no feature promotion', 'agent-prompt-builder': 'N_A: consuming existing assignment; no new handoff'}}
(OUT / 'source_binding.json').write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')
print('A02 source/task/prompt/Dispatch/schema/PreExec/claim/one-writer/no-replay: PASS')
