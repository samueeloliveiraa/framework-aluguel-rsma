from typing import Dict, Any, List
from framework_aluguel.framework.interfaces.i_ai_agent import IAIAgentEngine


class CReActAIAgent(IAIAgentEngine):
    """
    Componente de Agente de IA com padrão ReAct (Reasoning + Acting).
    Executa ciclos de pensamento (Thought), ação de filtragem (Action),
    observação de compatibilidade (Observation) e tomada de decisão.
    """

    def raciocinar_e_recomendar(self, perfil_inquilino: Dict[str, Any], catalogo_imoveis: List[Dict[str, Any]]) -> Dict[str, Any]:
        nome = perfil_inquilino.get("nome", "Inquilino")
        renda = perfil_inquilino.get("renda", 0.0)
        tipo = perfil_inquilino.get("tipo", "Qualquer")
        tem_pet = perfil_inquilino.get("tem_pet", False)
        quartos_min = perfil_inquilino.get("quartos_min", 1)

        passos = []

        # 1. Thought 1
        passos.append({
            "fase": "Thought",
            "detalhes": f"Agente analisando perfil de {nome}: renda de R$ {renda:,.2f}, quartos>={quartos_min}, pet={tem_pet}, tipo={tipo}."
        })

        # 2. Action 1 & Observation 1
        candidatos = []
        for im in catalogo_imoveis:
            if tipo != "Qualquer" and im.get("tipo", "").lower() != tipo.lower():
                continue
            if im.get("quartos", 0) < quartos_min:
                continue
            if tem_pet and not im.get("aceita_pets", False):
                continue
            candidatos.append(im)

        passos.append({
            "fase": "Action",
            "detalhes": f"Filtragem semântica no catálogo de {len(catalogo_imoveis)} imóveis."
        })
        passos.append({
            "fase": "Observation",
            "detalhes": f"Encontrados {len(candidatos)} imóveis aderentes aos filtros físicos e de regras."
        })

        # 3. Thought 2 (Scoring e Raciocínio de Match)
        passos.append({
            "fase": "Thought",
            "detalhes": "Calculando afinidade e custo/benefício relativo para ranquear a melhor recomendação."
        })

        recomendacoes = []
        for im in candidatos:
            custo_total = im.get("custos", {}).get("total_mensal", im.get("aluguel_base", 0.0))
            comprometimento = round((custo_total / renda * 100), 1) if renda > 0 else 100.0

            score = 100.0 - (comprometimento * 1.1)
            score += im.get("quartos", 1) * 4
            score += im.get("vagas", 0) * 3
            score = max(10.0, min(100.0, round(score, 1)))

            rec = dict(im)
            rec["score_agente"] = score
            rec["comprometimento_estimado_pct"] = comprometimento
            recomendacoes.append(rec)

        recomendacoes.sort(key=lambda x: x["score_agente"], reverse=True)

        if recomendacoes:
            melhor = recomendacoes[0]
            parecer = (
                f"**Parecer do Agente ReAct:** Recomendo o imovel **{melhor['titulo']}** ({melhor['tipo']}). "
                f"Possui score de afinidade de **{melhor['score_agente']}/100** com comprometimento de **{melhor['comprometimento_estimado_pct']}%** da renda."
            )
        else:
            parecer = f"Aviso: Nao encontramos imoveis que atendam conjuntamente a todos os requisitos solicitados por {nome}."

        return {
            "motor": self.get_agent_name(),
            "passos_raciocinio": passos,
            "recomendacoes": recomendacoes,
            "parecer_sintese": parecer
        }

    def get_agent_name(self) -> str:
        return "CReActAIAgent (Raciocínio ReAct com Análise Multicritério)"
