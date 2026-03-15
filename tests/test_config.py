"""Test per la configurazione."""

from ai_trading_agent.config import Settings


def test_default_settings():
    s = Settings()
    assert s.app_name == "ai-trading-agent"
    assert s.log_level in ("INFO", "DEBUG", "WARNING", "ERROR")


def test_capital_demo_default_true():
    s = Settings()
    assert s.capital_demo is True


def test_capital_base_url_demo():
    s = Settings()
    assert "demo-api-capital" in s.capital_base_url


def test_capital_client_instantiation():
    from ai_trading_agent.exchange import CapitalClient

    client = CapitalClient(
        api_key="test-key",
        api_password="test-pass",
        identifier="test-id",
        demo=True,
    )
    assert client.demo is True
    assert "demo" in client.base_url
