"""Test per la configurazione."""

from ai_trading_agent.config import Settings


def test_default_settings():
    s = Settings()
    assert s.app_name == "ai-trading-agent"
    assert s.log_level in ("INFO", "DEBUG", "WARNING", "ERROR")


def test_autotrade_webhook_url_default():
    s = Settings()
    assert s.autotrade_webhook_url == "http://ollasrv:8080/webhook/signal"
