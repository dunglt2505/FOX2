"""FOX2 GitHub-first source discovery. Read-only, version-agnostic, fail closed.

Python 3.11+. No third-party dependencies. GitHub token from GITHUB_TOKEN.
Discovery is not authority: release registry must explicitly nominate trusted refs and
manifest paths. This module never treats newest commit or highest version as EFFECTIVE.
"""
from __future__ import annotations
import base64, hashlib, json, os, re, urllib.parse, urllib.request
from dataclasses import dataclass
from typing import Callable

class SourceError(Exception): pass

@dataclass(frozen=True)
class Binding:
    family: str
    version: str
    ref: str
    commit_sha: str
    path: str
    sha256: str
    manifest_path: str
    manifest_commit: str

class GitHub:
    def __init__(self, repo: str, token: str | None = None, transport: Callable | None = None):
        if not re.fullmatch(r'[\w.-]+/[\w.-]+', repo): raise ValueError('Invalid repository')
        self.repo, self.token, self.transport = repo, token or os.getenv('GITHUB_TOKEN'), transport
    def get(self, path: str):
        if self.transport: return self.transport(path)
        url = 'https://api.github.com/repos/' + self.repo + '/' + path
        headers={'Accept':'application/vnd.github+json','User-Agent':'fox2-source-resolver','X-GitHub-Api-Version':'2022-11-28'}
        if self.token: headers['Authorization']='Bearer '+self.token
        with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=20) as response:
            return json.load(response)
    def commit(self, ref: str) -> str:
        x=self.get('commits/'+urllib.parse.quote(ref,safe=''))
        sha=x.get('sha','')
        if not re.fullmatch('[a-f0-9]{40}',sha): raise SourceError('Unverified commit')
        return sha
    def read_file(self, path: str, commit_sha: str) -> bytes:
        if path.startswith('/') or '..' in path.split('/'): raise SourceError('Invalid path')
        x=self.get('contents/'+urllib.parse.quote(path,safe='/')+'?ref='+commit_sha)
        if x.get('type')!='file' or x.get('encoding')!='base64': raise SourceError('Not a base64 file')
        return base64.b64decode(x['content'],validate=False)
    def tree(self, commit_sha: str):
        commit=self.get('git/commits/'+commit_sha)
        tree_sha=commit.get('tree',{}).get('sha','')
        tree=self.get('git/trees/'+tree_sha+'?recursive=1')
        if tree.get('truncated'): raise SourceError('Git tree truncated')
        return tree.get('tree',[])

def bind_effective(git: GitHub, registry_ref: str, registry_path: str, family: str) -> Binding:
    """Registry contract: {authority:'FOX2', families:{family:{ref,manifest_path}}}.
    Manifest contract: {family,version,status:'EFFECTIVE',source_path,
      source_sha256,commit_sha, superseded_by:null}. Reject missing evidence.
    Registry/manifest signatures or external approvals must be validated by the
    caller's trust policy; a Git file alone is not proof of governance authority.
    """
    registry_commit=git.commit(registry_ref)
    registry=json.loads(git.read_file(registry_path,registry_commit))
    if registry.get('authority')!='FOX2': raise SourceError('Untrusted registry identity')
    entry=registry.get('families',{}).get(family)
    if not isinstance(entry,dict): raise SourceError('Family not registered')
    ref,manifest_path=entry.get('ref'),entry.get('manifest_path')
    if not ref or not manifest_path: raise SourceError('Incomplete registry entry')
    manifest_commit=git.commit(ref)
    manifest=json.loads(git.read_file(manifest_path,manifest_commit))
    if manifest.get('family')!=family or manifest.get('status')!='EFFECTIVE' or manifest.get('superseded_by'):
        raise SourceError('No current EFFECTIVE claim')
    commit_sha=manifest.get('commit_sha','')
    if not re.fullmatch('[a-f0-9]{40}',commit_sha): raise SourceError('Missing immutable source commit')
    path,digest=manifest.get('source_path',''),manifest.get('source_sha256','')
    if not path or not re.fullmatch('[a-fA-F0-9]{64}',digest): raise SourceError('Missing content provenance')
    content=git.read_file(path,commit_sha)
    if hashlib.sha256(content).hexdigest()!=digest.lower(): raise SourceError('Source hash mismatch')
    return Binding(family,str(manifest.get('version','')),ref,commit_sha,path,digest.lower(),manifest_path,manifest_commit)

def discover(git: GitHub, refs: list[str], pattern: str = r'(registry|release.manifest|source.index)') -> dict:
    """Read-only inventory; does not declare anything EFFECTIVE."""
    results={}
    for ref in refs:
        try:
            sha=git.commit(ref)
            results[ref]={'commit':sha,'paths':[x['path'] for x in git.tree(sha) if x.get('type')=='blob' and re.search(pattern,x['path'],re.I)]}
        except Exception as exc:
            results[ref]={'error':str(exc)}
    return results

if __name__=='__main__':
    print(json.dumps({'status':'UNVERIFIED','reason':'Legacy Candidate CLI disabled; use native_registry with host authority verifier'}))
    raise SystemExit(2)
