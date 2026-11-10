"""
INFRAESTRUTURA DE MICROSSERVIÇOS: Service Bus & Event Logger
Permite comunicação desacoplada entre microsserviços e rastreabilidade didática.
"""
from typing import Dict, Any, List
from datetime import datetime


class ServiceBus:
    """Barramento simulado de comunicação entre microsserviços com log em tempo real."""

    def __init__(self):
        self.logs: List[Dict[str, Any]] = []

    def log_call(self, origem: str, destino: str, operacao: str, payload: Any, resposta: Any):
        registro = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "origem": origem,
            "destino": destino,
            "operacao": operacao,
            "payload": payload,
            "resposta": resposta
        }
        self.logs.append(registro)

    def obter_logs(self) -> List[Dict[str, Any]]:
        return list(self.logs)

    def limpar_logs(self):
        self.logs.clear()


# Instância global do barramento
bus = ServiceBus()
