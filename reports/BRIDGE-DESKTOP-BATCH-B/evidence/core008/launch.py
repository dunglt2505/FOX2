"""One-time Dispatch 008 claim and exclusive worktree guard."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
EV = Path(__file__).parent
BASE = '0c739db91553ab8dd39a30b221f079b9538b0836'
CONTROL = '737e9851b2367f5e2aeb6597d0445b6df0ffcc71'
ID = 'FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-008'
sys.path.insert(0, str(ROOT / 'agent_bridge/src'))
from fox2_agent_bridge.preexec.engine import writer_lock, competing_writer
from jsonschema import Draft202012Validator, FormatChecker


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def save(name, value):
    (EV/name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n', encoding='utf-8')


if __name__ == '__main__':
    with writer_lock(ROOT):
        assert git('rev-parse', 'HEAD').decode().strip() == BASE
        assert git('branch', '--show-current').decode().strip() == 'work/FOX2-BRIDGE-DESKTOP-BATCH-B'
        assert not competing_writer(ROOT)
        assert git('status', '--porcelain', '--untracked-files=all').decode().splitlines() == [
            '?? reports/BRIDGE-DESKTOP-BATCH-B/evidence/core008/launch.py']
        raw = git('show', CONTROL+':docs/agent_handoff/DISPATCH/'+ID+'.json')
        d = json.loads(raw)
        Draft202012Validator(json.loads(git('show', BASE+':docs/agent_handoff/FOX2_LOCAL_AGENT_DISPATCH_SCHEMA_v3.json')),
                            format_checker=FormatChecker()).validate(d)
        for name in ('dictionary', 'policy', 'task', 'prompt'):
            v = d[name]
            c = v.get('git_commit_sha', v.get('commit_sha', v.get('git_commit')))
            p = v.get('git_path', v.get('path'))
            assert hashlib.sha256(git('show', c+':'+p)).hexdigest() == v['sha256']
            if 'git_blob_sha1' in v:
                assert git('rev-parse', c+':'+p).decode().strip() == v['git_blob_sha1']
        save('historical_hashes.json', {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
             for p in git('ls-tree', '-r', '--name-only', BASE, '--', 'reports/BRIDGE-DESKTOP-BATCH-B').decode().splitlines()})
        with (EV/'claim.json').open('x', encoding='utf-8') as f:
            json.dump(dict(dispatch_id=ID, control_commit=CONTROL, source_head=BASE,
                           consumed=True, max_runs=1, prior_dispatches_replayed=False,
                           claimed_at=datetime.datetime.now(datetime.timezone.utc).isoformat()), f, indent=2)
        save('launch.json', dict(bindings='PASS', schema='PASS', clean_initial_tree='PASS',
             branch_worktree_source_remote='PASS', exclusive_writer_lock=True,
             permission='danger-full-access / approval never', routing=d['routing'],
             current_execution_proof='007 preserved; current authorized Codex session', real_runtime_touched=False))
        print('DISPATCH_008_CONSUMED; EXCLUSIVE_LOCK_HELD', flush=True)
        while not (EV/'release.lock').exists():
            time.sleep(1)
