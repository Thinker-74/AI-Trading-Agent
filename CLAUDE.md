# ai-trading-agent

## Panoramica
Agente AI di trading con architettura multi-broker (Capital.com demo-first), raccolta dati, forecasting, decisione LLM, persistenza su database e dashboard locale. Binance previsto come fase 2.

## Stack
- Python 3.11+
- PostgreSQL (persistenza)
- Capital.com REST API via httpx (broker primario, demo-first)
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
├── exchange/          # Broker adapter layer (Capital.com, Binance fase 2)
│   ├── base.py        # Interfaccia astratta ExchangeBase
│   └── capital_client.py  # Adapter Capital.com
├── storage/           # Persistenza PostgreSQL
└── dashboard/         # Dashboard locale
```
