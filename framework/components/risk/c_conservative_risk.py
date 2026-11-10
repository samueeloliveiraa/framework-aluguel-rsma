from typing import Dict, Any
from framework_aluguel.framework.interfaces.i_risk_evaluator import IRiskEvaluator


class CConservativeRiskEvaluator(IRiskEvaluator):
    """
    Componente de Análise de Risco Conservadora (Residencial Padrão).
    - Comprometimento máximo: 30% da renda líquida
    - Score de crédito mínimo: 700
    - Exigência de fiador ou caução integral de 3 meses
    """

    def avaliar_credito(self, renda_mensal: float, custo_total_mensal: float, score_credito: int = 750) -> Dict[str, Any]:
        if renda_mensal <= 0:
            return {
                "aprovado": False,
                "nivel_risco": "REJEITADO",
                "comprometimento_pct": 100.0,
                "parecer": "Renda informada é nula ou inválida.",
                "garantia_requerida": "Incompatível"
            }

        comprometimento = round((custo_total_mensal / renda_mensal) * 100, 1)

        if comprometimento <= 30.0 and score_credito >= 700:
            return {
                "aprovado": True,
                "nivel_risco": "BAIXO",
                "comprometimento_pct": comprometimento,
                "parecer": f"Aprovado integralmente com {comprometimento}% de comprometimento de renda.",
                "garantia_requerida": "Caução de 3 meses ou Fiador tradicional."
            }
        elif comprometimento <= 35.0:
            return {
                "aprovado": True,
                "nivel_risco": "MEDIO",
                "comprometimento_pct": comprometimento,
                "parecer": f"Comprometimento de {comprometimento}% ligeiramente acima dos 30%. Risco moderado.",
                "garantia_requerida": "Caução de 3 meses + Comprovação adicional de patrimônio."
            }
        else:
            return {
                "aprovado": False,
                "nivel_risco": "ALTO",
                "comprometimento_pct": comprometimento,
                "parecer": f"Comprometimento excessivo ({comprometimento}% > 35%). Risco elevado de inadimplência.",
                "garantia_requerida": "Requer composição de renda com segundo titular."
            }

    def get_evaluator_name(self) -> str:
        return "CConservativeRiskEvaluator (Teto 30% Renda / Score 700+)"
