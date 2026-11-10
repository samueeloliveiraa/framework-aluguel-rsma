#!/bin/bash
# Script de execucao para o Framework de Aluguel
cd "$(dirname "$0")"
echo "=========================================================="
echo "Iniciando Framework de Aluguel (Microservices + AI)"
echo "=========================================================="
streamlit run app.py --server.headless true --server.port 8501
