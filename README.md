# 🏠 Framework Didático de Gestão de Aluguel de Imóveis
### Microsserviços + Componentes de Software + Agentes de IA
**Universidade Federal de Alagoas — Instituto de Computação (UFAL/IC)**  
**Disciplina:** Reuso de Software e Metodologias Ágeis | **Docente:** Prof. Dr. Arturo Hernández Domínguez  
**Autor:** Francys Samuel Oliveira Pereira dos Santos  
**Repositório:** [https://github.com/samueeloliveiraa/framework-aluguel-rsma](https://github.com/samueeloliveiraa/framework-aluguel-rsma)

Este projeto foi desenvolvido como um **framework conceitual e didático**, simples e direto, para demonstrar na prática como estruturar um sistema moderno de locação de casas e apartamentos unindo três pilares fundamentais da engenharia de software contemporânea:

1. **Microsserviços (Microservices)**: Divisão de responsabilidades de negócio e dados independentes.
2. **Componentes de Software**: Módulos desacoplados e reutilizáveis de lógica de negócio pura.
3. **Agentes de Inteligência Artificial (AI Agents)**: Entidades orientadas a objetivos com capacidade de raciocínio (ReAct) e acionamento dinâmico de ferramentas (Tool Calling).

---

## 🎯 Arquitetura em Três Pilares

```
                                  [INTERFACE DO USUÁRIO]
                                     (Streamlit Web)
                                            │
                                            ▼
                       ┌─────────────────────────────────────────┐
                       │       MICROSSERVIÇO DE AGENTE AI        │
                       │           (AIAgentService)              │
                       │    Loop ReAct: Percepção ➔ Raciocínio   │
                       └────────────────────┬────────────────────┘
                                            │ (Tool Calling)
                   ┌────────────────────────┼────────────────────────┐
                   │                        │                        │
                   ▼                        ▼                        ▼
       ┌──────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
       │   MICROSSERVIÇO      │  │    COMPONENTES      │  │   MICROSSERVIÇO     │
       │   PropertyService    │  │     REUTILIZÁVEIS   │  │   ContractService   │
       │                      │  │                     │  │                     │
       │ • Catálogo de Casas  │  │ • PricingCalculator │  │ • Emissão de Minuta │
       │ • Catálogo de Aptos  │  │ • RiskEvaluator     │  │ • Assinatura        │
       │ • Disponibilidade    │  │ • Notification      │  │ • Ciclo do Contrato │
       └──────────┬───────────┘  └──────────┬──────────┘  └──────────┬──────────┘
                  │                         │                        │
                  └─────────────────────────┼────────────────────────┘
                                            ▼
                               ┌─────────────────────────┐
                               │       SERVICE BUS       │
                               │   Log & Rastreabilidade │
                               └─────────────────────────┘
```

---

## 🧩 O que é cada parte? (Para Entender)

### 1. Microsserviços (Microservices)
Ao invés de um sistema monolítico gigante onde tudo fica no mesmo banco e no mesmo código:
- **`PropertyService`**: É o serviço especialista em Imóveis. Ele sabe quais casas e apartamentos existem, bairros, quartos, se aceitam pets e seu status (Disponível ou Alugado).
- **`ContractService`**: É o serviço especialista em Contratos. Cuida de prazos, minuta de contrato, garantias e assinatura.
- **`AIAgentService`**: É o serviço autônomo de inteligência, atuando como o consultor que interage com os clientes e consome os demais serviços.

### 2. Componentes de Software (Software Components)
São módulos de código reutilizáveis, de lógica determinística e testável:
- **`PricingCalculatorComponent`**: Encapsula regras financeiras (cálculo de caução, seguro contra incêndio, taxa administrativa e total mensal).
- **`RiskEvaluatorComponent`**: Encapsula a análise de crédito (regras de comprometimento de renda até 30% a 35%, score e garantia locatícia necessária).
- **`NotificationComponent`**: Despacha alertas e notificações de eventos para inquilinos e proprietários.

### 3. Agente de IA (AI Agent)
Um script tradicional apenas executa um `if/else`. Já o **Agente de IA**:
- Possui um **Objetivo (Goal)**: Atender às necessidades de moradia do inquilino dentro da sua capacidade financeira real.
- Executa um **Ciclo ReAct (Reasoning + Acting)**:
  1. **Thought (Pensamento)**: Avalia o que o cliente pediu (ex: "tem cachorro e ganha R$ 8.500").
  2. **Action (Ação)**: Invoca a ferramenta de busca no `PropertyService`.
  3. **Observation (Observação)**: Analisa os imóveis retornados.
  4. **Thought (Pensamento)**: Aciona o `RiskEvaluatorComponent` para verificar se a renda cobre o aluguel sem endividar o inquilino.
  5. **Final Answer (Decisão)**: Gera uma recomendação explicada, ranqueada por score e orienta os próximos passos.

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.9+ instalado
- Streamlit

### Passo 1: Entrar no diretório
```bash
cd /home/usuario/Samuel/LLMS/framework_aluguel
```

### Passo 2: Executar
```bash
./run.sh
```
Ou diretamente:
```bash
streamlit run app.py
```

Abra seu navegador em: `http://localhost:8501`

---

## 📂 Estrutura de Arquivos

```
framework_aluguel/
├── app.py                         # Interface Web visual básica (Streamlit)
├── run.sh                         # Script de inicialização em 1 comando
├── requirements.txt               # Dependências do projeto
├── README.md                      # Este guia conceitual
│
├── components/                    # COMPONENTES DE SOFTWARE
│   ├── pricing_component.py       # Cálculo de taxas, caução e custos totais
│   ├── risk_evaluator_component.py# Análise de crédito e comprometimento de renda
│   └── notification_component.py  # Despacho de mensagens e auditoria
│
├── services/                      # MICROSSERVIÇOS AUTÔNOMOS
│   ├── property_service.py        # Gestão de Casas e Apartamentos
│   ├── contract_service.py        # Gestão de Contratos de Locação
│   └── ai_agent_service.py        # Agente de IA com ciclo ReAct e Tool Calling
│
└── gateway/                       # COMUNICAÇÃO ENTRE SERVIÇOS
    └── event_bus.py               # Barramento de eventos e rastreabilidade
```
