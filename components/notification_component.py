"""
COMPONENTE DE SOFTWARE: NotificationComponent
Responsabilidade: Notificação e registro de eventos do ciclo de aluguel.
"""
from datetime import datetime
from typing import List, Dict, Any


class NotificationComponent:
    """Componente responsável por despachar notificações (E-mail, SMS, Webhooks)."""

    def __init__(self):
        self._history: List[Dict[str, Any]] = []

    def notificar(self, canal: str, destinatario: str, assunto: str, mensagem: str) -> Dict[str, Any]:
        evento = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "canal": canal,
            "destinatario": destinatario,
            "assunto": assunto,
            "mensagem": mensagem
        }
        self._history.append(evento)
        return evento

    def get_historico(self) -> List[Dict[str, Any]]:
        return list(self._history)
