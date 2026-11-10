"""
ORQUESTRADOR DE MICROSERVIÇOS (Portas 8000 a 8004)
Inicia todos os 5 microserviços em portas dedicadas e exibe a tabela de status em tempo de execução.
"""
import sys
import os
import threading
import time
import urllib.request
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from framework_aluguel.microservices.api_gateway.gateway import run_gateway
from framework_aluguel.microservices.property_service.service import run as run_prop
from framework_aluguel.microservices.contract_service.service import run as run_contract
from framework_aluguel.microservices.ai_service.service import run as run_ai
from framework_aluguel.microservices.risk_service.service import run as run_risk

SERVICES = [
    ("API Gateway", 8000, run_gateway),
    ("PropertyService", 8001, run_prop),
    ("ContractService", 8002, run_contract),
    ("AIService", 8003, run_ai),
    ("RiskService", 8004, run_risk)
]


def start_all():
    print("=" * 75)
    print("🚀 INICIANDO ARQUITETURA DE MICROSERVIÇOS DE LOCAÇÃO (UFAL IC 2026)")
    print("=" * 75)

    threads = []
    for name, port, target_fn in SERVICES:
        t = threading.Thread(target=target_fn, args=(port,), daemon=True)
        t.start()
        threads.append(t)
        time.sleep(0.15)

    time.sleep(0.8)
    print("\n" + "=" * 75)
    print("📋 TABELA DE MICROSERVIÇOS EM EXECUÇÃO")
    print("=" * 75)
    print(f"{'Microsserviço':<22} {'Porta':<8} {'Status':<12} {'Health Endpoint'}")
    print("-" * 75)

    for name, port, _ in SERVICES:
        url = f"http://127.0.0.1:{port}/health"
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                status = "🟢 ONLINE" if resp.status == 200 else f"🟡 {resp.status}"
        except Exception:
            status = "🔴 OFFLINE"
        print(f"{name:<22} {port:<8} {status:<12} {url}")

    print("=" * 75)
    print("Pressione Ctrl+C para encerrar os serviços.")


if __name__ == "__main__":
    start_all()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nMicroserviços finalizados.")
