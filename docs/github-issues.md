# GitHub Issues — AI Trading Agent Roadmap

Flusso: **Data → Indicators → Strategy/Superbot (LLM locale) → Signal Sender → Autotrade → broker**

Zero API cloud. Zero accesso diretto ai broker.

---

## Issue #1: Signal sender verso Autotrade [COMPLETATA]

**Obiettivo:** Modulo exchange che invia segnali di trading al webhook di Autotrade.

**Deliverable:**
- `exchange/signal_sender.py` con `SignalSender` e `SignalPayload`
- Config `AUTOTRADE_WEBHOOK_URL`
- Test contratto webhook + test mock `SignalSender.send()`

**Criteri completamento:**
- [x] 18 test passano
- [x] Zero accessi diretti a broker nel codebase

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

## Issue #5: Strategy — Prompt builder + Superbot client + decision parser

**Obiettivo:** Costruire il prompt, inviarlo a Superbot (LLM locale), parsare la decisione e inoltrarla ad Autotrade.

**Deliverable:**
- Prompt builder: contesto mercato + indicatori + regole risk management
- Client Superbot: `POST /generate` con `{text, mode: "trading", stream: false}`
- Parser: estrae e valida JSON dal campo `response` (stringa)
- Schema decisione: `{action, symbol, direction, entry_price, stop_loss, take_profits, confidence, reasoning}`
- Logica: `action != "HOLD"` → `SignalPayload` → `SignalSender.send()`

**Criteri completamento:**
- Prompt deterministico su input fisso
- Parsing corretto di risposte valide e invalide
- Conversione a `SignalPayload` testata
- Test unitari passano

**Dipendenze:** Issue #1, Issue #3, Issue #4

---

## Mini Roadmap

```
Issue #1 (Signal Sender) [DONE] ────────────┐
                                             │
Issue #2 (Storage) ──> Issue #3 (Data) ─────>├──> Issue #5 (Strategy + Superbot)
                                             │
                       Issue #4 (Indicators) ┘
```
