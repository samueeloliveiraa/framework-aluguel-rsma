from typing import Dict, Any
from framework_aluguel.framework.interfaces.i_pricing_engine import IPricingEngine


class CStandardPricingEngine(IPricingEngine):
    """
    Componente de Precificação Padrão (Residencial Tradicional).
    - Caução: 3 meses de aluguel
    - Taxa administrativa: 5%
    - Seguro incêndio: 1.5%
    """

    def __init__(self, taxa_adm: float = 0.05, meses_caucao: int = 3):
        self.taxa_adm = taxa_adm
        self.meses_caucao = meses_caucao

    def calcular_custos(self, aluguel_base: float, condominio: float = 0.0, iptu: float = 0.0) -> Dict[str, Any]:
        seguro = round(aluguel_base * 0.015, 2)
        taxa = round(aluguel_base * self.taxa_adm, 2)
        total = round(aluguel_base + condominio + iptu + seguro + taxa, 2)
        caucao = round(aluguel_base * self.meses_caucao, 2)

        return {
            "aluguel_base": aluguel_base,
            "condominio": condominio,
            "iptu": iptu,
            "seguro_incendio": seguro,
            "taxa_administracao": taxa,
            "total_mensal": total,
            "caucao_exigida": caucao,
            "tipo_politica": "Padrão Residencial (3x Caução)"
        }

    def get_engine_name(self) -> str:
        return "CStandardPricingEngine (Tradicional 3x Caução)"
