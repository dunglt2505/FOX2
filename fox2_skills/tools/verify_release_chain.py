"""Audit a conditional native release baseline; never promote it to authority.

This CLI has no authority-file flag: serialized claims cannot create grants.
Trusted hosts use ReleaseChainVerifier with an independently verified provider.
"""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from shared.local_git import LocalGit
from shared.release_chain import ReleaseChainVerifier
from shared.native_registry import bind
from shared.core import Hold, digest


def audit(git, bootstrap, scope, cutoff):
    manifest_bytes=git.read_file(bootstrap['manifest_path'],bootstrap['commit'])
    manifest=json.loads(manifest_bytes)
    source=manifest.get('source_set_head',bootstrap['commit'])
    dictionary_bytes=git.read_file(bootstrap['dictionary_path'],source)
    dictionary=json.loads(dictionary_bytes)
    verifier=ReleaseChainVerifier(scope,cutoff)
    catalog=json.loads((Path(__file__).resolve().parents[1]/'contracts.json').read_bytes())
    families=sorted({f for contract in catalog.values() for f in contract['sources']})
    results={}
    for family in families:
        decision=verifier(bootstrap,dictionary_bytes,manifest_bytes,family)
        try:
            binding=bind(git,bootstrap,family,verifier)
        except Hold as error:
            binding={'status':error.status,'reason':str(error)}
        results[family]={'decision':decision,'binding':binding,
                         'path':dictionary.get('current',{}).get(family,{}).get('path')}
    return {'status':'AUTHORITY_UNVERIFIED','scope':scope,'cutoff':cutoff,
            'bootstrap':bootstrap,'source_commit':source,
            'dictionary_sha256':digest(dictionary_bytes),'manifest_sha256':digest(manifest_bytes),
            'families':results,'effects':[],
            'missing_authority':['independently certified trust root and release approval',
               'complete applicable competing-release inventory and supersession closure',
               'approved immutable refs and owning semantic source evidence'],
            'host_semantic_acceptance':'NOT_RUN'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['repo','manifest-commit','manifest-path','dictionary-path','scope','cutoff','output']:
        parser.add_argument('--'+name,required=True)
    args=parser.parse_args()
    git=LocalGit(args.repo)
    git.refresh()
    bootstrap={'commit':args.manifest_commit,'manifest_path':args.manifest_path,'dictionary_path':args.dictionary_path}
    result=audit(git,bootstrap,args.scope,args.cutoff)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':result['status'],'families_checked':len(result['families']),'effects':[]}))
    return 2


if __name__=='__main__':raise SystemExit(main())
