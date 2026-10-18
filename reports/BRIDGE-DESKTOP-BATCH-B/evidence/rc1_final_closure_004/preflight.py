"""Read-only immutable source/Dispatch verification for the single recovery run."""
import dataclasses
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)
def read(ref, path):
    return git('show', f'{ref}:{path}')
def sha(data):
    return hashlib.sha256(data).hexdigest()
control = 'dc79f8143eec471508bf37565bff38442ce0548a'
registry = 'b27f1085ee13d8dce56fd2735e100ea1616e6e23'
registry_path = 'docs/governance/FOX2_RC1_TRUST_BUNDLE_20261017/REGISTRY.json'
dispatch_path = 'docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-RC1-CODEX-004.json'
dispatch_bytes = read(control, dispatch_path)
d = json.loads(dispatch_bytes)
assert git('status', '--porcelain').decode().strip() in ('?? reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_final_closure_004/',)
assert git('branch', '--show-current').decode().strip() == d['runtime_contract']['branch']
assert git('rev-parse', 'HEAD').decode().strip() == d['runtime_contract']['base_sha']
assert str(ROOT).lower() == d['runtime_contract']['worktree'].replace('\\\\', '\\').lower()
assert d['max_runs'] == 1 and d['retry_of_dispatch_id'] == 'FOX2-DISPATCH-BRIDGE-RC1-CODEX-003'
assert d['routing'] == dict(model_policy='PINNED', auto_tier=None, model='gpt-6.1-sol', reasoning_effort='medium', permission_profile='FULL_ACCESS')
assert d['decision_receipt']['execution_authorized'] == 'YES'
for key in ('policy_check', 'task_state_check', 'source_binding_check', 'routing_r0_r7', 'assignment_check'):
    assert d['decision_receipt'][key] == 'PASS'
for key in ('task', 'prompt'):
    item = d[key]
    content = read(item.get('commit_sha', item.get('git_commit')), item['path'])
    assert sha(content) == item['sha256']
    if key == 'prompt':
        assert git('rev-parse', f"{item['git_commit']}:{item['path']}").decode().strip() == item['git_blob_sha1']
assert git('diff', '--name-only', d['source']['commit_sha'], d['runtime_contract']['base_sha']).decode().splitlines() == ['reports/BRIDGE-DESKTOP-BATCH-B/preexec/local_preflight.json']
receipt = json.loads((ROOT/'reports/BRIDGE-DESKTOP-BATCH-B/preexec/local_preflight.json').read_text())
assert receipt['source_head'] == d['source']['commit_sha']
assert receipt['overall_status'] == 'PASS' if 'overall_status' in receipt else receipt['status'] == 'PASS'
assert receipt['capabilities']['dotnet_wpf_build']['status'] == 'PASS'

skill_root = Path.home()/'.codex/plugins/cache/created-by-me-remote/fox2-skills-integrated/0.2.0'
spec = importlib.util.spec_from_file_location('fox2_resolver', skill_root/'shared/git_resolver.py')
resolver = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = resolver
spec.loader.exec_module(resolver)
cache = {}
def transport(path):
    if path not in cache:
        cache[path] = json.loads(subprocess.check_output(['gh', 'api', f'repos/dunglt2505/FOX2/{path}']))
    return cache[path]
remote = resolver.GitHub('dunglt2505/FOX2', transport=transport)
assert remote.read_file(dispatch_path, control) == dispatch_bytes
reg = json.loads(remote.read_file(registry_path, registry))
approval_ref = reg['owner_release_approval']['ref']
approval_bytes = remote.read_file(reg['owner_release_approval']['path'], approval_ref)
approval = json.loads(approval_bytes)
assert approval['status'] == 'APPROVED'
assert approval['whole_wp'] == 'FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
assert approval['immutable_source_commit'] == 'c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359'
assert not any(reg['protected_authority'].values())
bindings = {family: dataclasses.asdict(resolver.bind_effective(remote, registry, registry_path, family)) for family in reg['families']}
result = dict(status='PASS', attempt_started_utc=datetime.now(timezone.utc).isoformat(), dispatch_id=d['dispatch_id'], control_commit=control, dispatch_sha256=sha(dispatch_bytes), source=d['source'], execution_base=d['runtime_contract']['base_sha'], registry_commit=registry, approval_ref=approval_ref, approval_sha256=sha(approval_bytes), authority_basis='Externally nominated exact Owner approval in active user request; WP-only binding, no global promotion.', families=bindings, preexec='PASS_REUSED_0789e5d_RECEIPT_ONLY_DESCENDANT', routing=d['routing'], prior_dispatches_replayed=False)
(OUT/'preflight.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
(OUT/'dispatch.json').write_bytes(dispatch_bytes)
print(json.dumps(dict(status='PASS', families=len(bindings), dispatch=d['dispatch_id'])))
