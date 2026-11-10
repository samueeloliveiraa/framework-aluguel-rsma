from typing import Dict, Any
from framework_aluguel.framework.interfaces.i_risk_evaluator import IRiskEvaluator


class CFlexibleRiskEvaluator(IRiskEvaluator):
    """
    Componente de Análise de Risco Flexível (Universitário / Estudantil).
    - Comprometimento tolerado: até 45% da renda ou bolsa de estudos
    - Aceita comprovação de vínculo estudantil / fiador solidário familiar
    """

    def avaliar_credito(self, renda_mensal: float, custo_total_mensal: float, score_credito: int = 600) -> Dict[str, Any]:
        if renda_mensal <= 0:
            return {
                "aprovado": False,
                "nivel_risco": "REJEITADO",
                "comprometimento_pct": 100.0,
                "parecer": "Renda/Bolsa informada inválida.",
                "garantia_requerida": "Incompatível"
            }

        comprometimento = round((custo_total_mensal / renda_mensal) * 100, 1)

        if comprometimento <= 45.0:
            return {
                "aprovado": True,
                "nivel_risco": "BAIXO" if comprometimento <= 35.0 else "MEDIO",
                "comprometimento_pct": comprometimento,
                "parecer": f"Elegível para modalidade estudantil com comprometimento de {comprometimento}%.",
                "garantia_requerida": "Comprovante de matrícula + 1 mês de caução ou Fiador dos pais."
            }
        else:
            return {
                "aprovado": False,
                "nivel_risco": "ALTO",
                "comprometimento_pct": comprometimento,
                "parecer": f"Comprometimento de {comprometimento}% excede o limite tolerado de 45% até para linha estudantil.",
                "garantia_requerida": "Necessário inclusão de cotitular."
            }

    def get_evaluator_name(self) -> str:
        return "CFlexibleRiskEvaluator (Tolerância até 45% / Estudantil)"
