#!/bin/bash

echo "========================================="
echo " DIAGNÓSTICO DO AMBIENTE MAGALU CLOUD"
echo "========================================="

# Verifica se a CLI da Magalu Cloud está instalada
if ! command -v mgc >/dev/null 2>&1; then
    echo "Erro: CLI da Magalu Cloud (mgc) não está instalada."
    exit 1
fi

echo
echo "=== Informações do Sistema ==="
echo "Data: $(date)"
echo "Hostname: $(hostname)"
echo "Sistema: $(uname -a)"

echo
echo "=== Uso de Disco ==="
df -h

echo
echo "=== Memória ==="
free -h

echo
echo "=== Instâncias da Magalu Cloud ==="
mgc virtual-machine instances list

echo
echo "=== Fim do diagnóstico ==="
