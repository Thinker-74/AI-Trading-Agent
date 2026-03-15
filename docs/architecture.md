# Architettura

## Sistema a 3 progetti

```
AI-Trading-Agent          Superbot              Autotrade V2
(dati + indicatori)       (LLM locale)          (esecuzione broker)
        │                      │                      │
        │  POST /generate      │                      │
        │  {mode: "trading",   │                      │
        │   text: prompt}      │                      │
        ├─────────────────────>│                      │
        │                      │──> Ollama ──> LLM    │
        │                      │    (locale, GPU)     │
        │<─────────────────────│                      │
        │  {action, symbol,    │                      │
        │   entry, SL, TPs,   │                      │
        │   confidence}        │                      │
        │                      │                      │
        │  POST /webhook/signal                       │
        │  {symbol, direction,                        │
        │   entry_price, stop_loss, take_profits}     │
        ├────────────────────────────────────────────>│
        │                                             │──> Capital.com
        │                                             │──> Binance
        │                                             │──> MT4
```

Tutto su `ollasrv` (Ubuntu, LAN):
- **Superbot**: porta 5000 — orchestratore LLM locale
- **Ollama**: porta 11434 — inference engine (usato solo da Superbot)
- **Autotrade**: porta 8080 — esecuzione ordini sui broker

## Flusso dati interno

```
┌──────────┐    ┌──────────────┐    ┌─────────────┐    ┌───────────┐
│  Data    │───>│  Indicators  │───>│  Strategy   │───>│  Signal   │
│  Module  │    │  (RSI, EMA,  │    │  (prompt    │    │  Sender   │
│          │    │   MACD, ATR) │    │   builder)  │    │           │
└──────────┘    └──────────────┘    └──────┬──────┘    └─────┬─────┘
                                           │                 │
                                    POST /generate    POST /webhook/signal
                                           │                 │
                                      Superbot          Autotrade
```

## Integrazione Superbot

- **Endpoint**: `POST http://ollasrv:5000/generate`
- **Request**: `{text: "<prompt>", mode: "trading", stream: false}`
- **Response**: `{mode: "trading", model: "qwen2.5:14b", response: "<JSON stringa>"}`
- Il campo `response` contiene JSON come stringa — va parsato
- Schema decisione atteso: `{action, symbol, direction, entry_price, stop_loss, take_profits, confidence, reasoning}`
- Se `action == "HOLD"` → nessun segnale inviato

## Integrazione Autotrade

- **Endpoint**: `POST http://ollasrv:8080/webhook/signal`
- **Payload**: `{symbol, direction, entry_price?, stop_loss?, take_profits?}`
- **Risposta ok**: `{"ok": true, "results": [...]}`
- **Risposta errore**: `{"ok": false, "error": "descrizione"}`
- Symbol mapping automatico (es. XAUUSD -> GOLD su Capital.com)
- Split posizioni su multipli TP (40/20/40)

## Responsabilita'

| AI-Trading-Agent | NON fa |
|---|---|
| Raccoglie dati mercato | NON chiama API cloud LLM |
| Calcola indicatori tecnici | NON si connette a broker |
| Costruisce prompt di decisione | NON gestisce posizioni/ordini |
| Chiama Superbot per decisione | NON traduce simboli |
| Invia segnale ad Autotrade | NON fa auth su broker |
