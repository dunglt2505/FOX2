"""Package source and review evidence once; no upload or release operation."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT/'reports/FOX2-SKILLS-INTEGRATED-RELEASE'
archive = REPORT/'FOX2-SKILLS-INTEGRATED-REVIEW.zip'
manifest = REPORT/'delivery_manifest.json'
excluded = {archive, manifest, archive.with_suffix('.zip.sha256')}
paths = [p for base in [ROOT/'fox2_skills',REPORT] for p in base.rglob('*')
         if p.is_file() and p not in excluded and '__pycache__' not in p.parts and p.suffix != '.pyc']
data = {'status':'NOT_READY_REVIEW_BUNDLE', 'excludes':['delivery_manifest.json','*.zip','*.zip.sha256','__pycache__','*.pyc'],
        'files':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}}
manifest.write_text(json.dumps(data,indent=2),encoding='utf-8',newline='\n')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as out:
    for path in sorted(paths+[manifest]):
        out.write(path,path.relative_to(ROOT).as_posix())
hash_value = hashlib.sha256(archive.read_bytes()).hexdigest()
archive.with_suffix('.zip.sha256').write_text(hash_value+'  '+archive.name+'\n',encoding='utf-8',newline='\n')
with zipfile.ZipFile(archive) as check:
    assert check.testzip() is None
    for path, expected in data['files'].items():
        assert hashlib.sha256(check.read(path)).hexdigest() == expected
print(json.dumps({'bundle':str(archive),'files':len(paths)+1,'sha256':hash_value}))
