"""Test per il modulo exchange (signal sender)."""

import pytest

import httpx

from ai_trading_agent.exchange import SignalPayload, SignalSender


# --- SignalSender init ---


def test_signal_sender_default_url():
    sender = SignalSender()
    assert sender.webhook_url == "http://ollasrv:8080/webhook/signal"


def test_signal_sender_custom_url():
    sender = SignalSender(webhook_url="http://localhost:9090/webhook/signal")
    assert sender.webhook_url == "http://localhost:9090/webhook/signal"


# --- SignalPayload serializzazione ---


def test_signal_payload_full():
    payload = SignalPayload(
        symbol="XAUUSD",
        direction="BUY",
        entry_price=2650.50,
        stop_loss=2640.00,
        take_profits=[2660.00, 2670.00, 2680.00],
    )
    d = payload.to_dict()
    assert d["symbol"] == "XAUUSD"
    assert d["direction"] == "BUY"
    assert d["entry_price"] == 2650.50
    assert d["stop_loss"] == 2640.00
    assert d["take_profits"] == [2660.00, 2670.00, 2680.00]


def test_signal_payload_minimal():
    payload = SignalPayload(symbol="EURUSD", direction="SELL")
    d = payload.to_dict()
    assert d == {"symbol": "EURUSD", "direction": "SELL"}
    assert "entry_price" not in d
    assert "stop_loss" not in d
    assert "take_profits" not in d


def test_signal_payload_partial():
    payload = SignalPayload(
        symbol="BTCUSD",
        direction="BUY",
        stop_loss=60000.0,
    )
    d = payload.to_dict()
    assert d["stop_loss"] == 60000.0
    assert "entry_price" not in d
    assert "take_profits" not in d


# --- Contratto webhook: chiavi obbligatorie e tipi ---


def test_webhook_contract_required_keys():
    """Il payload deve sempre contenere symbol e direction."""
    payload = SignalPayload(symbol="XAUUSD", direction="BUY")
    d = payload.to_dict()
    assert "symbol" in d
    assert "direction" in d


def test_webhook_contract_direction_values():
    """direction deve essere BUY o SELL."""
    for valid in ("BUY", "SELL"):
        payload = SignalPayload(symbol="EURUSD", direction=valid)
        assert payload.to_dict()["direction"] == valid


def test_webhook_contract_symbol_is_string():
    payload = SignalPayload(symbol="XAUUSD", direction="BUY")
    assert isinstance(payload.to_dict()["symbol"], str)


def test_webhook_contract_entry_price_is_float():
    payload = SignalPayload(symbol="XAUUSD", direction="BUY", entry_price=2650.50)
    assert isinstance(payload.to_dict()["entry_price"], float)


def test_webhook_contract_take_profits_is_list():
    payload = SignalPayload(
        symbol="XAUUSD", direction="BUY", take_profits=[2660.0, 2670.0]
    )
    tp = payload.to_dict()["take_profits"]
    assert isinstance(tp, list)
    assert all(isinstance(v, float) for v in tp)


def test_webhook_contract_optional_fields_absent_when_none():
    """Campi opzionali non devono comparire nel dict se None."""
    payload = SignalPayload(symbol="EURUSD", direction="SELL")
    d = payload.to_dict()
    assert len(d) == 2


def test_webhook_contract_empty_take_profits():
    """Lista vuota di take_profits e' comunque inclusa nel payload."""
    payload = SignalPayload(symbol="XAUUSD", direction="BUY", take_profits=[])
    d = payload.to_dict()
    assert d["take_profits"] == []


# --- SignalSender.send() con mock httpx ---


@pytest.mark.asyncio
async def test_signal_sender_sends_correct_payload(httpx_mock):
    """Verifica che send() invii il JSON corretto all'URL configurato."""
    httpx_mock.add_response(
        url="http://testserver:8080/webhook/signal",
        json={"ok": True, "results": []},
    )

    sender = SignalSender(webhook_url="http://testserver:8080/webhook/signal")
    payload = SignalPayload(
        symbol="XAUUSD",
        direction="BUY",
        entry_price=2650.50,
        stop_loss=2640.00,
        take_profits=[2660.00, 2670.00, 2680.00],
    )
    result = await sender.send(payload)

    assert result == {"ok": True, "results": []}
    request = httpx_mock.get_request()
    assert request.method == "POST"
    assert request.headers["content-type"] == "application/json"
    import json

    body = json.loads(request.content)
    assert body["symbol"] == "XAUUSD"
    assert body["direction"] == "BUY"
    assert body["entry_price"] == 2650.50
    assert body["stop_loss"] == 2640.00
    assert body["take_profits"] == [2660.00, 2670.00, 2680.00]


@pytest.mark.asyncio
async def test_signal_sender_sends_minimal_payload(httpx_mock):
    """Payload minimo: solo symbol e direction."""
    httpx_mock.add_response(
        url="http://testserver:8080/webhook/signal",
        json={"ok": True, "results": []},
    )

    sender = SignalSender(webhook_url="http://testserver:8080/webhook/signal")
    payload = SignalPayload(symbol="EURUSD", direction="SELL")
    await sender.send(payload)

    import json

    body = json.loads(httpx_mock.get_request().content)
    assert body == {"symbol": "EURUSD", "direction": "SELL"}


@pytest.mark.asyncio
async def test_signal_sender_raises_on_http_error(httpx_mock):
    """send() deve propagare errori HTTP."""
    httpx_mock.add_response(
        url="http://testserver:8080/webhook/signal",
        status_code=500,
    )

    sender = SignalSender(webhook_url="http://testserver:8080/webhook/signal")
    payload = SignalPayload(symbol="XAUUSD", direction="BUY")

    with pytest.raises(httpx.HTTPStatusError):
        await sender.send(payload)


@pytest.mark.asyncio
async def test_signal_sender_raises_on_connection_error(httpx_mock):
    """send() deve propagare errori di connessione."""
    httpx_mock.add_exception(
        httpx.ConnectError("Connection refused"),
        url="http://unreachable:8080/webhook/signal",
    )

    sender = SignalSender(webhook_url="http://unreachable:8080/webhook/signal")
    payload = SignalPayload(symbol="XAUUSD", direction="BUY")

    with pytest.raises(httpx.ConnectError):
        await sender.send(payload)
