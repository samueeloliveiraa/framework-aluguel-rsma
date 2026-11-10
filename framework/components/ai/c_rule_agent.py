from typing import Dict, Any, List
from framework_aluguel.framework.interfaces.i_ai_agent import IAIAgentEngine


class CRuleBasedAIAgent(IAIAgentEngine):
    """
    Componente de Agente de IA Baseado em Regras e Heurísticas Rápidas.
    Focado em decisões determinísticas com baixa latência para estudantes ou aluguel rápido.
    """

    def raciocinar_e_recomendar(self, perfil_inquilino: Dict[str, Any], catalogo_imoveis: List[Dict[str, Any]]) -> Dict[str, Any]:
        tipo = perfil_inquilino.get("tipo", "Qualquer")
        tem_pet = perfil_inquilino.get("tem_pet", False)

        candidatos = []
        for im in catalogo_imoveis:
            if tipo != "Qualquer" and im.get("tipo", "").lower() != tipo.lower():
                continue
            if tem_pet and not im.get("aceita_pets", False):
                continue
            candidatos.append(im)

        # Ordena pelo menor custo total
        candidatos.sort(key=lambda x: x.get("custos", {}).get("total_mensal", 999999))

        return {
            "motor": self.get_agent_name(),
            "passos_raciocinio": [
                {"fase": "Regra 1", "detalhes": "Filtro booleano por tipo de imóvel e aceitação de pets"},
                {"fase": "Regra 2", "detalhes": "Ordenação econômica pelo menor valor total mensal"}
            ],
            "recomendacoes": candidatos,
            "parecer_sintese": f"Encontradas {len(candidatos)} opções ordenadas pelo critério de menor custo financeiro."
        }

    def get_agent_name(self) -> str:
        return "CRuleBasedAIAgent (Motor Heurístico de Menor Custo)"
