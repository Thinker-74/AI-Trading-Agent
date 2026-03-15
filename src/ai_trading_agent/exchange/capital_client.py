"""Adapter Capital.com per esecuzione ordini."""

import httpx

from .base import (
    AccountBalance,
    ExchangeBase,
    Instrument,
    Order,
    OrderSide,
    OrderType,
    Position,
)

DEMO_URL = "https://demo-api-capital.backend-capital.com"
LIVE_URL = "https://api-capital.backend-capital.com"


class CapitalClient(ExchangeBase):
    """Broker adapter per Capital.com (demo-first)."""

    def __init__(
        self,
        api_key: str,
        api_password: str,
        identifier: str,
        demo: bool = True,
    ):
        self.api_key = api_key
        self.api_password = api_password
        self.identifier = identifier
        self.demo = demo
        self.base_url = DEMO_URL if demo else LIVE_URL
        self._client: httpx.AsyncClient | None = None
        self._cst: str = ""
        self._security_token: str = ""

    def _auth_headers(self) -> dict[str, str]:
        return {
            "X-CAP-API-KEY": self.api_key,
            "CST": self._cst,
            "X-SECURITY-TOKEN": self._security_token,
        }

    async def connect(self) -> None:
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)
        resp = await self._client.post(
            "/api/v1/session",
            json={
                "identifier": self.identifier,
                "password": self.api_password,
            },
            headers={"X-CAP-API-KEY": self.api_key},
        )
        resp.raise_for_status()
        self._cst = resp.headers.get("CST", "")
        self._security_token = resp.headers.get("X-SECURITY-TOKEN", "")

    async def disconnect(self) -> None:
        if self._client:
            try:
                await self._client.delete(
                    "/api/v1/session",
                    headers=self._auth_headers(),
                )
            finally:
                await self._client.aclose()
                self._client = None

    async def healthcheck(self) -> bool:
        if not self._client:
            return False
        try:
            resp = await self._client.get("/api/v1/ping")
            return resp.status_code == 200
        except httpx.HTTPError:
            return False

    async def get_accounts(self) -> list[dict]:
        assert self._client is not None
        resp = await self._client.get(
            "/api/v1/accounts",
            headers=self._auth_headers(),
        )
        resp.raise_for_status()
        return resp.json().get("accounts", [])

    async def get_account_balance(self) -> AccountBalance:
        accounts = await self.get_accounts()
        if not accounts:
            return AccountBalance(balance=0.0, available=0.0, currency="EUR")
        acc = accounts[0]
        return AccountBalance(
            balance=acc.get("balance", {}).get("balance", 0.0),
            available=acc.get("balance", {}).get("available", 0.0),
            currency=acc.get("currency", "EUR"),
        )

    async def get_positions(self) -> list[Position]:
        assert self._client is not None
        resp = await self._client.get(
            "/api/v1/positions",
            headers=self._auth_headers(),
        )
        resp.raise_for_status()
        positions = []
        for p in resp.json().get("positions", []):
            pos = p.get("position", {})
            market = p.get("market", {})
            side = OrderSide.BUY if pos.get("direction") == "BUY" else OrderSide.SELL
            positions.append(
                Position(
                    symbol=market.get("epic", ""),
                    side=side,
                    quantity=pos.get("size", 0.0),
                    entry_price=pos.get("level", 0.0),
                    current_price=market.get("bid", 0.0),
                    pnl=pos.get("upl", 0.0),
                )
            )
        return positions

    async def get_instruments(self, search: str = "") -> list[Instrument]:
        assert self._client is not None
        params = {"searchTerm": search} if search else {}
        resp = await self._client.get(
            "/api/v1/markets",
            params=params,
            headers=self._auth_headers(),
        )
        resp.raise_for_status()
        instruments = []
        for m in resp.json().get("markets", []):
            instruments.append(
                Instrument(
                    symbol=m.get("epic", ""),
                    name=m.get("instrumentName", ""),
                    min_quantity=m.get("dealingRules", {})
                    .get("minDealSize", {})
                    .get("value", 0.0),
                    max_quantity=m.get("dealingRules", {})
                    .get("maxDealSize", {})
                    .get("value", 0.0),
                )
            )
        return instruments

    async def get_price(self, symbol: str) -> float:
        assert self._client is not None
        resp = await self._client.get(
            f"/api/v1/markets/{symbol}",
            headers=self._auth_headers(),
        )
        resp.raise_for_status()
        snapshot = resp.json().get("snapshot", {})
        return float(snapshot.get("bid", 0.0))

    async def get_prices(self, symbols: list[str]) -> dict[str, float]:
        prices = {}
        for symbol in symbols:
            prices[symbol] = await self.get_price(symbol)
        return prices

    async def place_order(
        self,
        symbol: str,
        side: OrderSide,
        quantity: float,
        order_type: OrderType = OrderType.MARKET,
        price: float | None = None,
    ) -> Order:
        assert self._client is not None
        body: dict = {
            "epic": symbol,
            "direction": side.value,
            "size": quantity,
        }
        if order_type == OrderType.LIMIT and price is not None:
            body["level"] = price
            body["type"] = "LIMIT"

        resp = await self._client.post(
            "/api/v1/positions",
            json=body,
            headers=self._auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return Order(
            order_id=data.get("dealReference", ""),
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            status=data.get("dealStatus", "PENDING"),
        )

    async def close_position(self, symbol: str) -> Order:
        positions = await self.get_positions()
        pos = next((p for p in positions if p.symbol == symbol), None)
        if pos is None:
            raise ValueError(f"Nessuna posizione aperta per {symbol}")

        close_side = OrderSide.SELL if pos.side == OrderSide.BUY else OrderSide.BUY
        return await self.place_order(
            symbol=symbol,
            side=close_side,
            quantity=pos.quantity,
        )
