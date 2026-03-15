# ai-trading-agent

AI trading agent for Capital.com demo-first execution, with modular decision engine, forecasting, logging, and future multi-broker support.

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  Data       │───>│  Forecasting │───>│  Decision   │
│  Collector  │    │  Engine      │    │  (LLM)      │
└─────────────┘    └──────────────┘    └──────┬──────┘
                                              │
┌─────────────┐    ┌──────────────┐           │
│  Dashboard  │<───│  Database    │<──────────┘
│  (locale)   │    │  (PostgreSQL)│
└─────────────┘    └──────────────┘
                          │
                   ┌──────┴──────┐
                   │ Broker      │
                   │ Adapter     │
                   │ Layer       │
                   └──────┬──────┘
                          │
              ┌───────────┼───────────┐
              │                       │
       ┌──────┴──────┐       ┌───────┴─────┐
       │ Capital.com │       │  Binance    │
       │ (active)    │       │  (phase 2)  │
       └─────────────┘       └─────────────┘
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
| `CAPITAL_API_KEY` | Capital.com API key |
| `CAPITAL_API_PASSWORD` | Capital.com API password |
| `CAPITAL_IDENTIFIER` | Capital.com account identifier |
| `CAPITAL_DEMO` | Use demo environment (default: `true`) |
| `DATABASE_URL` | PostgreSQL connection string |
| `OPENAI_API_KEY` | OpenAI API key |
| `ANTHROPIC_API_KEY` | Anthropic API key |

## Test

```bash
pytest
```

## Linting

```bash
ruff check src/ tests/
ruff format src/ tests/
```
