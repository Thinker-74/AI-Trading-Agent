# ai-trading-agent

## Panoramica
Agente AI di trading che analizza mercati, genera segnali e li invia al broker di esecuzione Autotrade via webhook. L'agente non esegue ordini direttamente — delega l'esecuzione ad Autotrade che gestisce Capital.com, Binance, MT4.

## Stack
- Python 3.11+
- PostgreSQL (persistenza)
- httpx (invio segnali via webhook)
- Autotrade (broker di esecuzione, repo separato)
- Provider LLM multipli (decisione)
- pytest + ruff (test e linting)

## Struttura progetto
```
src/ai_trading_agent/   # Package principale
tests/                  # Test suite
config/                 # File di configurazione
docs/                   # Documentazione
logs/                   # Log applicazione (gitignored)
tasks/                  # Task di lavoro
```

## Comandi utili
```bash
# Setup ambiente
python -m venv .venv
source .venv/Scripts/activate   # Windows bash
pip install -e ".[dev]"

# Test
pytest

# Linting
ruff check src/ tests/
ruff format src/ tests/
```

## Convenzioni
- Package name: `ai_trading_agent`
- Import style: absolute dal package root
- Config: variabili d'ambiente via `.env` + `python-dotenv`
- DB: SQLAlchemy come ORM

## Regole di progetto

1. **Plan mode obbligatorio** per task che toccano più di 1 file
2. **Test obbligatori** prima di dichiarare un task finito — esegui `pytest`
3. **Mai modificare `.env`** — modificare solo `.env.example`
4. **Test per ogni nuova funzionalità** — ogni feature deve avere test corrispondenti
5. **Lezioni apprese** — dopo ogni correzione dell'utente, aggiornare `tasks/lessons.md`
6. **Nessuna credenziale** in file versionati — solo in `.env` (gitignored)
7. **Separazione moduli** — mantenere separati: decision engine, exchange execution, data providers, forecasting
8. **Nessun accesso diretto ai broker** — tutti gli ordini passano via Autotrade webhook

## Moduli architetturali
```
src/ai_trading_agent/
├── config.py          # Configurazione runtime
├── main.py            # Entry point
├── data/              # Market data ingestion
├── news/              # News e sentiment analysis
├── indicators/        # Indicatori tecnici
├── forecasting/       # Modelli di previsione
├── strategy/          # Prompt builder + decision schema JSON
├── exchange/          # Signal sender → Autotrade webhook
│   └── signal_sender.py  # POST /webhook/signal
├── storage/           # Persistenza PostgreSQL
└── dashboard/         # Dashboard locale
```

## Integrazione Autotrade
- Webhook: `POST /webhook/signal` su `http://ollasrv:8080`
- Payload: `{symbol, direction, entry_price?, stop_loss?, take_profits?}`
- Autotrade gestisce: routing broker, symbol mapping, split posizioni, esecuzione
- Repo: https://github.com/Thinker-74/Autotrade
