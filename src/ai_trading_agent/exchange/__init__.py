"""Modulo exchange — invio segnali di trading al broker Autotrade."""

from .signal_sender import SignalPayload, SignalSender

__all__ = [
    "SignalPayload",
    "SignalSender",
]
