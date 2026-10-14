"""Immutable selection validation and observational CLI capabilities."""
import json
import re
import subprocess
from pathlib import Path

from .errors import DispatchInvalid, AgentNotStarted


def validate_selection(agent: dict[str, object]) -> dict[str, object]:
    product = agent.get('product')
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
    return {**agent, 'model_policy': policy,
            **({'model': 'auto', 'auto_tier': tier} if policy == 'NATIVE_AUTO' else {})}


def help_text(executable: Path, *subcommand: str) -> str:
    try:
        result = subprocess.run([str(executable), *subcommand, '--help'],
                                capture_output=True, text=True, timeout=15, check=False)
        return result.stdout if result.returncode == 0 else ''
    except (OSError, subprocess.TimeoutExpired):
        return ''


def policy_arguments(selection: dict[str, object], help_output: str) -> tuple[list[str], dict[str, object]]:
    agent = validate_selection(selection)
    arguments = []
    metadata = {'requested': agent, 'observed_model': None, 'observed_reasoning_effort': None,
                'quota': 'NOT_EXPOSED'}
    model = agent.get('model')
    if model:
        if '--model' not in help_output:
            raise AgentNotStarted('installed exact Agent CLI does not expose requested model support')
        arguments += ['--model', str(model)]
    if agent.get('reasoning_effort'):
        if '--config' not in help_output and '-c' not in help_output:
            raise AgentNotStarted('installed Codex CLI does not expose reasoning configuration')
        arguments += ['-c', f'model_reasoning_effort="{agent["reasoning_effort"]}"']
    if agent['product'] == 'COPILOT':
        if '--no-ask-user' not in help_output:
            raise AgentNotStarted('installed Copilot CLI lacks required non-interactive support')
        arguments += ['--no-ask-user']
        if '--output-format' in help_output:
            arguments += ['--output-format', 'json']
        if agent['model_policy'] == 'NATIVE_AUTO':
            # No speculative tier flag or global settings mutation. Native Auto
            # remains usable when task-local tier enforcement is unproven.
            metadata['auto_tier_status'] = 'AUTO_TIER_NOT_ENFORCED'
        if agent.get('max_ai_credits') is not None:
            if '--max-ai-credits' not in help_output:
                raise AgentNotStarted('installed Copilot CLI cannot enforce explicit credit bound')
            arguments += ['--max-ai-credits', str(agent['max_ai_credits'])]
    return arguments, metadata


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
        for key, target in [('model', 'observed_model'), ('reasoning_effort', 'observed_reasoning_effort')]:
            value = event.get(key)
            if isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9._/-]{1,100}', value):
                metadata[target] = value
    return metadata
