"""
MICROSERVIÇO 1: PropertyService (Porta 8001)
Catálogo e Gestão de Imóveis (Casas e Apartamentos).
"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

PROPERTIES = [
    {
        "id": "APT-101",
        "tipo": "Apartamento",
        "titulo": "Apto Moderno no Centro",
        "bairro": "Centro",
        "quartos": 2,
        "vagas": 1,
        "aceita_pets": True,
        "aluguel_base": 2200.0,
        "condominio": 450.0,
        "iptu": 110.0,
        "status": "DISPONIVEL"
    },
    {
        "id": "APT-202",
        "tipo": "Apartamento",
        "titulo": "Studio Compacto Universitário",
        "bairro": "Universitário",
        "quartos": 1,
        "vagas": 0,
        "aceita_pets": False,
        "aluguel_base": 1400.0,
        "condominio": 280.0,
        "iptu": 60.0,
        "status": "DISPONIVEL"
    },
    {
        "id": "CASA-301",
        "tipo": "Casa",
        "titulo": "Casa Ampla com Quintal e Churrasqueira",
        "bairro": "Jardim das Flores",
        "quartos": 3,
        "vagas": 2,
        "aceita_pets": True,
        "aluguel_base": 3600.0,
        "condominio": 0.0,
        "iptu": 180.0,
        "status": "DISPONIVEL"
    },
    {
        "id": "CASA-402",
        "tipo": "Casa",
        "titulo": "Sobrado em Condomínio Fechado",
        "bairro": "Parque Verde",
        "quartos": 4,
        "vagas": 3,
        "aceita_pets": True,
        "aluguel_base": 5200.0,
        "condominio": 600.0,
        "iptu": 320.0,
        "status": "DISPONIVEL"
    }
]


class PropertyHandler(BaseHTTPRequestHandler):

    def _send(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"status": "UP", "service": "PropertyService", "port": 8001})
        else:
            self._send(200, {"imoveis": PROPERTIES, "total": len(PROPERTIES)})


def run(port=8001):
    server = HTTPServer(("0.0.0.0", port), PropertyHandler)
    print(f"PropertyService rodando na porta {port}...")
    server.serve_forever()


if __name__ == "__main__":
    run()
