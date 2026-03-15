# Architettura

## Componenti principali

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
                                       └──────┬──────┘
                                              │
                              ┌───────────────┼───────────────┐
                              │               │               │
                       Capital.com       Binance           MT4
```

## Flusso dati

1. **Data Collector** — raccoglie dati di mercato (prezzi, indicatori) da fonti esterne
2. **Forecasting Engine** — elabora previsioni basate sui dati storici
3. **Decision (LLM)** — il modello LLM valuta previsioni e contesto per generare segnali di trading
4. **Signal Sender** — invia il segnale al webhook di Autotrade (`POST /webhook/signal`)
5. **Autotrade** — riceve il segnale, fa symbol mapping, routing broker, split posizioni, esecuzione
6. **Database** — persiste dati, previsioni, decisioni e segnali inviati
7. **Dashboard** — visualizzazione locale di stato, performance e log

## Integrazione Autotrade

L'agente AI non accede direttamente a nessun broker. Tutta l'esecuzione e' delegata ad Autotrade:

- **Endpoint**: `POST /webhook/signal`
- **Host default**: `http://ollasrv:8080`
- **Payload**: `{symbol, direction, entry_price?, stop_loss?, take_profits?}`
- **Symbol mapping**: Autotrade traduce automaticamente (es. XAUUSD → GOLD su Capital.com)
- **Split posizioni**: se multipli TP, Autotrade splitta 40/20/40
- **Broker supportati**: Capital.com, Binance, MT4 (via routing rules)
