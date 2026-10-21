"""Verify the user-pinned immutable chain; byte proof is not global release."""
from datetime import datetime, UTC
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
START = '94c936b1d93bbfcee5818db24dd75bd9bb32733f'
SOURCES = [
    ('registry', '1f04d62fb7039646c9a213f04a1f1eb17e0f2cc5', '1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35', None),
    ('resolution', 'b04ded4b9d7fb241dc69ad25097eb474807cf68c', '186fdbc72dc1b22e97330895142d68600591ac21', None),
    ('policy', '96175ac4f39197794a04e695f0046fa7ef9321fe', '2d373f374f906bf7959062050bbeae5350b0c482',
     '281bcd61bb8c2fb7929ac474f218adbd004bbca6bc21e5311944a0e590723e1e'),
    ('dictionary', 'b25f7f728de67cf8595bf24f22fcbd79ef50babc', '6c8f30e2e6b07f2e65e45c14faab99672d036083',
     '8a64771916d9e3d447f560658e20b307b5945a5d6b3820ea61cd0298636abe1d'),
    ('routing', 'bcd008983b61349646a5198ff243069f81484fae', '14d2e95e419cc67c3e0cf851cc806a96cf885b7e',
     '5759b9a8d63ef165ef63c60ecc601198e39296518c5a1eb91db54555ccd07205'),
    ('protocol', 'f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa', 'd34a022f2bda39a167a404c8530e57b30f337cb9', None),
    ('brd', 'e13820c05ec0c7e97853daa61f6f5fb6b73391cc', '99971d65ccb90874e75ace54e6a4f8ec21ba0188', None),
    ('techspec', 'e13820c05ec0c7e97853daa61f6f5fb6b73391cc', '5a82bd74b30f71f7b46652f67a70cd7768f68143', None),
    ('task', '653e49fc0d0f15981bf230995925c89d6994723d', '7f0b82e56f7bfa001e40bb176bb26b0ef918c609',
     '708ab8addd6e6cbcde581bc03efc66dfb518eb8ac575d568c2be825827e649b9'),
]


def git(*arguments):
    return subprocess.check_output(['git', *arguments], cwd=ROOT)


def main():
    observations = []
    for name, commit, blob, expected in SOURCES:
        rows = git('ls-tree', '-r', commit).decode().splitlines()
        matches = [r.split('\t', 1)[1] for r in rows if r.split('\t', 1)[0].endswith(' ' + blob)]
        assert len(matches) == 1, name
        raw = git('cat-file', 'blob', blob)
        observed = hashlib.sha256(raw).hexdigest()
        assert not expected or expected == observed, name
        observations.append(dict(id=name, commit=commit, blob=blob, path=matches[0],
                                 sha256=observed, status='SOURCE_BYTES_VERIFIED'))
    for path, commit in (
        ('docs/architecture/FOX2_BRIDGE_F1_G1_DESIGN_ACCEPTANCE_20261021.md', '9c27e7c7104facdb7f083350f38d2451939b6c2a'),
        ('docs/architecture/FOX2_BRIDGE_F1_G2_INTEGRATED_BUILD_SCOPE_CANDIDATE_20261021.md', '9410edb0d88631c33ffda8494b238ec9f4446dc1'),
        ('docs/architecture/FOX2_BRIDGE_F1_G2_SOURCE_ROUTE_PREEXEC_ENTRY_20261021.md', '0feff4223746a48e449bb961eecabb1d86388e41'),
        ('docs/architecture/FOX2_BRIDGE_F1_G2_PREEXEC_CONTRACT_CANDIDATE_20261021.md', '2f8fa342613ec7f64204d8e192559847581235e6'),
    ):
        raw = git('show', commit + ':' + path)
        assert raw == git('show', START + ':' + path)
        observations.append(dict(id=Path(path).stem, commit=commit, path=path,
            sha256=hashlib.sha256(raw).hexdigest(), status='SOURCE_BYTES_VERIFIED'))
    receipt_path = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/g2_preflight.json'
    receipt = json.loads((ROOT / receipt_path).read_text())
    assert receipt['status'] == 'PASS'
    assert receipt['candidate_route'] == dict(auto_tier=None, product='CODEX', model_policy='PINNED',
        model='gpt-6.1-sol', reasoning_effort='high', permission_profile='FULL_ACCESS')
    assert receipt['worktree']['competing_writer'] == 'NONE_OBSERVED'
    assert Path(receipt['worktree']['path']).resolve() == ROOT.resolve()
    assert receipt['dispatch_state'] == dict(dispatch_consumed=False, executable_dispatch_published=False)
    assert receipt['agent_execution_started'] is False
    git('merge-base', '--is-ancestor', receipt['source_head'], START)
    task_path = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/g2/task.md'
    assert git('show', receipt['source_head'] + ':' + task_path) == git('show', SOURCES[-1][1] + ':' + task_path)
    assert git('branch', '--show-current').decode().strip() == receipt['task_branch']
    result = {'command': 'python evidence/g2/source_readback.py', 'exit_code': 0,
        'observed_at': datetime.now(UTC).isoformat(), 'start_sha': START,
        'bindings': observations, 'preexec': {'path': receipt_path, 'status': receipt['status'],
            'checked_at': receipt['checked_at'], 'source_head': receipt['source_head']},
        'active_session': {'model': 'gpt-6.1-sol', 'effort': 'high', 'sandbox': 'danger-full-access',
            'approval': 'never', 'observed_turn_context': '2026-10-21T03:31:22.526Z'},
        'one_writer': 'NONE_OBSERVED: other active thread metadata uses project-chat workspace; no G2 writer observed',
        'authority': 'USER_PINNED_TASK_SCOPE + OWNER_G2_HOLD_LIFT + G1_DESIGN_ONLY',
        'global_brd_techspec_effective': False, 'runtime_enforcement': 'NOT_RUN_G3'}
    (OUT / 'source_readback.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n',
                                             encoding='utf-8', newline='\n')
    print('SOURCE_BYTES_VERIFIED; scoped G2 preexec/route/worktree verified; no global release claim')


if __name__ == '__main__':
    main()
