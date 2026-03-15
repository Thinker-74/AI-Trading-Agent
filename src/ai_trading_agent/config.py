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

    # Capital.com
    capital_api_key: str = field(default_factory=lambda: os.getenv("CAPITAL_API_KEY", ""))
    capital_api_password: str = field(
        default_factory=lambda: os.getenv("CAPITAL_API_PASSWORD", "")
    )
    capital_identifier: str = field(
        default_factory=lambda: os.getenv("CAPITAL_IDENTIFIER", "")
    )
    capital_demo: bool = field(
        default_factory=lambda: os.getenv("CAPITAL_DEMO", "true").lower() == "true"
    )

    @property
    def capital_base_url(self) -> str:
        if self.capital_demo:
            return "https://demo-api-capital.backend-capital.com"
        return "https://api-capital.backend-capital.com"

    # Database
    database_url: str = field(
        default_factory=lambda: os.getenv(
            "DATABASE_URL", "postgresql://user:password@localhost:5432/ai_trading"
        )
    )

    # LLM
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    anthropic_api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))

    # App
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))


settings = Settings()
