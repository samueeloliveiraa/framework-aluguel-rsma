from abc import ABC, abstractmethod
from typing import Dict, Any


class IRiskEvaluator(ABC):
    """
    Interface de Análise de Risco de Crédito e Inadimplência.
    HOTSPOT 2 - Deve ser implementado por cada aplicação para customizar
    as diretrizes de aprovação financeira (ex: conservadora x estudantil flexível).
    """

    @abstractmethod
    def avaliar_credito(self, renda_mensal: float, custo_total_mensal: float, score_credito: int = 700) -> Dict[str, Any]:
        """Realiza a análise de comprometimento de renda e elegibilidade."""
        pass

    @abstractmethod
    def get_evaluator_name(self) -> str:
        """Retorna o nome do avaliador de risco."""
        pass
