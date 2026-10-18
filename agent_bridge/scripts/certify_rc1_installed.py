"""Real paused per-user RC1 certification. Never dispatches an Agent or Canary.

Tests the installed binaries and restores a paused installed product. Update and
uninstall preserve durable data, repository worktrees and manually consumed IDs.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from fox2_agent_bridge.artifacts import write_json
from fox2_agent_bridge.installation import BRIDGE_ROOT, install, installed_version
from fox2_agent_bridge.process_lock import ProcessLock


def certify(package, sha, output, manual_artifact_receipt=None, pause_for_manual_artifact=False):
    if manual_artifact_receipt:
        proof = json.loads(manual_artifact_receipt.read_text())
        if (proof.get('status') != 'PASS' or proof.get('package_sha256') != sha or
                proof.get('fresh_installed_ui_save_verified') is not True):
            raise RuntimeError('Fresh UI-save proof for this exact installed package is required; no stale receipt replay')
    root = BRIDGE_ROOT
    class Evidence(dict):
        def __setitem__(self, key, value):
            super().__setitem__(key, value)
            write_json(output, self)
    results = Evidence({'format': 'FOX2_RC1_INSTALLED_CERTIFICATION_1', 'canary_009': 'UNTOUCHED',
               'agent_invocation': 'NONE', 'app_batch_b': 'NO_RESUME', 'status': 'IN_PROGRESS'})
    if not manual_artifact_receipt: write_json(output, results)
    pwsh = r'C:\Program Files\PowerShell\7\pwsh.exe'
    env = {k: v for k, v in os.environ.items() if k.upper() not in {'PYTHONPATH', 'PYTHONHOME'}}
    def cli(*args, parse=True):
        current = installed_version(root)
        python = root / 'versions' / current['package_sha256'] / 'runtime/Scripts/python.exe'
        process = subprocess.run([str(python), '-I', '-m', 'fox2_agent_bridge', *args],
            capture_output=True, text=True, timeout=120, env=env, creationflags=subprocess.CREATE_NO_WINDOW)
        if process.returncode:
            raise RuntimeError('Installed command failed: ' + args[0] + ' exit ' + str(process.returncode))
        return json.loads(process.stdout) if parse else process.stdout
    def wait_for(predicate, label, seconds=45):
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            if predicate(): return
            time.sleep(0.5)
        raise RuntimeError(label)
    def ps(code):
        process = subprocess.run([pwsh, '-NoProfile', '-NonInteractive', '-Command', code],
            capture_output=True, text=True, timeout=30, env=env, creationflags=subprocess.CREATE_NO_WINDOW)
        if process.returncode: raise RuntimeError('Certification PowerShell failed')
        return process.stdout.strip()
    def ui(action, artifact=None):
        process = subprocess.run([pwsh, '-NoProfile', '-NonInteractive', '-File',
            str(Path(__file__).with_name('certify_rc1_ui.ps1')), '-Action', action,
            *(['-Artifact', str(artifact)] if artifact else [])],
            capture_output=True, text=True, timeout=30, env=env, creationflags=subprocess.CREATE_NO_WINDOW)
        if process.returncode: raise RuntimeError('Installed UI certification failed: ' + action)
        return process.stdout.strip()
    def ui_count():
        return int(ps("@(Get-Process -Name 'FOX2.Bridge.Desktop' -ErrorAction SilentlyContinue).Count"))
    def launcher():
        result = subprocess.run([pwsh, '-NoProfile', '-NonInteractive', '-WindowStyle', 'Hidden',
            '-File', str(root / 'launch.ps1')], capture_output=True, timeout=120, env=env,
            creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode: raise RuntimeError('Stable installed launcher failed')
    if manual_artifact_receipt:
        prior = json.loads(output.read_text())
        assert prior['per_user_update']['package_sha256'] == sha
        for gate in ['close_hides_worker_survives', 'ui_crash_worker_survives', 'ui_restart_no_second_worker']:
            assert prior[gate] == 'PASS'
        results.update(prior)
        current = installed_version(root)
        assert current['package_sha256'] == sha
        initial = cli('control', 'status')
        assert initial['paused'] is True and ui_count() == (0 if prior.get('real_installed_poll') else 1)
        startup_before = initial.get('start_with_windows', False)
        config_before = (root / 'config/bridge.toml').read_bytes()
        recovery_ids = ['FOX2-DISPATCH-BRIDGE-RC1-CODEX-' + f'{i:03}' for i in (1, 2, 3)]
        consumption = root / 'data/manual_consumption.json'
        results['resumed_after'] = 'Installed lifecycle PASS; manual GUI artifact receipt bound to same package'
    else:
        current = installed_version(root)
        initial = cli('control', 'status')
        if not initial.get('paused') or initial.get('current_dispatch'):
            raise RuntimeError('Certification requires paused idle installed runtime')
        results['initial_package'] = current['package_sha256']
        startup_before = initial.get('start_with_windows', False)
        config_before = (root / 'config/bridge.toml').read_bytes()
        # Gracefully stop existing legacy supervisor before replacing binaries.
        cli('control', 'request-exit')
        wait_for(lambda: cli('control', 'status').get('state') == 'STOPPED', 'Existing Worker did not stop')
        wait_for(lambda: not (root / 'data/bridge.lock').read_bytes().strip(), 'Existing Worker retained lock')
        consumption = root / 'data/manual_consumption.json'
        existing = json.loads(consumption.read_text()) if consumption.exists() else {'format': 'FOX2_MANUAL_CONSUMPTION_1', 'dispatch_ids': []}
        recovery_ids = ['FOX2-DISPATCH-BRIDGE-RC1-CODEX-' + f'{i:03}' for i in (1, 2, 3)]
        existing['dispatch_ids'] = sorted(set(existing['dispatch_ids']) | set(recovery_ids))
        write_json(consumption, existing)
        results['per_user_update'] = install(package, sha)
        pointer_before = (root / 'current.json').read_bytes()
        try:
            install(package, '0' * 64)
            raise AssertionError('Corrupt update accepted')
        except ValueError:
            assert (root / 'current.json').read_bytes() == pointer_before
            assert cli('control', 'status')['paused'] is True
        results['failed_update_keeps_previous_usable'] = 'PASS_REAL_INTEGRITY_FAILURE_PLUS_STAGED_FAILURE_UNIT_TESTS'
        results['first_run'] = cli('setup')
        assert (root / 'config/bridge.toml').read_bytes() == config_before
        results['configuration_preserved'] = True
        # Controls are verified with the Worker stopped: no dispatch intake window.
        assert cli('control', 'resume')['paused'] is False
        assert cli('control', 'pause')['paused'] is True
        old_generation = cli('control', 'status').get('check_generation', 0)
        assert cli('control', 'check-now')['check_generation'] == old_generation + 1
        results['pause_resume_check_now'] = 'PASS_WITH_WORKER_STOPPED_NO_AGENT_INTAKE'
        results['startup_enable'] = cli('control', 'set-start-with-windows', '--enabled', 'true')
        task = json.loads(ps("$id=[Security.Principal.WindowsIdentity]::GetCurrent(); $t=Get-ScheduledTask -TaskName ('FOX2Bridge-'+$id.User.Value); @{level=[string]$t.Principal.RunLevel;logon=[string]$t.Principal.LogonType;instances=[string]$t.Settings.MultipleInstances;stable=$t.Actions.Arguments.Contains('launch.ps1')}|ConvertTo-Json -Compress"))
        assert task == {'level': 'Limited', 'logon': 'Interactive', 'instances': 'IgnoreNew', 'stable': True}
        results['task_scheduler'] = task
        launcher(); launcher()
        wait_for(lambda: cli('control', 'status').get('state') == 'PAUSED' and ui_count() == 1, 'Worker/UI startup failed')
        state = cli('control', 'status'); generation = state['generation']
        # Windows byte-range locks intentionally prevent reading live lock contents.
        worker_pid = 'LOCK_OWNER_PROVEN_BY_DUPLICATE_WORKER_REJECTION'
        results['ui_screens'] = json.loads(ui('inspect'))
        results['paused_check_now'] = ui('check')
        results['startup_single_instance'] = {'ui_count': ui_count(), 'worker_pid': worker_pid, 'worker_generation': generation, 'two_launches': True}
        # A second Worker cannot own the runtime even when started outside UI.
        python = root / 'versions' / sha / 'runtime/Scripts/python.exe'
        duplicate = subprocess.run([str(python), '-I', '-m', 'fox2_agent_bridge', 'worker'],
            capture_output=True, text=True, timeout=30, env=env, creationflags=subprocess.CREATE_NO_WINDOW)
        assert duplicate.returncode != 0 and 'LOCK_HELD' in duplicate.stderr
        results['worker_single_instance'] = 'LOCK_HELD'
        ui('close')
        assert ui_count() == 1 and cli('control', 'status')['generation'] == generation
        results['close_hides_worker_survives'] = 'PASS'
        launcher()
        wait_for(lambda: ui_count() == 1, 'Hidden singleton failed')
        ui('check')
        # Kill only presentation process to prove independent Worker ownership.
        ps("Get-Process -Name 'FOX2.Bridge.Desktop' | Stop-Process -Force")
        wait_for(lambda: ui_count() == 0, 'UI crash simulation failed')
        assert cli('control', 'status')['generation'] == generation and cli('control', 'status')['state'] == 'PAUSED'
        results['ui_crash_worker_survives'] = 'PASS'
        launcher(); wait_for(lambda: ui_count() == 1, 'UI restart failed'); ui('check')
        assert cli('control', 'status')['generation'] == generation
        results['ui_restart_no_second_worker'] = 'PASS'
        results['open_logs'] = cli('control', 'open-logs')
    if pause_for_manual_artifact:
        results['status'] = 'AWAITING_MANUAL_ARTIFACT'
        print('INSTALLED_LIFECYCLE_PREFIX=PASS; manual artifact confirmation next')
        return
    python = root / 'versions' / sha / 'runtime/Scripts/python.exe'
    if not results.get('real_installed_poll'):
        if manual_artifact_receipt:
            receipt = json.loads(manual_artifact_receipt.read_text())
            artifact = Path(receipt['source_selection'])
        else:
            artifact = output.parent / 'artifact-local-save.txt'
            artifact.write_bytes(b'FOX2 RC1 installed UI artifact certification\n')
        vault_root = Path(os.environ['LOCALAPPDATA']) / 'FOX2/BridgeDesktop/Artifacts'
        artifact_sha = hashlib.sha256(artifact.read_bytes()).hexdigest()
        prior_index = vault_root / 'index.json'
        prior_saved = {r['Sha256']: r['SavedAtUtc'] for r in json.loads(prior_index.read_text())} if prior_index.exists() else {}
        if manual_artifact_receipt:
            assert receipt['status'] == 'PASS' and receipt['package_sha256'] == sha
            assert receipt['source_sha256'] == artifact_sha
        else:
            ui('artifact', artifact)
        def saved_artifact():
            index = vault_root / 'index.json'
            return index.exists() and any(r['Sha256'] == artifact_sha and (manual_artifact_receipt is not None or r['SavedAtUtc'] != prior_saved.get(artifact_sha)) for r in json.loads(index.read_text()))
        wait_for(saved_artifact, 'Installed UI artifact save failed', 15)
        record = next(r for r in json.loads((vault_root / 'index.json').read_text()) if r['Sha256'] == artifact_sha)
        assert record['State'] == 'LOCAL_SAVED'
        assert hashlib.sha256((vault_root / record['VaultPath']).read_bytes()).hexdigest() == artifact_sha
        assert not list(vault_root.glob('.index-*'))
        vault_snapshot = {str(p.relative_to(vault_root)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in vault_root.rglob('*') if p.is_file()}
        if manual_artifact_receipt: assert receipt['record'] == record
        results['installed_artifact_vault'] = {'explicit_file_selection': True, 'record': record,
            'copied_sha256_verified': True, 'atomic_index_valid': True, 'git_synced': False, 'released': False}
        results['support_bundle'] = cli('diagnostics', '--output', str(output.parent / 'installed-support.zip'))
        cli('control', 'request-exit')
        wait_for(lambda: cli('control', 'status')['state'] == 'STOPPED', 'Worker-only graceful stop failed')
        assert ui_count() == 1
        from fox2_agent_bridge.installation import uninstall as source_uninstall
        from fox2_agent_bridge.errors import LockError, LockHeld
        pointer = (root / 'current.json').read_bytes()
        try:
            source_uninstall()
            raise AssertionError('Uninstall accepted a live Desktop')
        except (LockError, LockHeld):
            assert (root / 'current.json').read_bytes() == pointer
            assert (root / 'versions' / sha / 'payload/desktop/FOX2.Bridge.Desktop.exe').is_file()
        results['live_desktop_blocks_uninstall_before_deletion'] = 'PASS_WITH_WORKER_STOPPED'
        ui('exit')
        wait_for(lambda: ui_count() == 0 and cli('control', 'status')['state'] == 'STOPPED', 'Explicit graceful UI exit failed')
        with ProcessLock(root / 'data/bridge.lock'): results['graceful_exit_lock_released'] = True
        import sqlite3
        def execution_counts():
            with sqlite3.connect((root / 'data/bridge.db').as_uri() + '?mode=ro', uri=True) as connection:
                return {table: connection.execute('SELECT count(*) FROM ' + table).fetchone()[0]
                        for table in ('dispatches', 'executions')}
        before_poll = execution_counts()
        # poll-once is a read-only transport observation, never run-next/e2e or claim.
        results['real_installed_poll'] = cli('poll-once')
        assert execution_counts() == before_poll
        results['real_poll_did_not_claim_or_execute'] = before_poll
        assert results['real_installed_poll']['status'] in {'INITIALIZED', 'ADVANCED', 'NO_CHANGE', 'ALREADY_SEEN', 'CANDIDATES_DISCOVERED'}
        control_store = root / 'data/control.git'
        assert control_store.is_dir()
        origin = subprocess.check_output(['git', '--git-dir', str(control_store), 'remote', 'get-url', 'origin'], text=True).strip()
        results['control_store'] = {'path': str(control_store), 'remote': origin, 'installed_python': str(python), 'source_pythonpath': 'UNSET'}
    control_store = root / 'data/control.git'
    origin = subprocess.check_output(['git', '--git-dir', str(control_store), 'remote', 'get-url', 'origin'], text=True).strip()
    results['control_store'] = {'path': str(control_store), 'remote': origin, 'installed_python': str(python), 'source_pythonpath': 'UNSET'}
    vault_root = Path(os.environ['LOCALAPPDATA']) / 'FOX2/BridgeDesktop/Artifacts'
    vault_snapshot = {str(p.relative_to(vault_root)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in vault_root.rglob('*') if p.is_file()}
    # Safe uninstall uses external stable supervisor, not deleting interpreter.
    before_ids = {i: cli('status', '--dispatch-id', i)['dispatch']['dispatch_state'] for i in recovery_ids}
    durable_before = {p: p.read_bytes() for p in [root / 'config/bridge.toml', consumption]}
    uninstall = subprocess.run([pwsh, '-NoProfile', '-NonInteractive', '-File', str(root / 'uninstall.ps1')],
        capture_output=True, text=True, timeout=120, env=env, creationflags=subprocess.CREATE_NO_WINDOW)
    assert uninstall.returncode == 0
    results['uninstall'] = json.loads(uninstall.stdout)
    assert not (root / 'current.json').exists() and not any((root / 'versions').iterdir())
    assert (root / 'data/bridge.db').is_file() and all(p.read_bytes() == raw for p, raw in durable_before.items())
    assert all(hashlib.sha256((vault_root / p).read_bytes()).hexdigest() == digest for p, digest in vault_snapshot.items())
    results['artifact_vault_preserved_by_uninstall'] = True
    results['reinstall'] = install(package, sha)
    results['reinstalled_setup'] = cli('setup')
    after_ids = {i: cli('status', '--dispatch-id', i)['dispatch']['dispatch_state'] for i in recovery_ids}
    assert before_ids == after_ids and all(v == 'NEEDS_RECONCILIATION' for v in after_ids.values())
    results['durable_no_replay'] = after_ids
    results['startup_restored'] = cli('control', 'set-start-with-windows', '--enabled', 'true' if startup_before else 'false')
    assert cli('control', 'status')['paused'] is True
    results['final_package'] = sha; results['status'] = 'PASS'
    write_json(output, results)
    print('INSTALLED_RC1_CERTIFICATION=PASS')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--package', type=Path, required=True)
    parser.add_argument('--sha256', required=True); parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--manual-artifact-receipt', type=Path)
    parser.add_argument('--pause-for-manual-artifact', action='store_true')
    args = parser.parse_args(); certify(args.package, args.sha256, args.output, args.manual_artifact_receipt, args.pause_for_manual_artifact)
