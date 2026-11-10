"""Módulo Gateway e Comunicação de Microsserviços."""
from .event_bus import bus, ServiceBus

__all__ = ["bus", "ServiceBus"]
