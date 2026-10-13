"""Test-only Python 3.13 Windows temporary-directory compatibility.

Windows mode 0700 replaces inherited ACLs, denying the managed sandbox token.
Use normal inherited permissions for pytest temporary directories. This does
not modify existing permissions or change the sandbox's write authorization.
Load explicitly as a pytest plugin for this environment.
"""
import os

_mkdir = os.mkdir


def pytest_load_initial_conftests(early_config, parser, args):
    def mkdir(path, mode=0o777, *, dir_fd=None):
        if os.name == 'nt' and mode == 0o700:
            mode = 0o755
        return _mkdir(path, mode, dir_fd=dir_fd)
    os.mkdir = mkdir
