"""Current-user Desktop logon task. F1 service lifecycle is independent."""
from pathlib import Path
import subprocess

from .config import BridgeConfig
from .errors import ToolExecFailed
from .ledger import SQLiteLedger


def startup_command(config: BridgeConfig, enabled: bool) -> list[str]:
    scripts = Path(__file__).resolve().parents[2] / 'scripts'
    if not scripts.is_dir():
        scripts = Path(__file__).resolve().parent / 'resources'
    return [str((config.tool_paths or {})['pwsh']), '-NoProfile', '-NonInteractive',
            '-File', str(scripts / 'desktop_startup.ps1'),
            '-Enabled', 'true' if enabled else 'false']


def set_start_with_windows(config: BridgeConfig, enabled: bool) -> dict[str, object]:
    result = subprocess.run(startup_command(config, enabled), capture_output=True,
                            text=True, timeout=30, check=False,
                            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    if result.returncode:
        raise ToolExecFailed('per-user startup registration failed; no alternate privilege path')
    from .desktop import initialize_runtime
    ledger = initialize_runtime(config)
    ledger.update_worker(start_with_windows=enabled)
    return {'start_with_windows': enabled, 'scope': 'CURRENT_USER_LOGON_LIMITED'}
