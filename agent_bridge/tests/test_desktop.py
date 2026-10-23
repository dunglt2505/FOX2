"""Deterministic Desktop evidence; no paid Agent or real startup changes."""
from pathlib import Path
from types import SimpleNamespace
import json
import subprocess
import sys

import pytest

from fox2_agent_bridge.agent_policy import policy_arguments, validate_selection, observe_metadata
from fox2_agent_bridge.desktop import DesktopWorker, reconcile, control, STATES, BACKOFF
from fox2_agent_bridge.e2e_runner import BridgeE2ERunner
from fox2_agent_bridge.errors import DispatchInvalid, ToolExecFailed, LockHeld, WorkspaceBlocked
from fox2_agent_bridge.ledger import SQLiteLedger, MIGRATIONS, SCHEMA_VERSION, utc_now
from fox2_agent_bridge.ops_runner import BridgeOps, OpsRunResult
from fox2_agent_bridge.process_lock import ProcessLock
from fox2_agent_bridge.startup import startup_command, set_start_with_windows


def worker(config):
    clock = [0.0]
    calls = []
    def next_task():
        calls.append(1)
        return OpsRunResult('NO_ELIGIBLE_DISPATCH', 'NO_CHANGE', None, None, None)
    item = DesktopWorker(config, ops=SimpleNamespace(run_next=next_task), monotonic=lambda: clock[0])
    item.ledger.initialize()
    return item, clock, calls


def test_idle_pause_resume_check_now_durable(bridge_config):
    item, clock, calls = worker(bridge_config)
    assert item.tick() and len(calls) == 1
    assert item.tick() and len(calls) == 1
    item.ledger.control('pause')
    clock[0] = 100
    assert item.tick() and len(calls) == 1
    assert item.ledger.worker_state()['state'] == 'PAUSED'
    item.ledger.control('check-now')
    assert item.tick() and len(calls) == 1
    item.ledger.control('resume')
    assert item.tick() and len(calls) == 2
    item.ledger.control('check-now')
    assert item.tick() and len(calls) == 3
    other = SQLiteLedger(bridge_config.database_path)
    assert other.worker_state()['check_consumed'] == 2
    other.control('request-exit')
    assert not item.tick()


def test_backoff_bounded_and_resets(bridge_config):
    item, clock, _ = worker(bridge_config)
    def offline():
        raise ConnectionError('offline')
    item.ops.run_next = offline
    for expected in (*BACKOFF, 300, 300):
        item.tick()
        assert item.ledger.worker_state()['backoff_seconds'] == expected
        assert item.ledger.worker_state()['state'] == 'DEGRADED'
        clock[0] = item.due
    item.ops.run_next = lambda: OpsRunResult('NO_ELIGIBLE_DISPATCH', 'NO_CHANGE', None, None, None)
    item.tick()
    assert item.failures == 0
    assert item.ledger.worker_state()['backoff_seconds'] == 30
    clock[0] = item.due
    item.ops.run_next = offline
    item.tick()
    assert item.ledger.worker_state()['backoff_seconds'] == 30


def test_controls_work_while_singleton_owned(bridge_config):
    item, _, _ = worker(bridge_config)
    with item.lock:
        second = DesktopWorker(bridge_config)
        with pytest.raises(LockHeld):
            second.lock.acquire()
        for command in ('pause', 'resume', 'check-now', 'status', 'request-exit'):
            assert isinstance(control(bridge_config, command), dict)
        with pytest.raises(ValueError):
            control(bridge_config, 'shell arbitrary payload')


def test_control_cli_does_not_take_worker_lock(bridge_config, monkeypatch, capsys):
    from fox2_agent_bridge.__main__ import main
    monkeypatch.setattr('fox2_agent_bridge.config.load_config', lambda _: bridge_config)
    item, _, _ = worker(bridge_config)
    with item.lock:
        assert main(['control', 'pause']) == 0
        assert json.loads(capsys.readouterr().out)['paused'] is True
        assert main(['status']) == 0
        assert json.loads(capsys.readouterr().out)['worker']['paused'] is True


@pytest.mark.parametrize('stage,remote,outcome', [
    ('CLAIMED', False, 'SAFE_NOT_STARTED'),
    ('UNKNOWN', False, 'NEEDS_RECONCILIATION'),
    ('RUNNING', False, 'NEEDS_RECONCILIATION'),
    ('AGENT_EXITED', False, 'NEEDS_RECONCILIATION'),
    ('PUBLISHING', False, 'NEEDS_RECONCILIATION'),
    ('AGENT_EXITED', True, 'PUSHED_UNREVIEWED'),
    ('PUBLISHING', True, 'PUSHED_UNREVIEWED'),
])
def test_restart_stages_never_replay(bridge_config, stage, remote, outcome):
    ledger = SQLiteLedger(bridge_config.database_path)
    ledger.initialize()
    ledger.claim_dispatch(dispatch_id='exact', payload_hash='a'*64, execution_id='e', observed_at_utc=utc_now())
    # This legacy positive fixture models an AGENT-owned already-pushed result.
    # BRIDGE-owned recovery instead requires an immutable PUBLISHING commit SHA.
    payload = {'worktree': str(bridge_config.worktree_root/'exact'), '_agent_product': 'CODEX',
               'agent': {'product': 'CODEX'}, 'branch': 'work/exact',
               'delivery_owner': 'AGENT'}
    if stage != 'UNKNOWN':
        ledger.checkpoint('e', stage, {'payload': payload, 'before_head': 'a'*40, 'agent_stdout': 'marker', 'agent_exit_code': 0})
    calls = []
    def verify(**kwargs):
        calls.append(kwargs)
        assert kwargs['payload']['branch'] == 'work/exact'
        if not remote:
            raise WorkspaceBlocked('uncertain/offline')
        return 'b'*40, ('reports/exact/result.md',)
    result = reconcile(ledger, SimpleNamespace(_verify_result=verify))
    assert result[0]['outcome'] == outcome
    assert ledger.dispatch_status('exact')['dispatch_state'] == outcome
    assert not ledger.claim_dispatch(dispatch_id='exact', payload_hash='a'*64, execution_id='second', observed_at_utc=utc_now())
    assert reconcile(ledger, SimpleNamespace(_verify_result=verify)) == []
    assert len(calls) == (1 if stage in {'AGENT_EXITED', 'PUBLISHING'} else 0)


def test_v3_migration_preserves_dispatch_result_and_cursor(tmp_path):
    """Seed a real v3 database, not a pre-migration claim via the v5 API.

    v3 has no claim_authority: new claim_dispatch must fail closed against it.
    Migrating must preserve the historical result, cursor and consumed identity.
    """
    ledger = SQLiteLedger(tmp_path / 'old.db')
    now = utc_now()
    result_json = json.dumps({'after_head': 'b' * 40}, sort_keys=True)
    repository, branch, cursor_sha = 'dunglt2505/FOX2', 'work/control', 'c' * 40
    with ledger.connect() as connection:
        connection.execute('CREATE TABLE bridge_meta (key TEXT PRIMARY KEY,value TEXT NOT NULL)')
        for version in (1, 2, 3):
            for sql in MIGRATIONS[version]:
                connection.execute(sql)
        connection.execute(
            'INSERT INTO dispatches (dispatch_id, state, payload_hash, created_at_utc, updated_at_utc) '
            'VALUES (?, ?, ?, ?, ?)',
            ('preserved', 'PUSHED_UNREVIEWED', 'a' * 64, now, now),
        )
        connection.execute(
            'INSERT INTO executions (execution_id, dispatch_id, state, started_at_utc, '
            'finished_at_utc, result_json, error_code, error_message) '
            'VALUES (?, ?, ?, ?, ?, ?, NULL, NULL)',
            ('e', 'preserved', 'PUSHED_UNREVIEWED', now, now, result_json),
        )
        connection.execute(
            'INSERT INTO control_cursors (repository, control_branch, control_commit_sha, updated_at_utc) '
            'VALUES (?, ?, ?, ?)',
            (repository, branch, cursor_sha, now),
        )

    # v5 code cannot mint a claim against a v3 authority-less database.
    assert not ledger.claim_dispatch(
        dispatch_id='unadmitted', payload_hash='a' * 64,
        execution_id='denied', observed_at_utc=now,
    )
    with ledger.connect() as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM dispatches WHERE dispatch_id='unadmitted'"
        ).fetchone()[0] == 0

    assert ledger.initialize() == SCHEMA_VERSION
    assert ledger.dispatch_status('preserved')['result']['after_head'] == 'b' * 40
    assert ledger.get_control_cursor(repository, branch) == cursor_sha
    assert not ledger.claim_dispatch(
        dispatch_id='preserved', payload_hash='a' * 64,
        execution_id='new', observed_at_utc=now,
    )
    assert ledger.initialize() == SCHEMA_VERSION
    assert ledger.dispatch_status('preserved')['result']['after_head'] == 'b' * 40
    assert ledger.get_control_cursor(repository, branch) == cursor_sha


@pytest.mark.parametrize('product', ['CODEX','COPILOT'])
def test_exact_ops_selection(product):
    raw = json.dumps({'dispatch_id':'exact', 'agent':{'product':product}, 'runtime_contract':{'auto_execute':True}}).encode()
    assert BridgeOps._auto_execute_identity(raw) == (True, 'exact')


def test_model_commands_and_no_fabricated_observation():
    args, metadata = policy_arguments({'product':'COPILOT'}, '--model --no-ask-user --output-format --auto-tier')
    assert args == ['--model','auto','--no-ask-user','--output-format','json','--auto-tier','balance']
    assert metadata['auto_tier_status'] == 'APPLIED_TASK_LOCAL'
    assert metadata['requested']['auto_tier'] == 'balance'
    assert metadata['observed_model'] is None and metadata['quota'] == 'NOT_EXPOSED'
    assert 'allow-all' not in str(args) and 'yolo' not in str(args)
    observed = observe_metadata(metadata, '{"model":"explicit-model"}\nnot json')
    assert observed['observed_model'] == 'explicit-model'
    args, _ = policy_arguments({'product':'COPILOT','model_policy':'PINNED','model':'pinned', 'max_ai_credits':2},
                               '--model --no-ask-user --max-ai-credits')
    assert args == ['--model','pinned','--no-ask-user','--max-ai-credits','2']
    args, metadata = policy_arguments({'product':'CODEX','model_policy':'PINNED','model':'gpt-6.1-sol','reasoning_effort':'high'}, '--model --config')
    assert args == ['--model','gpt-6.1-sol','-c','model_reasoning_effort="high"']
    assert metadata['observed_reasoning_effort'] is None
    assert policy_arguments({'product':'CODEX'}, '')[0] == []


@pytest.mark.parametrize('selection,help_output', [
    ({'product':'COPILOT'}, ''),
    ({'product':'COPILOT','max_ai_credits':2}, '--model --no-ask-user'),
    ({'product':'CODEX','model_policy':'PINNED','model':'pinned'}, ''),
    ({'product':'CODEX','reasoning_effort':'high'}, '--model'),
])
def test_unsupported_cli_is_actionable_without_substitution(selection, help_output):
    with pytest.raises(ToolExecFailed):
        policy_arguments(selection, help_output)


@pytest.mark.parametrize('selection', [
    {'product':'UNKNOWN'}, {'product':'CODEX','model_policy':'PINNED'},
    {'product':'CODEX','reasoning_effort':'max'},
    {'product':'COPILOT','model':'other'}, {'product':'COPILOT','auto_tier':'unknown'},
    {'product':'COPILOT','max_ai_credits':True}, {'product':'CODEX','model':'x; arbitrary'},
])
def test_invalid_selection_rejected(selection):
    with pytest.raises(DispatchInvalid):
        validate_selection(selection)


def test_startup_command_idempotent_and_mocked_apply(bridge_config, monkeypatch):
    calls = []
    monkeypatch.setattr('fox2_agent_bridge.startup.subprocess.run',
                        lambda cmd, **kwargs: calls.append(cmd) or SimpleNamespace(returncode=0))
    set_start_with_windows(bridge_config, True)
    set_start_with_windows(bridge_config, True)
    set_start_with_windows(bridge_config, False)
    assert calls[0] == calls[1] == startup_command(bridge_config, True)
    assert calls[2][-1] == 'false'
    assert SQLiteLedger(bridge_config.database_path).worker_state()['start_with_windows'] is False
    script = (Path(__file__).parents[1]/'scripts/desktop_startup.ps1').read_text()
    assert '-RunLevel Limited' in script and '-LogonType Interactive' in script
    assert '-AtLogOn -User $Identity.Name' in script and '-Force' in script
    assert 'if ($Existing)' in script and 'Unregister-ScheduledTask -TaskName $TaskName' in script
    assert 'SYSTEM' not in script and 'Password' not in script


def test_tray_fixed_actions_hidden_launch_and_state_mapping():
    scripts = Path(__file__).parents[1]/'scripts'
    tray = (scripts/'desktop_tray.ps1').read_text()
    launcher = (scripts/'desktop_launcher.ps1').read_text()
    for action in ('pause','resume','check-now','request-exit','open-logs','set-start-with-windows','status'):
        assert action in tray
    for state in ('PAUSED','DEGRADED','ERROR','STOPPED','STOPPING'):
        assert state in tray and state in STATES
    assert 'Mutex.WaitOne(0)' in tray and 'CreateNoWindow = $true' in tray
    assert 'UseShellExecute = $false' in tray and 'ArgumentList.Add' in tray
    assert 'CreateNoWindow = $true' in launcher and 'UseShellExecute = $false' in launcher
    assert "fox2_agent_bridge.launcher" in launcher
    assert 'current_dispatch' in tray and 'last_result.status' in tray
    assert 'Invoke-Expression' not in tray


def test_open_logs_only_configured_path(bridge_config, monkeypatch):
    calls = []
    monkeypatch.setattr('fox2_agent_bridge.desktop.os.startfile', calls.append)
    control(bridge_config, 'open-logs')
    assert calls == [bridge_config.log_directory]


def test_durable_state_and_checkpoint_redact_secrets(bridge_config):
    ledger = SQLiteLedger(bridge_config.database_path)
    ledger.initialize()
    secret = 'gho_' + 'A'*30
    ledger.update_worker(last_error=secret)
    assert secret not in json.dumps(ledger.worker_state())
    ledger.claim_dispatch(dispatch_id='redact',payload_hash='a'*64,execution_id='e',observed_at_utc=utc_now())
    ledger.checkpoint('e','RUNNING',{'agent_stdout':secret, 'api_key':'synthetic'})
    assert secret not in ledger.pending_executions()[0]['checkpoint_json']


def test_graceful_exit_does_not_interrupt_active_task(bridge_config, monkeypatch):
    item, _, _ = worker(bridge_config)
    calls=[]
    def finish_task():
        item.ledger.control('request-exit')
        calls.append('task-completed')
        return OpsRunResult('PUSHED_UNREVIEWED','NO_CHANGE','exact','exact',{})
    item.ops.run_next=finish_task
    assert item.tick()
    assert calls == ['task-completed']
    assert not item.tick()


def test_worker_lifecycle_preserves_pause_and_releases_singleton(bridge_config, monkeypatch):
    item, _, _ = worker(bridge_config)
    item.ledger.control('pause')
    monkeypatch.setattr('fox2_agent_bridge.desktop.discover_all', lambda _: ())
    def request_stop(_):
        assert item.ledger.worker_state()['state'] == 'PAUSED'
        item.ledger.control('request-exit')
    item.sleep = request_stop
    item.run()
    state = item.ledger.worker_state()
    assert state['state'] == 'STOPPED' and state['paused']
    assert state['started'] and state['stopped'] and state['generation']
    with ProcessLock(bridge_config.bridge_root/'data/bridge.lock'):
        pass


@pytest.mark.parametrize('product,fail', [('CODEX',False),('COPILOT',False),('CODEX',True),('COPILOT',True)])
def test_full_runner_exact_routing_and_failure_no_fallback(bridge_config, monkeypatch, product, fail):
    from fox2_agent_bridge.codex_adapter import CodexAdapter
    from fox2_agent_bridge.copilot_adapter import CopilotAdapter
    ledger = SQLiteLedger(bridge_config.database_path)
    ledger.initialize()
    payload = {'dispatch_id':'exact','_payload_sha256':'a'*64, '_agent_product':product,
               'agent':{'product':product},'branch':'work/exact','worktree':str(bridge_config.worktree_root/'exact')}
    transport = SimpleNamespace(query_control_sha=lambda _: 'c'*40, fetch_control=lambda *_: None,
                                read_dispatch_blob=lambda *_: (b'{}','d'*40))
    runner = BridgeE2ERunner(bridge_config, ledger, transport=transport)
    monkeypatch.setattr('fox2_agent_bridge.e2e_runner.DispatchPoller.poll_once', lambda _:SimpleNamespace(status='NO_CHANGE'))
    monkeypatch.setattr(runner, '_validate_dispatch', lambda *args,**kwargs:payload)
    monkeypatch.setattr(runner, '_resolve_worktree', lambda _: (Path(payload['worktree']),'a'*40))
    monkeypatch.setattr(runner, '_resolve_prompt', lambda _: 'immutable prompt')
    monkeypatch.setattr(runner, '_prepare_required_parents', lambda **_:None)
    monkeypatch.setattr(runner, '_write_runtime_report_best_effort', lambda **_:None)
    monkeypatch.setattr(runner, '_commit_and_push_codex_result', lambda **_:('b'*40, ('reports/exact.md',)))
    calls=[]
    def agent_call(name):
        def call(self, **kwargs):
            calls.append((name, kwargs))
            assert kwargs['selection']['product'] == product
            if fail:
                raise ToolExecFailed('login/quota unavailable')
            return SimpleNamespace(exit_code=0,stdout='marker',stderr='',metadata={'observed_model':None})
        return call
    monkeypatch.setattr(CodexAdapter,'run_prompt',agent_call('CODEX'))
    monkeypatch.setattr(CopilotAdapter,'run_prompt',agent_call('COPILOT'))
    if fail:
        with pytest.raises(ToolExecFailed):
            runner.run_once(dispatch_path='exact')
    else:
        assert runner.run_once(dispatch_path='exact').agent_product == product
    assert [name for name,_ in calls] == [product]
    if product == 'COPILOT':
        assert calls[0][1]['allow_git'] is False
        assert calls[0][1]['allow_github_url'] is False
        assert calls[0][1]['no_ask_user'] is True
    assert not ledger.claim_dispatch(dispatch_id='exact',payload_hash='a'*64,execution_id='replay',observed_at_utc=utc_now())


def test_atomic_pause_blocks_claim(bridge_config):
    ledger = SQLiteLedger(bridge_config.database_path)
    ledger.initialize()
    ledger.control('pause')
    assert not ledger.claim_dispatch(dispatch_id='new',payload_hash='a'*64,execution_id='e',
                                     observed_at_utc=utc_now(),honor_controls=True)
    assert ledger.dispatch_state('new') is None


def test_legacy_ledger_snapshot_before_per_user_poll(bridge_config, monkeypatch, tmp_path):
    from fox2_agent_bridge.desktop import initialize_runtime
    legacy_root = tmp_path/'legacy'
    old = SQLiteLedger(legacy_root/'data/bridge.db')
    old.initialize()
    old.claim_dispatch(dispatch_id='consumed',payload_hash='a'*64,execution_id='old',observed_at_utc=utc_now())
    monkeypatch.setattr('fox2_agent_bridge.desktop.LEGACY_ROOT',legacy_root)
    monkeypatch.setattr('fox2_agent_bridge.desktop.BRIDGE_ROOT',bridge_config.bridge_root)
    new = initialize_runtime(bridge_config)
    assert new.dispatch_status('consumed')['payload_hash'] == 'a'*64
    assert old.dispatch_status('consumed')['execution_state'] == 'RUNNING'
    assert not new.claim_dispatch(dispatch_id='consumed',payload_hash='a'*64,execution_id='replay',observed_at_utc=utc_now())


def test_codex_adapter_passes_model_and_keeps_safety(bridge_config, monkeypatch, tmp_path):
    from fox2_agent_bridge.codex_adapter import CodexAdapter
    from test_codex_adapter import FakeProcess
    executable = tmp_path/'codex.exe'; executable.write_text('')
    worktree = bridge_config.worktree_root/'exact'; worktree.mkdir(parents=True)
    (worktree/'.git').write_text('fixture')
    adapter = CodexAdapter(bridge_config)
    monkeypatch.setattr(adapter,'_resolve_executable',lambda:executable)
    monkeypatch.setattr('fox2_agent_bridge.codex_adapter.help_text',lambda *_: __import__('conftest').FAKE_CLI_HELP)
    commands=[]
    monkeypatch.setattr('fox2_agent_bridge.codex_adapter.subprocess.Popen',
                        lambda cmd,**kwargs:commands.append(cmd) or FakeProcess(stdout='{"model":"observed"}\n',stderr=''))
    result=adapter.run_prompt(worktree=worktree,prompt='fixture',selection={'product':'CODEX','model_policy':'PINNED','model':'pinned','reasoning_effort':'high'})
    command=commands[0]
    assert command[command.index('--model')+1] == 'pinned'
    assert 'model_reasoning_effort="high"' in command
    assert command[command.index('--sandbox')+1] == 'danger-full-access'
    assert command[command.index('--ask-for-approval')+1] == 'never'
    assert result.metadata['observed_model'] == 'observed'


def test_powershell_scripts_parse_and_startup_mock_is_idempotent(tmp_path):
    scripts = Path(__file__).parents[1]/'scripts'
    harness=tmp_path/'check.ps1'
    harness.write_text('''param([string]$Scripts)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$ProbeIcon=[System.Windows.Forms.NotifyIcon]::new()
$ProbeTimer=[System.Windows.Forms.Timer]::new()
$ProbeIcon.Text='FOX2 Bridge: Running'
$ProbeTimer.Interval=2000
$ProbeTimer.Dispose(); $ProbeIcon.Dispose()
foreach ($File in Get-ChildItem -LiteralPath $Scripts -Filter 'desktop_*.ps1') {
  $Tokens=$null; $Errors=$null
  [System.Management.Automation.Language.Parser]::ParseFile($File.FullName,[ref]$Tokens,[ref]$Errors) | Out-Null
  if ($Errors.Count) { throw ($Errors | Out-String) }
}
$global:Fox2MockExists=$false; $global:Fox2MockRegistered=0; $global:Fox2MockDeleted=0
function Get-ScheduledTask { param($TaskName,$ErrorAction) if ($global:Fox2MockExists) { return @{TaskName=$TaskName} } }
function New-ScheduledTaskAction { param($Execute,$Argument) return @{Execute=$Execute; Argument=$Argument} }
function New-ScheduledTaskTrigger { param([switch]$AtLogOn,$User) return @{User=$User} }
function New-ScheduledTaskPrincipal { param($UserId,$LogonType,$RunLevel)
  if ($UserId -eq 'SYSTEM' -or $RunLevel -ne 'Limited' -or $LogonType -ne 'Interactive') { throw 'wrong principal' }
  return @{UserId=$UserId}
}
function New-ScheduledTaskSettingsSet { param($MultipleInstances,$ExecutionTimeLimit,[switch]$AllowStartIfOnBatteries,[switch]$DontStopIfGoingOnBatteries) return @{} }
function Register-ScheduledTask { param($TaskName,$Action,$Trigger,$Principal,$Settings,[switch]$Force)
  if (-not $Force -or $TaskName -notlike 'FOX2Bridge-S-1-*') { throw 'wrong task identity' }
  $global:Fox2MockExists=$true; $global:Fox2MockRegistered++
}
function Unregister-ScheduledTask { param($TaskName,$Confirm) $global:Fox2MockExists=$false; $global:Fox2MockDeleted++ }
# Dot-source because the fixed production script exits after disable; enable
# twice checks its force-update path with actual PowerShell binding.
. (Join-Path $Scripts 'desktop_startup.ps1') -Enabled true
. (Join-Path $Scripts 'desktop_startup.ps1') -Enabled true
if ($global:Fox2MockRegistered -ne 2 -or -not $global:Fox2MockExists) { throw 'enable not idempotent' }
& (Join-Path $Scripts 'desktop_startup.ps1') -Enabled false
& (Join-Path $Scripts 'desktop_startup.ps1') -Enabled false
if ($global:Fox2MockDeleted -ne 1 -or $global:Fox2MockExists) { throw 'disable not idempotent' }
'PARSE_AND_MOCK_STARTUP_PASS'
''',encoding='utf-8')
    result=subprocess.run([r'C:\Program Files\PowerShell\7\pwsh.exe','-NoProfile','-NonInteractive','-File',str(harness),'-Scripts',str(scripts)],capture_output=True,text=True,timeout=30)
    assert result.returncode == 0, result.stderr
    assert 'PARSE_AND_MOCK_STARTUP_PASS' in result.stdout


def test_idle_ops_invokes_zero_agents_and_resume_skips_consumed(bridge_config, monkeypatch):
    ledger=SQLiteLedger(bridge_config.database_path); ledger.initialize()
    monkeypatch.setattr('fox2_agent_bridge.ops_runner.DispatchPoller.poll_once',lambda _:SimpleNamespace(status='NO_CHANGE'))
    monkeypatch.setattr('fox2_agent_bridge.ops_runner.BridgeE2ERunner.run_once',
                        lambda *args,**kwargs:pytest.fail('idle or completed dispatch invoked an Agent'))
    ops=BridgeOps(bridge_config,ledger,transport=SimpleNamespace())
    monkeypatch.setattr(ops,'_eligible_dispatch',lambda:None)
    assert ops.run_next().status == 'NO_ELIGIBLE_DISPATCH'
    payload={'dispatch_id':'done','agent':{'product':'CODEX'},'runtime_contract':{'auto_execute':True}}
    path='docs/agent_handoff/exact/dispatch/done.json'
    ledger.claim_dispatch(dispatch_id='done',payload_hash='a'*64,execution_id='e',observed_at_utc=utc_now())
    ledger.finish_execution(dispatch_id='done',execution_id='e',dispatch_state='PUSHED_UNREVIEWED',
                            execution_state='PUSHED_UNREVIEWED',finished_at_utc=utc_now())
    ops=BridgeOps(bridge_config,ledger,transport=SimpleNamespace(
        query_control_sha=lambda _: 'a'*40,fetch_control=lambda *_:None,
        read_dispatch_blob=lambda *_:(json.dumps(payload).encode(),'b'*40)))
    monkeypatch.setattr(ledger,'list_candidate_discoveries',lambda *args,**kwargs:({'dispatch_path':path,'discovery_state':'DISCOVERED'},))
    ledger.control('pause'); ledger.control('resume')
    assert ops.run_next().status == 'NO_ELIGIBLE_DISPATCH'


def test_recovery_rejects_wrong_expected_remote_sha(bridge_config):
    ledger=SQLiteLedger(bridge_config.database_path); ledger.initialize()
    ledger.claim_dispatch(dispatch_id='exact',payload_hash='a'*64,execution_id='e',observed_at_utc=utc_now())
    ledger.checkpoint('e','PUBLISHING',{'payload':{'worktree':str(bridge_config.worktree_root/'exact'),
        '_agent_product':'CODEX','agent':{'product':'CODEX'}}, 'before_head':'a'*40,
        'agent_stdout':'marker','expected_result_sha':'c'*40})
    assert reconcile(ledger,SimpleNamespace(_verify_result=lambda **kwargs:('b'*40,('reports/result',))))[0]['outcome'] == 'NEEDS_RECONCILIATION'


def test_exact_result_verification_branch_ancestry_scope_acceptance(bridge_config, monkeypatch):
    ledger=SQLiteLedger(bridge_config.database_path); ledger.initialize()
    runner=BridgeE2ERunner(bridge_config,ledger)
    worktree=bridge_config.worktree_root/'exact'; (worktree/'reports').mkdir(parents=True)
    (worktree/'reports/result.md').write_text('evidence')
    payload={'branch':'work/exact','allowed_code_paths':[], 'allowed_report_paths':['reports/**'],
             'acceptance':{'required_paths':['reports/result.md'],'stdout_contains':'marker'}}
    calls=[]
    def git(args,**kwargs):
        calls.append(args)
        if 'branch' in args:return SimpleNamespace(stdout='work/exact')
        if 'status' in args:return SimpleNamespace(stdout='')
        if 'rev-parse' in args:return SimpleNamespace(stdout='b'*40)
        if 'diff' in args:
            return SimpleNamespace(stdout=b'reports/result.md\x00' if kwargs.get('binary') else 'reports/result.md')
        return SimpleNamespace(stdout='')
    monkeypatch.setattr(runner,'_git',git)
    monkeypatch.setattr(runner,'_remote_branch_head',lambda branch:'b'*40)
    assert runner._verify_result(payload=payload,worktree=worktree,before_head='a'*40,agent_stdout='marker',agent_label='CODEX')[0] == 'b'*40
    assert any('merge-base' in args and '--is-ancestor' in args for args in calls)
    monkeypatch.setattr(runner,'_remote_branch_head',lambda branch:'c'*40)
    with pytest.raises(WorkspaceBlocked):
        runner._verify_result(payload=payload,worktree=worktree,before_head='a'*40,agent_stdout='marker',agent_label='CODEX')
