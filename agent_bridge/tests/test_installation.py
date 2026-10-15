"""Installer integrity, transactional failure and durable no-replay regression."""
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import zipfile

import pytest

from fox2_agent_bridge import installation as module
from fox2_agent_bridge.desktop import initialize_runtime
from fox2_agent_bridge.ledger import SQLiteLedger, utc_now
from fox2_agent_bridge.process_lock import ProcessLock


def package(tmp_path, names=None, **changes):
    files = names or {'wheels/fox2_agent_bridge-0.1.0-py3-none-any.whl': b'fixture'}
    manifest = {'format':'FOX2_USER_PACKAGE_1', 'python':f'{module.sys.version_info.major}.{module.sys.version_info.minor}',
                'platform':module.sys.platform, 'dictionary_sha256':module.registry.SOURCE_SHA256,
                'source_sha256':'a'*64,
                'files':{n:hashlib.sha256(b).hexdigest() for n,b in files.items()}, **changes}
    path = tmp_path/'fixture.zip'
    with zipfile.ZipFile(path,'w') as archive:
        for name,raw in files.items(): archive.writestr(name,raw)
        archive.writestr('manifest.json',json.dumps(manifest))
    return path,hashlib.sha256(path.read_bytes()).hexdigest()


def test_bad_integrity_never_creates_installation(tmp_path,monkeypatch):
    root=tmp_path/'owned'; monkeypatch.setattr(module,'BRIDGE_ROOT',root)
    path,sha=package(tmp_path)
    with pytest.raises(ValueError,match='integrity'):
        module.install(path,'0'*64,root=root)
    assert not root.exists()
    with pytest.raises(ValueError,match='current-user'):
        module.install(path,sha,root=tmp_path/'outside')


@pytest.mark.parametrize('member',['../escape.whl','/absolute.whl','wheels/../escape.whl',
                                    'wheels\\escape.whl','wheels/C:escape.whl','unexpected.exe'])
def test_archive_path_attacks_rejected(tmp_path,member):
    path,sha=package(tmp_path,{member:b'fixture'})
    with pytest.raises(ValueError): module.verified_package(path,sha)


def test_manifest_dictionary_platform_and_member_drift_rejected(tmp_path):
    for change in ({'dictionary_sha256':'0'*64},{'platform':'other'},
                   {'python':'0.0'},{'files':{}},{'format':'other'}):
        path,sha=package(tmp_path,**change)
        with pytest.raises(ValueError,match='manifest'): module.verified_package(path,sha)


def test_failed_upgrade_retains_pointer_and_durable_files(tmp_path,monkeypatch):
    root=tmp_path/'owned'; monkeypatch.setattr(module,'BRIDGE_ROOT',root)
    root.mkdir(); (root/'data').mkdir(); (root/'config').mkdir()
    (root/'data/bridge.db').write_bytes(b'durable-ledger')
    (root/'config/bridge.toml').write_bytes(b'durable-config')
    original={'package_sha256':'b'*64,'source_sha256':'c'*64}
    (root/'current.json').write_text(json.dumps(original))
    def fail(*a,**k): raise ValueError('injected installation failure')
    monkeypatch.setattr(module,'_run',fail)
    path,sha=package(tmp_path)
    with pytest.raises(ValueError,match='injected'): module.install(path,sha,root=root)
    assert module.installed_version(root)==original
    assert not (root/'versions'/sha).exists()
    assert (root/'data/bridge.db').read_bytes()==b'durable-ledger'
    assert (root/'config/bridge.toml').read_bytes()==b'durable-config'


def test_running_worker_prevents_install_mutation(tmp_path,monkeypatch):
    root=tmp_path/'owned'; monkeypatch.setattr(module,'BRIDGE_ROOT',root)
    path,sha=package(tmp_path)
    from fox2_agent_bridge.errors import LockHeld
    with ProcessLock(root/'data/bridge.lock'):
        with pytest.raises(LockHeld): module.install(path,sha,root=root)
    assert not (root/'current.json').exists()
    assert not (root/'versions').exists()


def test_manual_consumption_blocks_prior_zero_ledger_rows_after_restart(bridge_config):
    root=bridge_config.bridge_root; (root/'data').mkdir(parents=True)
    ids=['FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-'+i for i in ('001','002','003')]
    (root/'data/manual_consumption.json').write_text(json.dumps({
        'format':'FOX2_MANUAL_CONSUMPTION_1','dispatch_ids':ids}))
    for _ in range(2):
        ledger=initialize_runtime(bridge_config)
        for identity in ids:
            assert not ledger.claim_dispatch(dispatch_id=identity,payload_hash='a'*64,
                execution_id='must-not-execute',observed_at_utc=utc_now())
    assert ledger.pending_executions()==()


def test_diagnostics_never_exports_raw_secrets_or_conversation(tmp_path,monkeypatch):
    root=tmp_path/'owned'; monkeypatch.setattr(module,'BRIDGE_ROOT',root)
    ledger=SQLiteLedger(root/'data/bridge.db'); ledger.initialize()
    ledger.update_worker(state='IDLE',paused=True,last_error='private password',
                         tools={'credential':'private password'},conversation='private conversation')
    (root/'config').mkdir(); (root/'config/bridge.toml').write_text('private password')
    result=module.diagnostics(tmp_path/'support.zip',root=root)
    with zipfile.ZipFile(tmp_path/'support.zip') as archive:
        assert archive.namelist()==['support.json']
        raw=archive.read('support.json')
    assert b'private' not in raw and b'conversation' not in raw and b'credential' not in raw
    assert result['sha256']==hashlib.sha256((tmp_path/'support.zip').read_bytes()).hexdigest()


def test_uninstall_refuses_unowned_directory_before_deletion(tmp_path,monkeypatch):
    root=tmp_path/'owned'; monkeypatch.setattr(module,'BRIDGE_ROOT',root)
    target=root/'versions'/('a'*64); target.mkdir(parents=True)
    (target/'unowned').write_text('keep')
    with pytest.raises(ValueError,match='unowned'): module.uninstall(root=root)
    assert (target/'unowned').read_text()=='keep'


def test_uninstall_preserves_claims_and_project_tree(tmp_path,monkeypatch):
    root=tmp_path/'owned'; monkeypatch.setattr(module,'BRIDGE_ROOT',root)
    project=tmp_path/'repository'; project.mkdir(); (project/'keep').write_bytes(b'untouched')
    ledger=SQLiteLedger(root/'data/bridge.db'); ledger.initialize()
    ledger.claim_dispatch(dispatch_id='FOX2-CONSUMED',payload_hash='a'*64,execution_id='one',observed_at_utc=utc_now())
    target=root/'versions'/('a'*64); target.mkdir(parents=True)
    (target/'receipt.json').write_text('{}')
    result=module.uninstall(root=root)
    assert result['status']=='UNINSTALLED' and not target.exists()
    assert (project/'keep').read_bytes()==b'untouched'
    assert not ledger.claim_dispatch(dispatch_id='FOX2-CONSUMED',payload_hash='a'*64,execution_id='two',observed_at_utc=utc_now())


@pytest.mark.parametrize('name', ['PYTHONPATH', 'PYTHONHOME', 'PythonPath', 'PythonHome'])
def test_installation_subprocess_strips_python_paths_preserves_os_environment(monkeypatch, name):
    monkeypatch.setenv(name, 'contaminated-python-location')
    monkeypatch.setenv('FOX2_INSTALL_SENTINEL', 'ordinary-environment-preserved')
    before = dict(os.environ)
    # Run a real child without -I: the helper itself must remove contamination.
    result = module._run([module.sys.executable, '-c',
                          'import os,json; print(json.dumps(dict(os.environ)))'])
    child = json.loads(result.stdout)
    assert not {'PYTHONPATH', 'PYTHONHOME'} & {key.upper() for key in child}
    assert child['FOX2_INSTALL_SENTINEL'] == 'ordinary-environment-preserved'
    for key in ('PATH', 'SystemRoot', 'TEMP', 'USERPROFILE'):
        if key in before:
            assert child[key] == before[key]
    assert dict(os.environ) == before


@pytest.mark.parametrize('failure_stage', [None, 0, 1, 2])
def test_install_sequence_is_hermetic_and_failure_is_sanitized(tmp_path, monkeypatch, failure_stage):
    root = tmp_path / 'owned'
    monkeypatch.setattr(module, 'BRIDGE_ROOT', root)
    monkeypatch.setenv('PYTHONPATH', 'contaminated-source')
    monkeypatch.setenv('PYTHONHOME', 'contaminated-home')
    monkeypatch.setenv('FOX2_INSTALL_SENTINEL', 'preserved')
    package_path, sha = package(tmp_path)
    calls = []

    def child(arguments, **kwargs):
        assert not (root / 'current.json').exists()
        assert not (root / 'versions' / sha / 'receipt.json').exists()
        assert not {'PYTHONPATH', 'PYTHONHOME'} & {key.upper() for key in kwargs['env']}
        assert kwargs['env']['FOX2_INSTALL_SENTINEL'] == 'preserved'
        assert kwargs['capture_output'] and kwargs['text'] and kwargs['timeout'] == 180
        stage = len(calls)
        calls.append(arguments)
        return subprocess.CompletedProcess(arguments, 17 if stage == failure_stage else 0,
            'private subprocess output' if stage == failure_stage else module.registry.SOURCE_SHA256 + '\n',
            'private subprocess error')

    monkeypatch.setattr(module.subprocess, 'run', child)
    if failure_stage is None:
        assert module.install(package_path, sha, root=root)['status'] == 'INSTALLED'
        assert (root / 'versions' / sha / 'receipt.json').is_file()
    else:
        with pytest.raises(ValueError) as error:
            module.install(package_path, sha, root=root)
        assert str(error.value) == 'installation subprocess failed: 17'
        assert not (root / 'current.json').exists()
        assert not (root / 'versions' / sha).exists()
    assert calls[0] == [module.sys.executable, '-m', 'venv', str(root / 'versions' / sha / 'runtime')]
    if len(calls) > 1:
        assert calls[1][1:6] == ['-m', 'pip', '--isolated', 'install', '--disable-pip-version-check']
        assert calls[1][6:9] == ['--no-index', '--only-binary=:all:', '--find-links']
        assert calls[1][-1].endswith('fox2_agent_bridge-0.1.0-py3-none-any.whl')
    if len(calls) > 2:
        assert calls[2][0] == calls[1][0]
        assert calls[2][1:3] == ['-I', '-c']
        assert 'import fox2_agent_bridge.project_dictionary' in calls[2][3]
        assert 'import fox2_agent_bridge.dispatch_schema_v3_contract' in calls[2][3]
        assert 'import jsonschema' in calls[2][3]
    assert len(calls) == (3 if failure_stage is None else failure_stage + 1)
