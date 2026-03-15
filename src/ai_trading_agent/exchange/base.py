"""Interfaccia astratta per broker adapter."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


@dataclass
class AccountBalance:
    balance: float
    available: float
    currency: str


@dataclass
class Instrument:
    symbol: str
    name: str
    min_quantity: float
    max_quantity: float


@dataclass
class Position:
    symbol: str
    side: OrderSide
    quantity: float
    entry_price: float
    current_price: float
    pnl: float


@dataclass
class Order:
    order_id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: float | None = None
    status: str = "PENDING"


class ExchangeBase(ABC):
    """Interfaccia astratta che ogni broker adapter deve implementare."""

    @abstractmethod
    async def connect(self) -> None:
        """Stabilisce la connessione con il broker."""

    @abstractmethod
    async def disconnect(self) -> None:
        """Chiude la connessione con il broker."""

    @abstractmethod
    async def healthcheck(self) -> bool:
        """Verifica che la connessione sia attiva."""

    @abstractmethod
    async def get_accounts(self) -> list[dict]:
        """Restituisce la lista degli account disponibili."""

    @abstractmethod
    async def get_account_balance(self) -> AccountBalance:
        """Restituisce il saldo dell'account corrente."""

    @abstractmethod
    async def get_positions(self) -> list[Position]:
        """Restituisce le posizioni aperte."""

    @abstractmethod
    async def get_instruments(self, search: str = "") -> list[Instrument]:
        """Restituisce gli strumenti disponibili."""

    @abstractmethod
    async def get_price(self, symbol: str) -> float:
        """Restituisce il prezzo corrente di uno strumento."""

    @abstractmethod
    async def get_prices(self, symbols: list[str]) -> dict[str, float]:
        """Restituisce i prezzi correnti di più strumenti."""

    @abstractmethod
    async def place_order(
        self,
        symbol: str,
        side: OrderSide,
        quantity: float,
        order_type: OrderType = OrderType.MARKET,
        price: float | None = None,
    ) -> Order:
        """Piazza un ordine."""

    @abstractmethod
    async def close_position(self, symbol: str) -> Order:
        """Chiude una posizione aperta."""
