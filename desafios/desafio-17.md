# FinOps Check - Magalu Cloud

> Ferramenta de identificação de recursos ociosos/órfãos na infraestrutura
> da Magalu Cloud, desenvolvida para o Sprint de Inovação (issue #17).

## Problema identificado

Em ambientes de nuvem é comum acumular recursos que continuam gerando
custo mesmo sem estar em uso real — Load Balancers sem instância
vinculada, volumes de Block Storage esquecidos, máquinas virtuais paradas.
Sem uma checagem automatizada, esse desperdício passa despercebido e se
acumula mês a mês.

## Solução

Um script em Python (`finops_check.py`) que:

1. Consulta os recursos **reais** da conta Magalu Cloud (Virtual Machines,
   Block Storage e Load Balancers) usando o **`mgc` CLI**, já autenticado
   com a API Key da conta.
2. Aplica regras para identificar recursos com possível desperdício:
   - **Load Balancer** com backend configurado mas sem nenhuma instância
     (`target`) recebendo tráfego
   - **Volume de Block Storage** sem instância anexada
   - **Máquina Virtual** existente mas parada (`state != running`)
3. Gera um relatório no terminal com o resumo do desperdício e o custo
   estimado, além de salvar os achados em `relatorio_desperdicio.csv`.

## Execução real

![Execução do finops_check.py no terminal](docs/execucao-terminal.png)

O script identificou, na minha própria conta, 2 Load Balancers reais que
existiam mas não tinham nenhuma instância recebendo tráfego — exatamente
o tipo de desperdício que o projeto se propõe a detectar.

## Como funciona a integração com a API real

Em vez de depender de um endpoint de billing/FOCUS (que não é documentado
publicamente pela Magalu Cloud — a tela de Faturamento do Console usa uma
API interna que exige sessão de login, não API Key), o script usa o
`mgc` CLI como intermediário:

```bash
mgc virtual-machine instances list -o json -r
mgc block-storage volumes list -o json -r
mgc load-balancer network-loadbalancers list -o json -r
```

A flag `-r` (raw) é essencial: sem ela, o `mgc` insere códigos de cor ANSI
na saída, mesmo pedindo `-o json`, o que quebra o parser.

## Proteção da API Key

- A API Key nunca fica no código-fonte.
- Fica em um arquivo `.env` local (fora do Git, listado no `.gitignore`).
- Um `.env.example` é versionado como modelo, sem valores reais.
- O `mgc` CLI já cuida da autenticação nas chamadas.

## Como executar

```bash
cd src/finops
python3 finops_check.py
```

Pré-requisitos:
- `mgc` CLI instalado e autenticado (`mgc auth login` ou API Key configurada)
- Python 3.10+

## Arquivos

- `finops_check.py` — script principal
- `.env.example` — modelo de configuração (não usado pelo mgc CLI, mantido
  para referência caso a integração evolua para chamadas HTTP diretas)
- `relatorio_desperdicio.csv` — gerado automaticamente após a execução
- `docs/execucao-terminal.png` — print da execução real

## Possíveis evoluções futuras

- Adicionar mais tipos de recurso (Object Storage, Kubernetes, DBaaS)
- Refinar os valores de `CUSTO_HORA_ESTIMADO` com a tabela de preços oficial
- Publicar o relatório automaticamente via GitHub Action (CI), rodando
  periodicamente
- Enviar alerta (Slack/e-mail) quando o custo estimado de desperdício
  ultrapassar um limite configurável