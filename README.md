# AI-Trading-Agent

AI trading agent that collects market data, computes technical indicators, builds a decision prompt and sends it to a local LLM (via [Superbot](https://github.com/Thinker-74/Superbot) + Ollama). If the signal is actionable, it forwards it to [Autotrade](https://github.com/Thinker-74/Autotrade) for broker execution.

No cloud APIs. No direct broker access.

## Architecture

```
AI-Trading-Agent          Superbot              Autotrade V2
(data + indicators)       (local LLM)           (broker execution)
        │                      │                      │
        │  POST /generate      │                      │
        ├─────────────────────>│                      │
        │                      │──> Ollama ──> LLM    │
        │<─────────────────────│                      │
        │                      │                      │
        │  POST /webhook/signal                       │
        ├────────────────────────────────────────────>│
        │                                             │──> Capital.com
        │                                             │──> Binance
```

All three services run on `ollasrv` (Ubuntu, LAN).

## Setup

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows bash
pip install -e ".[dev]"
cp .env.example .env
# Configure variables in .env
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SUPERBOT_URL` | Superbot endpoint | `http://ollasrv:5000` |
| `SUPERBOT_MODE` | Superbot mode for trading prompts | `trading` |
| `AUTOTRADE_WEBHOOK_URL` | Autotrade webhook | `http://ollasrv:8080/webhook/signal` |
| `DATABASE_URL` | PostgreSQL connection string | |
| `LOG_LEVEL` | Logging level | `INFO` |

## Signal Flow

1. Collect market data (candles, prices)
2. Compute indicators (RSI, EMA, MACD, Bollinger, ATR)
3. Build prompt with market context + indicators + risk rules
4. Send prompt to Superbot → local LLM decides
5. If action != HOLD → send `SignalPayload` to Autotrade
6. Autotrade handles symbol mapping, position splitting, broker execution

## Test

```bash
pytest
```

## Linting

```bash
ruff check src/ tests/
ruff format src/ tests/
```
