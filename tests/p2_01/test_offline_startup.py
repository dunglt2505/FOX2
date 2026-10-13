import asyncio
import importlib
import subprocess
import sys
from pathlib import Path
import httpx
from fox2.config import Settings


def test_startup_offline_and_diagnostics(deny_network, offline_runner):
    # ASGI in-process: lifespan + requests under socket/DNS denial, no actual bind.
    module = importlib.import_module("fox2.main")
    app = module.create_app()
    async def run():
        async with app.router.lifespan_context(app):
            transport=httpx.ASGITransport(app=app,client=("127.0.0.1",12345))
            async with httpx.AsyncClient(transport=transport,base_url="http://127.0.0.1:8000") as client:
                for _ in range(3):
                    response=await client.get("/api/health")
                    assert response.status_code==200
                    assert response.json()==dict(contract_version="market-data-v0.4-candidate",status="OK",provider_enabled=False)
                    sources=await client.get("/api/data-sources/health")
                    assert sources.status_code==200
                    assert len(sources.json())==3
                    for item in sources.json():
                        assert item["readiness"]=="UNAVAILABLE" and item["state"]=="UNKNOWN"
                        assert item["verified_until"] is None
                        assert "READY" not in str(item)
    offline_runner(run())
    assert deny_network==[]
    assert not app.router.on_startup and not app.router.on_shutdown

def test_defaults_ignore_credential_environment(monkeypatch):
    monkeypatch.setenv("DNSE_API_KEY","TEST_SENTINEL_SECRET")
    monkeypatch.setenv("FOX2_PROVIDER_ENABLED","true")
    settings=Settings()
    assert settings.host=="127.0.0.1"
    assert settings.provider_enabled is False and settings.network_enabled is False
    assert "TEST_SENTINEL_SECRET" not in settings.model_dump_json()

def test_fresh_process_startup_no_transport_construction():
    script = """
import asyncio, socket
loop=asyncio.new_event_loop()  # Windows harness wakeup socketpair only
attempts=[]
def denied(*args,**kwargs):
 attempts.append('FORBIDDEN_IO')
 raise AssertionError('Offline foundation attempted I/O')
for name in ('connect','connect_ex','bind','listen','sendto'):
 setattr(socket.socket,name,denied)
socket.create_connection=denied
socket.getaddrinfo=denied
import httpx
httpx.HTTPTransport.__init__=denied
httpx.AsyncHTTPTransport.__init__=denied
from fox2.main import app,create_app
async def run():
 async with app.router.lifespan_context(app):
  transport=httpx.ASGITransport(app=create_app(),client=('127.0.0.1',1))
  async with httpx.AsyncClient(transport=transport,base_url='http://127.0.0.1') as client:
   assert (await client.get('/api/health')).status_code==200
loop.run_until_complete(run())
loop.close()
assert not attempts
print('OFFLINE_IMPORT_STARTUP_TRANSPORT_PASS')
"""
    import os
    root=Path(__file__).resolve().parents[2]/"backend"/"src"
    result=subprocess.run([sys.executable,"-B","-c",script],capture_output=True,text=True,
        env=dict(os.environ,PYTHONPATH=str(root),PYTHONDONTWRITEBYTECODE="1"))
    assert result.returncode==0,result.stderr
    assert result.stdout.strip()=="OFFLINE_IMPORT_STARTUP_TRANSPORT_PASS"
