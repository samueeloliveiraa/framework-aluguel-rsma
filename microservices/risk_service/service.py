"""
MICROSERVIÇO 4: RiskService (Porta 8004)
Análise de Crédito, Risco Financeiro e Limite de Comprometimento.
"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler


class RiskHandler(BaseHTTPRequestHandler):

    def _send(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        self._send(200, {"status": "UP", "service": "RiskService", "port": 8004, "politica": "30% Margem Limite"})

    def do_POST(self):
        len_h = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(len_h).decode("utf-8")) if len_h > 0 else {}

        renda = body.get("renda", 5000.0)
        aluguel = body.get("aluguel", 1500.0)
        pct = round((aluguel / renda) * 100, 1) if renda > 0 else 100.0

        aprovado = pct <= 35.0
        self._send(200, {
            "aprovado": aprovado,
            "comprometimento_pct": pct,
            "risco": "BAIXO" if pct <= 30.0 else ("MEDIO" if pct <= 35.0 else "ALTO"),
            "garantia_sugerida": "Caução 3x" if aprovado else "Necessário Fiador/Cotitular"
        })


def run(port=8004):
    server = HTTPServer(("0.0.0.0", port), RiskHandler)
    print(f"📊 RiskService rodando na porta {port}...")
    server.serve_forever()


if __name__ == "__main__":
    run()
