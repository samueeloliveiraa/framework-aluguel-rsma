"""Interfaces dos Hotspots do Framework de Aluguel."""
from .i_pricing_engine import IPricingEngine
from .i_risk_evaluator import IRiskEvaluator
from .i_ai_agent import IAIAgentEngine
from .i_storage_strategy import IStorageStrategy

__all__ = ["IPricingEngine", "IRiskEvaluator", "IAIAgentEngine", "IStorageStrategy"]
