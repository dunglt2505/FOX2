"""Bounded minimal execution probes; no implementation prompts or raw evidence."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from ..agent_policy import validate_selection, observe_metadata, configuration_mismatch

MARKER = 'FOX2_PREFLIGHT_OK'
PROMPT = 'Reply exactly FOX2_PREFLIGHT_OK. Do not read or write files. Do not run tools.'


def observation(status='PASS', *, material=True, failure=None, code=0):
    return {'status': status, 'material': material, 'exit_code': code,
            'failure_class': failure, 'evidence': 'Bounded readiness observation; raw output omitted.'}


def classify(text: str, code: int, marker: bool) -> str:
    for pattern, label in [
        (r'auth|login|sign.?in|unauthorized|forbidden|credential', 'AUTH_REQUIRED'),
        (r'quota|rate.?limit|capacity|exhaust|insufficient|credit', 'CAPACITY_OR_QUOTA'),
        (r'unknown model|unsupported model|invalid.*model|reasoning', 'MODEL_OR_CONFIG_UNSUPPORTED'),
        (r'sandbox|approval|permission|unknown option|unrecognized option|unexpected argument', 'PERMISSION_OR_CLI_ARGS'),
    ]:
        if re.search(pattern, text, re.I):
            return label
    return 'RESPONSE_MARKER_MISSING' if code == 0 and not marker else 'CLI_NONZERO'


def resolve_tool(name: str) -> str | None:
    tool = shutil.which(name)
    if tool:
        return tool
    if os.name == 'nt' and name in {'node', 'npm', 'npx'}:
        path = Path(os.environ.get('ProgramFiles', 'C:/Program Files')) / 'nodejs' / (name + ('.exe' if name == 'node' else '.cmd'))
        if path.is_file():
            return str(path)
    return None


def run_tool(arguments, *, cwd, timeout=30, input=None):
    # .cmd tools need cmd.exe on Windows; list2cmdline quotes fixed arguments.
    if os.name == 'nt' and str(arguments[0]).lower().endswith(('.cmd', '.bat')):
        arguments = [os.environ.get('COMSPEC', 'cmd.exe'), '/d', '/s', '/c', subprocess.list2cmdline(arguments)]
    return subprocess.run(arguments, cwd=cwd, input=input, capture_output=True,
                          text=True, encoding='utf-8', errors='replace', timeout=timeout)


def tool_probe(name: str, worktree: Path):
    tool = resolve_tool(name)
    if not tool:
        return observation('MISSING', failure='TOOL_MISSING', code=None)
    args = [tool, '--version']
    if name == 'pwsh':
        args = [tool, '-NoLogo', '-NoProfile', '-Command', '$PSVersionTable.PSVersion.ToString()']
    if name == 'schtasks.exe':
        args = [tool, '/query', '/fo', 'CSV', '/nh']
    try:
        result = run_tool(args, cwd=worktree)
        return observation('PASS' if result.returncode == 0 else 'FAIL',
                           failure=None if result.returncode == 0 else 'TOOL_UNAVAILABLE', code=result.returncode)
    except (OSError, subprocess.TimeoutExpired):
        return observation('UNKNOWN', failure='TOOL_PROBE_FAILED', code=None)


def dotnet_wpf_build(worktree):
    """Prove that the installed .NET SDK can compile a minimal net8.0-windows WPF app."""
    tool = resolve_tool('dotnet')
    if not tool:
        return observation('MISSING', failure='TOOL_MISSING', code=None)
    if os.name != 'nt':
        return observation('FAIL', failure='WINDOWS_WPF_REQUIRED', code=None)
    try:
        with tempfile.TemporaryDirectory(prefix='fox2-wpf-preexec-') as directory:
            root = Path(directory)
            files = {
                'Probe.csproj': (
                    '<Project Sdk="Microsoft.NET.Sdk">\n'
                    '  <PropertyGroup>\n'
                    '    <OutputType>WinExe</OutputType>\n'
                    '    <TargetFramework>net8.0-windows</TargetFramework>\n'
                    '    <UseWPF>true</UseWPF>\n'
                    '    <Nullable>enable</Nullable>\n'
                    '    <ImplicitUsings>enable</ImplicitUsings>\n'
                    '    <RestoreIgnoreFailedSources>true</RestoreIgnoreFailedSources>\n'
                    '  </PropertyGroup>\n'
                    '</Project>\n'
                ),
                'App.xaml': (
                    '<Application x:Class="Probe.App" '
                    'xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" '
                    'xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml" '
                    'StartupUri="MainWindow.xaml"/>\n'
                ),
                'App.xaml.cs': (
                    'using System.Windows;\n'
                    'namespace Probe;\n'
                    'public partial class App : Application { }\n'
                ),
                'MainWindow.xaml': (
                    '<Window x:Class="Probe.MainWindow" '
                    'xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" '
                    'xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml" '
                    'Title="Probe"><Grid/></Window>\n'
                ),
                'MainWindow.xaml.cs': (
                    'using System.Windows;\n'
                    'namespace Probe;\n'
                    'public partial class MainWindow : Window { '
                    'public MainWindow() { InitializeComponent(); } }\n'
                ),
            }
            for name, content in files.items():
                (root / name).write_bytes(content.encode('utf-8'))
            project = root / 'Probe.csproj'
            result = run_tool(
                [tool, 'build', str(project), '-c', 'Release', '--nologo',
                 '--verbosity', 'quiet', '-p:RestoreIgnoreFailedSources=true'],
                cwd=root,
                timeout=90,
            )
            return observation(
                'PASS' if result.returncode == 0 else 'FAIL',
                failure=None if result.returncode == 0 else 'WPF_BUILD_UNAVAILABLE',
                code=result.returncode,
            )
    except subprocess.TimeoutExpired:
        return observation('UNKNOWN', failure='WPF_BUILD_PROBE_TIMEOUT', code=None)
    except (OSError, ValueError, TypeError):
        return observation('FAIL', failure='WPF_BUILD_PROBE_FAILED', code=None)


def npm_registry(worktree):
    tool = resolve_tool('npm')
    if not tool:
        return observation('NOT_RUN', failure='TOOL_MISSING', code=None)
    try:
        result = run_tool([tool, 'ping', '--silent'], cwd=worktree)
        return observation('PASS' if result.returncode == 0 else 'FAIL',
                           failure=None if result.returncode == 0 else 'NPM_REGISTRY_UNAVAILABLE', code=result.returncode)
    except (OSError, subprocess.TimeoutExpired):
        return observation('UNKNOWN', failure='NPM_REGISTRY_UNKNOWN', code=None)


def local_appdata(worktree):
    root = os.environ.get('LOCALAPPDATA')
    if not root or not Path(root).is_dir():
        return observation('MISSING', failure='LOCALAPPDATA_UNAVAILABLE', code=None)
    try:
        with tempfile.TemporaryFile(dir=root) as stream:
            stream.write(b'FOX2\n')
        return observation()
    except OSError:
        return observation('FAIL', failure='LOCALAPPDATA_NOT_WRITABLE', code=None)


def proof_marker(product, stdout):
    """Only assistant response events count, never echoed prompts or tool events."""
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict):
            continue
        if product == 'CODEX':
            item = event.get('item', {})
            if event.get('type') == 'item.completed' and item.get('type') == 'agent_message' and item.get('text', '').strip() == MARKER:
                return True
        elif event.get('type') == 'assistant.message' and event.get('data', {}).get('content', '').strip() == MARKER:
            return True
    return False


def agent_probe(route, worktree):
    route = validate_selection(route)
    product = route['product']
    tool = resolve_tool(product.lower())
    if not tool:
        return observation('MISSING', material=False, failure='TOOL_MISSING', code=None)
    if product == 'CODEX':
        args = [tool, '--ask-for-approval', 'never', 'exec', '--sandbox', 'danger-full-access', '--json']
        if route.get('model'):
            args += ['--model', route['model']]
        if route.get('reasoning_effort'):
            args += ['-c', f'model_reasoning_effort="{route["reasoning_effort"]}"']
        args += ['-']
        prompt = PROMPT
    else:
        args = [tool, '-C', str(worktree), '--prompt', PROMPT, '--allow-all-tools', '--allow-all-paths',
                '--allow-all-urls', '--model', route['model'], '--no-ask-user', '--output-format', 'json']
        if route.get('auto_tier'):
            args += ['--auto-tier', route['auto_tier']]
        prompt = None
    try:
        result = run_tool(args, cwd=worktree, timeout=60, input=prompt)
        metadata = observe_metadata({'requested': route}, result.stdout)
        if configuration_mismatch(metadata):
            return observation('FAIL', material=False, code=result.returncode,
                               failure='AGENT_CONFIGURATION_MISMATCH')
        if metadata.get('post_start_failure'):
            return observation('FAIL', material=False, code=result.returncode,
                               failure=classify(metadata['post_start_failure'], 1, False))
        marker = proof_marker(product, result.stdout)
        passed = result.returncode == 0 and marker
        return observation('PASS' if passed else 'FAIL', material=False, code=result.returncode,
                           failure=None if passed else classify(result.stdout + result.stderr, result.returncode, marker))
    except subprocess.TimeoutExpired:
        return observation('UNKNOWN', material=False, failure='PROBE_TIMEOUT', code=None)
    except OSError:
        return observation('FAIL', material=False, failure='TOOL_UNAVAILABLE', code=None)
