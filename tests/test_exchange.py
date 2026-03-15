"""Test per il modulo exchange (signal sender)."""

from ai_trading_agent.exchange import SignalPayload, SignalSender


def test_signal_sender_default_url():
    sender = SignalSender()
    assert sender.webhook_url == "http://ollasrv:8080/webhook/signal"


def test_signal_sender_custom_url():
    sender = SignalSender(webhook_url="http://localhost:9090/webhook/signal")
    assert sender.webhook_url == "http://localhost:9090/webhook/signal"


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
