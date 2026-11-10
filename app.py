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

st.set_page_config(
    page_title="Sistema de Aluguel | UFAL",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    :root {
        --bg: #f5f5f4;
        --panel: #ffffff;
        --soft: #f7f7f7;
        --stroke: rgba(15, 23, 42, 0.08);
        --text: #1f2937;
        --muted: #6b7280;
        --primary: #ff385c;
        --primary-dark: #e61d52;
        --success: #16a34a;
        --warning: #f59e0b;
        --shadow: 0 12px 28px rgba(15, 23, 42, 0.06);
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg);
        color: var(--text);
        font-family: Arial, Helvetica, sans-serif;
    }

    .block-container {
        max-width: 1280px;
        padding-top: 0.8rem;
        padding-bottom: 2.5rem;
    }

    header[data-testid="stHeader"],
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    #MainMenu {
        display: none;
    }

    .topbar {
        background: rgba(255,255,255,0.95);
        border: 1px solid var(--stroke);
        border-radius: 18px;
        padding: 0.9rem 1.1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .brand {
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        color: var(--text);
    }

    .nav-group {
        display: flex;
        align-items: center;
        gap: 0.85rem;
        font-size: 0.8rem;
        color: var(--muted);
        font-weight: 700;
    }

    .pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: #f3f4f6;
        border: 1px solid rgba(17,24,39,0.05);
        border-radius: 999px;
        padding: 0.4rem 0.7rem;
        color: var(--text);
    }

    .pill.primary {
        background: #111827;
        color: white;
        border: none;
        padding: 0.6rem 0.9rem;
    }

    .hero {
        background: #fff;
        border: 1px solid var(--stroke);
        border-radius: 26px;
        padding: 1.5rem 1.4rem 1.1rem 1.4rem;
        box-shadow: var(--shadow);
    }

    .hero h1 {
        margin: 0;
        font-size: 3.05rem;
        line-height: 1.02;
        letter-spacing: -0.07em;
        font-weight: 800;
        color: var(--text);
    }

    .hero p {
        margin-top: 0.6rem;
        color: var(--muted);
        font-size: 1.04rem;
    }

    .search-bar {
        display: grid;
        grid-template-columns: 1.4fr 1fr 1fr auto;
        gap: 0.7rem;
        margin-top: 1.1rem;
    }

    .search-box {
        min-height: 54px;
        display: flex;
        align-items: center;
        padding: 0 1rem;
        background: #f7f7f7;
        border: 1px solid rgba(17,24,39,0.08);
        border-radius: 12px;
        color: #374151;
        font-weight: 600;
    }

    .search-button {
        min-height: 54px;
        border: none;
        border-radius: 12px;
        background: linear-gradient(180deg, #ff385c 0%, #e61d52 100%);
        color: white;
        font-weight: 800;
        padding: 0 1.2rem;
        cursor: pointer;
    }

    .section-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.06em;
        margin: 2rem 0 0.9rem 0;
        color: var(--text);
    }

    .card-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0,1fr));
        gap: 1rem;
    }

    .listing-card {
        background: var(--panel);
        border: 1px solid var(--stroke);
        border-radius: 22px;
        overflow: hidden;
        box-shadow: 0 8px 16px rgba(15, 23, 42, 0.03);
    }

    .listing-thumb {
        height: 230px;
        background-size: cover;
        background-position: center;
        position: relative;
    }

    .listing-badge {
        position: absolute;
        left: 14px;
        top: 14px;
        background: rgba(255,255,255,0.92);
        border-radius: 999px;
        padding: 0.28rem 0.6rem;
        font-size: 0.7rem;
        line-height: 1;
        font-weight: 800;
        color: var(--text);
    }

    .listing-body {
        padding: 0.9rem 0.95rem 1rem 0.95rem;
    }

    .listing-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.6rem;
    }

    .listing-title {
        font-size: 1.06rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: var(--text);
    }

    .rating {
        font-size: 0.8rem;
        font-weight: 700;
        color: var(--text);
    }

    .listing-meta {
        color: var(--muted);
        margin-top: 0.35rem;
        font-size: 0.86rem;
        line-height: 1.45;
    }

    .price-row {
        margin-top: 0.7rem;
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: 0.5rem;
    }

    .price {
        font-size: 1.08rem;
        font-weight: 800;
        color: var(--text);
    }

    .period {
        font-size: 0.8rem;
        color: var(--muted);
        font-weight: 600;
    }

    .profile-wrap {
        display: grid;
        grid-template-columns: 1.8fr 1fr;
        gap: 1rem;
        margin-top: 0.5rem;
    }

    .panel {
        background: var(--panel);
        border: 1px solid var(--stroke);
        border-radius: 22px;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.03);
        padding: 1rem;
    }

    .panel-label {
        margin: 0 0 0.8rem 0;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--muted);
    }

    .form-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0,1fr));
        gap: 0.8rem;
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stSlider > div > div {
        background: #fff !important;
        border: 1px solid rgba(17,24,39,0.12) !important;
        border-radius: 12px !important;
    }

    .stButton > button {
        background: linear-gradient(180deg, #ff385c 0%, #e61d52 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        min-height: 44px !important;
        box-shadow: none !important;
    }

    div[data-testid="stNumberInput"],
    div[data-testid="stSlider"],
    div[data-testid="stSelectbox"],
    div[data-testid="stTextInput"] {
        background: transparent !important;
    }

    div[data-testid="stNumberInput"] > div,
    div[data-testid="stSlider"] > div,
    div[data-testid="stSelectbox"] > div,
    div[data-testid="stTextInput"] > div {
        background: #ffffff !important;
        border: 1px solid rgba(17,24,39,0.12) !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }

    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] input,
    div[data-testid="stTextInput"] input {
        background: #ffffff !important;
        color: #111827 !important;
    }

    div[data-testid="stSlider"] [role="slider"] {
        background: #ff385c !important;
        border: 2px solid #ff385c !important;
    }

    div[data-testid="stSlider"] [data-baseweb="slider"] > div > div:first-child {
        background: #e5e7eb !important;
    }

    .aside-box {
        background: linear-gradient(180deg, #ffffff 0%, #fafafa 100%);
        border: 1px solid var(--stroke);
        border-radius: 20px;
        padding: 1rem;
        min-height: 100%;
    }

    .aside-box h4 {
        margin: 0 0 0.8rem 0;
        font-size: 1.1rem;
        color: var(--text);
    }

    .check-list {
        margin: 0;
        padding-left: 1.2rem;
        color: var(--muted);
        line-height: 1.8;
    }

    .result-box {
        margin-top: 1rem;
        background: #fff;
        border: 1px solid var(--stroke);
        border-radius: 18px;
        padding: 0.9rem 1rem;
        box-shadow: 0 8px 16px rgba(15, 23, 42, 0.02);
        color: #374151;
        line-height: 1.6;
    }

    .result-box strong {
        color: var(--text);
    }

    .recommend-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0,1fr));
        gap: 1rem;
        margin-top: 1rem;
    }

    .recommend-card {
        background: #fff;
        border: 1px solid var(--stroke);
        border-radius: 18px;
        padding: 1rem;
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.02);
    }

    .recommend-card h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1.05rem;
        color: var(--text);
    }

    .recommend-card p {
        margin: 0.25rem 0;
        color: var(--muted);
    }

    .summary-box {
        background: #ffffff;
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 20px;
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.02);
    }

    .summary-box h4 {
        margin: 0 0 0.9rem 0;
        font-size: 1.2rem;
        font-weight: 800;
        color: #111827;
    }

    .summary-box ul {
        margin: 0;
        padding-left: 1.2rem;
        color: #475569;
        line-height: 1.9;
    }

    .recommend-banner {
        margin-top: 1rem;
        background: linear-gradient(180deg, #dff7eb 0%, #cfeee0 100%);
        border: 1px solid rgba(22, 163, 74, 0.2);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        color: #0f172a;
        font-size: 1.05rem;
        font-weight: 700;
        line-height: 1.5;
        box-shadow: 0 8px 18px rgba(22, 163, 74, 0.06);
    }

    @media (max-width: 980px) {
        .profile-wrap,
        .card-grid,
        .recommend-grid,
        .search-bar,
        .form-grid {
            grid-template-columns: 1fr;
        }

        .hero h1 {
            font-size: 2.4rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


if "app_residencial" not in st.session_state:
    st.session_state.app_residencial = AluguelResidencialApp()
    st.session_state.app_universitario = AluguelUniversitarioApp()
    st.session_state.ps = PropertyService()
    st.session_state.cs = ContractService(property_service=st.session_state.ps)
    st.session_state.agent = RentalAIAgent(property_service=st.session_state.ps, contract_service=st.session_state.cs)

app_res = st.session_state.app_residencial
ps = st.session_state.ps

st.markdown(
    """
    <div class="topbar">
      <div class="brand">Sistema de Aluguel</div>
      <div class="nav-group">
        <span class="pill">Explorar</span>
        <span class="pill">Inquilinos</span>
        <span class="pill primary">Entrar</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>Encontre um lugar que pareça seu lar</h1>
      <p>Uma interface elegante para demonstrar locação residencial com IA, risco financeiro e recomendação em um fluxo completo.</p>
      <div class="search-bar">
        <div class="search-box">Localização: Maceió, AL</div>
        <div class="search-box">Check-in</div>
        <div class="search-box">Check-out</div>
        <button class="search-button">Buscar</button>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Descubra opções exclusivas</div>', unsafe_allow_html=True)

imoveis = ps.listar_imoveis()[:4]
images = [
    "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=900&q=80",
]

cards = st.columns(4)
for idx, im in enumerate(imoveis):
    with cards[idx]:
        st.markdown(
            f"""
            <div class="listing-card">
              <div class="listing-thumb" style="background-image: url('{images[idx]}');">
                <span class="listing-badge">Preferido</span>
              </div>
              <div class="listing-body">
                <div class="listing-head">
                  <div class="listing-title">{im['titulo']}</div>
                  <div class="rating">★ 4.9</div>
                </div>
                <div class="listing-meta">{im['bairro']} · {im['quartos']} quartos · {im['banheiros']} banheiros</div>
                <div class="price-row">
                  <div class="price">R$ {im['aluguel_base']:,.2f}</div>
                  <div class="period">/ mês</div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-title">Perfil do inquilino</div>', unsafe_allow_html=True)

profile_wrap = st.container()
with profile_wrap:
    left_col, right_col = st.columns([2.2, 1.1])

    with left_col:
        with st.form("perfil_inquilino"):
            form_cols = st.columns(3)
            with form_cols[0]:
                nome = st.text_input("Nome", value="Maria Souza")
            with form_cols[1]:
                tipo = st.selectbox("Tipo desejado", ["Qualquer", "Apartamento", "Casa"], index=0)
            with form_cols[2]:
                tem_pet = st.checkbox("Aceita pets", value=True)

            second_cols = st.columns([1.15, 1.15, 1.1])
            with second_cols[0]:
                renda = st.number_input("Renda mensal", min_value=1500.0, max_value=50000.0, value=8500.0, step=100.0)
            with second_cols[1]:
                quartos_min = st.slider("Quartos mínimos", min_value=1, max_value=5, value=2)
            with second_cols[2]:
                orcamento = st.number_input("Orçamento máximo", min_value=1000.0, max_value=30000.0, value=4500.0, step=200.0)

            submitted = st.form_submit_button("Simular recomendação", use_container_width=True)

    with right_col:
        st.markdown(
            """
            <div class="summary-box">
              <h4>Preferências do inquilino</h4>
              <ul>
                <li>Perfil de renda validado</li>
                <li>Tipo de imóvel selecionado</li>
                <li>Quartos e pets considerados</li>
                <li>Match com IA em tempo real</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

if submitted:
    perfil = {
        "nome": nome,
        "renda": float(renda),
        "tipo": tipo,
        "quartos_min": int(quartos_min),
        "tem_pet": bool(tem_pet),
        "orcamento": float(orcamento),
    }
    resultado = app_res.processar_fluxo_locacao(perfil, ps.listar_imoveis())
    parecer = resultado["resultado_agente"]["parecer_sintese"]
    st.markdown(f'<div class="recommend-banner">{parecer}</div>', unsafe_allow_html=True)

    recomendacoes = resultado["resultado_agente"]["recomendacoes"]
    if recomendacoes:
        st.markdown('<div class="section-title" style="font-size: 1.7rem; margin-top: 1.5rem;">Top recomendações da IA</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for idx, rec in enumerate(recomendacoes[:3]):
            with cols[idx]:
                st.markdown(
                    f"""
                    <div class="recommend-card">
                      <h4>{rec['titulo']}</h4>
                      <p><strong>Tipo:</strong> {rec['tipo']}</p>
                      <p><strong>Score:</strong> {rec['score_agente']}/100</p>
                      <p><strong>Comprometimento:</strong> {rec['comprometimento_estimado_pct']}% da renda</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
