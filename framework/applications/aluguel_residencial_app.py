"""
APLICAÇÃO 1: AluguelResidencialApp
Construída REUSANDO o RentalFramework através do padrão Template Method.
Público-alvo: Famílias e inquilinos tradicionais (Casas e Apartamentos de médio/alto padrão).
Customização dos 4 Hotspots:
- Pricing: CStandardPricingEngine (3x caução, 5% taxa adm)
- Risco: CConservativeRiskEvaluator (Teto 30% renda, score 700+)
- Agente IA: CReActAIAgent (Raciocínio ReAct aprofundado)
- Storage: CSQLiteStorage (Banco relacional persistente)
"""
import sys
import os

# Adiciona diretório raiz ao sys.path para permitir execução direta
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from framework_aluguel.framework.rental_framework import RentalFramework
from framework_aluguel.framework.components.pricing.c_standard_pricing import CStandardPricingEngine
from framework_aluguel.framework.components.risk.c_conservative_risk import CConservativeRiskEvaluator
from framework_aluguel.framework.components.ai.c_react_agent import CReActAIAgent
from framework_aluguel.framework.components.storage.c_sqlite_storage import CSQLiteStorage


class AluguelResidencialApp(RentalFramework):
    """Aplicação 1 de Locação Residencial Tradicional."""

    def configurar_pricing(self) -> None:
        # Implementa Hotspot 1
        self.pricing_engine = CStandardPricingEngine(taxa_adm=0.05, meses_caucao=3)

    def configurar_risco(self) -> None:
        # Implementa Hotspot 2
        self.risk_evaluator = CConservativeRiskEvaluator()

    def configurar_agente_ia(self) -> None:
        # Implementa Hotspot 3
        self.ai_agent = CReActAIAgent()

    def configurar_storage(self) -> None:
        # Implementa Hotspot 4
        self.storage = CSQLiteStorage(db_path="/tmp/aluguel_residencial.db")


if __name__ == "__main__":
    app = AluguelResidencialApp()
    config = app.inicializar_framework()
    print("=" * 60)
    print(f"Aplicação 1 Inicializada: {app.get_framework_info()}")
    print("Componentes plugados nos Hotspots:")
    for k, v in config.items():
        print(f"  - {k}: {v}")
    print("=" * 60)
