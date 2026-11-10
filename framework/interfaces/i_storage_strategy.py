from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class IStorageStrategy(ABC):
    """
    Interface da Estratégia de Persistência de Dados.
    HOTSPOT 4 - Deve ser implementado por cada aplicação para definir onde
    e como persistir imóveis, propostas e contratos (SQLite, Memória, PostgreSQL).
    """

    @abstractmethod
    def salvar_contrato(self, contrato: Dict[str, Any]) -> bool:
        """Salva um contrato no repositório."""
        pass

    @abstractmethod
    def listar_contratos(self) -> List[Dict[str, Any]]:
        """Lista os contratos armazenados."""
        pass

    @abstractmethod
    def get_storage_name(self) -> str:
        """Retorna o nome da estratégia de armazenamento."""
        pass
