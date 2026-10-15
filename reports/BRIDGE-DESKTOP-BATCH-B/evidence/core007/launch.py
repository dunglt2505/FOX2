"""Dispatch 007 launch guard; holds the worktree lock until explicit release."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
EV = Path(__file__).parent
BASE = 'ce7a8253926b7489c79311e26d7dc75ba8c81fc6'
CONTROL = '7bac9176a24bbcbdd49f2074f88d355c5d88d906'
ID = 'FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-007'
sys.path.insert(0, str(ROOT / 'agent_bridge/src'))
from fox2_agent_bridge.preexec.engine import writer_lock, competing_writer
from fox2_agent_bridge.preexec.probes import agent_probe, tool_probe
from jsonschema import Draft202012Validator, FormatChecker


def save(name, value):
    (EV / name).write_text(json.dumps(value, sort_keys=True, indent=2) + '\n', encoding='utf-8', newline='\n')


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


if __name__ == '__main__':
    with writer_lock(ROOT):
        assert git('rev-parse', 'HEAD').decode().strip() == BASE
        assert git('branch', '--show-current').decode().strip() == 'work/FOX2-BRIDGE-DESKTOP-BATCH-B'
        assert git('ls-remote', 'origin', 'refs/heads/work/FOX2-BRIDGE-DESKTOP-BATCH-B').decode().split()[0] == BASE
        # The only write since the independently verified clean preflight is this guard.
        changed = git('status', '--porcelain=v1', '--untracked-files=all').decode().splitlines()
        assert changed == ['?? reports/BRIDGE-DESKTOP-BATCH-B/evidence/core007/launch.py'], changed
        assert not competing_writer(ROOT)
        raw = git('show', CONTROL + ':docs/agent_handoff/DISPATCH/' + ID + '.json')
        dispatch = json.loads(raw)
        schema = json.loads(git('show', BASE + ':docs/agent_handoff/FOX2_LOCAL_AGENT_DISPATCH_SCHEMA_v3.json'))
        Draft202012Validator(schema, format_checker=FormatChecker()).validate(dispatch)
        bindings = {}
        for name in ('dictionary', 'policy', 'task', 'prompt'):
            v = dispatch[name]
            commit = v.get('git_commit_sha', v.get('commit_sha', v.get('git_commit')))
            path = v.get('git_path', v.get('path'))
            assert hashlib.sha256(git('show', commit + ':' + path)).hexdigest() == v['sha256']
            if 'git_blob_sha1' in v:
                assert git('rev-parse', commit + ':' + path).decode().strip() == v['git_blob_sha1']
            bindings[name] = dict(commit=commit, path=path, sha256=v['sha256'], verified=True)
        assert not git('diff', '28550c49f07075c80cd730da9be80c72e5bc5e76', BASE, '--', 'agent_bridge').strip()
        route = dict(product='CODEX', **dispatch['routing'])
        tools = {n: tool_probe(n, ROOT) for n in ('git', 'python', 'pwsh', 'schtasks.exe')}
        assert all(v['status'] == 'PASS' for v in tools.values())
        probe = agent_probe(route, ROOT)
        save('readiness.json', dict(route=route, tools=tools, current_pinned_auth_capacity_probe=probe))
        assert probe['status'] == 'PASS', 'current route unavailable; no implementation authorized'
        previous = {p: hashlib.sha256(git('show', BASE + ':' + p)).hexdigest()
                    for p in git('ls-tree', '-r', '--name-only', BASE, '--', 'reports/BRIDGE-DESKTOP-BATCH-B').decode().splitlines()}
        save('historical_hashes.json', previous)
        with (EV / 'claim.json').open('x', encoding='utf-8', newline='\n') as stream:
            json.dump(dict(dispatch_id=ID, control_commit=CONTROL, source_head=BASE,
                           claimed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                           dispatch_consumed=True, max_runs=1, no_retry=True,
                           prior_dispatches_replayed=False), stream, indent=2)
            stream.write('\n')
        save('launch.json', dict(status='PASS', bindings=bindings, schema_validation='PASS',
             dispatch_sha256=hashlib.sha256(raw).hexdigest(), route=route,
             permission='danger-full-access / approval never', source_head=BASE,
             initial_clean_tree_independently_verified=True, competing_writer='NONE_OBSERVED',
             guard_pid=os.getpid(), worktree_lock_held=True, real_runtime_touched=False,
             core006_exact_package_and_wheel_independently_verified=True))
        print('DISPATCH_007_CLAIMED; LAUNCH_PASS; WORKTREE_LOCK_HELD', flush=True)
        while not (EV / 'release.lock').exists():
            time.sleep(1)
        print('WORKTREE_LOCK_RELEASED', flush=True)
