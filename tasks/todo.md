# TODO — AI Trading Agent Roadmap

## In corso

### Step 1. Exchange — Signal sender verso Autotrade
- [x] `SignalSender` con invio JSON a webhook Autotrade
- [x] `SignalPayload` dataclass con campi opzionali
- [x] Config `AUTOTRADE_WEBHOOK_URL`
- [x] Test unitari
- [ ] Test integrazione con Autotrade in esecuzione

## Da fare

### Step 2. Storage — Setup database e modelli SQLAlchemy
- Connessione PostgreSQL via `DATABASE_URL`
- Modelli base: `Candle`, `Trade`, `Signal`, `Position`
- Migration iniziale (Alembic o script SQL)
- Test: connessione, CRUD su ogni modello

### Step 3. Data — Market data ingestion
- Client per raccolta dati di mercato (prezzi, candele)
- Polling periodico
- Salvataggio dati grezzi su `storage`
- Test: fetch dati, validazione schema

### Step 4. Indicators — Indicatori tecnici
- Calcolo su DataFrame pandas (RSI, EMA, MACD, Bollinger, ATR)
- Input: serie di candele dal modulo `data`
- Output: DataFrame arricchito con colonne indicatori
- Test: valori noti su dati sintetici

### Step 5. Strategy — Prompt builder e decision schema JSON
- Schema JSON per la decisione (action, size, confidence, reasoning)
- Prompt builder che assembla: contesto mercato + indicatori + regole
- Supporto multi-provider LLM (OpenAI, Anthropic)
- Output: `SignalPayload` da inviare via `SignalSender`
- Test: validazione schema, prompt deterministico su input fisso

## Completati
