import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'shared'))
import base64,hashlib,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from legacy_git_resolver import GitHub,bind_effective,SourceError,discover
SHA='a'*40;SHA2='b'*40
source=b'policy contents'
registry={'authority':'FOX2','families':{'policy':{'ref':'release','manifest_path':'manifest.json'}}}
manifest={'family':'policy','version':'dynamic','status':'EFFECTIVE','source_path':'docs/policy.md','source_sha256':hashlib.sha256(source).hexdigest(),'commit_sha':SHA,'superseded_by':None}
def response(data):return {'type':'file','encoding':'base64','content':base64.b64encode(data).decode()}
def mock(path):
    if path.startswith('commits/'):return {'sha':SHA2 if path.endswith('release') else SHA}
    if path.startswith('contents/registry.json'):return response(json.dumps(registry).encode())
    if path.startswith('contents/manifest.json'):return response(json.dumps(manifest).encode())
    if path.startswith('contents/docs/policy.md'):return response(source)
    if path.startswith('git/commits/'):return {'tree':{'sha':SHA}}
    if path.startswith('git/trees/'):return {'tree':[{'path':'docs/release_manifest.json','type':'blob'}]}
    raise AssertionError(path)
class Test(unittest.TestCase):
    def test_valid(self):self.assertEqual(bind_effective(GitHub('dunglt2505/FOX2',transport=mock),'main','registry.json','policy').sha256,manifest['source_sha256'])
    def test_wrong_hash(self):
        old=manifest['source_sha256'];manifest['source_sha256']='0'*64
        try:self.assertRaises(SourceError,bind_effective,GitHub('dunglt2505/FOX2',transport=mock),'main','registry.json','policy')
        finally:manifest['source_sha256']=old
    def test_candidate(self):
        manifest['status']='CANDIDATE'
        try:self.assertRaises(SourceError,bind_effective,GitHub('dunglt2505/FOX2',transport=mock),'main','registry.json','policy')
        finally:manifest['status']='EFFECTIVE'
    def test_missing_family(self):self.assertRaises(SourceError,bind_effective,GitHub('dunglt2505/FOX2',transport=mock),'main','registry.json','routing')
    def test_discovery(self):self.assertEqual(len(discover(GitHub('dunglt2505/FOX2',transport=mock),['main'])['main']['paths']),1)
if __name__=='__main__':unittest.main()
