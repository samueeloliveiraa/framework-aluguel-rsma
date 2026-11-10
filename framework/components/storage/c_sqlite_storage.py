import sqlite3
import json
from typing import Dict, Any, List
from framework_aluguel.framework.interfaces.i_storage_strategy import IStorageStrategy


class CSQLiteStorage(IStorageStrategy):
    """Componente de Persistência em Banco Relacional SQLite Local."""

    def __init__(self, db_path: str = "/tmp/aluguel_framework.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contratos (
                    id TEXT PRIMARY KEY,
                    inquilino TEXT,
                    imovel_id TEXT,
                    valor_mensal REAL,
                    dados_json TEXT
                )
            """)
            conn.commit()

    def salvar_contrato(self, contrato: Dict[str, Any]) -> bool:
        cid = contrato.get("contrato_id", "CTR-0")
        inquilino = contrato.get("inquilino_nome", "Desconhecido")
        imovel_id = contrato.get("imovel_id", "DESCONHECIDO")
        valor = contrato.get("valor_total_mensal", 0.0)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO contratos VALUES (?, ?, ?, ?, ?)",
                (cid, inquilino, imovel_id, valor, json.dumps(contrato))
            )
            conn.commit()
        return True

    def listar_contratos(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT dados_json FROM contratos")
            rows = cursor.fetchall()
            return [json.loads(r[0]) for r in rows]

    def get_storage_name(self) -> str:
        return f"CSQLiteStorage (SQLite em {self.db_path})"
