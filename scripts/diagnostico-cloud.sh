#!/bin/bash

echo "================================"
echo " Diagnóstico de Ambiente Cloud "
echo "================================"

echo ""
echo "Data da verificação:"
date

echo ""
echo "Nome da máquina:"
hostname

echo ""
echo "Sistema operacional:"
cat /etc/os-release | grep PRETTY_NAME

echo ""
echo "Uso de disco:"
df -h /

echo ""
echo "Memória:"
free -h

echo ""
echo "Processos principais:"
ps aux --sort=-%mem | head -6

echo ""
echo "Docker:"
if command -v docker >/dev/null 2>&1
then
    docker --version
else
    echo "Docker não instalado"
fi

echo ""
echo "Diagnóstico finalizado."
