"""Shared acceptance: actual local bare-remote publication and adversarial boundaries."""
from dataclasses import replace
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from jsonschema import ValidationError

from fox2_agent_bridge import project_dictionary as registry
from fox2_agent_bridge.preexec import PreExec, Requirements
from fox2_agent_bridge.preexec.engine import InfrastructureFailure, canonical, git, writer_lock
from fox2_agent_bridge.preexec.probes import observation, proof_marker, agent_probe, classify
from fox2_agent_bridge.preexec.profiles import ROUTES

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def task(tmp_path):
    remote = tmp_path / 'remote.git'
    subprocess.run(['git', 'init', '--bare', str(remote)], check=True, capture_output=True)
    repo = tmp_path / 'task'; repo.mkdir()
    git(repo, 'init', '-b', 'work/FOX2-TEST')
    git(repo, 'config', 'user.email', 'test@example.invalid')
    git(repo, 'config', 'user.name', 'PreExec Test')
    git(repo, 'config', 'core.autocrlf', 'false')
    paths = [registry.SOURCE_PATH, *(registry.CURRENT[k]['path'] for k in
             registry.CURRENT_CONTRACT_SHA256)]
    for relative in paths:
        target = repo / relative; target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(git(ROOT, 'show', registry.SOURCE_COMMIT + ':' + relative))
    task_path = 'docs/agent_handoff/FOX2-TEST/task.md'
    (repo / task_path).parent.mkdir(parents=True)
    (repo / task_path).write_bytes(b'# test immutable task\n')
    git(repo, 'add', '.')
    git(repo, 'commit', '-m', 'source')
    git(repo, 'remote', 'add', 'origin', str(remote))
    git(repo, 'push', 'origin', 'HEAD:refs/heads/work/FOX2-TEST')
    config = Requirements('FOX2-TEST', 'work/FOX2-TEST', repo,
                          git(repo, 'rev-parse', 'HEAD').decode().strip(), task_path,
                          'reports/FOX2-TEST/preexec/receipt.json', ROUTES)
    return config, remote


def engine(config, statuses=None, checks=None):
    statuses = statuses or {'CODEX': 'PASS', 'COPILOT': 'FAIL'}
    return PreExec(config, checks=checks, writer_observer=lambda _: False,
                   probe=lambda route, _: observation(statuses[route['product']],
                       failure='AUTH_REQUIRED' if statuses[route['product']] != 'PASS' else None))


@pytest.mark.parametrize('state,exit_code', [('PASS', 0), ('BLOCKED', 20), ('INFRA_FAILED', 30)])
def test_preflight_durable_statuses(task, state, exit_code):
    config, remote = task
    def check(_):
        if state == 'INFRA_FAILED':
            raise RuntimeError('authorization=secret')
        return observation('PASS' if state == 'PASS' else 'MISSING', failure=None if state == 'PASS' else 'TOOL_MISSING')
    result = engine(config, checks={'material_tool': check}).run()
    assert result.exit_code == exit_code and result.receipt['status'] == state
    assert result.remote_sha == git(config.worktree, 'rev-parse', 'HEAD').decode().strip()
    content = subprocess.check_output(['git', '--git-dir', str(remote), 'show',
                     result.remote_sha + ':' + config.receipt_path])
    assert content == canonical(result.receipt)
    assert b'\r' not in content and not content.startswith(b'\xef\xbb\xbf') and content.endswith(b'\n')
    assert b'authorization=secret' not in content
    assert result.receipt['dispatch_state'] == {'executable_dispatch_published': False, 'dispatch_consumed': False}
    assert result.receipt['agent_execution_started'] is False
    assert git(config.worktree, 'diff', config.source_head, '--name-only').decode().strip() == config.receipt_path


def test_alternative_agent_route_materiality(task):
    config, _ = task
    result = engine(config).run(publish=False)
    assert result.exit_code == 0
    assert not result.receipt['capabilities']['copilot']['material']
    assert not result.receipt['capabilities']['codex']['material']
    assert result.receipt['capabilities']['eligible_agent_route']['material']
    assert result.receipt['candidate_route'] == ROUTES[1]
    both = engine(config, {'CODEX': 'PASS', 'COPILOT': 'PASS'}).run(publish=False)
    assert both.receipt['candidate_route'] is None


def test_pinned_agent_materiality(task):
    config, _ = task
    result = engine(replace(config, pinned_agent='COPILOT')).run(publish=False)
    assert result.exit_code == 20
    assert result.receipt['capabilities']['copilot']['material']
    assert result.receipt['capabilities']['eligible_agent_route']['status'] == 'FAIL'
    assert result.receipt['candidate_route'] is None


def test_schema_rejects_nested_unknown_status_and_fields(task):
    config, _ = task
    runner = engine(config); result = runner.run(publish=False)
    receipt = result.receipt
    receipt['capabilities']['codex']['status'] = 'INVENTED'
    with pytest.raises(ValidationError): runner.validate_receipt(receipt)
    receipt['capabilities']['codex']['status'] = 'PASS'
    receipt['capabilities']['codex']['raw_output'] = 'secret'
    with pytest.raises(ValidationError): runner.validate_receipt(receipt)


@pytest.mark.parametrize('case', ['branch', 'head', 'writer', 'wip', 'dictionary'])
def test_unsafe_worktree_never_probes_or_publishes(task, case):
    config, _ = task
    if case == 'branch': config = replace(config, branch='work/FOX2-OTHER')
    elif case == 'head': config = replace(config, source_head='0'*40)
    elif case == 'wip': (config.worktree / 'unrelated.txt').write_text('WIP')
    elif case == 'dictionary':
        path = config.worktree / registry.SOURCE_PATH
        path.write_text('{}')
        git(config.worktree, 'add', '.'); git(config.worktree, 'commit', '-m', 'drift')
        config = replace(config, source_head=git(config.worktree, 'rev-parse', 'HEAD').decode().strip())
    runner = PreExec(config, probe=lambda *_: pytest.fail('unsafe state probed'),
                     writer_observer=lambda _: case == 'writer')
    result = runner.run()
    assert result.exit_code >= 30 and result.remote_sha is None


def test_stale_receipt_only_cleanup(task):
    config, _ = task
    receipt = engine(config).run(publish=False).receipt
    path = config.worktree / config.receipt_path
    path.parent.mkdir(parents=True); path.write_bytes(canonical(receipt))
    git(config.worktree, 'add', '--', config.receipt_path)
    assert engine(config).run().failure == 'RECEIPT_WIP'
    result = engine(config).run(cleanup=True)
    assert result.exit_code == 0 and result.receipt['worktree']['stale_receipt_cleanup'] == 'SAFE_ONLY'


@pytest.mark.parametrize('mode', ['foreign', 'raw', 'unrelated'])
def test_cleanup_requires_objective_proof(task, mode):
    config, _ = task
    receipt = engine(config).run(publish=False).receipt
    path = config.worktree / config.receipt_path
    path.parent.mkdir(parents=True)
    if mode == 'foreign': receipt['wp_id'] = 'FOX2-FOREIGN'
    path.write_bytes(b'raw user WIP' if mode == 'raw' else canonical(receipt))
    if mode == 'unrelated': (config.worktree / 'unrelated.txt').write_bytes(b'WIP')
    before = path.read_bytes()
    result = engine(config).run(cleanup=True)
    assert result.exit_code >= 30 and path.read_bytes() == before


def test_concurrent_writer_lock(task):
    config, _ = task
    with writer_lock(config.worktree):
        assert engine(config).run().failure == 'COMPETING_WRITER'
    assert engine(config).run(publish=False).exit_code == 0


@pytest.mark.parametrize('termination', ['normal', 'exception', 'killed'])
def test_cross_process_lock_exclusivity_and_release(task, termination):
    config, _ = task
    code = '''
import sys
from pathlib import Path
from fox2_agent_bridge.preexec.engine import writer_lock
try:
    with writer_lock(Path(sys.argv[1])):
        print('LOCKED', flush=True)
        sys.stdin.readline()
        if sys.argv[2] == 'exception': raise RuntimeError('test failure')
except RuntimeError:
    pass
'''
    child = subprocess.Popen([sys.executable, '-u', '-c', code, str(config.worktree), termination],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             text=True, env={**os.environ, 'PYTHONPATH': str(ROOT / 'agent_bridge/src')})
    try:
        assert child.stdout.readline().strip() == 'LOCKED'
        before = git(config.worktree, 'rev-parse', 'HEAD')
        calls = []
        runner = engine(config)
        runner.probe = lambda *_: calls.append('UNSAFE_PROBE')
        assert runner.run().failure == 'COMPETING_WRITER'
        assert not calls and git(config.worktree, 'rev-parse', 'HEAD') == before
        assert not (config.worktree / config.receipt_path).exists()
        if termination == 'killed': child.kill()
        else: child.stdin.write('\n'); child.stdin.flush()
        child.wait(timeout=10)
        assert engine(config).run(publish=False).exit_code == 0
    finally:
        if child.poll() is None: child.kill(); child.wait(timeout=10)
        for stream in (child.stdin, child.stdout, child.stderr): stream.close()


def test_lock_release_after_body_failure(task):
    config, _ = task
    with pytest.raises(RuntimeError):
        with writer_lock(config.worktree): raise RuntimeError('test failure')
    with writer_lock(config.worktree): pass


@pytest.mark.skipif(os.name != 'nt', reason='Windows byte-range lock failures')
@pytest.mark.parametrize('operation', ['acquire', 'release'])
def test_lock_os_failure_is_safe_and_handle_closes(task, monkeypatch, operation):
    import errno
    import msvcrt
    config, _ = task
    original = msvcrt.locking
    def failing(fd, mode, size):
        if mode == (msvcrt.LK_NBLCK if operation == 'acquire' else msvcrt.LK_UNLCK):
            raise OSError(errno.EIO, 'fixed test failure')
        return original(fd, mode, size)
    monkeypatch.setattr(msvcrt, 'locking', failing)
    result = engine(config).run(publish=False)
    assert result.exit_code >= 30 and result.remote_sha is None
    assert result.failure == ('WRITER_LOCK_FAILED' if operation == 'acquire' else 'WRITER_RELEASE_FAILED')
    monkeypatch.setattr(msvcrt, 'locking', original)
    assert engine(config).run(publish=False).exit_code == 0


@pytest.mark.parametrize('key', ['policy', 'preflight_receipt_schema', 'preexec_evidence_protocol'])
def test_canonical_contract_source_drift_cannot_weaken_validation(task, key):
    config, _ = task
    path = config.worktree / registry.CURRENT[key]['path']
    path.write_bytes(b'{}\n')
    git(config.worktree, 'add', '--', registry.CURRENT[key]['path'])
    git(config.worktree, 'commit', '-m', 'adversarial contract drift')
    config = replace(config, source_head=git(config.worktree, 'rev-parse', 'HEAD').decode().strip())
    runner = engine(config); runner.probe = lambda *_: pytest.fail('drift must fail before probes')
    assert runner.run().failure == 'CONTRACT_SOURCE_DRIFT'


def test_missing_source_contract_emits_safe_schema_receipt_without_probe(task):
    config, _ = task
    git(config.worktree, 'rm', '--', registry.SOURCE_PATH)
    git(config.worktree, 'commit', '-m', 'missing source contract')
    config = replace(config, source_head=git(config.worktree, 'rev-parse', 'HEAD').decode().strip())
    runner = engine(config); runner.probe = lambda *_: pytest.fail('unsafe source must not probe')
    result = runner.run()
    assert result.failure == 'SOURCE_CONTRACT_UNAVAILABLE'
    assert result.receipt['status'] == 'INFRA_FAILED' and result.remote_sha is None
    runner.validate_receipt(result.receipt)
    assert not (config.worktree / config.receipt_path).exists()


def test_cli_failure_snapshot_has_no_pushed_marker(task):
    config, _ = task
    snapshot = config.worktree.parent / 'snapshot'
    process = subprocess.run([sys.executable, str(ROOT / 'agent_bridge/scripts/preexec.py'),
        '--profile', 'app', '--worktree', str(config.worktree), '--source-head', config.source_head,
        '--snapshot-root', str(snapshot), '--snapshot-path', config.receipt_path], capture_output=True)
    assert process.returncode >= 30
    assert b'RECEIPT_PUSHED=' not in process.stdout
    raw = (snapshot / config.receipt_path).read_bytes()
    receipt = json.loads(raw)
    assert receipt['status'] == 'INFRA_FAILED' and raw == canonical(receipt)
    assert receipt['worktree']['status'] == 'INFRA_FAILED'


@pytest.mark.parametrize('status', ['PASS', 'BLOCKED'])
def test_cli_snapshot_cannot_return_durable_publication_exit_code(task, monkeypatch, capsys, status):
    import importlib.util
    config, _ = task
    spec = importlib.util.spec_from_file_location('preexec_cli', ROOT / 'agent_bridge/scripts/preexec.py')
    cli = importlib.util.module_from_spec(spec); spec.loader.exec_module(cli)
    monkeypatch.setattr(cli, 'identity', lambda _: (config.wp_id, config.branch, config.task_path, config.receipt_path))
    monkeypatch.setattr(cli, 'PreExec', lambda requirements, **_: engine(requirements,
        checks={'material_tool': lambda _: observation('PASS' if status == 'PASS' else 'MISSING')}))
    output = config.worktree.parent / 'diagnostic'
    before = git(config.worktree, 'rev-parse', 'HEAD')
    assert cli.main(['--profile', 'rollout', '--worktree', str(config.worktree),
        '--source-head', config.source_head, '--snapshot-root', str(output),
        '--snapshot-path', config.receipt_path]) == 33
    text = capsys.readouterr().out
    assert 'RECEIPT_PUSHED=' not in text and 'PREFLIGHT_PUBLICATION=NOT_ATTEMPTED' in text
    assert json.loads((output / config.receipt_path).read_bytes())['status'] == status
    assert git(config.worktree, 'rev-parse', 'HEAD') == before


@pytest.mark.parametrize('event,failure', [
    ({'model': 'different-model'}, 'AGENT_CONFIGURATION_MISMATCH'),
    ({'reasoning_effort': 'high'}, 'AGENT_CONFIGURATION_MISMATCH'),
    ({'permission_profile': 'BOUNDED_EXPLICIT'}, 'AGENT_CONFIGURATION_MISMATCH'),
    ({'error': {'code': 'quota_exceeded'}}, 'CAPACITY_OR_QUOTA'),
    ({'error': {'code': 'authentication_error'}}, 'AUTH_REQUIRED'),
    ({'type': 'error'}, 'CLI_NONZERO'),
])
def test_success_marker_cannot_override_structured_probe_failure(tmp_path, monkeypatch, event, failure):
    import fox2_agent_bridge.preexec.probes as probes
    from types import SimpleNamespace
    monkeypatch.setattr(probes, 'resolve_tool', lambda _: 'codex')
    output = json.dumps(event) + '\n' + json.dumps({'type': 'item.completed',
              'item': {'type': 'agent_message', 'text': 'FOX2_PREFLIGHT_OK'}})
    monkeypatch.setattr(probes, 'run_tool', lambda *_a, **_k: SimpleNamespace(returncode=0, stdout=output, stderr=''))
    result = agent_probe(dict(ROUTES[1]), tmp_path)
    assert result['status'] == 'FAIL' and result['failure_class'] == failure


@pytest.mark.parametrize('payload', ['null', '[]', '42', '"FOX2_PREFLIGHT_OK"'])
def test_non_object_probe_events_do_not_prove_readiness(payload):
    assert not proof_marker('CODEX', payload)


@pytest.mark.parametrize('relative', ['../escape.json', 'reports/../escape.json', 'C:/escape.json', 'reports\\escape.json'])
def test_receipt_path_cannot_escape_worktree(task, relative):
    config, _ = task
    runner = engine(replace(config, receipt_path=relative))
    runner.probe = lambda *_: pytest.fail('unsafe path must never probe')
    assert runner.run().exit_code >= 30


def test_staged_unrelated_file_is_preserved_and_never_published(task):
    config, _ = task
    path = config.worktree / 'unrelated.txt'; path.write_bytes(b'preserve staged WIP\n')
    git(config.worktree, 'add', '--', 'unrelated.txt')
    assert engine(config).run().failure == 'UNRELATED_WIP'
    assert path.read_bytes() == b'preserve staged WIP\n'
    assert git(config.worktree, 'diff', '--cached', '--name-only').strip() == b'unrelated.txt'


@pytest.mark.parametrize('mutation', ['receipt', 'unrelated'])
def test_commit_hook_mutation_never_reaches_push(task, monkeypatch, mutation):
    config, _ = task
    import fox2_agent_bridge.preexec.engine as module
    original = module.git
    def altered(root, *args):
        if args[0] == 'push': pytest.fail('out-of-scope or altered receipt must never push')
        if args[0] == 'commit':
            path = config.receipt_path if mutation == 'receipt' else 'unrelated.txt'
            (root / path).write_bytes(b'changed by hook\n')
            original(root, 'add', '--', path)
        return original(root, *args)
    monkeypatch.setattr(module, 'git', altered)
    result = engine(config).run()
    assert result.remote_sha is None and result.exit_code >= 30
    assert result.failure == ('COMMITTED_RECEIPT_MISMATCH' if mutation == 'receipt' else 'COMMITTED_ALLOWLIST_FAILED')


@pytest.mark.parametrize('operation', ['commit', 'push', 'ls-remote', 'fetch'])
def test_no_false_pushed_marker_on_publication_failure(task, monkeypatch, operation):
    config, _ = task
    import fox2_agent_bridge.preexec.engine as module
    original = module.git; count = 0
    def failing(root, *args):
        nonlocal count
        if args[0] == operation:
            count += 1
            if operation != 'ls-remote' or count == 2:
                raise InfrastructureFailure('GIT_OPERATION_FAILED')
        return original(root, *args)
    monkeypatch.setattr(module, 'git', failing)
    result = engine(config).run()
    assert result.exit_code >= 30 and result.remote_sha is None
    assert result.receipt['status'] == 'PASS'


def test_remote_readback_mismatch(task, monkeypatch):
    config, _ = task
    import fox2_agent_bridge.preexec.engine as module
    original = module.git; count = 0
    def mismatch(root, *args):
        nonlocal count
        if args[0] == 'ls-remote':
            count += 1
            if count == 2: return b'0'*40 + b'\trefs/heads/work/FOX2-TEST\n'
        return original(root, *args)
    monkeypatch.setattr(module, 'git', mismatch)
    assert engine(config).run().failure == 'REMOTE_READBACK_FAILED'


def test_probe_product_mutation_prevents_publication(task):
    config, _ = task
    runner = engine(config)
    def mutation(route, root):
        (root / 'bad-edit.txt').write_bytes(b'bad')
        return observation()
    runner.probe = mutation
    assert runner.run().failure == 'UNRELATED_WIP'


def test_unknown_material_remains_hold_and_preserves_first_blocker(task):
    config, _ = task
    runner = engine(config, checks={'first': lambda _: observation('MISSING', failure='TOOL_MISSING'),
                                  'unknown': lambda _: observation('UNKNOWN', failure='UNPROVEN')})
    result = runner.run(publish=False)
    assert result.exit_code == 20 and result.receipt['blockers'][0]['code'] == 'CHECK_FIRST'
    assert any('HOLD_UNKNOWN' in note for note in result.receipt['notes'])


@pytest.mark.parametrize('product', ['CODEX', 'COPILOT'])
def test_echoed_prompt_does_not_prove_agent_readiness(product):
    assert not proof_marker(product, json.dumps({'type': 'prompt', 'text': 'FOX2_PREFLIGHT_OK'}))
    assert not proof_marker(product, 'FOX2_PREFLIGHT_OK')
    event = {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'FOX2_PREFLIGHT_OK'}} if product == 'CODEX' else {'type': 'assistant.message', 'data': {'content': 'FOX2_PREFLIGHT_OK'}}
    assert proof_marker(product, json.dumps(event))


def test_no_agent_substitution_exact_probe_arguments(tmp_path, monkeypatch):
    import fox2_agent_bridge.preexec.probes as probes
    from types import SimpleNamespace
    recorded = []
    monkeypatch.setattr(probes, 'resolve_tool', lambda _: 'codex')
    def run(args, **kwargs):
        recorded.append((args, kwargs))
        return SimpleNamespace(returncode=1, stdout='secret token quota exhausted', stderr='')
    monkeypatch.setattr(probes, 'run_tool', run)
    route = dict(ROUTES[1])
    value = agent_probe(route, tmp_path)
    assert len(recorded) == 1 and route == ROUTES[1]
    args = recorded[0][0]
    assert args[args.index('--model') + 1] == route['model']
    assert 'model_reasoning_effort="medium"' in args
    assert args[args.index('--sandbox') + 1] == 'danger-full-access'
    assert args[args.index('--ask-for-approval') + 1] == 'never'
    assert value['failure_class'] == 'CAPACITY_OR_QUOTA' and 'secret' not in json.dumps(value)


def test_sanitized_failure_classification():
    assert classify('https://name:password@host unauthorized token', 1, False) == 'AUTH_REQUIRED'
    assert classify('invalid model private output', 1, False) == 'MODEL_OR_CONFIG_UNSUPPORTED'
    assert classify('random private output', 1, False) == 'CLI_NONZERO'


@pytest.mark.parametrize('wp,profile', [('FOX2-M1-A-APP-BATCH-B', 'app'), ('FOX2-BRIDGE-DESKTOP-BATCH-B', 'bridge'), ('FOX2-PREEXEC-ROLLOUT-V1', 'rollout')])
def test_thin_adapters(wp, profile):
    name = 'recover_and_preflight.ps1' if profile == 'rollout' else 'preflight.ps1'
    text = (ROOT / 'docs/agent_handoff' / wp / name).read_text()
    assert len(text.splitlines()) < 30 and 'agent_bridge/scripts/preexec.py' in text
    assert f'"{profile}"' in text
    assert 'git ' not in text and 'Probe-' not in text and 'ConvertTo-Json' not in text
