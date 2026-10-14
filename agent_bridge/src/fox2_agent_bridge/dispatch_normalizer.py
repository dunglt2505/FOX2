"""External dispatch shapes converge before common validation and execution."""
import re

from .agent_policy import ADAPTER_REGISTRY
from .errors import DispatchInvalid
from . import project_dictionary as registry


def _mapping(payload, key):
    value = payload.get(key)
    if not isinstance(value, dict):
        raise DispatchInvalid(f'{key} must be an object')
    return value


def _equal(payload, key, expected):
    value = payload.get(key)
    if type(value) is not type(expected) or value != expected:
        raise DispatchInvalid(f'{key} mismatch; expected {expected}')


def _hash(payload, key, size):
    value = payload.get(key)
    if not isinstance(value, str) or not re.fullmatch(f'[0-9a-f]{{{size}}}', value):
        raise DispatchInvalid(f'{key} must be a {size}-char immutable hash')


def _strings(payload, key):
    value = payload.get(key)
    if (not isinstance(value, list) or
            not all(isinstance(item, str) and item.strip() for item in value) or
            len(value) != len(set(value))):
        raise DispatchInvalid(f'{key} must be a unique non-empty string list')


def _bound_identity(payload, path_key, commit_key):
    _hash(payload, commit_key, 40)
    _hash(payload, 'sha256', 64)
    path = payload.get(path_key)
    if (not isinstance(path, str) or '\\' in path or
            not path.startswith('docs/') or any(part in {'', '.', '..'} for part in path.split('/'))):
        raise DispatchInvalid(f'{path_key} must be a repository document path')


def normalize_dispatch(external: dict, control_branch: str) -> dict:
    schema = external.get('schema_version')
    if not isinstance(schema, str) or schema not in registry.SUPPORTED_DISPATCH_SCHEMAS:
        raise DispatchInvalid('unsupported dispatch schema_version')
    if schema == '0.6':
        return {**external, '_external_schema_version': schema}

    _equal(external, 'project', registry.PROJECT_ID)
    _equal(external, 'workspace_id', registry.WORKSPACE_ID)
    _equal(external, 'dispatch_action', 'EXECUTE_LOCAL_AGENT')
    _equal(external, 'max_runs', 1)
    execution_path = external.get('execution_path')
    if not isinstance(execution_path, str) or execution_path not in registry.IDENTIFIERS['execution_paths']:
        raise DispatchInvalid('unsupported execution_path')
    if execution_path != 'BRIDGE':
        raise DispatchInvalid('execution_path is not authorized for Bridge auto-execution')
    owner = external.get('delivery_owner')
    if not isinstance(owner, str) or owner not in registry.IDENTIFIERS['delivery_owners']:
        raise DispatchInvalid('delivery_owner is required')

    if schema == registry.CURRENT_DISPATCH_SCHEMA:
        dictionary = _mapping(external, 'dictionary')
        for key, expected in [('version', registry.DICTIONARY_VERSION),
                              ('git_path', registry.SOURCE_PATH),
                              ('sha256', registry.SOURCE_SHA256),
                              ('git_commit_sha', registry.SOURCE_COMMIT)]:
            _equal(dictionary, key, expected)
        if 'dictionary_id' in dictionary:
            _equal(dictionary, 'dictionary_id', registry.DICTIONARY_ID)

    policy = _mapping(external, 'policy')
    _bound_identity(policy, 'git_path', 'git_commit_sha')
    if schema == registry.CURRENT_DISPATCH_SCHEMA:
        _equal(policy, 'version', registry.CURRENT['policy']['version'])
        _equal(policy, 'git_path', registry.CURRENT['policy']['path'])
    else:
        # Legacy immutable records retain their own Policy binding.
        version = policy.get('version')
        if not isinstance(version, str) or not re.fullmatch(r'\d+\.\d+\.\d+', version):
            raise DispatchInvalid('invalid legacy policy version')
        _equal(policy, 'git_path', f'docs/governance/FOX2_POLICY_V{version}.md')

    task = _mapping(external, 'task')
    _bound_identity(task, 'path', 'commit_sha')
    if not re.fullmatch(r'docs/agent_handoff/.+/task\.md', task['path']):
        raise DispatchInvalid('task.path must be a bound handoff task.md')
    source = _mapping(external, 'source')
    _hash(source, 'commit_sha', 40)
    _equal(source, 'git_source_ready', 'YES')
    receipt = _mapping(external, 'decision_receipt')
    for key in ('policy_check', 'task_state_check', 'source_binding_check',
                'routing_r0_r7', 'assignment_check'):
        _equal(receipt, key, 'PASS')
    if receipt.get('material_capability_check') not in ('PASS', 'PASS_NON_MATERIAL_DEVIATION'):
        raise DispatchInvalid('material_capability_check must pass')
    _equal(receipt, 'execution_authorized', 'YES')
    _equal(receipt, 'code_allowed', 'YES')

    runtime = _mapping(external, 'runtime_contract')
    _equal(runtime, 'repo', registry.REPOSITORY)
    for key in ('required_capabilities', 'stop_conditions', 'allowed_code_paths', 'allowed_report_paths'):
        _strings(runtime, key)
    _strings(external, 'required_tests')
    if 'dev_shell_capabilities' in runtime:
        raise DispatchInvalid('legacy dev_shell_capabilities are not part of this dispatch shape')
    permissions = _mapping(external, 'permissions')
    for key, value in registry.PROTECTED_AUTHORITY_DEFAULTS.items():
        _equal(permissions, key, value)
    routing = _mapping(external, 'routing')
    for key in ('model_policy', 'permission_profile'):
        if key not in routing:
            raise DispatchInvalid(f'routing.{key} is required')
    product = external.get('target_agent')
    if not isinstance(product, str) or product not in registry.IDENTIFIERS['agent_products']:
        raise DispatchInvalid('target_agent mismatch')
    interface, adapter_path = ADAPTER_REGISTRY[product]
    agent = {key: routing[key] for key in ('model_policy', 'permission_profile', 'model',
                                         'auto_tier', 'reasoning_effort') if key in routing}
    agent.update(product=product, interface=interface)
    return {**external, '_external_schema_version': schema,
            '_dispatch_execution_path': execution_path, 'type': 'NORMAL_AGENT_DISPATCH',
            'repository': runtime['repo'], 'control_ref': f'refs/heads/{control_branch}',
            'agent': agent, 'execution_path': adapter_path,
            'permission_profile': routing['permission_profile'],
            **{key: runtime.get(key) for key in ('branch', 'worktree', 'base_sha',
                                               'allowed_code_paths', 'allowed_report_paths')}}
