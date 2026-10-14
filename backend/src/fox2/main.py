"""Run with a loopback ASGI server; this factory performs no I/O."""
from ipaddress import ip_address
from urllib.parse import urlsplit
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fox2.api.health import health_router
from fox2.config import Settings
from fox2.api.market import market_router
from fox2.application.registry import ApplicationError
from fox2.runtime import OfflineRuntime


def _loopback_host(host: str | None) -> bool:
    if host == "localhost":
        return True
    try:
        return host is not None and ip_address(host).is_loopback
    except ValueError:
        return False


def create_app(settings: Settings | None = None, *, runtime: OfflineRuntime | None = None) -> FastAPI:
    settings = settings or Settings()
    runtime = runtime if runtime is not None else OfflineRuntime(settings)
    app = FastAPI(title="FOX2 Offline M1-A", docs_url=None, redoc_url=None, openapi_url=None)

    @app.middleware("http")
    async def local_only(request: Request, call_next):
        if request.client is None or not _loopback_host(request.client.host):
            return JSONResponse({"detail": "Local access required"}, status_code=403)
        if len(request.headers.getlist('host')) != 1 or len(request.headers.getlist('origin')) > 1:
            return JSONResponse({"detail": "Invalid request"}, status_code=400)
        try:
            authority = request.headers['host']
            host = urlsplit('http://' + authority)
            valid_host = (host.hostname in ('127.0.0.1', 'localhost', '::1')
                          and host.netloc == authority and host.username is None
                          and not host.path and not host.query and not host.fragment
                          and not authority.endswith(':')
                          and (host.port is None or 1 <= host.port <= 65535)
                          and not any(c.isspace() for c in authority))
        except ValueError:
            valid_host = False
        if not valid_host:
            return JSONResponse({"detail": "Invalid host"}, status_code=400)
        origin = request.headers.get("origin")
        if origin is not None:
            try:
                parsed = urlsplit(origin)
                valid = (parsed.scheme == "http" and _loopback_host(parsed.hostname)
                         and parsed.netloc == host.netloc and not parsed.path
                         and not parsed.query and not parsed.fragment and parsed.username is None
                         and parsed.port == host.port and origin == 'http://' + host.netloc)
            except ValueError:
                valid = False
            if not valid:
                return JSONResponse({"detail": "Origin denied"}, status_code=403)
        if request.method == 'PUT':
            content_types = request.headers.getlist('content-type')
            if len(content_types) != 1 or content_types[0].split(';')[0].strip().lower() != 'application/json':
                return JSONResponse({"detail": "JSON content type required"}, status_code=415)
            size = 0
            chunks = []
            async for chunk in request.stream():
                size += len(chunk)
                if size > 65536:
                    return JSONResponse({"detail": "Request too large"}, status_code=413)
                chunks.append(chunk)
            request._body = b''.join(chunks)
        return await call_next(request)

    @app.exception_handler(ApplicationError)
    async def application_failure(request, error):
        return JSONResponse({"detail": error.detail}, status_code=error.status)

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request, error):
        return JSONResponse({"detail": "Invalid request"}, status_code=422)

    @app.exception_handler(Exception)
    async def sanitized_failure(request, error):
        return JSONResponse({"detail": "Service unavailable"}, status_code=503)

    app.include_router(health_router(settings, runtime.dsm))
    app.include_router(market_router(runtime))
    return app

app = create_app()
