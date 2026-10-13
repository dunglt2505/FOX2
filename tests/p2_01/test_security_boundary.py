import ast
import asyncio
from pathlib import Path
import subprocess
import sys
import httpx
import pytest
from pydantic import ValidationError
from fox2.config import Settings
from fox2.main import create_app

@pytest.mark.parametrize("settings", [dict(host="0.0.0.0"),dict(host="example.com"),
    dict(provider_enabled=True),dict(network_enabled=True),dict(profile="ISOLATED_TEST"),
    dict(api_key="TEST_SENTINEL_SECRET")])
def test_unsafe_configuration_rejected(settings):
    with pytest.raises(ValidationError): Settings(**settings)

@pytest.mark.parametrize("host,origin,peer,status", [
    ("127.0.0.1:8000",None,"127.0.0.1",200),
    ("localhost:8000","http://localhost:8000","127.0.0.1",200),
    ("evil.example",None,"127.0.0.1",400),
    ("127.0.0.1:8000","https://evil.example","127.0.0.1",403),
    ("127.0.0.1:8000","null","127.0.0.1",403),
    ("127.0.0.1:8000","http://127.0.0.1:9000","127.0.0.1",403),
    ("127.0.0.1:8000",None,"192.0.2.1",403)])
def test_loopback_host_origin_guards(host,origin,peer,status,offline_runner):
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=create_app(),client=(peer,123)),
                                     base_url="http://127.0.0.1:8000") as client:
            headers={"host":host}
            if origin: headers["origin"]=origin
            assert (await client.get("/api/health",headers=headers)).status_code==status
    offline_runner(run())

def test_route_allowlist():
    app=create_app()
    assert {(r.path,frozenset(r.methods)) for r in app.routes}=={
        ("/api/health",frozenset({"GET"})),("/api/data-sources/health",frozenset({"GET"}))}

def test_sanitized_failure(offline_runner):
    app=create_app()
    @app.get("/test-error")
    def fail(): raise RuntimeError("TEST_SENTINEL_SECRET private account")
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app,client=("127.0.0.1",1),
            raise_app_exceptions=False),base_url="http://127.0.0.1") as client:
            r=await client.get("/test-error")
            assert r.status_code==503 and r.json()=={"detail":"Service unavailable"}
    offline_runner(run())

def test_domain_dependency_boundary():
    root=Path(__file__).resolve().parents[2]/"backend"/"src"/"fox2"
    allowed={"typing","dataclasses","datetime","json","importlib","pydantic","jsonschema","fox2"}
    for group in ("contracts","validation","ports"):
        for file in (root/group).glob("*.py"):
            tree=ast.parse(file.read_text())
            for node in ast.walk(tree):
                if isinstance(node,ast.Import): names=[a.name for a in node.names]
                elif isinstance(node,ast.ImportFrom):
                    if node.level: continue
                    names=[node.module or ""]
                else: continue
                for name in names:
                    assert name.split(".")[0] in allowed,(file,name)
                    if name.startswith("fox2."):
                        assert name.split(".")[1] in ("contracts","validation","ports"),(file,name)
    assert not (root/"provider").exists() and not (root/"store").exists() and not (root/"dsm").exists()

def test_fresh_process_domain_imports_without_framework():
    root=Path(__file__).resolve().parents[2]/"backend"/"src"
    script = """
import importlib.abc, sys
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in ('fastapi','sqlite3','httpx','requests','dnse','tests'):
   raise AssertionError('Forbidden dependency: '+fullname)
sys.meta_path.insert(0,Deny())
import fox2.contracts.market, fox2.validation.schema, fox2.validation.semantics
import fox2.ports.store, fox2.ports.dsm, fox2.ports.preferences
print('DOMAIN_IMPORT_PASS')
"""
    import os
    env=dict(os.environ,PYTHONPATH=str(root),PYTHONDONTWRITEBYTECODE="1")
    r=subprocess.run([sys.executable,"-B","-c",script],env=env,capture_output=True,text=True)
    assert r.returncode==0,r.stderr
    assert r.stdout.strip()=="DOMAIN_IMPORT_PASS"

def test_frozen_port_signatures():
    import inspect
    from fox2.ports.store import StoreReadPort,StoreWritePort
    from fox2.ports.dsm import DSMSelectPort
    from fox2.ports.preferences import PreferenceRepositoryPort
    for cls,method,names in [
        (StoreReadPort,"get_observation",["self","instrument_id","capability","at_or_before"]),
        (StoreWritePort,"append_and_promote",["self","candidate","ingest_audit"]),
        (DSMSelectPort,"select",["self","capability","instrument_id","use_context"]),
        (PreferenceRepositoryPort,"replace_if_version",["self","expected_version","items"])]:
        assert cls._is_protocol
        assert list(inspect.signature(getattr(cls,method)).parameters)==names
