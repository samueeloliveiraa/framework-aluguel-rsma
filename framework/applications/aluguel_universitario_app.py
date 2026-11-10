"""
APLICAÇÃO 2: AluguelUniversitarioApp
Construída REUSANDO o RentalFramework através do padrão Template Method.
Público-alvo: Estudantes universitários, pós-graduandos e locações de temporada/studios.
Customização dos 4 Hotspots:
- Pricing: CSeasonalPricingEngine (1x caução, 10% desconto pontualidade)
- Risco: CFlexibleRiskEvaluator (Teto flexível até 45%, comprovação de matrícula)
- Agente IA: CRuleBasedAIAgent (Otimização econômica e agilidade)
- Storage: CSQLiteStorage (Banco local)
"""
import sys
import os

# Adiciona diretório raiz ao sys.path para permitir execução direta
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from framework_aluguel.framework.rental_framework import RentalFramework
from framework_aluguel.framework.components.pricing.c_seasonal_pricing import CSeasonalPricingEngine
from framework_aluguel.framework.components.risk.c_flexible_risk import CFlexibleRiskEvaluator
from framework_aluguel.framework.components.ai.c_rule_agent import CRuleBasedAIAgent
from framework_aluguel.framework.components.storage.c_sqlite_storage import CSQLiteStorage


class AluguelUniversitarioApp(RentalFramework):
    """Aplicação 2 de Locação Universitária e Estudantil."""

    def configurar_pricing(self) -> None:
        # Implementa Hotspot 1
        self.pricing_engine = CSeasonalPricingEngine(desconto_pontualidade_pct=0.10)

    def configurar_risco(self) -> None:
        # Implementa Hotspot 2
        self.risk_evaluator = CFlexibleRiskEvaluator()

    def configurar_agente_ia(self) -> None:
        # Implementa Hotspot 3
        self.ai_agent = CRuleBasedAIAgent()

    def configurar_storage(self) -> None:
        # Implementa Hotspot 4
        self.storage = CSQLiteStorage(db_path="/tmp/aluguel_universitario.db")


if __name__ == "__main__":
    app = AluguelUniversitarioApp()
    config = app.inicializar_framework()
    print("=" * 60)
    print(f"Aplicação 2 Inicializada: {app.get_framework_info()}")
    print("Componentes plugados nos Hotspots:")
    for k, v in config.items():
        print(f"  - {k}: {v}")
    print("=" * 60)
