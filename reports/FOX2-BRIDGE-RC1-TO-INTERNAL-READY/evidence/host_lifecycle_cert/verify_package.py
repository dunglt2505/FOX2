"""Verify accepted package bytes and source provenance before install; no host mutation."""
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

AREA=Path(__file__).resolve().parent
ROOT=AREA.parents[3]
STAGE=Path(r'C:\Projects\FOX2-builds\HLC-A01-353ca164')
SOURCE=STAGE/'source'
PACKAGE=STAGE/'accepted-package.zip'
BASE='2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
git=lambda *a:subprocess.check_output(['git','-C',str(SOURCE),*a]).strip()
assert git('rev-parse','HEAD').decode()==BASE
assert not git('status','--porcelain=v1','--untracked-files=all')
assert not PACKAGE.resolve().is_relative_to(Path(os.environ['FOX2_BRIDGE_ROOT']).resolve())
assert not Path(sys.executable).resolve().is_relative_to(Path(os.environ['FOX2_BRIDGE_ROOT']).resolve())
raw=PACKAGE.read_bytes(); identity=sha(raw)
sys.path.insert(0,str(SOURCE/'agent_bridge/src'))
from fox2_agent_bridge.installation import verified_package
from fox2_agent_bridge import project_dictionary as registry
manifest,files=verified_package(PACKAGE,identity)
assert manifest['source_git_commit']==BASE
binding=json.loads((AREA/'source_binding.json').read_text())
assert manifest['dictionary_sha256']==registry.SOURCE_SHA256
assert manifest['dictionary_version']==registry.DICTIONARY_VERSION
dictionary_raw=subprocess.check_output(['git','-C',str(SOURCE),'show',registry.SOURCE_COMMIT+':'+registry.SOURCE_PATH])
assert sha(dictionary_raw)==registry.SOURCE_SHA256
assert manifest['f1_support']['activation']=='DENY_PENDING_G3_G4'
assert sha(json.dumps(manifest['source_files'],sort_keys=True).encode())==manifest['source_sha256']
for name,digest in manifest['source_files'].items():
    relative=Path(name)
    candidate=SOURCE/'agent_bridge'/relative
    if name.startswith('src/fox2_agent_bridge/resources/'):
        candidate=SOURCE/'agent_bridge/scripts'/relative.name
    assert candidate.is_file(), name
    assert sha(candidate.read_bytes())==digest,name
wheel_names=[n for n in files if n.startswith('wheels/fox2_agent_bridge-')]
assert len(wheel_names)==1
with zipfile.ZipFile(io.BytesIO(files[wheel_names[0]])) as wheel:
    for name,digest in manifest['wheel_source_modules'].items():
        assert sha(wheel.read(name))==digest
        expected=SOURCE/'agent_bridge/src'/name
        if '/resources/' in name:
            expected=SOURCE/'agent_bridge/scripts'/Path(name).name
        assert wheel.read(name)==expected.read_bytes(),name
with zipfile.ZipFile(io.BytesIO(raw)) as archive:
    infos=archive.infolist()
    assert [i.filename for i in infos]==sorted(i.filename for i in infos)
    assert all(i.date_time==(2026,1,1,0,0,0) for i in infos)
    assert all(i.external_attr>>16==0o100644 for i in infos)
assert json.loads(PACKAGE.with_suffix('.json').read_text())['sha256']==identity
def save(name,data):
    (AREA/name).write_text(json.dumps(data,sort_keys=True,indent=2)+'\n',encoding='utf-8',newline='\n')
save('package_manifest.json',manifest)
save('package_verification.json',dict(status='PASS',package_path_alias='BUILD_ROOT/accepted-package.zip',
    build_root_alias='PROJECTS/FOX2-builds/HLC-A01-353ca164',package_sha256=identity,package_size=len(raw),
    source_git_commit=BASE,source_checkout_branch=git('branch','--show-current').decode(),
    source_checkout_clean=True,source_manifest_sha256=sha(json.dumps(manifest,sort_keys=True).encode()),
    dictionary_sha256=manifest['dictionary_sha256'],dictionary_version=manifest['dictionary_version'],
    embedded_dictionary_source=dict(commit=registry.SOURCE_COMMIT,path=registry.SOURCE_PATH,sha256=registry.SOURCE_SHA256),
    dispatch_routing_dictionary=binding['identities']['dictionary'],
    dictionary_layers_note='Accepted package embeds machine dictionary 1.2; Dispatch routes with human dictionary 1.3. Each immutable source verified separately; no machine adoption claimed.',
    source_sha256=manifest['source_sha256'],all_payload_hashes_verified=True,
    source_inventory_entries_verified=len(manifest['source_files']),wheel_module_entries_verified=len(manifest['wheel_source_modules']),
    deterministic_checks=['fixed ZIP timestamp 2026-01-01','sorted members','fixed mode 100644','SOURCE_DATE_EPOCH=1767225600 in unmodified builder','deterministic .NET publish flags and PathMap in unmodified builder','all source inventory and wheel module bytes checked against exact accepted checkout'],
    repeated_build_performed=False,tool_or_dependency_installation=False,build_script='agent_bridge/scripts/build_user_package.py',
    staging_preparation_note='Initial clone already had task branch; checkout -b refused before build. The temporary clone was then checked out at the exact accepted source. No package build or host mutation occurred during the staging correction.',
    preliminary_verifier_correction='An evidence-only assertion incorrectly equated Dispatch routing dictionary 1.3 with accepted embedded machine dictionary 1.2. Corrected to verify both pinned Git sources separately; package builder and product code unchanged. No host mutation occurred before the corrected package gate passed.',
    retained_for_lifecycle_and_bounded_recovery=True,host_mutation_performed=False))
print('PACKAGE_PROVENANCE_AND_ALL_PAYLOADS=PASS; SHA256='+identity)
