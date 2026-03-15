"""Test per la configurazione."""

from ai_trading_agent.config import Settings


def test_default_settings():
    s = Settings()
    assert s.app_name == "ai-trading-agent"
    assert s.log_level in ("INFO", "DEBUG", "WARNING", "ERROR")


def test_superbot_url_default():
    s = Settings()
    assert s.superbot_url == "http://ollasrv:5000"


def test_superbot_mode_default():
    s = Settings()
    assert s.superbot_mode == "trading"


def test_autotrade_webhook_url_default():
    s = Settings()
    assert s.autotrade_webhook_url == "http://ollasrv:8080/webhook/signal"


def test_no_cloud_llm_keys():
    """Config non deve avere chiavi API cloud LLM."""
    s = Settings()
    assert not hasattr(s, "openai_api_key")
    assert not hasattr(s, "anthropic_api_key")
