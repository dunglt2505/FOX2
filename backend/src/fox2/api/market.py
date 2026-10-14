"""Only approved offline public market and local preference routes."""
from datetime import datetime, timedelta
from typing import Annotated, Literal
from fastapi import APIRouter, Query, Request

from fox2.application.registry import ApplicationError
from fox2.contracts.base import DTO
from fox2.contracts.instruments import Instrument, InstrumentSearchResult
from fox2.contracts.market import MarketDataEnvelope
from fox2.contracts.watchlist import WatchlistPreference, WatchlistReplace


class StockResult(DTO):
    instrument: Instrument
    quote: MarketDataEnvelope


def allowed_queries(request: Request, allowed: set[str], repeated: str | None = None):
    names = list(request.query_params.keys())
    if (set(names) - allowed or any(len(request.query_params.getlist(k)) != 1
                                   for k in names if k != repeated)):
        raise ApplicationError(422, 'Invalid request')


def utc_window(start: str, end: str) -> tuple[datetime, datetime]:
    try:
        # Require timestamps rather than accepting ISO dates as midnight.
        if 'T' not in start or 'T' not in end:
            raise ValueError()
        a, b = datetime.fromisoformat(start), datetime.fromisoformat(end)
        if a.utcoffset() != timedelta(0) or b.utcoffset() != timedelta(0):
            raise ValueError()
        if not timedelta(days=1) <= b - a <= timedelta(days=366):
            raise ValueError()
        return a, b
    except ValueError:
        raise ApplicationError(422, 'Invalid request') from None


def market_router(runtime) -> APIRouter:
    router = APIRouter()

    @router.get('/api/market/overview', response_model=list[MarketDataEnvelope])
    def overview(request: Request, symbols: Annotated[list[str] | None, Query(max_length=100)] = None):
        allowed_queries(request, {'symbols'}, 'symbols')
        if symbols is not None and len(set(symbols)) != len(symbols):
            raise ApplicationError(422, 'Invalid request')
        instruments = ([runtime.registry.resolve(s, 'INDEX') for s in symbols]
                       if symbols is not None else runtime.registry.indices())
        return [runtime.market.envelope(i, 'INDEX') for i in instruments]

    @router.get('/api/stocks', response_model=InstrumentSearchResult)
    def stocks(request: Request, query: Annotated[str, Query(max_length=32)] = '',
               limit: Annotated[int, Query(ge=1, le=100)] = 20,
               cursor: Annotated[str | None, Query(max_length=43)] = None):
        allowed_queries(request, {'query', 'limit', 'cursor'})
        return runtime.registry.search(query, limit, cursor)

    @router.get('/api/stocks/{symbol}', response_model=StockResult)
    def stock(symbol: str, request: Request):
        allowed_queries(request, set())
        instrument = runtime.registry.resolve(symbol)
        return StockResult(instrument=instrument, quote=runtime.market.envelope(instrument, 'QUOTE'))

    @router.get('/api/stocks/{symbol}/bars', response_model=MarketDataEnvelope)
    def bars(symbol: str, request: Request,
             start: Annotated[str, Query(alias='from', max_length=40)],
             end: Annotated[str, Query(alias='to', max_length=40)],
             timeframe: Literal['1D'] = '1D', basis: Literal['RAW', 'ADJUSTED', 'UNKNOWN'] = 'RAW'):
        allowed_queries(request, {'from', 'to', 'timeframe', 'basis'})
        a, b = utc_window(start, end)
        return runtime.market.envelope(runtime.registry.resolve(symbol), 'BARS', start=a, end=b, basis=basis)

    @router.get('/api/watchlist', response_model=WatchlistPreference)
    def watchlist(request: Request):
        allowed_queries(request, set())
        return runtime.watchlist.read()

    @router.put('/api/watchlist', response_model=WatchlistPreference)
    def replace_watchlist(body: WatchlistReplace, request: Request):
        allowed_queries(request, set())
        return runtime.watchlist.replace(body)

    return router
