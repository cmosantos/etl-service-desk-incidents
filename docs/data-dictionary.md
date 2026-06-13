# Dicionário de dados

Este documento descreve os campos utilizados pelo projeto ETL Service Desk Incidents.

## Dados de entrada

| Campo | Tipo esperado | Obrigatório | Exemplo | Descrição |
|---|---|---:|---|---|
| `ticket_id` | texto | Sim | `INC000001` | Identificador único do incidente |
| `created_at` | data ISO | Sim | `2025-12-01T08:30:00` | Data e hora de abertura |
| `resolved_at` | data ISO | Sim | `2025-12-01T09:45:00` | Data e hora de resolução |
| `priority` | texto | Sim | `P2` | Prioridade operacional do chamado |
| `category` | texto | Não | `M365` | Categoria original do incidente |
| `title` | texto | Sim | `Outlook não abre` | Resumo do problema |
| `description` | texto | Sim | `Erro ao iniciar o Outlook` | Detalhamento do incidente |
| `requester` | texto | Não | `user001@empresa.com` | Solicitante do chamado |

## Campos enriquecidos

| Campo | Tipo lógico | Exemplo | Regra |
|---|---|---|---|
| `resolution_minutes` | inteiro | `75` | Diferença em minutos entre resolução e abertura |
| `sla_minutes` | inteiro | `120` | Meta definida pela prioridade |
| `is_sla_breach` | inteiro booleano | `0` ou `1` | Indica se o tempo ultrapassou a meta |
| `dow` | texto | `Monday` | Dia da semana da abertura |
| `hour` | inteiro | `8` | Hora da abertura |
| `category_pred` | texto | `M365` | Categoria calculada pelas regras |

## Metas de SLA

| Prioridade | Minutos |
|---|---:|
| P1 | 60 |
| P2 | 120 |
| P3 | 240 |
| P4 | 480 |

Prioridades não reconhecidas recebem a meta padrão de 240 minutos.

## Categorias calculadas

| Categoria | Termos considerados |
|---|---|
| `M365` | Outlook, Teams, Exchange, Defender, Microsoft 365, M365 |
| `Rede` | VPN, switch, latência, perda de pacote, link intermitente, roteador |
| `Acesso` | senha, MFA, permissão, bloqueado, conta desabilitada, falha de login |
| `Backup` | backup, restore, Veeam, job com falha, storage |
| `Servidor` | utilizada como categoria padrão |

## Regras de qualidade

- registros sem `ticket_id` são descartados;
- ocorrências repetidas do mesmo `ticket_id` são removidas;
- as colunas obrigatórias são verificadas antes da transformação;
- datas devem estar em formato compatível com `datetime.fromisoformat`;
- os dados de exemplo são sintéticos e não representam usuários reais.
