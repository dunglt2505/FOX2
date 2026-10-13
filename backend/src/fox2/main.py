"""Run with a loopback ASGI server; this factory performs no I/O."""
from ipaddress import ip_address
from urllib.parse import urlsplit
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fox2.api.health import health_router
from fox2.config import Settings


def _loopback_host(host: str | None) -> bool:
    if host == "localhost":
        return True
    try:
        return host is not None and ip_address(host).is_loopback
    except ValueError:
        return False


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    app = FastAPI(title="FOX2 Foundation", docs_url=None, redoc_url=None, openapi_url=None)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost", "[::1]"])

    @app.middleware("http")
    async def local_only(request: Request, call_next):
        if request.client is None or not _loopback_host(request.client.host):
            return JSONResponse({"detail": "Local access required"}, status_code=403)
        origin = request.headers.get("origin")
        if origin:
            try:
                parsed = urlsplit(origin)
                host = urlsplit("http://" + request.headers.get("host", ""))
                valid = (parsed.scheme == "http" and _loopback_host(parsed.hostname)
                         and parsed.netloc == host.netloc and not parsed.path
                         and not parsed.query and not parsed.fragment and parsed.username is None)
            except ValueError:
                valid = False
            if not valid:
                return JSONResponse({"detail": "Origin denied"}, status_code=403)
        return await call_next(request)

    @app.exception_handler(Exception)
    async def sanitized_failure(request, error):
        return JSONResponse({"detail": "Service unavailable"}, status_code=503)

    app.include_router(health_router(settings))
    return app

app = create_app()
