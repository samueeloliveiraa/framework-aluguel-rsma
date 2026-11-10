from typing import Dict, Any
from framework_aluguel.framework.interfaces.i_pricing_engine import IPricingEngine


class CSeasonalPricingEngine(IPricingEngine):
    """
    Componente de Precificação Flexível / Universitária / Temporada.
    - Caução reduzida: 1 mês
    - Desconto de pontualidade: 10%
    - Taxa administrativa reduzida: 2%
    """

    def __init__(self, desconto_pontualidade_pct: float = 0.10):
        self.desconto_pct = desconto_pontualidade_pct

    def calcular_custos(self, aluguel_base: float, condominio: float = 0.0, iptu: float = 0.0) -> Dict[str, Any]:
        seguro = round(aluguel_base * 0.01, 2)
        desconto = round(aluguel_base * self.desconto_pct, 2)
        aluguel_com_desconto = round(aluguel_base - desconto, 2)
        total = round(aluguel_com_desconto + condominio + iptu + seguro, 2)
        caucao = round(aluguel_base * 1.0, 2)  # Apenas 1 mês

        return {
            "aluguel_base": aluguel_base,
            "desconto_pontualidade": desconto,
            "condominio": condominio,
            "iptu": iptu,
            "seguro_incendio": seguro,
            "total_mensal": total,
            "caucao_exigida": caucao,
            "tipo_politica": "Universitária / Flexível (1x Caução + 10% Desconto)"
        }

    def get_engine_name(self) -> str:
        return "CSeasonalPricingEngine (Universitário/Flexível 1x Caução)"
