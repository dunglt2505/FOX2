"""Retain functional assertions from superseded upstream stage-only tests."""
import ast
from pathlib import Path
import subprocess
import sys
import os


def test_frozen_domain_dependency_boundaries():
    root = Path.cwd() / 'backend/src/fox2'
    allowed = {'typing', 'dataclasses', 'datetime', 'json', 'importlib', 'pydantic', 'jsonschema', 'fox2'}
    for group in ('contracts', 'validation', 'ports'):
        for file in (root / group).glob('*.py'):
            for node in ast.walk(ast.parse(file.read_text())):
                if isinstance(node, ast.Import): names = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom):
                    if node.level: continue
                    names = [node.module or '']
                else: continue
                for name in names:
                    assert name.split('.')[0] in allowed
                    if name.startswith('fox2.'):
                        assert name.split('.')[1] in ('contracts', 'validation', 'ports')
    assert not (root / 'provider').exists()
    assert (root / 'store').is_dir() and (root / 'dsm').is_dir()


def test_runtime_never_imports_tests_or_transport():
    root = Path.cwd() / 'backend/src/fox2'
    for group in ('api', 'application', 'runtime'):
        for file in (root / group).glob('*.py'):
            for node in ast.walk(ast.parse(file.read_text())):
                names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ''] if isinstance(node, ast.ImportFrom) else []
                assert not any(n.startswith(('tests', 'httpx', 'requests', 'aiohttp', 'dnse', 'fox2.provider')) for n in names)


def test_fresh_process_import_startup_and_requests_without_transport():
    script = '''
import asyncio, socket, importlib.abc, sys
loop = asyncio.new_event_loop()
attempts = []
def deny(*args, **kwargs):
 attempts.append('NETWORK')
 raise AssertionError('Forbidden transport')
for name in ('connect','connect_ex','bind','listen','sendto'):
 setattr(socket.socket, name, deny)
for name in ('create_connection','getaddrinfo','gethostbyname','gethostbyname_ex','gethostbyaddr'):
 setattr(socket, name, deny)
import httpx
httpx.HTTPTransport.__init__ = deny
httpx.AsyncHTTPTransport.__init__ = deny
class NoFixtures(importlib.abc.MetaPathFinder):
 def find_spec(self, fullname, path=None, target=None):
  if fullname.startswith(('tests.', 'fox2.provider', 'dnse')):
   raise AssertionError('Forbidden runtime dependency')
sys.meta_path.insert(0, NoFixtures())
from fox2.main import app
async def run():
 async with app.router.lifespan_context(app):
  async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app,client=('127.0.0.1',1)), base_url='http://127.0.0.1') as c:
   for path in ('/api/health','/api/data-sources/health','/api/stocks','/api/market/overview'):
    assert (await c.get(path)).status_code == 200
   assert (await c.put('/api/watchlist',json={'expected_version':0,'items':[]})).status_code == 503
loop.run_until_complete(run())
loop.close()
assert not attempts
print('OFFLINE_NO_NETWORK_PASS')
'''
    result = subprocess.run([sys.executable, '-B', '-c', script], capture_output=True, text=True,
                            env=dict(os.environ, PYTHONPATH=str(Path.cwd() / 'backend/src'), PYTHONDONTWRITEBYTECODE='1'))
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == 'OFFLINE_NO_NETWORK_PASS'
