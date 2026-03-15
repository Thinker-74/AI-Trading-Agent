"""Client per invio segnali di trading al webhook Autotrade."""

from dataclasses import dataclass

import httpx


@dataclass
class SignalPayload:
    symbol: str
    direction: str  # "BUY" o "SELL"
    entry_price: float | None = None
    stop_loss: float | None = None
    take_profits: list[float] | None = None

    def to_dict(self) -> dict:
        d: dict = {
            "symbol": self.symbol,
            "direction": self.direction,
        }
        if self.entry_price is not None:
            d["entry_price"] = self.entry_price
        if self.stop_loss is not None:
            d["stop_loss"] = self.stop_loss
        if self.take_profits is not None:
            d["take_profits"] = self.take_profits
        return d


class SignalSender:
    """Invia segnali di trading al webhook di Autotrade."""

    def __init__(self, webhook_url: str = "http://ollasrv:8080/webhook/signal"):
        self.webhook_url = webhook_url

    async def send(self, signal: SignalPayload) -> dict:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                self.webhook_url,
                json=signal.to_dict(),
            )
            resp.raise_for_status()
            return resp.json()
