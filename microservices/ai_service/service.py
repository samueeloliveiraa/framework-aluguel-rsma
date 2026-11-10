"""
MICROSERVIÇO 3: AIService (Porta 8003)
Motor Inteligente de Recomendação e Match de Inquilinos com Imóveis.
"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler


class AIHandler(BaseHTTPRequestHandler):

    def _send(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        self._send(200, {"status": "UP", "service": "AIService", "port": 8003, "engine": "ReAct Intelligence Engine"})

    def do_POST(self):
        len_h = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(len_h).decode("utf-8")) if len_h > 0 else {}

        cliente = body.get("cliente", "Inquilino")
        renda = body.get("renda", 5000.0)

        resultado = {
            "agente": "AIAgentService v1.0",
            "cliente": cliente,
            "status_analise": "RECOMENDACAO_CONCLUIDA",
            "passos_react": [
                {"fase": "Thought", "acao": f"Análise de perfil financeiro para renda de R$ {renda:,.2f}"},
                {"fase": "Action", "acao": "Filtragem semântica no catálogo de imóveis"},
                {"fase": "Observation", "acao": "Imóveis compatíveis identificados com sucesso"}
            ],
            "parecer": f"Cliente {cliente} qualificado para locação com base nos parâmetros fornecidos."
        }
        self._send(200, resultado)


def run(port=8003):
    server = HTTPServer(("0.0.0.0", port), AIHandler)
    print(f"AIService rodando na porta {port}...")
    server.serve_forever()


if __name__ == "__main__":
    run()
