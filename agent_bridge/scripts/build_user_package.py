"""Produce a deterministic offline Windows package using an isolated build Python.

Requires an already provisioned build venv; never modifies the host environment.
Dependencies are downloaded as wheels at the exact versions in that environment.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def run(args, **kwargs):
    result = subprocess.run([str(a) for a in args], capture_output=True, text=True, **kwargs)
    if result.returncode:
        raise RuntimeError('packaging command failed: ' + result.stderr[-1200:])
    return result.stdout


def inspect_build_environment(python: Path) -> dict:
    """Resolve ALL package versions in the exact isolated build interpreter.

    Never obtain runtime wheel pins from the CHAT/host interpreter: that can
    silently mix two environments and break offline package provenance.
    """
    script = (
        'import sys,importlib.metadata as m,json; '
        'names=("jsonschema","attrs","referencing","rpds-py","jsonschema-specifications"); '
        'print(json.dumps(dict(isolated=sys.prefix!=sys.base_prefix, '
        'python=f"{sys.version_info.major}.{sys.version_info.minor}",platform=sys.platform, '
        'setuptools=m.version("setuptools"),wheel=m.version("wheel"),'
        'dependencies={name:m.version(name) for name in names})))'
    )
    check = json.loads(run([python, '-I', '-c', script]))
    expected = {'jsonschema', 'attrs', 'referencing', 'rpds-py',
                'jsonschema-specifications'}
    versions = check.get('dependencies')
    interpreter = check.get('python')
    platform = check.get('platform')
    if (not isinstance(interpreter, str) or
            not isinstance(platform, str) or not platform or
            not re.fullmatch(r'3\.\d+', interpreter) or
            not check.get('isolated') or
            not 80 <= int(check['setuptools'].split('.')[0]) < 90 or
            not isinstance(versions, dict) or set(versions) != expected or
            any(not isinstance(value, str) or not value for value in versions.values())):
        raise ValueError('a complete isolated setuptools >=80,<90 build environment is required')
    return check


def source_git_commit() -> str:
    """Bind package provenance to a clean, checked-out Git source."""
    import re
    repository = ROOT.parent

    def git(*args: str):
        return subprocess.run(
            ['git', '-C', str(repository), *args],
            capture_output=True, text=True, check=False,
        )

    identity = git('rev-parse', '--verify', 'HEAD')
    if identity.returncode or not re.fullmatch(r'[0-9a-f]{40}', identity.stdout.strip()):
        raise ValueError('an immutable Git source commit is required to package Bridge')

    status = git('status', '--porcelain', '--untracked-files=all', '--',
                 'agent_bridge/src', 'agent_bridge/scripts', 'agent_bridge/desktop_app')
    if status.returncode:
        raise ValueError('cannot verify package source worktree')
    # These are excluded from packaged Python sources / WPF source inventory.
    excluded = ('/__pycache__/', '/.pytest_cache/', '/bin/', '/obj/',
                '/publish/', '/build/', '/dist/', '/.venv/', '/.build-venv/')
    for line in status.stdout.splitlines():
        path = line[3:].replace('\\', '/')
        if any(item in path for item in excluded) or path.endswith(('.pyc', '.pyo')):
            continue
        if '.egg-info/' in path:
            continue
        raise ValueError('package source worktree has uncommitted code')
    return identity.stdout.strip()



def verify_wheel_source_modules(wheel: Path, source: Path) -> dict[str, str]:
    """Ensure the actual wheel carries exactly the staged Python module bytes.

    This is a build-time integrity consistency check, NOT proof that an old
    Windows executor is retired or permission to enable dispatch claims.
    """
    package_root = source / 'src' / 'fox2_agent_bridge'
    modules = {
        p.relative_to(package_root).as_posix(): p
        for p in sorted(package_root.rglob('*.py'))
        if p.is_file()
    }
    if not {'ledger.py', 'desktop.py', '__init__.py'} <= modules.keys():
        raise ValueError('mandatory Bridge modules are absent from build source')

    result = {}
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        for relative, path in modules.items():
            member = 'fox2_agent_bridge/' + relative
            if names.count(member) != 1:
                raise ValueError('missing or duplicated Bridge wheel module')
            raw = path.read_bytes()
            if archive.read(member) != raw:
                raise ValueError('Bridge wheel module differs from build source')
            result[member] = hashlib.sha256(raw).hexdigest()
    return result



def build(output: Path, python: Path) -> dict:
    check = inspect_build_environment(python)
    with tempfile.TemporaryDirectory(prefix='fox2-package-') as td:
        stage = Path(td)
        source = stage / 'source'
        shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns(
            '.venv', '.build-venv', '__pycache__', '*.pyc', '*.egg-info', 'build', 'dist', '.pytest_cache', 'reports', 'test_artifacts', 'bin', 'obj', 'publish'))
        resources = source / 'src/fox2_agent_bridge/resources'
        resources.mkdir()
        scripts = {p.name: p.read_bytes() for p in (ROOT/'scripts').glob('desktop_*.ps1')}
        for name, raw in scripts.items():
            (resources/name).write_bytes(raw)
        wheels = stage / 'wheels'
        wheels.mkdir()
        env = {**os.environ, 'SOURCE_DATE_EPOCH': '1767225600'}
        run([python, '-m', 'build', '--wheel', '--no-isolation', '--outdir', wheels, source], env=env)
        run([python, '-m', 'pip', '--isolated', 'download', '--disable-pip-version-check',
             '--only-binary=:all:', '--no-deps', '--dest', wheels,
             *[f'{n}=={v}' for n,v in check['dependencies'].items()]])
        package_wheels = sorted(wheels.glob('fox2_agent_bridge-*.whl'))
        if len(package_wheels) != 1:
            raise ValueError('exactly one Bridge wheel is required')
        wheel_source_modules = verify_wheel_source_modules(package_wheels[0], source)
        files = {f'wheels/{p.name}': p.read_bytes() for p in sorted(wheels.glob('*.whl'))}
        files.update({f'scripts/{name}': raw.replace(b'\r\n', b'\n') for name,raw in scripts.items()})
        desktop = ROOT / 'desktop_app/src/FOX2.Bridge.Desktop/FOX2.Bridge.Desktop.csproj'
        desktop_output = stage / 'desktop'
        # Self-contained WPF is usable on clean Windows without a shared .NET runtime.
        run(['dotnet', 'publish', desktop, '-c', 'Release', '-r', 'win-x64', '--self-contained', 'true',
             '-p:PublishSingleFile=false', '-p:ContinuousIntegrationBuild=true',
             '-p:PathMap=' + str(ROOT / 'desktop_app') + '=/_/desktop_app', '-o', desktop_output])
        files.update({f'desktop/{p.name}': p.read_bytes() for p in sorted(desktop_output.iterdir())
                      if p.is_file() and p.suffix in ('.exe', '.dll', '.json', '.config')})
        if 'desktop/FOX2.Bridge.Desktop.exe' not in files:
            raise ValueError('complete Desktop publication is required')
        sha = lambda b: hashlib.sha256(b).hexdigest()
        source_files = {str(p.relative_to(source)).replace('\\','/'):sha(p.read_bytes())
                        for p in sorted((source/'src').rglob('*')) if p.is_file() and
                        not p.name.endswith('.pyc') and '.egg-info' not in str(p)}
        source_files.update({str(p.relative_to(ROOT)).replace('\\','/'):sha(p.read_bytes())
                             for p in (ROOT/'desktop_app').rglob('*') if p.is_file() and
                             p.suffix in ('.cs', '.xaml', '.csproj') and not {'bin','obj','publish'} & set(p.parts)})
        sys.path.insert(0,str(ROOT/'src'))
        from fox2_agent_bridge import project_dictionary as registry
        manifest = {'format':'FOX2_USER_PACKAGE_1', 'python':check['python'],
                    'platform':check['platform'], 'dictionary_sha256':registry.SOURCE_SHA256,
                    'dictionary_version':registry.DICTIONARY_VERSION,
                    'desktop':'NET8_WPF_SELF_CONTAINED_WIN_X64',
                    'source_sha256':sha(json.dumps(source_files,sort_keys=True).encode()),
                    'source_git_commit':source_git_commit(),
                    'source_files':source_files,
                    'wheel_source_modules':wheel_source_modules,
                    'dependencies':check['dependencies'],
                    'files':{n:sha(b) for n,b in files.items()}}
        files['manifest.json'] = (json.dumps(manifest,sort_keys=True,indent=2)+'\n').encode()
        output.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
            for name,raw in sorted(files.items()):
                info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0))
                info.external_attr=0o100644 << 16
                info.compress_type=zipfile.ZIP_DEFLATED
                archive.writestr(info,raw,compresslevel=9)
        result={'package':output.name,'sha256':sha(output.read_bytes()),'manifest':manifest,
                'build_backend':check['setuptools'],'wheel':check['wheel']}
        output.with_suffix('.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8',newline='\n')
        return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--build-python',required=True,type=Path)
    args=parser.parse_args()
    result=build(args.output,args.build_python)
    print(json.dumps({k:v for k,v in result.items() if k!='manifest'},sort_keys=True))
