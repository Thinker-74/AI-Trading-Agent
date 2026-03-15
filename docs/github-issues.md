# GitHub Issues — AI Trading Agent Roadmap

Flusso: **AI decides → Signal Sender → Autotrade webhook → broker (Capital.com, Binance, MT4)**

L'agente non accede direttamente a nessun broker. Genera segnali e li invia ad Autotrade via `POST /webhook/signal`.

---

## Issue #1: Signal sender verso Autotrade [COMPLETATA]

**Obiettivo:** Modulo exchange che invia segnali di trading al webhook di Autotrade.

**Deliverable:**
- `exchange/signal_sender.py` con `SignalSender` e `SignalPayload`
- Config `AUTOTRADE_WEBHOOK_URL` (default `http://ollasrv:8080/webhook/signal`)
- Test contratto webhook (chiavi obbligatorie, tipi, campi opzionali assenti quando None)
- Test `SignalSender.send()` con mock httpx (payload corretto, errori HTTP, errori connessione)

**Criteri completamento:**
- [x] `pytest` — 18 test passano
- [x] Zero accessi diretti a broker nel codebase
- [x] Payload conforme allo schema Autotrade: `{symbol, direction, entry_price?, stop_loss?, take_profits?}`

**Dipendenze:** Nessuna

---

## Issue #2: Storage — Database e modelli SQLAlchemy

**Obiettivo:** Setup persistenza PostgreSQL con modelli base per dati di mercato, segnali e trade.

**Deliverable:**
- Modelli SQLAlchemy: `Candle`, `Trade`, `Signal`, `Position`
- Engine e session factory
- Migration iniziale
- Modello `SentSignal` per tracciare i segnali inviati ad Autotrade

**Criteri completamento:**
- Test CRUD su ogni modello passano
- Connessione a PostgreSQL locale funzionante

**Dipendenze:** Nessuna

---

## Issue #3: Data ingestion

**Obiettivo:** Raccolta dati di mercato (candele, prezzi) da fonti esterne.

**Deliverable:**
- Modulo `data/` con client per fetch candele e prezzi
- Polling periodico configurabile
- Salvataggio su storage

**Criteri completamento:**
- Fetch dati funzionante
- Dati salvati correttamente nel database

**Dipendenze:** Issue #2

---

## Issue #4: Indicatori tecnici

**Obiettivo:** Calcolo indicatori tecnici su serie storiche di candele.

**Deliverable:**
- Modulo `indicators/` con RSI, EMA, MACD, Bollinger, ATR
- Input: DataFrame candele, Output: DataFrame arricchito

**Criteri completamento:**
- Test con valori noti su dati sintetici
- Nessuna dipendenza da API esterne

**Dipendenze:** Issue #2 (per schema candele)

---

## Issue #5: Strategy — Prompt builder e decision engine

**Obiettivo:** Costruire il prompt per LLM e generare `SignalPayload` da inviare ad Autotrade.

**Deliverable:**
- Schema JSON decisione (action, size, confidence, reasoning)
- Prompt builder con contesto mercato + indicatori + regole
- Supporto multi-provider (OpenAI, Anthropic)
- Conversione output LLM → `SignalPayload` → `SignalSender.send()`

**Criteri completamento:**
- Schema JSON validato
- Prompt deterministico su input fisso
- Test unitari passano

**Dipendenze:** Issue #1, Issue #3, Issue #4

---

## Mini Roadmap

```
Issue #1 (Signal Sender) [DONE] ────────────┐
                                             │
Issue #2 (Storage) ──> Issue #3 (Data) ─────>├──> Issue #5 (Strategy)
                                             │
                       Issue #4 (Indicators) ┘
```
