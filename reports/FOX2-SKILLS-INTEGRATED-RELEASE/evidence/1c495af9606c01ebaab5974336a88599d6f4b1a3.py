"""Pinned binding drift, external identities and shared runtime regression gates."""
import importlib.util
import json
from pathlib import Path

import pytest

from fox2_agent_bridge import project_dictionary as registry
from fox2_agent_bridge import dispatch_schema_v3_contract as schema_contract
from fox2_agent_bridge.config import BridgeConfig
from fox2_agent_bridge.dispatch_poller import _candidate_path, _parse_tree_listing
from fox2_agent_bridge.e2e_runner import BridgeE2ERunner
from fox2_agent_bridge.errors import ConfigInvalid, DispatchInvalid, PathInvalid
from fox2_agent_bridge.ledger import SQLiteLedger
from test_e2e_runner import _dispatch_payload


def bound_dispatch(legacy, schema='3.0'):
    """External v2 shape plus the current v3 Dictionary identity block."""
    product = legacy['agent']['product']
    routing = {key: value for key, value in legacy['agent'].items()
               if key not in ('product', 'interface')}
    routing.setdefault('model_policy', 'NATIVE_AUTO' if product == 'COPILOT' else 'CURRENT_CONFIG')
    routing.setdefault('permission_profile', 'FULL_ACCESS')
    policy = registry.CURRENT['policy'] if schema == '3.0' else {
        'version': '1.8.6', 'path': 'docs/governance/FOX2_POLICY_V1.8.6.md'}
    return {'schema_version': schema, 'project': registry.PROJECT_ID,
            'dispatch_id': legacy['dispatch_id'], 'wp_id': legacy['wp_id'],
            'dispatch_action': 'EXECUTE_LOCAL_AGENT', 'workspace_id': registry.WORKSPACE_ID,
            'target_agent': product, 'routing': routing, 'execution_path': 'BRIDGE',
            'delivery_owner': legacy.get('delivery_owner', 'BRIDGE'), 'max_runs': 1,
            'dictionary': {'version': registry.DICTIONARY_VERSION, 'git_path': registry.SOURCE_PATH,
                           'sha256': registry.SOURCE_SHA256, 'git_commit_sha': registry.SOURCE_COMMIT},
            'policy': {'version': policy['version'], 'git_path': policy['path'],
                       'sha256': '1'*64, 'git_commit_sha': '2'*40},
            'task': {'path': 'docs/agent_handoff/FOX2-TASK/task.md',
                     'sha256': '3'*64, 'commit_sha': '4'*40},
            'source': {'commit_sha': '5'*40, 'git_source_ready': 'YES'},
            'prompt': legacy['prompt'], 'permissions': legacy['permissions'],
            'decision_receipt': {**{key: 'PASS' for key in ('policy_check', 'task_state_check',
                'source_binding_check', 'routing_r0_r7', 'assignment_check', 'material_capability_check')},
                'execution_authorized': 'YES', 'code_allowed': 'YES', 'dev_grant_ref': 'TEST_OWNER_AUTH'},
            'runtime_contract': {'repo': registry.REPOSITORY,
                **{key: legacy[key] for key in ('branch', 'worktree', 'base_sha',
                                               'allowed_code_paths', 'allowed_report_paths')},
                'required_capabilities': ['PYTEST'], 'stop_conditions': ['TEST_FAILURE']},
            'required_tests': ['python -m pytest -q'],
            'created_by': 'CHAT', 'created_at': '2026-10-14T08:45:00Z'}


def test_project_dictionary_binding_deterministic_drift():
    path = Path(__file__).parents[1] / 'scripts/generate_project_dictionary.py'
    spec = importlib.util.spec_from_file_location('generator', path)
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    raw = generator.source_bytes()
    expected = generator.generate(raw)
    assert generator.generate(raw) == expected == generator.OUTPUT.read_bytes()
    assert b'\r' not in expected and expected.endswith(b'\n')
    altered = json.loads(raw)
    altered['compatibility']['control_branch']['current'] = 'work/drift'
    assert generator.generate(json.dumps(altered).encode()) != expected
    print('PROJECT_DICTIONARY_BINDING=PASS')


def test_dictionary_control_branch_registry():
    assert BridgeConfig().control_branch == registry.CONTROL_BRANCH == 'work/FOX2-DISPATCH-chat'
    assert BridgeConfig(control_branch='work/FOX2-LOCAL-DISPATCH-chat').control_branch in registry.SUPPORTED_CONTROL_BRANCHES
    with pytest.raises(ConfigInvalid):
        BridgeConfig(control_branch='work/arbitrary')


@pytest.mark.parametrize('path,accepted', [
    ('docs/agent_handoff/DISPATCH/FOX2-DISPATCH-001.json', True),
    ('docs/agent_handoff/DISPATCH_V2/FOX2-DISPATCH-001.json', True),
    ('docs/agent_handoff/FOX2-WP/dispatch/FOX2-DISPATCH-001.json', True),
    ('docs/agent_handoff/DISPATCH/nested/id.json', False),
    ('docs/agent_handoff/unrelated.json', False),
    ('docs/agent_handoff/DISPATCH_V3/id.json', False),
])
def test_dictionary_stable_dispatch_discovery(path, accepted):
    assert _candidate_path(path.encode()) is accepted
    entries = _parse_tree_listing(b'100644 blob ' + b'a'*40 + b'\t' + path.encode() + b'\0', 'b'*40)
    assert bool(entries) is accepted


@pytest.fixture
def validation(bridge_config):
    ledger = SQLiteLedger(bridge_config.database_path)
    ledger.initialize()
    runner = BridgeE2ERunner(bridge_config, ledger)
    def validate(payload, filename=None):
        return runner._validate_dispatch(json.dumps(payload).encode(),
            dispatch_path='docs/agent_handoff/DISPATCH/' + (filename or payload['dispatch_id']) + '.json',
            observed_blob_sha='e'*40)
    return validate


@pytest.mark.parametrize('schema', ['3.0', '2.0', '0.6'])
@pytest.mark.parametrize('product', ['CODEX', 'COPILOT'])
@pytest.mark.parametrize('owner', ['AGENT', 'BRIDGE'])
def test_dictionary_schema_exact_normalized_tuple(bridge_config, validation, schema, product, owner):
    legacy = _dispatch_payload(bridge_config.worktree_root / 'task')
    legacy['delivery_owner'] = owner
    legacy['agent'] = {'product': product, 'interface': 'OPENAI_CODEX_CLI' if product == 'CODEX' else 'GITHUB_COPILOT_CLI',
                       'permission_profile': 'FULL_ACCESS',
                       **({'model_policy': 'PINNED', 'model': 'gpt-6.1-sol', 'reasoning_effort': 'medium'}
                          if product == 'CODEX' else {'model_policy': 'NATIVE_AUTO', 'auto_tier': 'balance'})}
    legacy['execution_path'] = f'BRIDGE_DIRECT_{product}_CLI'
    external = legacy if schema == '0.6' else bound_dispatch(legacy, schema)
    normalized = validation(external)
    expected = {**legacy['agent'], **({'model': 'auto'} if product == 'COPILOT' else {})}
    assert normalized['agent'] == expected
    assert normalized['delivery_owner'] == owner
    for key in ('branch', 'worktree', 'base_sha', 'allowed_code_paths', 'allowed_report_paths', 'prompt'):
        assert normalized[key] == legacy[key]
    assert normalized['execution_path'] == legacy['execution_path']
    assert normalized['_copilot_shell_tools'] == []
    assert normalized['_external_schema_version'] == schema


@pytest.mark.parametrize('block,key,value', [
    ('dictionary', 'version', '2.0'), ('dictionary', 'git_path', 'docs/wrong.json'),
    ('dictionary', 'sha256', '0'*64), ('dictionary', 'git_commit_sha', '0'*40),
    ('policy', 'version', '1.8.6'), ('policy', 'git_path', 'docs/wrong.md'),
    ('policy', 'sha256', 'bad'), ('task', 'path', 'docs/agent_handoff/../task.md'),
    ('source', 'git_source_ready', 'NO'), ('decision_receipt', 'policy_check', 'FAIL'),
    ('decision_receipt', 'execution_authorized', 'NO'), ('decision_receipt', 'code_allowed', 'NO'),
    ('runtime_contract', 'repo', 'other/repo'), ('runtime_contract', 'required_capabilities', ['X','X']),
    ('runtime_contract', 'stop_conditions', None), ('runtime_contract', 'worktree', 'C:/outside'),
    ('routing', 'permission_profile', 'BOUNDED_EXPLICIT'), ('routing', 'model_policy', 'UNKNOWN'),
    ('routing', 'reasoning_effort', 'high'),
    ('permissions', 'pr_create', True), ('permissions', 'merge_allowed', True),
    ('permissions', 'production_provider', True), ('permissions', 'broker_write', True),
    ('permissions', 'live', True),
    (None, 'delivery_owner', None), (None, 'workspace_id', 'OTHER'),
    (None, 'project', 'OTHER'), (None, 'target_agent', []), (None, 'max_runs', True),
    (None, 'required_tests', ['']), (None, 'schema_version', '4.0'),
])
def test_dictionary_v3_fails_closed(bridge_config, validation, block, key, value):
    payload = bound_dispatch(_dispatch_payload(bridge_config.worktree_root / 'task'))
    (payload if block is None else payload[block])[key] = value
    with pytest.raises((DispatchInvalid, PathInvalid)):
        validation(payload)


@pytest.mark.parametrize('schema', ['3.0', '2.0'])
@pytest.mark.parametrize('path', ['MANUAL_LOCAL', 'VSCODE_ONE_CLICK'])
def test_dictionary_non_bridge_never_spawned(bridge_config, monkeypatch, schema, path):
    from types import SimpleNamespace
    payload = bound_dispatch(_dispatch_payload(bridge_config.worktree_root / 'task'), schema)
    payload['execution_path'] = path
    transport = SimpleNamespace(query_control_sha=lambda _: 'c'*40, fetch_control=lambda *_: None,
        read_dispatch_blob=lambda *_: (json.dumps(payload).encode(), 'd'*40))
    ledger = SQLiteLedger(bridge_config.database_path)
    ledger.initialize()
    runner = BridgeE2ERunner(bridge_config, ledger, transport=transport)
    monkeypatch.setattr('fox2_agent_bridge.e2e_runner.DispatchPoller.poll_once', lambda _: SimpleNamespace(status='NO_CHANGE'))
    monkeypatch.setattr(runner, '_resolve_worktree', lambda _: pytest.fail('must reject before workspace/spawn'))
    with pytest.raises(DispatchInvalid, match='auto-execution'):
        runner.run_once(dispatch_path='docs/agent_handoff/DISPATCH/' + payload['dispatch_id'] + '.json')
    assert not ledger.pending_executions()


def test_dictionary_filename_and_legacy_bound_policy(bridge_config, validation):
    payload = bound_dispatch(_dispatch_payload(bridge_config.worktree_root / 'task'), '2.0')
    assert validation(payload)['policy']['version'] == '1.8.6'
    with pytest.raises(DispatchInvalid, match='dispatch_id'):
        validation(payload, 'transitional-001')
    del payload['delivery_owner']
    with pytest.raises(DispatchInvalid, match='delivery_owner'):
        validation(payload)


@pytest.mark.parametrize('schema', ['2.0', '3.0'])
def test_dictionary_codex_nullable_routing_preserved(bridge_config, validation, schema):
    legacy = _dispatch_payload(bridge_config.worktree_root / 'task')
    legacy['agent'] = {'product': 'CODEX', 'model_policy': 'PINNED', 'model': 'gpt-6.1-sol',
                       'reasoning_effort': 'medium', 'auto_tier': None,
                       'permission_profile': 'FULL_ACCESS'}
    payload = bound_dispatch(legacy, schema)
    normalized = validation(payload)
    assert normalized['agent']['auto_tier'] is None
    assert normalized['agent']['reasoning_effort'] == 'medium'
    payload['routing']['model_policy'] = 'NATIVE_AUTO'
    with pytest.raises(DispatchInvalid):
        validation(payload)
    payload['routing']['model_policy'] = 'PINNED'
    payload['routing']['model'] = None
    with pytest.raises(DispatchInvalid):
        validation(payload)


def test_dictionary_explicit_legacy_profile_v06(bridge_config):
    from dataclasses import replace
    config = replace(bridge_config, control_branch='work/FOX2-LOCAL-DISPATCH-chat')
    ledger = SQLiteLedger(config.database_path)
    ledger.initialize()
    payload = _dispatch_payload(config.worktree_root / 'task')
    payload['control_ref'] = 'refs/heads/' + config.control_branch
    result = BridgeE2ERunner(config, ledger)._validate_dispatch(json.dumps(payload).encode(),
        dispatch_path='docs/agent_handoff/FOX2-WP/dispatch/' + payload['dispatch_id'] + '.json',
        observed_blob_sha='e'*40)
    assert result['delivery_owner'] == 'BRIDGE'
    assert result['control_ref'] == payload['control_ref']

def test_dispatch_schema_v3_binding_deterministic_drift():
    path = Path(__file__).parents[1] / 'scripts/generate_dispatch_schema_v3_contract.py'
    spec = importlib.util.spec_from_file_location('schema_generator', path)
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    raw = generator.source_bytes()
    expected = generator.generate(raw)
    assert expected == generator.OUTPUT.read_bytes()
    assert schema_contract.SOURCE_SHA256 == __import__('hashlib').sha256(raw).hexdigest()
    assert schema_contract.DISPATCH_SCHEMA_V3 == json.loads(raw)
    print('DISPATCH_V3_SCHEMA_BINDING=PASS')


@pytest.mark.parametrize('field', sorted(schema_contract.DISPATCH_SCHEMA_V3['required']))
def test_dictionary_v3_required_fields_fail_closed(bridge_config, validation, field):
    payload = bound_dispatch(_dispatch_payload(bridge_config.worktree_root / 'task'))
    payload.pop(field)
    with pytest.raises((DispatchInvalid, PathInvalid)):
        validation(payload)


@pytest.mark.parametrize('block', [
    None, 'dictionary', 'policy', 'task', 'prompt', 'source', 'routing',
    'permissions', 'decision_receipt', 'runtime_contract',
])
def test_dictionary_v3_additional_properties_fail_closed(bridge_config, validation, block):
    payload = bound_dispatch(_dispatch_payload(bridge_config.worktree_root / 'task'))
    target = payload if block is None else payload[block]
    target['_unexpected'] = 'must-fail'
    with pytest.raises((DispatchInvalid, PathInvalid), match='unexpected field'):
        validation(payload)


@pytest.mark.parametrize('block,key,value', [
    (None, 'created_by', 'CODEX'),
    (None, 'created_at', '2026-10-14 08:45:00'),
    (None, 'created_at', '2026-10-14T08:45:00'),
    ('decision_receipt', 'dev_grant_ref', ''),
])
def test_dictionary_v3_metadata_constraints_fail_closed(bridge_config, validation, block, key, value):
    payload = bound_dispatch(_dispatch_payload(bridge_config.worktree_root / 'task'))
    target = payload if block is None else payload[block]
    target[key] = value
    with pytest.raises((DispatchInvalid, PathInvalid)):
        validation(payload)

