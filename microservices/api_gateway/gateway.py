"""
API GATEWAY (Porta 8000)
Ponto único de entrada, autenticação, roteamento e proxy para os microserviços.
"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error

# Mapeamento dos microserviços e suas portas dedicadas
SERVICES = {
    "properties": "http://127.0.0.1:8001",
    "contracts": "http://127.0.0.1:8002",
    "ai": "http://127.0.0.1:8003",
    "risk": "http://127.0.0.1:8004"
}

PUBLIC_ROUTES = ["/health", "/api/properties", "/docs"]


class APIGatewayHandler(BaseHTTPRequestHandler):

    def _send_json(self, status: int, data: dict):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        # Health check da Gateway e do status de todos os microserviços
        if self.path == "/health" or self.path == "/":
            self._send_json(200, {
                "gateway": "API Gateway Online",
                "porta": 8000,
                "servicos_registrados": {
                    "PropertyService": "Porta 8001 (/api/properties)",
                    "ContractService": "Porta 8002 (/api/contracts)",
                    "AIService": "Porta 8003 (/api/ai)",
                    "RiskService": "Porta 8004 (/api/risk)"
                }
            })
            return

        # Roteamento para microserviços
        for prefix, target_url in SERVICES.items():
            if self.path.startswith(f"/api/{prefix}"):
                sub_path = self.path[len(f"/api/{prefix}"):] or "/"
                url = f"{target_url}{sub_path}"
                try:
                    req = urllib.request.Request(url, method="GET")
                    with urllib.request.urlopen(req, timeout=3) as resp:
                        res_data = json.loads(resp.read().decode("utf-8"))
                        self._send_json(resp.status, res_data)
                        return
                except Exception as e:
                    self._send_json(502, {"error": f"Falha ao conectar no microserviço {prefix}: {str(e)}"})
                    return

        self._send_json(404, {"error": f"Rota não encontrada no Gateway: {self.path}"})

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b"{}"

        for prefix, target_url in SERVICES.items():
            if self.path.startswith(f"/api/{prefix}"):
                sub_path = self.path[len(f"/api/{prefix}"):] or "/"
                url = f"{target_url}{sub_path}"
                try:
                    req = urllib.request.Request(url, data=post_data, headers={"Content-Type": "application/json"}, method="POST")
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        res_data = json.loads(resp.read().decode("utf-8"))
                        self._send_json(resp.status, res_data)
                        return
                except Exception as e:
                    self._send_json(502, {"error": f"Falha ao conectar no microserviço {prefix}: {str(e)}"})
                    return

        self._send_json(404, {"error": "Endpoint não encontrado no Gateway"})


def run_gateway(port=8000):
    server = HTTPServer(("0.0.0.0", port), APIGatewayHandler)
    print(f"API Gateway rodando na porta {port}...")
    server.serve_forever()


if __name__ == "__main__":
    run_gateway()
