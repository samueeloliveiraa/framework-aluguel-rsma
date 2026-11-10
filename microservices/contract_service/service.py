"""
MICROSERVIÇO 2: ContractService (Porta 8002)
Emissão e Gestão do Ciclo de Vida de Contratos de Locação.
"""
import json
import uuid
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

CONTRACTS = []


class ContractHandler(BaseHTTPRequestHandler):

    def _send(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"status": "UP", "service": "ContractService", "port": 8002})
        else:
            self._send(200, {"contratos": CONTRACTS, "total": len(CONTRACTS)})

    def do_POST(self):
        len_h = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(len_h).decode("utf-8")) if len_h > 0 else {}

        novo_contrato = {
            "contrato_id": f"CTR-{str(uuid.uuid4())[:6].upper()}",
            "inquilino": body.get("inquilino", "Cliente Padrão"),
            "imovel_id": body.get("imovel_id", "APT-101"),
            "valor_mensal": body.get("valor_mensal", 2500.0),
            "status": "PROPOSTA_EMITIDA",
            "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        CONTRACTS.append(novo_contrato)
        self._send(201, {"mensagem": "Contrato criado", "contrato": novo_contrato})


def run(port=8002):
    server = HTTPServer(("0.0.0.0", port), ContractHandler)
    print(f"📝 ContractService rodando na porta {port}...")
    server.serve_forever()


if __name__ == "__main__":
    run()
