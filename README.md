# AI-Trading-Agent

AI trading agent that analyzes markets, generates signals, and sends them to [Autotrade](https://github.com/Thinker-74/Autotrade) for execution via webhook. No direct broker access — Autotrade handles Capital.com, Binance, MT4.

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  Data       │───>│  Forecasting │───>│  Decision   │
│  Collector  │    │  Engine      │    │  (LLM)      │
└─────────────┘    └──────────────┘    └──────┬──────┘
                                              │
┌─────────────┐    ┌──────────────┐    ┌──────┴──────┐
│  Dashboard  │<───│  Database    │<───│  Signal     │
│  (locale)   │    │  (PostgreSQL)│    │  Sender     │
└─────────────┘    └──────────────┘    └──────┬──────┘
                                              │
                                     POST /webhook/signal
                                              │
                                       ┌──────┴──────┐
                                       │  Autotrade  │
                                       │  (external) │
                                       └──────┬──────┘
                                              │
                              ┌───────────────┼───────────────┐
                              │               │               │
                       Capital.com       Binance           MT4
```

## Setup

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows bash
pip install -e ".[dev]"
cp .env.example .env
# Configure variables in .env
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AUTOTRADE_WEBHOOK_URL` | Autotrade webhook endpoint (default: `http://ollasrv:8080/webhook/signal`) |
| `DATABASE_URL` | PostgreSQL connection string |
| `OPENAI_API_KEY` | OpenAI API key |
| `ANTHROPIC_API_KEY` | Anthropic API key |

## Signal Format

```json
{
  "symbol": "XAUUSD",
  "direction": "BUY",
  "entry_price": 2650.50,
  "stop_loss": 2640.00,
  "take_profits": [2660.00, 2670.00, 2680.00]
}
```

All fields except `symbol` and `direction` are optional. Autotrade handles symbol mapping, position splitting, and broker routing.

## Test

```bash
pytest
```

## Linting

```bash
ruff check src/ tests/
ruff format src/ tests/
```
