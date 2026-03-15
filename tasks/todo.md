# TODO — Capital.com-first Roadmap

## In corso

### Step 1. Exchange — Broker adapter layer e Capital.com client
- [x] Interfaccia astratta `ExchangeBase` con metodi standard
- [x] Dataclass comuni: `Order`, `Position`, `Instrument`, `AccountBalance`
- [x] `CapitalClient` adapter con auth header-based e demo-first
- [x] Test: import, istanziazione, URL demo vs live
- [ ] Test integrazione con Capital.com demo (richiede credenziali)

## Da fare

### Step 2. Storage — Setup database e modelli SQLAlchemy
- Connessione PostgreSQL via `DATABASE_URL`
- Modelli base: `Candle`, `Trade`, `Signal`, `Position`
- Migration iniziale (Alembic o script SQL)
- Test: connessione, CRUD su ogni modello

### Step 3. Data — Market data ingestion via Capital.com
- Client wrapper per Capital.com REST API (candele, prezzi)
- Polling periodico
- Salvataggio dati grezzi su `storage`
- Test: fetch dati in demo, validazione schema

### Step 4. Indicators — Indicatori tecnici
- Calcolo su DataFrame pandas (RSI, EMA, MACD, Bollinger, ATR)
- Input: serie di candele dal modulo `data`
- Output: DataFrame arricchito con colonne indicatori
- Test: valori noti su dati sintetici

### Step 5. Strategy — Prompt builder e decision schema JSON
- Schema JSON per la decisione (action, size, confidence, reasoning)
- Prompt builder che assembla: contesto mercato + indicatori + regole
- Supporto multi-provider LLM (OpenAI, Anthropic)
- Test: validazione schema, prompt deterministico su input fisso

## Completati
