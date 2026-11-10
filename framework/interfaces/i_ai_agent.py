from abc import ABC, abstractmethod
from typing import Dict, Any, List


class IAIAgentEngine(ABC):
    """
    Interface do Motor do Agente de Inteligência Artificial.
    HOTSPOT 3 - Deve ser implementado por cada aplicação para definir a estratégia
    de raciocínio do agente (ex: ReAct multi-etapas, regras heurísticas, LLM avançado).
    """

    @abstractmethod
    def raciocinar_e_recomendar(self, perfil_inquilino: Dict[str, Any], catalogo_imoveis: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Executa o ciclo de raciocínio e gera recomendações e parecer."""
        pass

    @abstractmethod
    def get_agent_name(self) -> str:
        """Retorna o nome do motor de agente de IA."""
        pass
