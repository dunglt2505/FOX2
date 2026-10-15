"""Per-user offline installation, transactional updates and bounded support export.

Only version directories created from a verified package are removed. Durable
configuration, dispatch claims and results survive uninstall and reinstall.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

from .artifacts import write_json, write_text
from .paths import BRIDGE_ROOT
from .process_lock import ProcessLock
from . import project_dictionary as registry


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def safe_root(root: Path) -> Path:
    root = root.absolute()
    for item in (root, *root.parents):
        if item.is_symlink() or item.is_junction():
            raise ValueError('installation path contains a link or junction')
    if root.resolve() != BRIDGE_ROOT.resolve():
        raise ValueError('installation is restricted to the current-user Bridge directory')
    return root


def verified_package(package: Path, expected_sha256: str) -> tuple[dict, dict[str, bytes]]:
    if not re.fullmatch('[0-9a-fA-F]{64}', expected_sha256):
        raise ValueError('an independently supplied package SHA256 is required')
    raw = package.read_bytes()
    if digest(raw) != expected_sha256.lower():
        raise ValueError('package integrity mismatch')
    import io
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        entries = archive.infolist()
        if len(entries) > 500 or sum(i.file_size for i in entries) > 100_000_000:
            raise ValueError('package exceeds limits')
        files = {}
        for item in entries:
            name = item.filename
            path = PurePosixPath(name)
            if (path.is_absolute() or '\\' in name or ':' in name or
                    any(p in ('', '.', '..') for p in name.split('/')) or
                    name in files or (item.external_attr >> 16) & 0o170000 == 0o120000):
                raise ValueError('unsafe package member')
            files[name] = archive.read(item)
    manifest = json.loads(files.pop('manifest.json'))
    if (manifest.get('format') != 'FOX2_USER_PACKAGE_1' or
            manifest.get('dictionary_sha256') != registry.SOURCE_SHA256 or
            manifest.get('python') != f'{sys.version_info.major}.{sys.version_info.minor}' or
            manifest.get('platform') != sys.platform or
            manifest.get('files') != {n: digest(b) for n, b in files.items()}):
        raise ValueError('package manifest or runtime binding mismatch')
    for name in files:
        if not (name.startswith('wheels/') and name.endswith('.whl') or
                name.startswith('scripts/') and name.endswith('.ps1')):
            raise ValueError('unexpected package payload')
    return manifest, files


def installed_version(root: Path) -> dict | None:
    pointer = root / 'current.json'
    if not pointer.exists():
        return None
    current = json.loads(pointer.read_text(encoding='utf-8'))
    if not re.fullmatch('[0-9a-f]{64}', current.get('package_sha256', '')):
        raise ValueError('invalid installation pointer')
    return current


def _installation_environment() -> dict[str, str]:
    """Keep the caller's OS environment without inherited Python path settings."""
    return {name: value for name, value in os.environ.items()
            if name.upper() not in {'PYTHONPATH', 'PYTHONHOME'}}


def _run(arguments: list[str], *, timeout=180) -> subprocess.CompletedProcess:
    result = subprocess.run(arguments, capture_output=True, text=True, timeout=timeout,
                            env=_installation_environment(),
                            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    if result.returncode:
        # Never expose pip environment, auth configuration, or arbitrary subprocess output.
        raise ValueError('installation subprocess failed: ' + str(result.returncode))
    return result


def _version_path(root: Path, package_sha256: str) -> Path:
    if not re.fullmatch('[0-9a-f]{64}', package_sha256):
        raise ValueError('invalid package identity')
    path = root / 'versions' / package_sha256
    for item in (root / 'versions', path):
        if item.is_symlink() or item.is_junction():
            raise ValueError('version directory cannot be a link')
    return path


def install(package: Path, expected_sha256: str, *, root: Path = BRIDGE_ROOT) -> dict:
    root = safe_root(root)
    manifest, files = verified_package(package, expected_sha256)
    identity = expected_sha256.lower()
    root.mkdir(parents=True, exist_ok=True)
    with ProcessLock(root / 'data' / 'install.lock'), ProcessLock(root / 'data' / 'bridge.lock'):
        previous = installed_version(root)
        target = _version_path(root, identity)
        if previous and previous['package_sha256'] == identity and target.exists():
            return {'status': 'ALREADY_INSTALLED', **previous}
        if target.exists():
            raise ValueError('unreferenced version requires explicit reconciliation')
        target.mkdir(parents=True)
        try:
            payload = target / 'payload'
            for name, raw in files.items():
                path = payload / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
            runtime = target / 'runtime'
            _run([sys.executable, '-m', 'venv', str(runtime)])
            python = runtime / 'Scripts' / 'python.exe'
            wheelhouse = payload / 'wheels'
            wheels = list(wheelhouse.glob('fox2_agent_bridge-*.whl'))
            if len(wheels) != 1:
                raise ValueError('package must contain exactly one Bridge wheel')
            _run([str(python), '-m', 'pip', '--isolated', 'install', '--disable-pip-version-check',
                  '--no-index', '--only-binary=:all:', '--find-links', str(wheelhouse), str(wheels[0])])
            proof = _run([str(python), '-I', '-c',
                          'import fox2_agent_bridge.project_dictionary as r; '
                          'import fox2_agent_bridge.dispatch_schema_v3_contract; '
                          'import jsonschema; print(r.SOURCE_SHA256)'])
            if proof.stdout.strip() != registry.SOURCE_SHA256:
                raise ValueError('installed runtime dictionary mismatch')
            write_json(target / 'receipt.json', {'package_sha256': identity, 'manifest': manifest})
            # Stable launcher resolves the atomic pointer after every upgrade.
            write_text(root / 'launch.ps1', LAUNCHER)
            # The uninstall supervisor must never execute a version's Python.
            base_python = Path(sys._base_executable).resolve()
            if base_python.is_relative_to((root / 'versions').resolve()) or not base_python.is_file():
                raise ValueError('uninstall requires an external base interpreter')
            write_text(root / 'uninstall.py', UNINSTALL_BOOTSTRAP)
            write_text(root / 'uninstall.ps1', UNINSTALL_LAUNCHER.replace(
                '__BASE_PYTHON__', str(base_python).replace("'", "''")))
            current = {'package_sha256': identity, 'source_sha256': manifest['source_sha256']}
            write_json(root / 'current.json', current)
            return {'status': 'UPDATED' if previous else 'INSTALLED', **current}
        except BaseException:
            # Target was created by this call, inside the fixed owned versions directory.
            if target.resolve().parent != (root / 'versions').resolve():
                raise ValueError('unsafe rollback path')
            shutil.rmtree(target)
            raise


LAUNCHER = r'''param()
$ErrorActionPreference = 'Stop'
$Current = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'current.json') -Raw | ConvertFrom-Json
if ($Current.package_sha256 -notmatch '^[0-9a-f]{64}$') { throw 'Invalid Bridge installation' }
$Tray = Join-Path $PSScriptRoot ('versions/' + $Current.package_sha256 + '/payload/scripts/desktop_launcher.ps1')
& $Tray
'''


UNINSTALL_LAUNCHER = r'''param()
$ErrorActionPreference = 'Stop'
# A stable, synchronous supervisor outside versions; no installed Python parent.
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONHOME -ErrorAction SilentlyContinue
& '__BASE_PYTHON__' -I -B (Join-Path $PSScriptRoot 'uninstall.py')
exit $LASTEXITCODE
'''


UNINSTALL_BOOTSTRAP = '''"""Stable external uninstall entry point. No arbitrary arguments or import paths."""
import json
import os
from pathlib import Path
import re
import sys

try:
    if len(sys.argv) != 1:
        raise ValueError('uninstall bootstrap accepts no arguments')
    root = Path(__file__).absolute().parent
    for item in (root, *root.parents):
        if item.is_symlink() or item.is_junction():
            raise ValueError('uninstall bootstrap path contains a link')
    versions = root / 'versions'
    if Path(sys.executable).resolve().is_relative_to(versions.resolve()):
        raise ValueError('uninstall bootstrap requires an external interpreter')
    current = json.loads((root / 'current.json').read_text(encoding='utf-8'))
    identity = current.get('package_sha256', '')
    if not re.fullmatch('[0-9a-f]{64}', identity):
        raise ValueError('invalid installation pointer')
    version = versions / identity
    for item in (versions, version, version / 'runtime', version / 'runtime/Lib',
                 version / 'runtime/Lib/site-packages'):
        if item.is_symlink() or item.is_junction():
            raise ValueError('uninstall import path contains a link')
    if not (version / 'receipt.json').is_file():
        raise ValueError('unowned version directory; uninstall stopped')
    os.chdir(root)
    sys.path.insert(0, str(version / 'runtime/Lib/site-packages'))
    from fox2_agent_bridge.__main__ import main
    raise SystemExit(main(['uninstall']))
except (ValueError, OSError, KeyError) as error:
    # No arbitrary subprocess output or configuration enters the error receipt.
    print(json.dumps({'status': 'ERROR', 'error': 'external uninstall bootstrap failed'}), file=sys.stderr)
    raise SystemExit(2)
'''


def first_run(*, root: Path = BRIDGE_ROOT) -> dict:
    root = safe_root(root)
    current = installed_version(root)
    if current is None:
        raise ValueError('install Bridge before setup')
    version = _version_path(root, current['package_sha256'])
    python = version / 'runtime/Scripts/python.exe'
    from .config import BridgeConfig, load_config, default_tool_paths
    from .desktop import initialize_runtime
    from .preexec.probes import resolve_tool
    config_path = root / 'config/bridge.toml'
    tools = default_tool_paths(root)
    tools['python'] = python
    for name in tools:
        found = resolve_tool(name)
        if found and not (tools[name] and tools[name].is_file()):
            tools[name] = Path(found)
    for required in ('git', 'codex', 'pwsh', 'python'):
        if not tools[required] or not tools[required].is_file():
            raise ValueError('setup requires tool: ' + required)
    auth = subprocess.run([str(tools['codex']), 'login', 'status'], capture_output=True, timeout=30)
    if auth.returncode:
        raise ValueError('sign in using the official Codex login flow before setup')
    from .paths import PROJECT_ROOT, WORKTREE_ROOT
    if not PROJECT_ROOT.is_dir() or not WORKTREE_ROOT.is_dir():
        raise ValueError('confirm the FOX2 repository and worktree locations before setup')
    remote = _run([str(tools['git']), '-C', str(PROJECT_ROOT), 'ls-remote', '--refs',
                   'origin', 'refs/heads/' + registry.CONTROL_BRANCH], timeout=30)
    if len(remote.stdout.strip().splitlines()) != 1:
        raise ValueError('configured FOX2 control branch is unavailable')
    if not config_path.exists():
        # Configuration is immutable to automatic upgrades; no credentials are stored.
        write_text(config_path, '[tools]\n' + '\n'.join(
            f'{name} = {json.dumps(str(path))}' for name, path in tools.items() if path and name != 'python'))
    config = load_config(config_path)
    ledger = initialize_runtime(config)
    # First-run starts paused until the user deliberately resumes dispatch intake.
    if not ledger.worker_state().get('setup_complete'):
        ledger.update_worker(setup_complete=True, paused=True)
    return {'status': 'SETUP_COMPLETE', 'paused': ledger.worker_state().get('paused', False),
            'configuration': str(config_path), 'dictionary_sha256': registry.SOURCE_SHA256,
            'stages': {'runtime':'PASS', 'repository':'PASS', 'worktrees':'PASS', 'git':'PASS',
                       'codex':'AUTHENTICATED', 'copilot':'OPTIONAL_NOT_SELECTED',
                       'dispatch':'READABLE', 'startup':'USER_OPT_IN', 'health':'PASS'}}


def uninstall(*, root: Path = BRIDGE_ROOT) -> dict:
    root = safe_root(root)
    if Path(sys.executable).resolve().is_relative_to((root / 'versions').resolve()):
        # Windows has no synchronous process overlay preserving the caller's
        # wait handle. Never spawn a deleting child and wait inside its target.
        raise ValueError('installed interpreter cannot uninstall itself; run the stable Bridge uninstall.ps1')
    from .config import load_config
    from .startup import set_start_with_windows
    with ProcessLock(root / 'data/install.lock'), ProcessLock(root / 'data/bridge.lock'):
        if (root / 'config/bridge.toml').exists():
            set_start_with_windows(load_config(root / 'config/bridge.toml'), False)
        versions = root / 'versions'
        if versions.exists():
            # Validate all targets before deleting any version.
            targets = list(versions.iterdir())
            for path in targets:
                _version_path(root, path.name)
                if not (path / 'receipt.json').is_file():
                    raise ValueError('unowned version directory; uninstall stopped')
                for child in path.rglob('*'):
                    if child.is_symlink() or child.is_junction():
                        raise ValueError('link in owned version; uninstall stopped')
            for path in targets:
                shutil.rmtree(path)
            if any(versions.iterdir()):
                raise ValueError('version deletion incomplete; uninstall stopped')
        for name in ('current.json', 'launch.ps1', 'uninstall.py', 'uninstall.ps1'):
            (root / name).unlink(missing_ok=True)
        if any((root / name).exists() for name in ('current.json', 'launch.ps1', 'uninstall.py', 'uninstall.ps1')):
            raise ValueError('installation artifact deletion incomplete; uninstall stopped')
    return {'status': 'UNINSTALLED', 'preserved': ['config', 'data', 'logs', 'reports'],
            'project_worktrees': 'UNTOUCHED'}


def diagnostics(output: Path, *, root: Path = BRIDGE_ROOT) -> dict:
    """Export a small whitelist, never raw config/logs/checkpoints/prompts or DB."""
    root = safe_root(root)
    from .ledger import SQLiteLedger
    ledger = SQLiteLedger(root / 'data/bridge.db')
    worker = ledger.worker_state()
    summary = {'format': 'FOX2_SUPPORT_1', 'installation': installed_version(root),
               'dictionary_version': registry.DICTIONARY_VERSION,
               'dictionary_sha256': registry.SOURCE_SHA256,
               'worker': {k: worker[k] for k in ('state', 'paused', 'heartbeat', 'setup_complete') if k in worker},
               'recent': [{k: row[k] for k in ('dispatch_id', 'dispatch_state', 'execution_state')}
                          for row in ledger.recent_status(limit=20)]}
    raw = (json.dumps(summary, sort_keys=True, indent=2) + '\n').encode()
    from .preexec.engine import secret_scan
    secret_scan(raw)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        info = zipfile.ZipInfo('support.json', date_time=(2026, 1, 1, 0, 0, 0))
        archive.writestr(info, raw)
    return {'status': 'EXPORTED', 'sha256': digest(output.read_bytes()), 'files': ['support.json']}
