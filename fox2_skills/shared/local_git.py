"""Read immutable bytes from a freshly authenticated Git fetch; no effectivity claim."""
import re
import subprocess
from .errors import SourceError


class LocalGit:
    def __init__(self, root):
        self.root, self.authenticated = root, False

    def refresh(self):
        self.authenticated = False
        # A public fetch alone does not prove authenticated access.
        subprocess.run(['gh', 'api', 'user', '--jq', '.login'], cwd=self.root,
                       check=True, capture_output=True, timeout=30)
        subprocess.run(['git', 'fetch', 'origin'], cwd=self.root, check=True,
                       capture_output=True, timeout=90)
        self.authenticated = True

    def read_file(self, path, commit):
        if not re.fullmatch('[a-f0-9]{40}', commit):
            raise SourceError('Immutable commit required')
        if not path or path.startswith(('/', '-')) or any(x in path for x in ['\\', ':']) or '..' in path.split('/'):
            raise SourceError('Unsafe Git path')
        return subprocess.check_output(['git', 'show', commit + ':' + path], cwd=self.root, timeout=20)
