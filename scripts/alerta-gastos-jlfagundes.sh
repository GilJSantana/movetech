#!/bin/bash

# Variaveis
LIMITE_ALERTA=50.00
ACCRUAL_PERIOD="2026-07"
URL="https://api.magalu.cloud/consumption/usage?accrual_period=$ACCRUAL_PERIOD"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)" # BASH_SOURCE aponta para o arquivo atual no caso este script

# Esse trecho é para carregar as variaveis de ambiente para os processos filhos (outros scripts chamados por este)
# Se usar somente source .env as variaveis de ambiente nao serao carregadas para os processos filhos
if [ -f "$SCRIPT_DIR/../.env" ]; then
    set -a # Ativa a exportação automática de variáveis de ambiente.
    . "$SCRIPT_DIR/../.env" # Carrega variaveis para este script
    set +a # Desativa a exportação automática de variáveis de ambiente.
fi

if [ -z "${API_KEY:-}" ]; then
    echo "[ERRO] Defina API_KEY no arquivo .env."
    exit 1
fi

consultar_gasto_total() {
    echo "Consultando a API..." >&2 # manda essa mensagem para o stderr, e nao para stdout que é a saida desta função.
    local response # variavel para o scopo somente desta funcao
    response=$(curl -fL --progress-bar --location "$URL" --header "x-api-key: $API_KEY") || return 1

    # grep filtra o campo BilledCost, cut pega o valor numérico, e awk soma todos os valores encontrados
    echo "$response" | \
        grep -o '"BilledCost":"[^"]*"' |
        cut -d'"' -f4 | \
        awk '{sum += $1} END {printf "%.2f", sum}'
}

GASTO_ATUAL=$(consultar_gasto_total) || {
    echo "[ERRO] Nao foi possivel consultar o gasto total."
    exit 1
}

echo "Consumo total para o período $ACCRUAL_PERIOD: R$ $GASTO_ATUAL"

# awk esta sendo usado para comparar valores
# BEGIN executa o bloco para o awk ler os valores e fazer a comparacao
# exit encerra o awk com o status 0, ou 1, lembrando que tem a negacao para inverter
if awk "BEGIN { exit !($GASTO_ATUAL > $LIMITE_ALERTA) }"; then
    echo "[ALERTA] O limite de R$ $LIMITE_ALERTA foi atingido!"
fi