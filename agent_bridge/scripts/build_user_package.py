"""Produce a deterministic offline Windows package using an isolated build Python.

Requires an already provisioned build venv; never modifies the host environment.
Dependencies are downloaded as wheels at the exact versions in that environment.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import importlib.metadata
import os
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


def build(output: Path, python: Path) -> dict:
    check = json.loads(run([python, '-I', '-c',
        'import sys,importlib.metadata as m,json; '
        'print(json.dumps(dict(isolated=sys.prefix!=sys.base_prefix, '
        'setuptools=m.version("setuptools"),wheel=m.version("wheel"))))']))
    check['dependencies'] = {n:importlib.metadata.version(n) for n in
        ['jsonschema','attrs','referencing','rpds-py','jsonschema-specifications']}
    if not check['isolated'] or not 80 <= int(check['setuptools'].split('.')[0]) < 90:
        raise ValueError('an isolated setuptools >=80,<90 environment is required')
    with tempfile.TemporaryDirectory(prefix='fox2-package-') as td:
        stage = Path(td)
        source = stage / 'source'
        shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns(
            '.venv', '__pycache__', '*.pyc', '*.egg-info', 'build', 'dist', '.pytest_cache', 'reports', 'test_artifacts'))
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
        files = {f'wheels/{p.name}': p.read_bytes() for p in sorted(wheels.glob('*.whl'))}
        files.update({f'scripts/{name}': raw.replace(b'\r\n', b'\n') for name,raw in scripts.items()})
        sha = lambda b: hashlib.sha256(b).hexdigest()
        source_files = {str(p.relative_to(source)).replace('\\','/'):sha(p.read_bytes())
                        for p in sorted((source/'src').rglob('*')) if p.is_file() and
                        not p.name.endswith('.pyc') and '.egg-info' not in str(p)}
        sys.path.insert(0,str(ROOT/'src'))
        from fox2_agent_bridge import project_dictionary as registry
        manifest = {'format':'FOX2_USER_PACKAGE_1', 'python':f'{sys.version_info.major}.{sys.version_info.minor}',
                    'platform':sys.platform, 'dictionary_sha256':registry.SOURCE_SHA256,
                    'dictionary_version':registry.DICTIONARY_VERSION,
                    'source_sha256':sha(json.dumps(source_files,sort_keys=True).encode()),
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
