"""Whole Batch A acceptance with fake CLI and actual local Git publication."""
import json
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError
from pathlib import Path
from types import SimpleNamespace

import pytest

from conftest import FAKE_CLI_HELP
from test_e2e_runner import _dispatch_payload
from fox2_agent_bridge.agent_policy import (ExecutionTuple, configuration_mismatch, observe_metadata,
    permission_arguments, policy_arguments, tool_compatibility, validate_selection)
from fox2_agent_bridge.artifacts import canonical_text, text_hygiene, write_json, write_text
from fox2_agent_bridge.codex_adapter import CodexAdapter, CodexRunResult
from fox2_agent_bridge.copilot_adapter import CopilotAdapter, CopilotRunResult
from fox2_agent_bridge.config import BridgeConfig
from fox2_agent_bridge.desktop import reconcile
from fox2_agent_bridge.e2e_runner import BridgeE2ERunner
from fox2_agent_bridge.errors import AgentNotStarted, DatabaseError, DispatchInvalid, ReplayBlocked, ToolExecFailed
from fox2_agent_bridge.ledger import SQLiteLedger, utc_now
from fox2_agent_bridge.logging_config import configure_logging, log_event


@pytest.mark.parametrize('product', ['CODEX', 'COPILOT'])
def test_batch_full_access_preflight_blocks_before_spawn(bridge_config, monkeypatch, product):
    worktree = bridge_config.worktree_root / 'permission'
    worktree.mkdir(parents=True)
    (worktree / '.git').write_text('fixture')
    adapter = (CodexAdapter if product == 'CODEX' else CopilotAdapter)(bridge_config)
    monkeypatch.setattr(adapter, '_resolve_executable', lambda: Path(shutil.which('python')))
    monkeypatch.setattr(f'fox2_agent_bridge.{product.lower()}_adapter.help_text', lambda *_: '--model --config')
    monkeypatch.setattr(f'fox2_agent_bridge.{product.lower()}_adapter.subprocess.Popen',
                        lambda *_a, **_k: pytest.fail('permission preflight must prevent launch'))
    with pytest.raises(AgentNotStarted, match='material required'):
        adapter.run_prompt(worktree=worktree, prompt='fixture', selection={'product':product})
    with pytest.raises(DispatchInvalid, match='no downgrade'):
        permission_arguments({'product': product, 'permission_profile':'READ_ONLY'}, FAKE_CLI_HELP)


def test_batch_exact_policies_and_material_compatibility():
    selection = {'product':'CODEX','model_policy':'PINNED','model':'gpt-6.1-sol','reasoning_effort':'high'}
    args, metadata = policy_arguments(selection, FAKE_CLI_HELP)
    assert args == ['--model','gpt-6.1-sol','-c','model_reasoning_effort="high"']
    assert metadata['observed_model'] is metadata['observed_reasoning_effort'] is None
    for tier in ('efficiency', 'balance', 'intelligence'):
        args, metadata = policy_arguments({'product':'COPILOT','auto_tier':tier}, FAKE_CLI_HELP)
        assert args[args.index('--model')+1] == 'auto'
        assert args[args.index('--auto-tier')+1] == tier
        assert metadata['auto_tier_status'] == 'APPLIED_TASK_LOCAL'
    with pytest.raises(AgentNotStarted):
        policy_arguments({'product':'COPILOT','auto_tier':'intelligence'}, '--model --no-ask-user')
    result = tool_compatibility('new 99', 'old 1', FAKE_CLI_HELP, ('--model', '--config'))
    assert result['status'] == 'PASS' and result['version_deviation']
    for help_text in ('', '--model-fallback'):
        with pytest.raises(AgentNotStarted):
            tool_compatibility('old 1', 'old 1', help_text, ('--model',))


def test_batch_immutable_tuple_and_usage_survive_restart(bridge_config):
    ledger = SQLiteLedger(bridge_config.database_path); ledger.initialize()
    ledger.claim_dispatch(dispatch_id='usage',payload_hash='a'*64,execution_id='e',observed_at_utc=utc_now())
    selection = validate_selection({'product':'CODEX','model_policy':'PINNED','model':'exact','reasoning_effort':'high'})
    execution_tuple = ExecutionTuple('usage','work/exact','fixture','b'*64,json.dumps(selection,sort_keys=True),'AGENT')
    with pytest.raises(FrozenInstanceError):
        execution_tuple.branch = 'work/other'
    _, metadata = policy_arguments(selection, FAKE_CLI_HELP)
    observe_metadata(metadata, json.dumps({'model':'exact','reasoning_effort':'high','permission_profile':'FULL_ACCESS',
        'usage':{'input_tokens':100,'output_tokens':20,'ai_credits':0.25,'api_key':'ignored'},
        'capacity':{'remaining':10,'limit':50,'status':'available','secret':'ignored'}}))
    context = {'execution_tuple':execution_tuple.as_dict(),'agent_metadata':metadata}
    ledger.checkpoint('e','RUNNING',context)
    ledger.update_worker(execution_display={'requested':selection,'metadata':metadata})
    reopened = SQLiteLedger(bridge_config.database_path)
    actual = reopened.dispatch_status('usage')['checkpoint']['agent_metadata']
    assert actual['usage'] == {'input_tokens':100,'output_tokens':20,'ai_credits':0.25}
    assert actual['capacity'] == {'remaining':10,'limit':50,'status':'available'}
    assert reopened.worker_state()['execution_display']['metadata'] == actual
    assert not configuration_mismatch(actual)
    with pytest.raises(DatabaseError, match='immutable'):
        reopened.checkpoint('e','RUNNING',{**context,'execution_tuple':{**execution_tuple.as_dict(),'branch':'work/other'}})
    for command in ('status',):
        before = reopened.worker_state()
        assert reopened.control(command) == before == reopened.worker_state()


@pytest.mark.parametrize('code', ['quota_exceeded','capacity_unavailable','authentication_error'])
@pytest.mark.parametrize('product', ['CODEX','COPILOT'])
@pytest.mark.parametrize('schema', ['0.6', '2.0', '3.0'])
def test_batch_post_start_zero_exit_capacity_never_publishes(bridge_config, monkeypatch, product, code, schema):
    ledger = SQLiteLedger(bridge_config.database_path); ledger.initialize()
    payload = _dispatch_payload(bridge_config.worktree_root/'exact')
    payload.update(dispatch_id='exact', branch='work/exact', delivery_owner='AGENT')
    payload['agent'] = validate_selection({'product': product,
        'interface': 'OPENAI_CODEX_CLI' if product == 'CODEX' else 'GITHUB_COPILOT_CLI'})
    payload['execution_path'] = f'BRIDGE_DIRECT_{product}_CLI'
    if schema != '0.6':
        from test_project_dictionary import bound_dispatch
        payload = bound_dispatch(payload, schema)
    raw = json.dumps(payload).encode()
    dispatch_id = payload['dispatch_id']
    dispatch_path = 'docs/agent_handoff/DISPATCH/' + dispatch_id + '.json'
    transport = SimpleNamespace(query_control_sha=lambda _: 'c'*40,fetch_control=lambda *_:None,
        read_dispatch_blob=lambda *_:(raw,'d'*40))
    runner=BridgeE2ERunner(bridge_config,ledger,transport=transport)
    monkeypatch.setattr('fox2_agent_bridge.e2e_runner.DispatchPoller.poll_once',lambda _:SimpleNamespace(status='NO_CHANGE'))
    payload = runner._validate_dispatch(raw, dispatch_path=dispatch_path, observed_blob_sha='d'*40)
    monkeypatch.setattr(runner,'_resolve_worktree',lambda _:(Path(payload['worktree']),'a'*40))
    monkeypatch.setattr(runner,'_resolve_prompt',lambda _:'fixture')
    monkeypatch.setattr(runner,'_prepare_required_parents',lambda **_:None)
    monkeypatch.setattr(runner,'_verify_result',lambda **_:pytest.fail('capacity failure must not verify/publish'))
    monkeypatch.setattr(runner,'_commit_and_push_codex_result',lambda **_:pytest.fail('duplicate publication'))
    calls=[]
    def invoke(self, **kwargs):
        calls.append(product)
        _,metadata=policy_arguments(payload['agent'],FAKE_CLI_HELP)
        observe_metadata(metadata,json.dumps({'error':{'code':code},'usage':{'output_tokens':7}}))
        kwargs['configuration'](metadata)
        cls=CodexRunResult if product=='CODEX' else CopilotRunResult
        return cls('EXITED',0,'structured failure','','fake',payload['worktree'],metadata)
    monkeypatch.setattr(CodexAdapter if product=='CODEX' else CopilotAdapter,'run_prompt',invoke)
    monkeypatch.setattr(CopilotAdapter if product=='CODEX' else CodexAdapter,'run_prompt',
                        lambda *_a,**_k:pytest.fail('Agent substitution'))
    with pytest.raises(ToolExecFailed,match='post-start'):
        runner.run_once(dispatch_path=dispatch_path)
    state=SQLiteLedger(bridge_config.database_path).dispatch_status(dispatch_id)
    assert state['dispatch_state']==state['execution_state']=='NEEDS_RECONCILIATION'
    assert state['checkpoint']['agent_metadata']['usage']['output_tokens']==7
    assert reconcile(ledger,runner)==[]
    with pytest.raises(ReplayBlocked):
        runner.run_once(dispatch_path=dispatch_path)
    assert calls==[product]


@pytest.mark.parametrize('product',['CODEX','COPILOT'])
@pytest.mark.parametrize('owner',['AGENT','BRIDGE'])
@pytest.mark.parametrize('schema', ['0.6', '2.0', '3.0'])
def test_batch_real_git_delivery_has_one_publication_path(tmp_path, monkeypatch, product, owner, schema):
    root=tmp_path/'worktrees'; root.mkdir()
    repo=root/'task'; remote=tmp_path/'remote.git'
    def git(*args):
        return subprocess.run(['git',*args],capture_output=True,text=True,encoding='utf-8',check=True).stdout.strip()
    git('init','--bare',str(remote)); git('init',str(repo))
    git('-C',str(repo),'config','user.name','Fixture');git('-C',str(repo),'config','user.email','fixture@local.invalid')
    write_text(repo/'seed.txt','seed');git('-C',str(repo),'add','seed.txt');git('-C',str(repo),'commit','-m','seed')
    git('-C',str(repo),'checkout','-b','work/exact');git('-C',str(repo),'remote','add','origin',str(remote))
    git('-C',str(repo),'push','origin','work/exact')
    base=git('-C',str(repo),'rev-parse','HEAD')
    monkeypatch.setattr('fox2_agent_bridge.config.PROJECT_ROOT',repo)
    monkeypatch.setattr('fox2_agent_bridge.config.WORKTREE_ROOT',root)
    config=BridgeConfig(local_repo=repo,worktree_root=root,bridge_root=tmp_path/'bridge',
                        tool_paths={'git':Path(shutil.which('git'))})
    payload=_dispatch_payload(repo);payload.update(branch='work/exact',base_sha=base,delivery_owner=owner)
    payload['agent']={'product':product,'interface':'OPENAI_CODEX_CLI' if product=='CODEX' else 'GITHUB_COPILOT_CLI',
                      'model_policy':'PINNED','model':'fixture-model'}
    payload['execution_path']=f'BRIDGE_DIRECT_{product}_CLI'
    if schema != '0.6':
        from test_project_dictionary import bound_dispatch
        payload = bound_dispatch(payload, schema)
    raw=json.dumps(payload).encode()
    transport=SimpleNamespace(query_control_sha=lambda _:'c'*40,fetch_control=lambda *_:None,
        read_dispatch_blob=lambda *_:(raw,'d'*40))
    ledger=SQLiteLedger(config.database_path);ledger.initialize()
    def verify_fixture_tests(root, tree, names):
        # This integration uses a fake Agent and a trusted fixture verifier.
        # The verifier checks actual artifact bytes, outside Agent stdout.
        artifact = root/'reports/FOX2-BRIDGE-E2E-CANARY/result.md'
        passed = artifact.read_text().strip() == 'fixture result'
        return {'tree_sha': tree, 'results': {
            name: 'PASS' if passed else 'FAIL' for name in names}}
    runner=BridgeE2ERunner(config,ledger,transport=transport,
                         required_test_verifier=verify_fixture_tests)
    monkeypatch.setattr('fox2_agent_bridge.e2e_runner.DispatchPoller.poll_once',lambda _:SimpleNamespace(status='NO_CHANGE'))
    monkeypatch.setattr(runner,'_resolve_prompt',lambda _:'immutable fixture')
    publisher_calls=[]
    publish=runner._commit_and_push_codex_result
    def bridge_publish(**kwargs):
        publisher_calls.append('BRIDGE');return publish(**kwargs)
    monkeypatch.setattr(runner,'_commit_and_push_codex_result',bridge_publish)
    def invoke(self, **kwargs):
        assert kwargs['selection']['product']==product
        assert f'Dispatch delivery owner: {owner}' in kwargs['prompt']
        _,metadata=policy_arguments(kwargs['selection'],FAKE_CLI_HELP)
        metadata['applied_permission']={'profile':'FULL_ACCESS','status':'APPLIED'}
        observe_metadata(metadata,'{"model":"fixture-model","usage":{"input_tokens":12,"output_tokens":3}}')
        kwargs['configuration'](metadata)
        write_text(repo/'reports/FOX2-BRIDGE-E2E-CANARY/result.md','fixture result')
        if owner=='AGENT':
            publisher_calls.append('AGENT')
            git('-C',str(repo),'add','reports');git('-C',str(repo),'commit','-m','Agent result')
            git('-C',str(repo),'push','origin','HEAD:refs/heads/work/exact')
        cls=CodexRunResult if product=='CODEX' else CopilotRunResult
        return cls('EXITED',0,'marker','','fake',str(repo),metadata)
    monkeypatch.setattr(CodexAdapter if product=='CODEX' else CopilotAdapter,'run_prompt',invoke)
    monkeypatch.setattr(CopilotAdapter if product=='CODEX' else CodexAdapter,'run_prompt',
                        lambda *_a,**_k:pytest.fail('Agent substitution'))
    dispatch_path='docs/agent_handoff/dispatch/'+payload['dispatch_id']+'.json'
    result=runner.run_once(dispatch_path=dispatch_path)
    assert publisher_calls==[owner]
    assert result.status=='PUSHED_UNREVIEWED'
    assert result.after_head==git('--git-dir',str(remote),'rev-parse','refs/heads/work/exact')
    assert git('-C',str(repo),'rev-list','--count',base+'..HEAD')=='1'
    assert ledger.dispatch_status(payload['dispatch_id'])['checkpoint']['execution_tuple']['delivery_owner']==owner
    snapshot=config.bridge_root/'data/results'/f"{payload['dispatch_id']}.json"
    text_hygiene(snapshot)
    assert json.loads(snapshot.read_text())['result']['agent_metadata']['usage']['input_tokens']==12
    with pytest.raises(ReplayBlocked):
        # Skip pre-execution base check to exercise the retained dispatch identity.
        monkeypatch.setattr(runner,'_resolve_worktree',lambda _:(repo,base))
        runner.run_once(dispatch_path=dispatch_path)
    assert publisher_calls==[owner]


def test_batch_canonical_artifacts_and_logs(tmp_path):
    path=tmp_path/'artifact.json'
    write_json(path,{'z':'text  \r\nline\t','a':1});text_hygiene(path)
    assert path.read_bytes().endswith(b'\n') and b'\r' not in path.read_bytes()
    first=path.read_bytes();write_json(path,{'a':1,'z':'text  \r\nline\t'});assert path.read_bytes()==first
    assert canonical_text('a \r\nb\t\r')=='a\nb\n'
    path.write_bytes(b'bad \r\n')
    with pytest.raises(ValueError):text_hygiene(path)
    logger=configure_logging(tmp_path/'logs')
    log_event(logger,component='test',event='usage',context={'input_tokens':42,'secret':'synthetic'})
    for handler in tuple(logger.handlers):handler.close();logger.removeHandler(handler)
    log=tmp_path/'logs/bridge.log';text_hygiene(log)
    assert json.loads(log.read_text())['context']=={'input_tokens':42,'secret':'<REDACTED>'}


def test_batch_claim_race_consumes_once(bridge_config):
    ledger=SQLiteLedger(bridge_config.database_path);ledger.initialize()
    def claim(number):
        return ledger.claim_dispatch(dispatch_id='race',payload_hash='a'*64,execution_id=str(number),observed_at_utc=utc_now())
    with ThreadPoolExecutor(max_workers=8) as pool:
        results=list(pool.map(claim,range(8)))
    assert sum(results)==1
    assert len(ledger.pending_executions())==1


def test_batch_tray_usage_controls_are_read_only():
    tray=(Path(__file__).parents[1]/'scripts/desktop_tray.ps1').read_text()
    for name in ('Model','Permission','Usage','Capacity'):
        assert f'${name}.Enabled = $false' in tray
        assert f'${name}.add_Click' not in tray
    assert 'execution_display' in tray and 'NOT_EXPOSED' in tray
    assert 'set-model' not in tray and 'set-permission' not in tray


@pytest.mark.parametrize('product',['CODEX','COPILOT'])
def test_batch_streamed_telemetry_survives_output_tail(bridge_config, monkeypatch, product):
    from test_codex_adapter import FakeProcess as CodexProcess
    from test_copilot_adapter import FakeProcess as CopilotProcess
    worktree=bridge_config.worktree_root/'stream';worktree.mkdir(parents=True)
    (worktree/'.git').write_text('fixture')
    cls=CodexAdapter if product=='CODEX' else CopilotAdapter
    adapter=cls(bridge_config)
    monkeypatch.setattr(adapter,'_resolve_executable',lambda:Path(shutil.which('python')))
    selection={'product':product,'model_policy':'PINNED','model':'exact'}
    output='{"model":"exact","usage":{"input_tokens":23}}\n'+('padding'*5000)+'\n'
    commands=[]; observations=[]
    def spawn(command,**kwargs):
        commands.append(command)
        proc=CodexProcess if product=='CODEX' else CopilotProcess
        return proc(stdout=output,stderr='')
    monkeypatch.setattr(f'fox2_agent_bridge.{product.lower()}_adapter.subprocess.Popen',spawn)
    result=adapter.run_prompt(worktree=worktree,prompt='fixture',selection=selection,
                             configuration=lambda value:observations.append(json.loads(json.dumps(value))))
    assert result.metadata['usage']=={'input_tokens':23} and result.metadata['observed_model']=='exact'
    assert 'input_tokens' not in result.stdout
    assert observations[-1]['usage']=={'input_tokens':23}
    command=commands[0]
    if product=='CODEX':
        assert command[command.index('--sandbox')+1]=='danger-full-access'
        assert command[command.index('--ask-for-approval')+1]=='never'
    else:
        for flag in ('--allow-all-tools','--allow-all-paths','--allow-all-urls','--no-ask-user'):
            assert flag in command
    assert result.metadata['tool_compatibility']['status']=='PASS'


@pytest.mark.parametrize('stage',['AGENT_EXITED','PUBLISHING'])
@pytest.mark.parametrize('fault',['missing_exit','permission_mismatch','quota','model_mismatch'])
def test_batch_restart_requires_positive_exit_and_configuration(bridge_config,stage,fault):
    ledger=SQLiteLedger(bridge_config.database_path);ledger.initialize()
    ledger.claim_dispatch(dispatch_id='recover',payload_hash='a'*64,execution_id='e',observed_at_utc=utc_now())
    context={'agent_exit_code':0}
    _,metadata=policy_arguments({'product':'CODEX','model_policy':'PINNED','model':'exact'},FAKE_CLI_HELP)
    if fault=='missing_exit':context.pop('agent_exit_code')
    elif fault=='permission_mismatch':metadata['observed_permission_profile']='READ_ONLY'
    elif fault=='model_mismatch':metadata['observed_model']='alternate'
    else:metadata['post_start_failure']='quota_exceeded'
    context['agent_metadata']=metadata
    ledger.checkpoint('e',stage,context)
    assert reconcile(ledger,SimpleNamespace(_verify_result=lambda **_:pytest.fail('unproven recovery')))[0]['outcome']=='NEEDS_RECONCILIATION'


@pytest.mark.parametrize('field,value',[('permission_profile','READ_ONLY'),('delivery_owner','UNKNOWN')])
def test_batch_dispatch_permission_and_owner_fail_closed(bridge_config,field,value):
    ledger=SQLiteLedger(bridge_config.database_path);ledger.initialize()
    payload=_dispatch_payload(bridge_config.worktree_root/'exact');payload[field]=value
    with pytest.raises(DispatchInvalid):
        BridgeE2ERunner(bridge_config,ledger)._validate_dispatch(json.dumps(payload).encode(),
            dispatch_path='docs/agent_handoff/dispatch/'+payload['dispatch_id']+'.json',observed_blob_sha='e'*40)


def test_batch_unknown_usage_is_not_fabricated():
    _,metadata=policy_arguments({'product':'COPILOT','auto_tier':'intelligence'},FAKE_CLI_HELP)
    observe_metadata(metadata,'not json model=pretend usage=999\n'+json.dumps({'usage':{'input_tokens':True,'cost_usd':float('nan')}}))
    assert metadata['observed_model'] is metadata['usage'] is metadata['capacity'] is None
    assert metadata['quota']=='NOT_EXPOSED'
    for bad in ({'product':'CODEX','sandbox':'workspace-write'}, {'product':'CODEX','approval_policy':'on-request'}):
        with pytest.raises(DispatchInvalid,match='mismatch'):validate_selection(bad)
