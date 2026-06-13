<p align="center">
  <img src="./assets/etl-service-desk-banner.svg" alt="Banner do projeto ETL Service Desk Incidents" width="100%" />
</p>

<h1 align="center">ETL Service Desk Incidents</h1>

<p align="center">
  Pipeline em Python para processar incidentes de suporte, classificar chamados, calcular tempo de resolução, identificar violações de SLA e gerar saídas prontas para análise.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/ETL-Pipeline-0F766E?style=for-the-badge" alt="ETL Pipeline">
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Service%20Desk-SLA-7C3AED?style=for-the-badge" alt="Service Desk SLA">
  <img src="https://img.shields.io/badge/Status-Concluído-15803D?style=for-the-badge" alt="Status concluído">
</p>

---

## Visão geral

Este projeto simula um cenário de **Service Desk** no qual dados de incidentes precisam ser organizados e transformados em informações úteis para acompanhamento operacional.

O pipeline recebe um arquivo CSV, valida as colunas obrigatórias, remove registros inválidos e duplicados, classifica os chamados por categoria, calcula o tempo de resolução, compara cada incidente com a meta de SLA e gera três tipos de saída:

- arquivo CSV tratado;
- banco de dados SQLite;
- relatório em Markdown com indicadores consolidados.

O projeto foi desenvolvido utilizando apenas a **biblioteca padrão do Python**, sem dependências externas.

---

## Valor para o negócio

Em uma operação real de suporte, dados de chamados costumam estar espalhados, incompletos ou difíceis de analisar. Este projeto demonstra como um pipeline simples pode ajudar a:

- identificar categorias com maior volume de incidentes;
- acompanhar a distribuição dos chamados por prioridade;
- medir violações de SLA;
- padronizar dados antes de enviá-los para relatórios ou dashboards;
- criar uma base estruturada para análises futuras;
- reduzir trabalho manual na consolidação de informações operacionais.

---

## Arquitetura do pipeline

```mermaid
flowchart LR
    A[CSV de incidentes] --> B[Extração]
    B --> C[Validação de colunas]
    C --> D[Limpeza e deduplicação]
    D --> E[Classificação por regras]
    E --> F[Cálculo de resolução e SLA]
    F --> G[Agregações operacionais]
    G --> H[CSV tratado]
    G --> I[SQLite]
    G --> J[Relatório Markdown]
```

---

## Funcionalidades

### Extração

- leitura de arquivos CSV;
- validação das colunas obrigatórias;
- tratamento inicial dos registros de entrada.

### Transformação

- remoção de registros sem `ticket_id`;
- eliminação de chamados duplicados;
- cálculo do tempo de resolução em minutos;
- definição da meta de SLA conforme a prioridade;
- identificação de violação de SLA;
- enriquecimento com dia da semana e hora de abertura;
- classificação automática por palavras-chave.

### Carregamento

- geração de CSV tratado;
- criação de banco SQLite;
- geração de relatório em Markdown;
- consolidação por categoria e prioridade;
- cálculo da taxa de violação de SLA.

---

## Regras de SLA

| Prioridade | Meta de resolução |
|---|---:|
| P1 | 60 minutos |
| P2 | 120 minutos |
| P3 | 240 minutos |
| P4 | 480 minutos |

Um incidente é marcado como violação quando o tempo de resolução ultrapassa a meta definida para sua prioridade.

---

## Classificação dos chamados

A classificação é feita por regras simples baseadas em palavras-chave presentes no título e na descrição.

| Categoria | Exemplos de palavras-chave |
|---|---|
| Microsoft 365 | Outlook, Teams, Exchange, Defender, M365 |
| Rede | VPN, switch, latência, perda de pacote, roteador |
| Acesso | senha, MFA, permissão, bloqueio, falha de login |
| Backup | backup, restore, Veeam, job, storage |
| Servidor | categoria padrão quando nenhuma regra anterior é encontrada |

> O classificador é propositalmente simples e não utiliza machine learning. Ele demonstra uma primeira etapa de automação baseada em regras.

---

## Estrutura dos dados de entrada

| Campo | Descrição |
|---|---|
| `ticket_id` | Identificador único do incidente |
| `created_at` | Data e hora de abertura no formato ISO |
| `resolved_at` | Data e hora de resolução no formato ISO |
| `priority` | Prioridade P1, P2, P3 ou P4 |
| `category` | Categoria original do chamado |
| `title` | Título do incidente |
| `description` | Descrição do problema |
| `requester` | Solicitante do chamado |

---

## Campos gerados pelo pipeline

| Campo | Descrição |
|---|---|
| `resolution_minutes` | Tempo total de resolução em minutos |
| `sla_minutes` | Meta de SLA associada à prioridade |
| `is_sla_breach` | Indicador de violação: `0` ou `1` |
| `dow` | Dia da semana da abertura |
| `hour` | Hora de abertura |
| `category_pred` | Categoria calculada pelas regras |

---

## Resultado do exemplo atual

O repositório inclui um relatório gerado a partir de **500 incidentes sintéticos**.

| Indicador | Resultado |
|---|---:|
| Registros de entrada | 500 |
| Registros processados | 500 |
| Registros descartados | 0 |
| Violações de SLA em P1 | 70,09% |
| Violações de SLA em P2 | 38,10% |
| Violações de SLA em P3 | 0,00% |
| Violações de SLA em P4 | 0,00% |

Consulte o relatório completo em [`outputs/reports/summary.md`](./outputs/reports/summary.md).

---

## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/cmosantos/etl-service-desk-incidents.git
cd etl-service-desk-incidents
```

### 2. Crie o ambiente virtual

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale os requisitos

```bash
pip install -r requirements.txt
```

O projeto não possui bibliotecas externas; o arquivo existe apenas para documentar essa característica.

### 4. Gere os dados de exemplo

```bash
python -m src.generate_sample_data
```

Esse comando cria um arquivo com 500 incidentes sintéticos em:

```text
data/raw/incidents.csv
```

### 5. Execute o pipeline

```bash
python -m src.pipeline --input data/raw/incidents.csv
```

---

## Saídas geradas

```text
data/processed/incidents_clean.csv
outputs/db/incidents.sqlite
outputs/reports/summary.md
```

Também é possível personalizar os caminhos:

```bash
python -m src.pipeline \
  --input data/raw/incidents.csv \
  --clean_csv data/processed/incidents_clean.csv \
  --db outputs/db/incidents.sqlite \
  --report outputs/reports/summary.md
```

No PowerShell, use o acento grave para quebrar linhas:

```powershell
python -m src.pipeline `
  --input data/raw/incidents.csv `
  --clean_csv data/processed/incidents_clean.csv `
  --db outputs/db/incidents.sqlite `
  --report outputs/reports/summary.md
```

---

## Estrutura do projeto

```text
etl-service-desk-incidents/
├── assets/
│   └── etl-service-desk-banner.svg
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── architecture.md
│   └── data-dictionary.md
├── outputs/
│   ├── db/
│   └── reports/
│       └── summary.md
├── src/
│   ├── extract.py
│   ├── generate_sample_data.py
│   ├── load.py
│   ├── pipeline.py
│   └── transform.py
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Limitações atuais

- os dados utilizados são sintéticos;
- a classificação é baseada em palavras-chave;
- o banco SQLite grava os campos como texto;
- ainda não há interface gráfica ou dashboard;
- ainda não há testes automatizados.

Essas limitações foram mantidas de forma transparente porque o objetivo atual é demonstrar o fluxo ETL e o raciocínio operacional aplicado a incidentes de Service Desk.

---

## Próximas evoluções

- adicionar testes unitários;
- validar datas e prioridades com mensagens de erro mais claras;
- criar dashboard com indicadores de SLA;
- adicionar análise de tendência por período;
- integrar dados exportados de Jira ou outra ferramenta ITSM;
- substituir o classificador de regras por um modelo de machine learning;
- criar execução automatizada com GitHub Actions.

---

## Autor

**Cláudio Santos**  
Analista de Suporte Júnior | Microsoft 365 | Cloud e Automação com IA

- [GitHub](https://github.com/cmosantos)
- [LinkedIn](https://www.linkedin.com/in/claudio--santos/)
- [Portfólio](https://future-cloud-ai.lovable.app)
- [Hashnode](https://claudiosantos.hashnode.dev)

---

<p align="center">
  Projeto desenvolvido para demonstrar tratamento de dados, automação operacional e análise de incidentes de Service Desk com Python.
</p>
