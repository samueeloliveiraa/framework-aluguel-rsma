"""
COMPONENTE DE SOFTWARE: PricingCalculatorComponent
Responsabilidade: Cálculo de custos, taxas, caução e custos mensais totais de locação.
Princípio: Alta coesão, baixo acoplamento e interface determinística.
"""
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class PricingBreakdown:
    aluguel_base: float
    condominio: float
    iptu: float
    seguro_incendio: float
    taxa_servico: float
    total_mensal: float
    caucao_sugerida: float


class PricingCalculatorComponent:
    """Componente reutilizável para cálculos financeiros de locação."""

    def __init__(self, taxa_servico_pct: float = 0.05, meses_caucao: int = 3):
        self.taxa_servico_pct = taxa_servico_pct
        self.meses_caucao = meses_caucao

    def calcular_custos(self, aluguel_base: float, condominio: float = 0.0, iptu: float = 0.0) -> PricingBreakdown:
        """Calcula o detalhamento de custos e valores de entrada."""
        # Seguro contra incêndio estimado proporcional ao aluguel
        seguro_incendio = round(aluguel_base * 0.015, 2)
        taxa_servico = round(aluguel_base * self.taxa_servico_pct, 2)
        total_mensal = round(aluguel_base + condominio + iptu + seguro_incendio + taxa_servico, 2)
        caucao = round(aluguel_base * self.meses_caucao, 2)

        return PricingBreakdown(
            aluguel_base=aluguel_base,
            condominio=condominio,
            iptu=iptu,
            seguro_incendio=seguro_incendio,
            taxa_servico=taxa_servico,
            total_mensal=total_mensal,
            caucao_sugerida=caucao
        )

    def to_dict(self, breakdown: PricingBreakdown) -> Dict[str, Any]:
        return {
            "aluguel_base": breakdown.aluguel_base,
            "condominio": breakdown.condominio,
            "iptu": breakdown.iptu,
            "seguro_incendio": breakdown.seguro_incendio,
            "taxa_servico": breakdown.taxa_servico,
            "total_mensal": breakdown.total_mensal,
            "caucao_sugerida": breakdown.caucao_sugerida
        }
