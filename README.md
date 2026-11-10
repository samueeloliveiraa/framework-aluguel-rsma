# Framework Didatico de Gestao de Aluguel de Imoveis
### Microsservicos + Componentes de Software + Agentes de IA
**Universidade Federal de Alagoas — Instituto de Computacao (UFAL/IC)**  
**Disciplina:** Reuso de Software e Metodologias Ageis | **Docente:** Prof. Dr. Arturo Hernandez Dominguez  
**Autor:** Francys Samuel Oliveira Pereira dos Santos  
**Repositorio:** [https://github.com/samueeloliveiraa/framework-aluguel-rsma](https://github.com/samueeloliveiraa/framework-aluguel-rsma)

Este projeto foi desenvolvido como um **framework conceitual e didatico**, simples e direto, para demonstrar na pratica como estruturar um sistema moderno de locacao de casas e apartamentos unindo tres pilares fundamentais da engenharia de software contemporanea:

1. **Microsservicos (Microservices)**: Divisao de responsabilidades de negocio e dados independentes.
2. **Componentes de Software**: Modulos desacoplados e reutilizaveis de logica de negocio pura.
3. **Agentes de Inteligencia Artificial (AI Agents)**: Entidades orientadas a objetivos com capacidade de raciocinio (ReAct) e acionamento dinamico de ferramentas (Tool Calling).

---

## 1. Arquitetura em Tres Pilares

```
                                  [INTERFACE DO USUARIO]
                                     (Streamlit Web)
                                            |
                                            v
                       +-----------------------------------------+
                       |       MICROSSERVICO DE AGENTE AI        |
                       |           (AIAgentService)              |
                       |    Loop ReAct: Percepcao -> Raciocinio  |
                       +--------------------+--------------------+
                                            | (Tool Calling)
                   +------------------------+------------------------+
                   |                        |                        |
                   v                        v                        v
       +----------------------+  +---------------------+  +---------------------+
       |   MICROSSERVICO      |  |    COMPONENTES      |  |   MICROSSERVICO     |
       |   PropertyService    |  |     REUTILIZAVEIS   |  |   ContractService   |
       |                      |  |                     |  |                     |
       | - Catalogo de Casas  |  | - PricingCalculator |  | - Emissao de Minuta |
       | - Catalogo de Aptos  |  | - RiskEvaluator     |  | - Assinatura        |
       | - Disponibilidade    |  | - Notification      |  | - Ciclo do Contrato |
       +----------+-----------+  +----------+----------+  +----------+----------+
                  |                         |                        |
                  +-------------------------+------------------------+
                                            |
                                            v
                               +-------------------------+
                               |       SERVICE BUS       |
                               |   Log & Rastreabilidade |
                               +-------------------------+
```

---

## 2. O que e cada parte? (Para Entender)

### 2.1 Microsservicos (Microservices)
Ao inves de um sistema monolitico gigante onde tudo fica no mesmo banco e no mesmo codigo:
- **`PropertyService`**: E o servico especialista em Imoveis. Ele gerencia quais casas e apartamentos existem, bairros, quartos, se aceitam pets e seu status (Disponivel ou Alugado).
- **`ContractService`**: E o servico especialista em Contratos. Cuida de prazos, minuta de contrato, garantias e assinatura.
- **`AIAgentService`**: E o servico autonomo de inteligencia, atuando como o consultor que interage com os clientes e consome os demais servicos.

### 2.2 Componentes de Software (Software Components)
Sao modulos de codigo reutilizaveis, de logica deterministica e testavel:
- **`PricingCalculatorComponent`**: Encapsula regras financeiras (calculo de caucao, seguro contra incendio, taxa administrativa e total mensal).
- **`RiskEvaluatorComponent`**: Encapsula a analise de credito (regras de comprometimento de renda ate 30% a 35%, score e garantia locaticia necessaria).
- **`NotificationComponent`**: Despacha alertas e notificacoes de eventos para inquilinos e proprietarios.

### 2.3 Agente de IA (AI Agent)
Um script tradicional apenas executa um `if/else`. Ja o **Agente de IA**:
- Possui um **Objetivo (Goal)**: Atender as necessidades de moradia do inquilino dentro da sua capacidade financeira real.
- Executa um **Ciclo ReAct (Reasoning + Acting)**:
  1. **Thought (Pensamento)**: Avalia o que o cliente pediu (ex: "tem cachorro e ganha R$ 8.500").
  2. **Action (Acao)**: Invoca a ferramenta de busca no `PropertyService`.
  3. **Observation (Observacao)**: Analisa os imoveis retornados.
  4. **Thought (Pensamento)**: Aciona o `RiskEvaluatorComponent` para verificar se a renda cobre o aluguel sem endividar o inquilino.
  5. **Final Answer (Decisao)**: Gera uma recomendacao explicada, ranqueada por score e orienta os proximos passos.

---

## 3. Como Executar

### Pre-requisitos
- Python 3.9+ instalado
- Streamlit

### Passo 1: Entrar no diretorio
```bash
cd framework_aluguel
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

## 4. Estrutura de Arquivos

```
framework_aluguel/
├── app.py                         # Interface Web visual basica (Streamlit)
├── run.sh                         # Script de inicializacao em 1 comando
├── requirements.txt               # Dependencias do projeto
├── README.md                      # Este guia conceitual
│
├── framework/                     # CAMADA DE REUSO (FRAMEWORK BASE)
│   ├── rental_framework.py        # Classe Abstrata com Template Method
│   ├── interfaces/                # Interfaces dos 4 Hotspots
│   ├── components/                # 8 Componentes de Software
│   └── applications/              # 2 Aplicacoes concretas
│
├── microservices/                 # MICROSSERVICOS DISTRIBUIDOS
│   ├── api_gateway/gateway.py     # Porta 8000
│   ├── property_service/          # Porta 8001
│   ├── contract_service/          # Porta 8002
│   ├── ai_service/                # Porta 8003
│   ├── risk_service/              # Porta 8004
│   └── run_all.py                 # Orquestrador dos servicos
│
└── gateway/                       # COMUNICACAO ENTRE SERVICOS
    └── event_bus.py               # Barramento de eventos e rastreabilidade
```
