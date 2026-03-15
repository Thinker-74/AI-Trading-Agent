# ai-trading-agent

## Panoramica
Agente AI di trading che raccoglie dati di mercato, calcola indicatori tecnici, costruisce un prompt di decisione e lo invia a Superbot (LLM locale via Ollama). Se il segnale e' operativo, lo inoltra ad Autotrade per l'esecuzione sui broker.

Zero API cloud. Zero accesso diretto ai broker.

## Architettura a 3 progetti

```
AI-Trading-Agent          Superbot              Autotrade V2
(dati + indicatori)       (LLM locale)          (esecuzione broker)
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

Tutto su `ollasrv` (Ubuntu, LAN):
- Superbot: porta 5000
- Autotrade: porta 8080
- Ollama: porta 11434 (usato solo da Superbot)

## Stack
- Python 3.11+
- PostgreSQL (persistenza)
- httpx (chiamate HTTP a Superbot e Autotrade)
- Superbot (LLM locale via Ollama, repo separato)
- Autotrade V2 (esecuzione broker, repo separato)
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
9. **Nessuna API cloud LLM** — tutte le decisioni passano via Superbot (LLM locale)

## Moduli architetturali
```
src/ai_trading_agent/
├── config.py          # Configurazione runtime
├── main.py            # Entry point
├── data/              # Market data ingestion
├── news/              # News e sentiment analysis
├── indicators/        # Indicatori tecnici
├── forecasting/       # Modelli di previsione
├── strategy/          # Prompt builder → Superbot → parse risposta
├── exchange/          # Signal sender → Autotrade webhook
│   └── signal_sender.py  # POST /webhook/signal
├── storage/           # Persistenza PostgreSQL
└── dashboard/         # Dashboard locale
```

## Integrazione Superbot
- Endpoint: `POST http://ollasrv:5000/generate`
- Payload: `{text: "<prompt>", mode: "trading", stream: false}`
- Risposta: `{mode, model, response: "<JSON stringa>"}`
- Il campo `response` va parsato da stringa a JSON
- Repo: https://github.com/Thinker-74/Superbot

## Integrazione Autotrade
- Endpoint: `POST http://ollasrv:8080/webhook/signal`
- Payload: `{symbol, direction, entry_price?, stop_loss?, take_profits?}`
- Autotrade gestisce: routing broker, symbol mapping, split posizioni, esecuzione
- Repo: https://github.com/Thinker-74/Autotrade
