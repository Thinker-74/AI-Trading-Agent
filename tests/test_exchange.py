"""Test per il modulo exchange."""

from ai_trading_agent.exchange import CapitalClient, ExchangeBase
from ai_trading_agent.exchange.base import OrderSide, OrderType


def test_exchange_base_is_abstract():
    import inspect

    assert inspect.isabstract(ExchangeBase)


def test_capital_client_is_subclass():
    assert issubclass(CapitalClient, ExchangeBase)


def test_capital_client_demo_url():
    client = CapitalClient(
        api_key="k", api_password="p", identifier="i", demo=True
    )
    assert client.base_url == "https://demo-api-capital.backend-capital.com"


def test_capital_client_live_url():
    client = CapitalClient(
        api_key="k", api_password="p", identifier="i", demo=False
    )
    assert client.base_url == "https://api-capital.backend-capital.com"


def test_order_side_enum():
    assert OrderSide.BUY.value == "BUY"
    assert OrderSide.SELL.value == "SELL"


def test_order_type_enum():
    assert OrderType.MARKET.value == "MARKET"
    assert OrderType.LIMIT.value == "LIMIT"
