from abc import ABC, abstractmethod
from typing import Dict, Any


class IPricingEngine(ABC):
    """
    Interface do Mecanismo de Precificação de Locação.
    HOTSPOT 1 - Deve ser implementado por cada aplicação para customizar
    as regras financeiras de cálculo do aluguel, taxas, caução e descontos.
    """

    @abstractmethod
    def calcular_custos(self, aluguel_base: float, condominio: float, iptu: float) -> Dict[str, Any]:
        """Calcula o detalhamento de custos e valores mensais."""
        pass

    @abstractmethod
    def get_engine_name(self) -> str:
        """Retorna a identificação do motor de precificação."""
        pass
