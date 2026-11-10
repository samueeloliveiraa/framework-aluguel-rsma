"""
INTERFACE VISUAL DO FRAMEWORK DE ALUGUEL DE IMOVEIS (UFAL IC 2026)
Integracao completa:
- Template Method com Hotspots e Frozen Spots
- Componentes de Software Reutilizaveis
- 2 Aplicacoes construidas a partir do Framework
- Agentes de IA com Loop ReAct
- Microservicos em portas dedicadas (8000 a 8004)
"""
import sys
import os
import urllib.request
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

import streamlit as st
from framework_aluguel.framework.applications.aluguel_residencial_app import AluguelResidencialApp
from framework_aluguel.framework.applications.aluguel_universitario_app import AluguelUniversitarioApp
from framework_aluguel.services.property_service import PropertyService
from framework_aluguel.services.contract_service import ContractService
from framework_aluguel.services.ai_agent_service import RentalAIAgent
from framework_aluguel.gateway.event_bus import bus

st.set_page_config(
    page_title="Framework de Aluguel | UFAL IC 2026",
    layout="wide"
)

# Inicializacao no Session State
if "app_residencial" not in st.session_state:
    st.session_state.app_residencial = AluguelResidencialApp()
    st.session_state.app_universitario = AluguelUniversitarioApp()
    st.session_state.ps = PropertyService()
    st.session_state.cs = ContractService(property_service=st.session_state.ps)
    st.session_state.agent = RentalAIAgent(property_service=st.session_state.ps, contract_service=st.session_state.cs)

app_res: AluguelResidencialApp = st.session_state.app_residencial
app_uni: AluguelUniversitarioApp = st.session_state.app_universitario
ps: PropertyService = st.session_state.ps
cs: ContractService = st.session_state.cs
agent: RentalAIAgent = st.session_state.agent

# Cabecalho Principal
st.title("Framework para Sistemas de Gerenciamento de Aluguel")
st.markdown("##### *Universidade Federal de Alagoas — Instituto de Computacao (UFAL/IC)*")
st.caption("Disciplina: **Reuso de Software e Metodologias Ageis** | Professor: **Dr. Arturo Hernandez Dominguez**")

st.info("""
Este sistema demonstra o reuso de software atraves de tres pilares:
1. **Framework Orientado a Objeto com Template Method**: Frozen spots fixos e 4 Hotspots de adaptacao.
2. **2 Aplicacoes Derivadas**: *AluguelResidencialApp* (Tradicional/Familiar) e *AluguelUniversitarioApp* (Estudantil/Flexivel).
3. **Arquitetura de Microservicos**: 5 servicos independentes operando em portas dedicadas (8000 a 8004).
""")

tabs = st.tabs([
    "Aplicacoes do Framework (Hotspots)",
    "Agente AI (Match & ReAct)",
    "Catalogo (PropertyService)",
    "Contratos (ContractService)",
    "Status dos Microservicos (Portas)",
    "Relatorio & Conceitos"
])

# ==============================================================================
# TAB 1: AS 2 APLICACOES DO FRAMEWORK (HOTSPOTS E FROZEN SPOTS)
# ==============================================================================
with tabs[0]:
    st.subheader("Demonstracao do Reuso: As 2 Aplicacoes Construidas")
    st.write("O `RentalFramework` define o **Template Method** fixo (`processar_fluxo_locacao`). As aplicacoes apenas customizam os **Hotspots**.")

    col_app1, col_app2 = st.columns(2)

    with col_app1:
        st.markdown("### Aplicacao 1: `AluguelResidencialApp`")
        st.caption("Voltada para locacao residencial tradicional de casas e apartamentos familiares.")
        config_res = app_res.inicializar_framework()

        with st.container(border=True):
            st.markdown(f"**Framework Base:** `{app_res.get_framework_info()}`")
            st.markdown(f"**Hotspot 1 (Pricing):** `{config_res['pricing_engine']}`")
            st.markdown(f"**Hotspot 2 (Risco):** `{config_res['risk_evaluator']}`")
            st.markdown(f"**Hotspot 3 (Agente AI):** `{config_res['ai_agent']}`")
            st.markdown(f"**Hotspot 4 (Storage):** `{config_res['storage_strategy']}`")

            st.divider()
            if st.button("Executar Teste da Aplicacao 1 (Residencial)", key="btn_app1"):
                catalogo = ps.listar_imoveis()
                perfil = {"nome": "Familia Oliveira", "renda": 12000.0, "tipo": "Casa", "quartos_min": 3, "tem_pet": True}
                resultado = app_res.processar_fluxo_locacao(perfil, catalogo)
                st.success("Fluxo Template Method executado com sucesso!")
                st.json(resultado["resultado_agente"]["parecer_sintese"])

    with col_app2:
        st.markdown("### Aplicacao 2: `AluguelUniversitarioApp`")
        st.caption("Voltada para estudantes universitarios, pos-graduandos e locacao de studios/temporada.")
        config_uni = app_uni.inicializar_framework()

        with st.container(border=True):
            st.markdown(f"**Framework Base:** `{app_uni.get_framework_info()}`")
            st.markdown(f"**Hotspot 1 (Pricing):** `{config_uni['pricing_engine']}`")
            st.markdown(f"**Hotspot 2 (Risco):** `{config_uni['risk_evaluator']}`")
            st.markdown(f"**Hotspot 3 (Agente AI):** `{config_uni['ai_agent']}`")
            st.markdown(f"**Hotspot 4 (Storage):** `{config_uni['storage_strategy']}`")

            st.divider()
            if st.button("Executar Teste da Aplicacao 2 (Universitario)", key="btn_app2"):
                catalogo = ps.listar_imoveis()
                perfil = {"nome": "Estudante Carlos", "renda": 3500.0, "tipo": "Apartamento", "quartos_min": 1, "tem_pet": False}
                resultado = app_uni.processar_fluxo_locacao(perfil, catalogo)
                st.success("Fluxo Template Method executado com sucesso!")
                st.json(resultado["resultado_agente"]["parecer_sintese"])

# ==============================================================================
# TAB 2: AGENTE DE IA (INQUILINO)
# ==============================================================================
with tabs[1]:
    st.subheader("Consultor Virtual Inteligente de Aluguel (AI Agent)")
    st.write("O agente analisa o perfil do cliente, calcula scores multicriterio e formula recomendacoes personalizadas.")

    c_left, c_right = st.columns([1, 2])
    with c_left:
        st.markdown("#### Parametros do Inquilino")
        nome = st.text_input("Nome", value="Samuel Silva")
        email = st.text_input("E-mail", value="samuel@exemplo.com")
        renda = st.number_input("Renda Mensal (R$)", 1000.0, 50000.0, 8500.0, 500.0)
        tipo = st.selectbox("Tipo de Imovel", ["Qualquer", "Apartamento", "Casa"])
        quartos = st.slider("Minimo de Quartos", 1, 4, 2)
        tem_pet = st.checkbox("Possui Pets", value=True)
        orcamento = st.number_input("Orcamento Maximo Mensal (R$)", 1000.0, 30000.0, 4500.0, 200.0)
        btn_ia = st.button("Acionar Agente AI", type="primary", use_container_width=True)

    with c_right:
        if btn_ia:
            with st.spinner("Agente executando loop ReAct (Thought -> Action -> Observation)..."):
                resp = agent.processar_solicitacao(nome, renda, tipo, tem_pet, quartos, orcamento)
                st.session_state.resp_ia = (resp, nome, email, renda)

        if "resp_ia" in st.session_state:
            resp, r_nome, r_email, r_renda = st.session_state.resp_ia
            if resp.status_geral == "APROVADO_RECOMENDADO":
                st.success(resp.parecer)
            elif resp.status_geral == "ATENCAO_RISCO":
                st.warning(resp.parecer)
            else:
                st.info(resp.parecer)

            with st.expander("Raciocinio Interno do Agente (ReAct Loop)", expanded=True):
                for p in resp.passos_executados:
                    st.markdown(f"**{p.etapa}:** {p.descricao}")
                    if p.detalhes:
                        st.caption(f"Detalhes: {p.detalhes}")
                    st.divider()

            if resp.recomendacoes:
                st.markdown("#### Imoveis Recomendados")
                for im in resp.recomendacoes:
                    c1, c2, c3 = st.columns([2, 1, 1])
                    with c1:
                        st.markdown(f"**{im['titulo']}** (`{im['id']}`) - *{im['tipo']}*")
                        st.caption(f"Bairro: {im['bairro']} | {im['quartos']} quartos | Pets: {'Sim' if im['aceita_pets'] else 'Nao'}")
                    with c2:
                        st.markdown(f"Total: :green[**R$ {im['custos']['total_mensal']:,.2f}/mes**]")
                    with c3:
                        if st.button(f"Gerar Proposta ({im['id']})", key=f"btn_p_{im['id']}"):
                            nova = cs.criar_proposta(im['id'], r_nome, r_email, r_renda)
                            st.success(f"Proposta #{nova['contrato_id']} emitida no ContractService!")
                            st.rerun()

# ==============================================================================
# TAB 3: CATALOGO DE IMOVEIS (PROPERTY SERVICE)
# ==============================================================================
with tabs[2]:
    st.subheader("Microsservico de Imoveis (PropertyService)")
    for im in ps.listar_imoveis():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {im['tipo']}: {im['titulo']} (`{im['id']}`)")
                st.write(f"**Bairro:** {im['bairro']} | **Quartos:** {im['quartos']} | **Pets:** {'Sim' if im['aceita_pets'] else 'Nao'}")
                st.caption(im['descricao'])
            with col2:
                st.markdown(f"**Status:** `{im['status']}`")
                st.markdown(f"**Aluguel Base:** R$ {im['aluguel_base']:,.2f}")
                st.markdown(f"**Condominio:** R$ {im['condominio']:,.2f}")
                st.markdown(f"**Total Mensal:** :green[**R$ {im['custos']['total_mensal']:,.2f}**]")

# ==============================================================================
# TAB 4: CONTRATOS (CONTRACT SERVICE)
# ==============================================================================
with tabs[3]:
    st.subheader("Microsservico de Contratos (ContractService)")
    contratos = cs.listar_contratos()
    if not contratos:
        st.info("Nenhuma proposta emitida ainda. Gere uma proposta na aba do Agente AI.")
    else:
        for c in contratos:
            with st.container(border=True):
                c1, c2, c3 = st.columns([2, 2, 1])
                with c1:
                    st.markdown(f"#### Contrato `{c['contrato_id']}`")
                    st.write(f"**Inquilino:** {c['inquilino_nome']}")
                    st.write(f"**Imovel:** {c['imovel_titulo']}")
                with c2:
                    st.write(f"**Valor Mensal:** R$ {c['valor_total_mensal']:,.2f}")
                    st.write(f"**Garantia:** {c['garantia_adotada']}")
                with c3:
                    st.markdown(f"**Status:** `{c['status']}`")
                    if c['status'] == "PROPOSTA_EMITIDA":
                        if st.button("Assinar Contrato", key=f"sign_{c['contrato_id']}"):
                            cs.assinar_contrato(c['contrato_id'])
                            st.success("Contrato assinado e ativado!")
                            st.rerun()

# ==============================================================================
# TAB 5: STATUS DOS MICROSERVICOS
# ==============================================================================
with tabs[4]:
    st.subheader("Status dos Microservicos em Execucao")
    st.write("Verificacao em tempo real dos endpoints de saude dos 5 microservicos:")

    servicos_info = [
        {"nome": "API Gateway", "porta": 8000, "url": "http://127.0.0.1:8000/health", "desc": "Ponto de entrada, roteamento e autenticacao"},
        {"nome": "PropertyService", "porta": 8001, "url": "http://127.0.0.1:8001/health", "desc": "Catalogo de casas e apartamentos"},
        {"nome": "ContractService", "porta": 8002, "url": "http://127.0.0.1:8002/health", "desc": "Ciclo de vida dos contratos e alugueis"},
        {"nome": "AIService", "porta": 8003, "url": "http://127.0.0.1:8003/health", "desc": "Motor de IA com inteligencia ReAct"},
        {"nome": "RiskService", "porta": 8004, "url": "http://127.0.0.1:8004/health", "desc": "Analise de credito e risco financeiro"}
    ]

    for s in servicos_info:
        col_s1, col_s2, col_s3, col_s4 = st.columns([2, 1, 1, 3])
        with col_s1:
            st.markdown(f"**{s['nome']}**")
        with col_s2:
            st.code(f"Porta {s['porta']}")
        with col_s3:
            try:
                with urllib.request.urlopen(s['url'], timeout=0.8) as resp:
                    if resp.status == 200:
                        st.success("[ONLINE]")
                    else:
                        st.warning(f"[{resp.status}]")
            except Exception:
                st.info("[STANDBY]")
        with col_s4:
            st.caption(s['desc'])
        st.divider()

    st.markdown("""
Para iniciar os 5 microservicos simultaneamente em portas reais de rede, execute no terminal:
```bash
python3 framework_aluguel/microservices/run_all.py
```
""")

# ==============================================================================
# TAB 6: RELATORIO E CONCEITOS
# ==============================================================================
with tabs[5]:
    st.subheader("Resumo dos Padroes de Reuso e Metodologias Ageis")
    st.markdown("""
- **Template Method (GoF):** Define o esqueleto de um algoritmo na classe base (`RentalFramework`), delegando a implementacao de passos especificos para subclasses (`AluguelResidencialApp` e `AluguelUniversitarioApp`).
- **Frozen Spots (Pontos Fixos):** Algoritmo canonico `processar_fluxo_locacao` e metadados do framework.
- **Hotspots (Pontos de Variacao):** `configurar_pricing()`, `configurar_risco()`, `configurar_agente_ia()`, `configurar_storage()`.
- **Componentes de Software:** Classes com alta coesao e baixo acoplamento (`CStandardPricingEngine`, `CConservativeRiskEvaluator`, etc.).
- **Microservicos:** Separacao de responsabilidades de rede (Portas 8000 a 8004) orquestrados pelo API Gateway.
- **Agentes de IA:** Loops ReAct que executam percepcao, raciocinio e acionamento de ferramentas.
""")
