"""Stable interactive Desktop launch and non-granting F1 service observation.

The fixed installed runtime alone may enter here. Presentation never starts or
owns the Worker. Standard handles are DEVNULL so callers can finish immediately.
"""
from __future__ import annotations
import os
from pathlib import Path
import subprocess
import sys

from .installation import installed_version, safe_root, _version_path
from .paths import BRIDGE_ROOT


def launch() -> dict:
    root = safe_root(BRIDGE_ROOT)
    current = installed_version(root)
    if current is None:
        raise ValueError('installed Bridge is required')
    version = _version_path(root, current['package_sha256'])
    python = version / 'runtime/Scripts/python.exe'
    if Path(sys.executable).resolve() != python.resolve() or not python.is_file():
        raise ValueError('launcher requires the current installed interpreter')
    environment = {k: v for k, v in os.environ.items() if k.upper() not in {'PYTHONPATH', 'PYTHONHOME'}}
    def spawn(arguments):
        return subprocess.Popen(arguments, cwd=root, env=environment, stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0), close_fds=True)
    from .f1_client import inspect_authority
    authority = inspect_authority()
    desktop = version / 'payload/desktop/FOX2.Bridge.Desktop.exe'
    ui = None
    try:
        for path in (version / 'payload', desktop.parent, desktop):
            if path.is_symlink() or path.is_junction(): raise ValueError('linked Desktop payload')
        if not desktop.is_file(): raise ValueError('Desktop payload is unavailable')
        ui = spawn([str(desktop)])
    except (ValueError, OSError):
        pass
    return {'worker_started': False, 'desktop_started': ui is not None,
            'f1_authority': authority,
            'package_sha256': current['package_sha256']}


if __name__ == '__main__':
    import json
    if len(sys.argv) != 1:
        raise SystemExit('launcher accepts no arguments')
    print(json.dumps(launch(), sort_keys=True))
