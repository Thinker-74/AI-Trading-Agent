# Architettura

## Componenti principali

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

## Broker Adapter Layer

Il modulo `exchange/` implementa un pattern adapter con:

- **`ExchangeBase`** — interfaccia astratta (ABC) che definisce il contratto per tutti i broker
- **`CapitalClient`** — adapter concreto per Capital.com REST API
- Futuri adapter (es. Binance) implementeranno la stessa interfaccia

## Flusso dati

1. **Data Collector** — raccoglie dati di mercato (prezzi, orderbook) via broker adapter o API dati
2. **Forecasting Engine** — elabora previsioni basate sui dati storici
3. **Decision (LLM)** — il modello LLM valuta previsioni e contesto per generare segnali di trading
4. **Broker Adapter** — esegue gli ordini sul broker configurato (Capital.com demo-first)
5. **Database** — persiste dati, previsioni, decisioni e trade
6. **Dashboard** — visualizzazione locale di stato, performance e log

## Capital.com API

- Auth: header-based (X-CAP-API-KEY, CST, X-SECURITY-TOKEN)
- Demo: `demo-api-capital.backend-capital.com`
- Live: `api-capital.backend-capital.com`
- Libreria HTTP: `httpx` (async)
