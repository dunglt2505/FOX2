"""Install into a new isolated directory and rollback only unchanged owned files."""
import hashlib
import json
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def install(source, destination):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if destination.exists() or destination.is_relative_to(source):
        raise ValueError('Destination must be new and outside source package')
    files = [p for p in source.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc']
    expected = {p.relative_to(source).as_posix(): sha(p) for p in files}
    destination.mkdir(parents=True)
    for path, expected_hash in expected.items():
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((source / path).read_bytes())
        if sha(target) != expected_hash:
            raise RuntimeError('Installation readback failed')
    return {'status':'PACKAGE_BYTES_INSTALLED_HOST_INVOCATION_NOT_RUN', 'root':str(destination), 'files':expected}


def rollback(receipt):
    root = Path(receipt['root']).resolve()
    # Validate the entire receipt before deleting any file; preserve modified WIP.
    for path, expected in receipt['files'].items():
        target = (root / path).resolve()
        if not target.is_relative_to(root) or not target.is_file() or sha(target) != expected:
            raise ValueError('Rollback conflict; no files deleted')
    for path in receipt['files']:
        (root / path).unlink()
    return {'status':'OWNED_PACKAGE_FILES_REMOVED', 'root':str(root)}


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('action', choices=['install','rollback'])
    p.add_argument('--source')
    p.add_argument('--destination')
    p.add_argument('--receipt', required=True)
    a = p.parse_args()
    if a.action == 'install':
        result = install(a.source, a.destination)
        Path(a.receipt).write_text(json.dumps(result,indent=2), encoding='utf-8', newline='\n')
    else:
        result = rollback(json.loads(Path(a.receipt).read_text(encoding='utf-8')))
    print(json.dumps(result if a.action == 'rollback' else {'status':result['status'],'files':len(result['files'])}))
