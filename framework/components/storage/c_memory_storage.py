from typing import Dict, Any, List
from framework_aluguel.framework.interfaces.i_storage_strategy import IStorageStrategy


class CMemoryStorage(IStorageStrategy):
    """Componente de Persistência Volátil em Memória RAM (para testes e prototipagem)."""

    def __init__(self):
        self._db: Dict[str, Dict[str, Any]] = {}

    def salvar_contrato(self, contrato: Dict[str, Any]) -> bool:
        cid = contrato.get("contrato_id", f"CTR-{len(self._db) + 1}")
        self._db[cid] = dict(contrato)
        return True

    def listar_contratos(self) -> List[Dict[str, Any]]:
        return list(self._db.values())

    def get_storage_name(self) -> str:
        return "CMemoryStorage (Em memória RAM)"
