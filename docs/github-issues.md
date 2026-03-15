# GitHub Issues — Roadmap Capital.com-first

## Issue #1: Broker adapter layer e Capital.com client

**Obiettivo:** Creare l'interfaccia astratta `ExchangeBase` e il primo adapter concreto `CapitalClient` per Capital.com demo.

**Deliverable:**
- `exchange/base.py` con `ExchangeBase(ABC)` e dataclass comuni
- `exchange/capital_client.py` con `CapitalClient` completo
- Test unitari per import, istanziazione, URL demo/live

**Criteri completamento:**
- `pytest tests/test_exchange.py` passa
- Zero riferimenti a Hyperliquid nel codebase

**Dipendenze:** Nessuna

---

## Issue #2: Storage — Database e modelli SQLAlchemy

**Obiettivo:** Setup persistenza PostgreSQL con modelli base per dati di mercato, segnali e trade.

**Deliverable:**
- Modelli SQLAlchemy: `Candle`, `Trade`, `Signal`, `Position`
- Engine e session factory
- Migration iniziale

**Criteri completamento:**
- Test CRUD su ogni modello passano
- Connessione a PostgreSQL locale funzionante

**Dipendenze:** Nessuna

---

## Issue #3: Data ingestion via Capital.com

**Obiettivo:** Raccolta dati di mercato (candele, prezzi) tramite Capital.com REST API.

**Deliverable:**
- Modulo `data/` con client per fetch candele e prezzi
- Polling periodico configurabile
- Salvataggio su storage

**Criteri completamento:**
- Fetch dati da Capital.com demo funzionante
- Dati salvati correttamente nel database

**Dipendenze:** Issue #1, Issue #2

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

**Obiettivo:** Costruire il prompt per LLM e lo schema JSON di decisione.

**Deliverable:**
- Schema JSON decisione (action, size, confidence, reasoning)
- Prompt builder con contesto mercato + indicatori + regole
- Supporto multi-provider (OpenAI, Anthropic)

**Criteri completamento:**
- Schema JSON validato
- Prompt deterministico su input fisso
- Test unitari passano

**Dipendenze:** Issue #3, Issue #4

---

## Mini Roadmap

```
Issue #1 (Exchange) ──┐
                      ├──> Issue #3 (Data) ──┐
Issue #2 (Storage) ───┘                      ├──> Issue #5 (Strategy)
                      Issue #4 (Indicators) ──┘
```
