"""Configurazione applicazione da variabili d'ambiente."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

# Carica .env dalla root del progetto
_env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_env_path)


@dataclass(frozen=True)
class Settings:
    app_name: str = "ai-trading-agent"

    # Superbot (LLM locale via Ollama)
    superbot_url: str = field(
        default_factory=lambda: os.getenv("SUPERBOT_URL", "http://ollasrv:5000")
    )
    superbot_mode: str = field(
        default_factory=lambda: os.getenv("SUPERBOT_MODE", "trading")
    )

    # Autotrade webhook
    autotrade_webhook_url: str = field(
        default_factory=lambda: os.getenv(
            "AUTOTRADE_WEBHOOK_URL", "http://ollasrv:8080/webhook/signal"
        )
    )

    # Database
    database_url: str = field(
        default_factory=lambda: os.getenv(
            "DATABASE_URL", "postgresql://user:password@localhost:5432/ai_trading"
        )
    )

    # App
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))


settings = Settings()
