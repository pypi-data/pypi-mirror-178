from typing import Any, Generic, TypeVar

from ccxt.base.exchange import Exchange

_Exchange = TypeVar("_Exchange", bound=Exchange)


class CCXTWrapperBase(Generic[_Exchange]):
    _ex: _Exchange

    def __init__(self, exchange: _Exchange):
        self._ex = exchange

    async def __aenter__(self) -> "CCXTWrapperBase[_Exchange]":
        await self._ex.__aenter__()
        await self._ex.load_markets()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self._ex.__aexit__(exc_type, exc_val, exc_tb)

    @property
    def exchange(self) -> _Exchange:
        return self._ex
