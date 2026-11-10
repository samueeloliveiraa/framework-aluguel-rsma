"""
COMPONENTE DE SOFTWARE: RiskEvaluatorComponent
Responsabilidade: Análise de crédito e risco de inadimplência do inquilino.
Princípio: Regra de negócio encapsulada em componente puro, facilmente mockável ou plugável.
"""
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class RiskAssessment:
    aprovado: bool
    nivel_risco: str  # "BAIXO", "MEDIO", "ALTO", "REJEITADO"
    comprometimento_renda_pct: float
    motivo: str
    garantia_exigida: str


class RiskEvaluatorComponent:
    """Componente de Análise de Risco de Crédito Imobiliário."""

    def __init__(self, teto_comprometimento: float = 0.30):
        # Por padrão imobiliário brasileiro: aluguel não deve passar de 30% da renda bruta
        self.teto_comprometimento = teto_comprometimento

    def avaliar(self, renda_mensal: float, custo_total_mensal: float, score_credito: int = 750) -> RiskAssessment:
        if renda_mensal <= 0:
            return RiskAssessment(
                aprovado=False,
                nivel_risco="REJEITADO",
                comprometimento_renda_pct=100.0,
                motivo="Renda informada inválida ou zerada.",
                garantia_exigida="Nenhuma (Não elegível)"
            )

        comprometimento = custo_total_mensal / renda_mensal
        comprometimento_pct = round(comprometimento * 100, 1)

        if comprometimento <= self.teto_comprometimento and score_credito >= 700:
            return RiskAssessment(
                aprovado=True,
                nivel_risco="BAIXO",
                comprometimento_renda_pct=comprometimento_pct,
                motivo=f"Renda compatível (comprometimento de {comprometimento_pct}%, dentro do limite de 30%). Bom score.",
                garantia_exigida="Caução simples (1 a 2 meses) ou Sem Fiador."
            )
        elif comprometimento <= 0.35 and score_credito >= 550:
            return RiskAssessment(
                aprovado=True,
                nivel_risco="MEDIO",
                comprometimento_renda_pct=comprometimento_pct,
                motivo=f"Comprometimento de {comprometimento_pct}% ligeiramente acima do ideal (30%). Risco moderado.",
                garantia_exigida="Caução de 3 meses ou Fiador solidário."
            )
        elif comprometimento <= 0.45:
            return RiskAssessment(
                aprovado=False,
                nivel_risco="ALTO",
                comprometimento_renda_pct=comprometimento_pct,
                motivo=f"Comprometimento de renda elevado ({comprometimento_pct}%). Risco considerável de inadimplência.",
                garantia_exigida="Necessário compor renda com mais um inquilino ou Seguro-Fiança."
            )
        else:
            return RiskAssessment(
                aprovado=False,
                nivel_risco="REJEITADO",
                comprometimento_renda_pct=comprometimento_pct,
                motivo=f"Custo mensal ({custo_total_mensal}) consome {comprometimento_pct}% da renda líquida. Incompatível.",
                garantia_exigida="Não aprovado para esta faixa de valor."
            )

    def to_dict(self, assessment: RiskAssessment) -> Dict[str, Any]:
        return {
            "aprovado": assessment.aprovado,
            "nivel_risco": assessment.nivel_risco,
            "comprometimento_renda_pct": assessment.comprometimento_renda_pct,
            "motivo": assessment.motivo,
            "garantia_exigida": assessment.garantia_exigida
        }
