"""Entry point dell'applicazione."""

from ai_trading_agent import __version__
from ai_trading_agent.config import settings


def main() -> None:
    print(f"ai-trading-agent v{__version__} starting...")
    print(f"Log level: {settings.log_level}")


if __name__ == "__main__":
    main()
