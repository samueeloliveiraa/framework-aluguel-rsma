from abc import ABC, abstractmethod
from typing import Dict, Any, List
from framework_aluguel.framework.interfaces.i_pricing_engine import IPricingEngine
from framework_aluguel.framework.interfaces.i_risk_evaluator import IRiskEvaluator
from framework_aluguel.framework.interfaces.i_ai_agent import IAIAgentEngine
from framework_aluguel.framework.interfaces.i_storage_strategy import IStorageStrategy


class RentalFramework(ABC):
    """
    Classe base do Framework de Locação de Imóveis (Apartamentos e Casas).
    Implementa o padrão de projeto Template Method.

    ESTE É O NÚCLEO DO FRAMEWORK:
    - Frozen Spots: Partes fixas que definem a arquitetura e a ordem de execução do fluxo.
    - Hotspots: Pontos de variação customizáveis implementados pelas aplicações derivadas.
    """

    def __init__(self):
        # Componentes definidos pelos hotspots
        self.pricing_engine: IPricingEngine = None
        self.risk_evaluator: IRiskEvaluator = None
        self.ai_agent: IAIAgentEngine = None
        self.storage: IStorageStrategy = None

    # =========================================================================
    # TEMPLATE METHOD (FROZEN SPOT): Define o algoritmo fixo de inicialização
    # Este método não deve ser sobrescrito pelas subclasses!
    # =========================================================================
    def inicializar_framework(self) -> Dict[str, Any]:
        """Orquestra a configuração inicial dos 4 hotspots na ordem correta."""
        self.configurar_pricing()
        self.configurar_risco()
        self.configurar_agente_ia()
        self.configurar_storage()
        return self.obter_configuracao_consolidada()

    # =========================================================================
    # TEMPLATE METHOD DE PROCESSO (FROZEN SPOT): Fluxo padrão de processamento
    # =========================================================================
    def processar_fluxo_locacao(self, perfil_inquilino: Dict[str, Any], catalogo_imoveis: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executa o fluxo canônico de atendimento de aluguel:
        1. Enriquecimento de preços com o PricingEngine configurado (Hotspot 1)
        2. Avaliação de risco financeiro com o RiskEvaluator configurado (Hotspot 2)
        3. Raciocínio do Agente de IA para matching e recomendação (Hotspot 3)
        4. Preparação da minuta para persistência no Storage (Hotspot 4)
        """
        # Garante que os componentes foram inicializados
        if not all([self.pricing_engine, self.risk_evaluator, self.ai_agent, self.storage]):
            self.inicializar_framework()

        # 1. Enriquecimento com precificação
        imoveis_precificados = []
        for im in catalogo_imoveis:
            item = dict(im)
            custos = self.pricing_engine.calcular_custos(
                aluguel_base=im.get("aluguel_base", 0.0),
                condominio=im.get("condominio", 0.0),
                iptu=im.get("iptu", 0.0)
            )
            item["custos"] = custos
            imoveis_precificados.append(item)

        # 2. Raciocínio e recomendação pelo Agente de IA
        resultado_agente = self.ai_agent.raciocinar_e_recomendar(
            perfil_inquilino=perfil_inquilino,
            catalogo_imoveis=imoveis_precificados
        )

        # 3. Consolidação final
        return {
            "framework": self.get_framework_info(),
            "perfil_inquilino": perfil_inquilino,
            "componentes_ativos": self.obter_configuracao_consolidada(),
            "resultado_agente": resultado_agente
        }

    # =========================================================================
    # HOTSPOTS: Métodos abstratos que cada aplicação DEVE customizar
    # =========================================================================
    @abstractmethod
    def configurar_pricing(self) -> None:
        """HOTSPOT 1: Define qual motor de precificação e taxas utilizar."""
        pass

    @abstractmethod
    def configurar_risco(self) -> None:
        """HOTSPOT 2: Define a política de análise de crédito e garantias."""
        pass

    @abstractmethod
    def configurar_agente_ia(self) -> None:
        """HOTSPOT 3: Define o agente de IA e sua estratégia de raciocínio."""
        pass

    @abstractmethod
    def configurar_storage(self) -> None:
        """HOTSPOT 4: Define a estratégia de persistência de dados."""
        pass

    # =========================================================================
    # FROZEN SPOTS COMPLEMENTARES
    # =========================================================================
    def obter_configuracao_consolidada(self) -> Dict[str, Any]:
        """Retorna o inventário dos componentes plugados nos hotspots."""
        return {
            "pricing_engine": self.pricing_engine.get_engine_name() if self.pricing_engine else None,
            "risk_evaluator": self.risk_evaluator.get_evaluator_name() if self.risk_evaluator else None,
            "ai_agent": self.ai_agent.get_agent_name() if self.ai_agent else None,
            "storage_strategy": self.storage.get_storage_name() if self.storage else None
        }

    def get_framework_info(self) -> str:
        """Retorna a identificação oficial do framework."""
        return "RentalFramework v1.0 - UFAL IC 2026"
