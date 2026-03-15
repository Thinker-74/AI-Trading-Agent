# TODO — AI Trading Agent Roadmap

## In corso

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

### Step 5. Strategy — Prompt builder + Superbot client + parser risposta
- Prompt builder: assembla contesto mercato + indicatori + regole risk management
- Client Superbot: `POST http://ollasrv:5000/generate` con `{text, mode: "trading", stream: false}`
- Parser: estrae JSON dalla risposta `response` (stringa → dict)
- Schema decisione: `{action, symbol, direction, entry_price, stop_loss, take_profits, confidence, reasoning}`
- Logica: se `action != "HOLD"` → converte in `SignalPayload` → `SignalSender.send()`
- Test: prompt deterministico, parsing risposta valida/invalida, conversione a SignalPayload

## Completati

### Step 1. Exchange — Signal sender verso Autotrade
- [x] `SignalSender` con invio JSON a webhook Autotrade
- [x] `SignalPayload` dataclass con campi opzionali
- [x] Config `AUTOTRADE_WEBHOOK_URL` (default `http://ollasrv:8080/webhook/signal`)
- [x] Test contratto webhook (chiavi obbligatorie, tipi, campi opzionali)
- [x] Test `SignalSender.send()` con mock httpx (payload, errori HTTP, errori connessione)
