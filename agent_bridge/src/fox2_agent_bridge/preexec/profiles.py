"""Task-specific registrations only; lifecycle belongs to the shared engine."""
from functools import partial
from .probes import tool_probe, npm_registry, local_appdata

ROUTES = (
    {'product': 'COPILOT', 'model_policy': 'NATIVE_AUTO', 'model': 'auto', 'auto_tier': 'balance',
     'reasoning_effort': None, 'permission_profile': 'FULL_ACCESS'},
    {'product': 'CODEX', 'model_policy': 'PINNED', 'model': 'gpt-6.1-sol', 'auto_tier': None,
     'reasoning_effort': 'medium', 'permission_profile': 'FULL_ACCESS'},
)


def checks(profile):
    tools = {'app': ('git', 'python', 'pwsh', 'node', 'npm', 'npx'),
             'bridge': ('git', 'python', 'pwsh', 'schtasks.exe'),
             'rollout': ('git', 'python', 'pwsh')}[profile]
    result = {name: partial(tool_probe, name) for name in tools}
    if profile == 'app':
        result['npm_registry'] = npm_registry
    if profile == 'bridge':
        result['local_appdata_per_user_write'] = local_appdata
    return result


def identity(profile):
    wp = {'app': 'FOX2-M1-A-APP-BATCH-B', 'bridge': 'FOX2-BRIDGE-DESKTOP-BATCH-B',
          'rollout': 'FOX2-PREEXEC-ROLLOUT-V1'}[profile]
    report = 'BRIDGE-DESKTOP-BATCH-B' if profile == 'bridge' else wp
    return wp, 'work/' + wp, f'docs/agent_handoff/{wp}/task.md', f'reports/{report}/preexec/local_preflight.json'
