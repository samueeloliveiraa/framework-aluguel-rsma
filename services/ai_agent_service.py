"""
MICROSSERVIÇO: AIAgentService (Agente Inteligente de Locação)
Responsabilidade: Orquestrar busca, conciliar preferências, avaliar crédito e orientar o inquilino.

Padrão de Agente: ReAct (Reasoning + Acting)
- Percepção: Perfil e necessidades do inquilino
- Raciocínio: Pensamento sobre compatibilidade e risco
- Ferramentas (Tools):
    * tool_buscar_imoveis (PropertyService)
    * tool_avaliar_risco_financeiro (RiskEvaluatorComponent)
    * tool_simular_contrato (ContractService)
- Ação: Parecer final estruturado e recomendação ao usuário
"""
from typing import Dict, Any, List
from dataclasses import dataclass
from framework_aluguel.services.property_service import PropertyService
from framework_aluguel.services.contract_service import ContractService
from framework_aluguel.components.risk_evaluator_component import RiskEvaluatorComponent
from framework_aluguel.gateway.event_bus import bus


@dataclass
class AgentStep:
    etapa: str         # "Thought" (Pensamento), "Action" (Ação/Tool), "Observation" (Observação)
    descricao: str
    detalhes: Any = None


@dataclass
class AgentResponse:
    parecer: str
    recomendacoes: List[Dict[str, Any]]
    passos_executados: List[AgentStep]
    status_geral: str


class RentalAIAgent:
    """Agente de Inteligência Artificial para Gestão de Locação e Match Imobiliário."""

    def __init__(self, property_service: PropertyService, contract_service: ContractService):
        self.property_service = property_service
        self.contract_service = contract_service
        self.risk_evaluator = RiskEvaluatorComponent()

    def processar_solicitacao(
        self,
        nome_cliente: str,
        renda_mensal: float,
        tipo_desejado: str,      # "Apartamento", "Casa" ou "Qualquer"
        precisa_pet: bool,
        quartos_min: int,
        orcamento_max: float
    ) -> AgentResponse:
        """Executa o ciclo de raciocínio e ação (ReAct Loop) do Agente."""
        passos: List[AgentStep] = []

        # ==============================================================
        # PASSO 1: PERCEPÇÃO E RACIOCÍNIO INICIAL (Thought 1)
        # ==============================================================
        passos.append(AgentStep(
            etapa="Thought (Raciocínio)",
            descricao=(
                f"O inquilino {nome_cliente} possui renda de R$ {renda_mensal:,.2f}. "
                f"Critérios: Tipo={tipo_desejado}, Quartos>={quartos_min}, Aceita Pets={precisa_pet}, Orçamento Max=R$ {orcamento_max:,.2f}. "
                f"Devo consultar o microsserviço de Imóveis (PropertyService) para encontrar candidatos."
            )
        ))

        # ==============================================================
        # PASSO 2: AÇÃO DE FERRAMENTA (Action 1 -> PropertyService)
        # ==============================================================
        passos.append(AgentStep(
            etapa="Action (Chamada de Microsserviço)",
            descricao="Executando ferramenta: PropertyService.listar_imoveis()",
            detalhes={
                "tipo": tipo_desejado if tipo_desejado != "Qualquer" else None,
                "aceita_pets": precisa_pet,
                "quartos_min": quartos_min,
                "max_aluguel": orcamento_max
            }
        ))

        candidatos = self.property_service.listar_imoveis(
            tipo=tipo_desejado if tipo_desejado != "Qualquer" else None,
            aceita_pets=precisa_pet,
            quartos_min=quartos_min,
            max_aluguel=orcamento_max
        )

        passos.append(AgentStep(
            etapa="Observation (Observação)",
            descricao=f"PropertyService retornou {len(candidatos)} imóvel(is) elegível(is) no catálogo.",
            detalhes=[f"{c['id']} - {c['titulo']} (R$ {c['custos']['total_mensal']}/mês)" for c in candidatos]
        ))

        # Se nenhum imóvel for encontrado
        if not candidatos:
            passos.append(AgentStep(
                etapa="Thought (Raciocínio)",
                descricao="Nenhum imóvel atende concomitantemente todos os filtros de tipo, orçamento e pet. Devo orientar o cliente."
            ))
            return AgentResponse(
                parecer=f"Olá {nome_cliente}! Não encontramos imóveis disponíveis com exatamente essas características e teto de R$ {orcamento_max:,.2f}. Sugiro flexibilizar a faixa de valor ou os requisitos de quartos.",
                recomendacoes=[],
                passos_executados=passos,
                status_geral="SEM_RESULTADOS"
            )

        # ==============================================================
        # PASSO 3: RACIOCÍNIO FINANCEIRO E ANÁLISE DE RISCO (Thought 2 & Action 2)
        # ==============================================================
        passos.append(AgentStep(
            etapa="Thought (Raciocínio)",
            descricao=(
                "Agora preciso analisar a saúde financeira da operação para cada candidato. "
                "Vou acionar o Componente de Software 'RiskEvaluatorComponent' para testar se a renda "
                "comporta o aluguel sem ultrapassar o limiar de 30% a 35%."
            )
        ))

        imoveis_avaliados = []

        for imovel in candidatos:
            custo_total = imovel["custos"]["total_mensal"]

            # Aciona o Componente de Software de Risco
            avaliacao_risco = self.risk_evaluator.avaliar(
                renda_mensal=renda_mensal,
                custo_total_mensal=custo_total
            )

            # Cálculo de score de afinidade do Agente (0 a 100)
            score = 100.0
            # Penaliza comprometimento de renda
            score -= (avaliacao_risco.comprometimento_renda_pct * 1.2)
            # Bonifica se tiver vagas e quartos extras
            score += (imovel["quartos"] * 3) + (imovel["vagas"] * 2)
            score = max(10.0, min(100.0, round(score, 1)))

            imovel_analisado = dict(imovel)
            imovel_analisado["analise_risco"] = self.risk_evaluator.to_dict(avaliacao_risco)
            imovel_analisado["score_agente"] = score
            imoveis_avaliados.append(imovel_analisado)

        # Ordena pelo score calculado pelo Agente
        imoveis_avaliados.sort(key=lambda x: x["score_agente"], reverse=True)

        passos.append(AgentStep(
            etapa="Observation (Observação)",
            descricao=f"Análise de crédito concluída para {len(imoveis_avaliados)} opções.",
            detalhes=[
                f"{im['id']}: Risco {im['analise_risco']['nivel_risco']} "
                f"({im['analise_risco']['comprometimento_renda_pct']}% da renda) - Score Agente: {im['score_agente']}"
                for im in imoveis_avaliados
            ]
        ))

        # ==============================================================
        # PASSO 4: SÍNTESE E PARECER DO AGENTE (Final Answer)
        # ==============================================================
        melhor = imoveis_avaliados[0]
        risco_melhor = melhor["analise_risco"]

        if risco_melhor["aprovado"]:
            status_geral = "APROVADO_RECOMENDADO"
            passos.append(AgentStep(
                etapa="Thought (Raciocínio)",
                descricao=f"A melhor opção é o imóvel {melhor['id']} ({melhor['titulo']}). A renda atende as regras e o risco é aceitável. O cliente pode emitir a proposta de locação no ContractService."
            ))
            parecer = (
                f"🎯 **Parecer do Agente AI para {nome_cliente}:**\n\n"
                f"Encontrei **{len(imoveis_avaliados)} opção(ões)** compatível(is). "
                f"Sua melhor opção é **{melhor['titulo']}** ({melhor['tipo']}).\n\n"
                f"📊 **Análise Financeira:**\n"
                f"- Custo total: **R$ {melhor['custos']['total_mensal']:,.2f}/mês**\n"
                f"- Comprometimento de renda: **{risco_melhor['comprometimento_renda_pct']}%**\n"
                f"- Avaliação de risco: **{risco_melhor['nivel_risco']}**\n"
                f"- Garantia sugerida: **{risco_melhor['garantia_exigida']}**\n\n"
                f"💡 **Recomendação:** Seu perfil foi pré-aprovado! Você já pode gerar a minuta de contrato diretamente."
            )
        else:
            status_geral = "ATENCAO_RISCO"
            passos.append(AgentStep(
                etapa="Thought (Raciocínio)",
                descricao=f"Os imóveis encontrados ultrapassam a margem segura de comprometimento financeiro para a renda informada (R$ {renda_mensal})."
            ))
            parecer = (
                f"⚠️ **Parecer do Agente AI para {nome_cliente}:**\n\n"
                f"Encontramos imóveis fisicamente compatíveis, porém a análise financeira indicou **risco elevado**.\n"
                f"O imóvel mais próximo ({melhor['titulo']}) comprometeria **{risco_melhor['comprometimento_renda_pct']}%** da sua renda mensal.\n\n"
                f"📌 **Solução proposta pelo Agente:** Para locar este imóvel, recomendamos compor renda com outra pessoa ou apresentar garantia locatícia adicional."
            )

        bus.log_call(
            origem="Client/App",
            destino="AIAgentService",
            operacao="processar_solicitacao",
            payload={"cliente": nome_cliente, "renda": renda_mensal},
            resposta=f"Status: {status_geral}, Recomendações: {len(imoveis_avaliados)}"
        )

        return AgentResponse(
            parecer=parecer,
            recomendacoes=imoveis_avaliados,
            passos_executados=passos,
            status_geral=status_geral
        )
