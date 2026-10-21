"""Read-only Git/claim/source binding for this single offline attempt."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
git = lambda *args: subprocess.check_output(['git', '-C', str(ROOT), *args])
sha = lambda b: hashlib.sha256(b).hexdigest()
claim_path = Path(git('rev-parse', '--absolute-git-dir').decode().strip()) / 'fox2-attempts'
claims = list(claim_path.glob('*.claim.json'))
assert len(claims) == 1
claim = json.loads(claims[0].read_text())
base = claim['runtime_base']
assert git('rev-parse', 'HEAD').decode().strip() == base
assert claim['state'] == 'STARTED_CONSUMED' and claim['attempt_number'] == claim['max_runs'] == 1
assert (claim['model'], claim['reasoning_effort'], claim['permission_profile']) == ('gpt-6.1-sol', 'high', 'FULL_ACCESS')
assert git('branch', '--show-current').decode().strip() == claim['task_branch']
remote = git('ls-remote', '--refs', 'origin', 'refs/heads/' + claim['task_branch']).decode().split()[0]
assert remote == base
dispatch_path = 'docs/agent_handoff/DISPATCH/' + claim['dispatch_id'] + '.json'
dispatch_bytes = git('show', claim['dispatch_commit'] + ':' + dispatch_path)
assert git('rev-parse', claim['dispatch_commit'] + ':' + dispatch_path).decode().strip() == claim['dispatch_blob']
dispatch = json.loads(dispatch_bytes)
assert dispatch['runtime_contract']['base_sha'] == base
assert dispatch['task']['sha256'] == claim['task_sha256']
assert dispatch['routing']['model'] == claim['model']
assert dispatch['runtime_contract']['branch'] == claim['task_branch']
control_remote = git('ls-remote', '--refs', 'origin', 'refs/heads/' + claim['dispatch_control_branch']).decode().split()[0]
assert control_remote == claim['dispatch_commit']
for earlier, later in [(claim['failed_result_source'], base), (claim['product_source'], claim['failed_result_source'])]:
    subprocess.run(['git', '-C', str(ROOT), 'merge-base', '--is-ancestor', earlier, later], check=True)
assert not git('diff', '--name-only', claim['failed_result_source'], base, '--', 'agent_bridge').strip()
assert set(git('diff', '--name-only', claim['failed_result_source'], base).decode().splitlines()) == {
    'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/lifecycle_wpf_contract_rework/' + p
    for p in ['task.md', 'prompt.md', 'preexec_a01.ps1', 'preexec_a01_v2.ps1']
} | {'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/lifecycle_wpf_contract_rework_a01.json'}
bindings = []
for name, commit, relative, expected in [
    ('task', claim['task_commit'], dispatch['task']['path'], claim['task_sha256']),
    ('prompt', claim['prompt_commit'], dispatch['prompt']['path'], claim['prompt_sha256']),
    ('policy', dispatch['policy']['git_commit_sha'], dispatch['policy']['git_path'], dispatch['policy']['sha256']),
    ('dictionary', dispatch['dictionary']['git_commit_sha'], dispatch['dictionary']['git_path'], dispatch['dictionary']['sha256']),
]:
    raw = git('show', commit + ':' + relative)
    assert sha(raw) == expected
    if name in ['task', 'prompt']:
        assert (ROOT / relative).read_bytes() == raw
    bindings.append({'name': name, 'commit': commit, 'path': relative, 'sha256': sha(raw)})
test_root = Path('C:/Projects/FOX2/.git/wpf-a01-test')
identical = []
for path in git('ls-files', 'agent_bridge').decode().splitlines() + ['agent_bridge/tests/test_lifecycle_wpf_contract.py']:
    assert (ROOT / path).read_bytes() == (test_root / path).read_bytes(), path
    identical.append({'path': path, 'sha256': sha((ROOT / path).read_bytes())})
try:
    with (claim_path / (claim['task_id'] + '.writer.lock')).open('rb'):
        pass
except PermissionError:
    writer_lock = 'OBSERVED_EXCLUSIVE_LOCK_HELD_BY_LAUNCHER'
else:
    raise AssertionError('writer lock not held')
value = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS',
    'stage': 'OFFLINE_BUILD_CORRECTION', 'claim': claim, 'dispatch_path': dispatch_path,
    'dispatch_sha256': sha(dispatch_bytes), 'remote_task_head_at_entry': remote,
    'remote_control_head': control_remote, 'bindings': bindings,
    'writer_lock': writer_lock, 'writer_observation': 'Initial process inventory: one task-scoped CODEX exec PID 1784; this process. No subagents.',
    'entry_worktree': 'CLEAN; observed before source writes', 'pre_start_product_changes': [],
    'test_snapshot': str(test_root), 'test_snapshot_files': identical,
    'test_snapshot_note': 'Detached same-base test worktree with exact byte copies of the three implementation/test files. No test edits or persistent Git/host configuration.',
    'historical_host_dispatch': 'CONSUMED_NO_REPLAY', 'real_host_lifecycle': 'NOT_RUN',
    'worker_f1_g3_g4_canary_mutation': 'NOT_RUN'}
(OUT / 'source_binding.json').write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
print('Source/task/prompt/policy/dictionary/Dispatch/claim/writer/test-snapshot binding: PASS')
