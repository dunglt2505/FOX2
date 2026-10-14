"""Immutable selection validation and observational CLI capabilities."""
import json
import re
import subprocess
import math
from dataclasses import dataclass
from pathlib import Path

from .errors import DispatchInvalid, AgentNotStarted

ADAPTER_REGISTRY = {'CODEX': ('OPENAI_CODEX_CLI', 'BRIDGE_DIRECT_CODEX_CLI'),
                    'COPILOT': ('GITHUB_COPILOT_CLI', 'BRIDGE_DIRECT_COPILOT_CLI')}


@dataclass(frozen=True)
class ExecutionTuple:
    """Serialized once before launch; observations never change requested routing."""
    dispatch_id: str
    branch: str
    worktree: str
    prompt_sha256: str
    selection_json: str
    delivery_owner: str

    def as_dict(self):
        selection = json.loads(self.selection_json)
        route = ADAPTER_REGISTRY[selection['product']]
        return {'dispatch_id': self.dispatch_id, 'branch': self.branch, 'worktree': self.worktree,
                'prompt_sha256': self.prompt_sha256, 'selection': selection,
                'interface': route[0], 'execution_path': route[1], 'delivery_owner': self.delivery_owner}


def require_capabilities(help_output: str, required: tuple[str, ...]) -> None:
    missing = [flag for flag in required if not re.search(re.escape(flag) + r'(?![\w-])', help_output)]
    if missing:
        raise AgentNotStarted('material required CLI capabilities missing/unknown: ' + ', '.join(missing))


def tool_compatibility(version: str | None, expected_version: str | None,
                       help_output: str, required: tuple[str, ...]) -> dict[str, object]:
    require_capabilities(help_output, required)
    return {'status': 'PASS', 'version': version, 'expected_version': expected_version,
            'version_deviation': bool(expected_version and version != expected_version),
            'required_capabilities': list(required)}


def validate_selection(agent: dict[str, object]) -> dict[str, object]:
    product = agent.get('product')
    permission = agent.get('permission_profile', 'FULL_ACCESS')
    if permission != 'FULL_ACCESS':
        raise DispatchInvalid('exact requested permission_profile must be FULL_ACCESS; no downgrade')
    if product == 'CODEX' and (agent.get('sandbox', 'danger-full-access') != 'danger-full-access'
                               or agent.get('approval_policy', 'never') != 'never'):
        raise DispatchInvalid('CODEX Full Access sandbox/approval mismatch')
    policy = agent.get('model_policy', 'CURRENT_CONFIG' if product == 'CODEX' else 'NATIVE_AUTO')
    allowed = {'CODEX': {'PINNED', 'CURRENT_CONFIG', 'PINNED_PREFERRED'},
               'COPILOT': {'NATIVE_AUTO', 'PINNED'}}
    if not isinstance(product, str) or product not in allowed or not isinstance(policy, str) or policy not in allowed[product]:
        raise DispatchInvalid('unsupported exact Agent/model policy')
    model = agent.get('model')
    if model is not None and (not isinstance(model, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._/-]*', model)):
        raise DispatchInvalid('model must be a plain model identifier')
    if policy in {'PINNED', 'PINNED_PREFERRED'} and not model:
        raise DispatchInvalid('pinned model is required')
    if policy in {'PINNED', 'PINNED_PREFERRED'} and model == 'auto':
        raise DispatchInvalid('pinned model must not request native Auto')
    if policy == 'CURRENT_CONFIG' and model is not None:
        raise DispatchInvalid('CURRENT_CONFIG must not request a model override')
    effort = agent.get('reasoning_effort')
    if effort is not None and (not isinstance(effort, str) or product != 'CODEX' or effort not in {'low', 'medium', 'high'}):
        raise DispatchInvalid('unsupported reasoning_effort')
    tier = agent.get('auto_tier', 'balance')
    if not isinstance(tier, str) or tier not in {'efficiency', 'balance', 'intelligence'}:
        raise DispatchInvalid('unsupported auto_tier')
    if policy == 'NATIVE_AUTO' and model not in {None, 'auto'}:
        raise DispatchInvalid('native Auto requires model auto')
    credits = agent.get('max_ai_credits')
    if credits is not None and (product != 'COPILOT' or isinstance(credits, bool)
                                or not isinstance(credits, (int, float)) or not 0 < credits < 1000000):
        raise DispatchInvalid('max_ai_credits must be an explicit positive finite bound')
    return {**agent, 'model_policy': policy, 'permission_profile': permission,
            **({'model': 'auto', 'auto_tier': tier} if policy == 'NATIVE_AUTO' else {})}


def help_text(executable: Path, *subcommand: str) -> str:
    try:
        result = subprocess.run([str(executable), *subcommand, '--help'],
                                capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=15, check=False)
        return result.stdout if result.returncode == 0 else ''
    except (OSError, subprocess.TimeoutExpired):
        return ''


def version_text(executable: Path) -> str | None:
    try:
        result = subprocess.run([str(executable), '--version'], capture_output=True, text=True,
                                encoding='utf-8', errors='replace', timeout=15, check=False)
        output = result.stdout.strip() or result.stderr.strip()
        return output.splitlines()[0][:200] if result.returncode == 0 and output else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def policy_arguments(selection: dict[str, object], help_output: str) -> tuple[list[str], dict[str, object]]:
    agent = validate_selection(selection)
    arguments = []
    metadata = {'requested': agent, 'observed_model': None, 'observed_reasoning_effort': None,
                'observed_permission_profile': None, 'observed_auto_tier': None,
                'usage': None, 'capacity': None, 'quota': 'NOT_EXPOSED',
                'observation_source': 'STRUCTURED_CLI_ONLY'}
    model = agent.get('model')
    if model:
        require_capabilities(help_output, ('--model',))
        arguments += ['--model', str(model)]
    if agent.get('reasoning_effort'):
        require_capabilities(help_output, ('--config',))
        arguments += ['-c', f'model_reasoning_effort="{agent["reasoning_effort"]}"']
    if agent['product'] == 'COPILOT':
        require_capabilities(help_output, ('--no-ask-user',))
        arguments += ['--no-ask-user']
        if '--output-format' in help_output:
            arguments += ['--output-format', 'json']
        if agent['model_policy'] == 'NATIVE_AUTO':
            require_capabilities(help_output, ('--auto-tier',))
            arguments += ['--auto-tier', str(agent['auto_tier'])]
            metadata['auto_tier_status'] = 'APPLIED_TASK_LOCAL'
        if agent.get('max_ai_credits') is not None:
            require_capabilities(help_output, ('--max-ai-credits',))
            arguments += ['--max-ai-credits', str(agent['max_ai_credits'])]
    return arguments, metadata


def permission_arguments(selection: dict[str, object], help_output: str) -> tuple[list[str], dict[str, object]]:
    agent = validate_selection(selection)
    if agent['product'] == 'CODEX':
        require_capabilities(help_output, ('--sandbox', 'danger-full-access', '--ask-for-approval', 'never'))
        return ['--ask-for-approval', 'never'], {'profile': 'FULL_ACCESS', 'sandbox': 'danger-full-access',
                                                 'approval_policy': 'never', 'status': 'APPLIED'}
    require_capabilities(help_output, ('--allow-all-tools', '--allow-all-paths', '--allow-all-urls'))
    return ['--allow-all-tools', '--allow-all-paths', '--allow-all-urls'], {'profile': 'FULL_ACCESS', 'status': 'APPLIED'}


def configuration_mismatch(metadata: dict[str, object]) -> bool:
    requested = metadata.get('requested') or {}
    for observed, requested_key in [('observed_permission_profile', 'permission_profile'),
                                    ('observed_reasoning_effort', 'reasoning_effort'),
                                    ('observed_auto_tier', 'auto_tier')]:
        if requested.get(requested_key) is not None and metadata.get(observed) is not None and metadata[observed] != requested.get(requested_key):
            return True
    return bool(requested.get('model_policy') in {'PINNED', 'PINNED_PREFERRED'} and
                metadata.get('observed_model') is not None and metadata['observed_model'] != requested.get('model'))


def observe_metadata(metadata: dict[str, object], stdout: str) -> dict[str, object]:
    # Only explicit structured CLI fields count as observations. Requested values
    # are never copied into actual fields and text/model guesses are not evidence.
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except (ValueError, TypeError):
            continue
        if not isinstance(event, dict):
            continue
        # Configuration/usage events are explicit; ordinary response text is not parsed.
        for key, target in [('model', 'observed_model'), ('reasoning_effort', 'observed_reasoning_effort'),
                            ('permission_profile', 'observed_permission_profile'), ('auto_tier', 'observed_auto_tier')]:
            value = event.get(key)
            if isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9._/-]{1,100}', value):
                metadata[target] = value
        usage = event.get('usage')
        if isinstance(usage, dict):
            accepted = {key: value for key, value in usage.items()
                        if key in {'input_tokens', 'output_tokens', 'cached_input_tokens', 'total_tokens',
                                   'ai_credits', 'premium_requests', 'cost_usd'}
                        and not isinstance(value, bool) and isinstance(value, (int, float))
                        and math.isfinite(value) and value >= 0}
            if accepted:
                metadata['usage'] = {**(metadata.get('usage') or {}), **accepted}
        capacity = event.get('capacity')
        if isinstance(capacity, dict):
            accepted = {key: value for key, value in capacity.items()
                        if key in {'remaining', 'limit', 'reset_at', 'status'}
                        and ((isinstance(value, (int, float)) and not isinstance(value, bool)
                              and math.isfinite(value) and value >= 0)
                             or (isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9:._+/-]{1,100}', value)))}
            if accepted:
                metadata['capacity'] = accepted
                metadata['quota'] = 'EXPOSED'
                if accepted.get('status') in {'exhausted', 'unavailable', 'blocked'}:
                    metadata['post_start_failure'] = 'capacity_unavailable'
        failure = event.get('error')
        code = failure.get('code') if isinstance(failure, dict) else event.get('code')
        if code in {'quota_exceeded', 'rate_limit_exceeded', 'capacity_unavailable',
                    'authentication_error', 'unauthorized', 'insufficient_quota'}:
            metadata['post_start_failure'] = code
        elif event.get('type') == 'error':
            metadata['post_start_failure'] = 'structured_cli_error'
    return metadata
