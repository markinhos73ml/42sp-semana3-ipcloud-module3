#!/bin/bash
# localstack-clean.sh
# Script para parar, remover e reiniciar o LocalStack
# Uso:
#   ./localstack-clean.sh          → limpeza e reinício normal
#   ./localstack-clean.sh --hard   → limpeza completa (containers + imagens + volumes)

set -e

echo "Limpando containers antigos do LocalStack..."

# Parar containers LocalStack em execução
docker ps -q --filter "ancestor=localstack/localstack" | while read -r cid; do
    echo "Parando container $cid..."
    docker stop "$cid" >/dev/null 2>&1
done

# Remover containers antigos LocalStack
docker ps -aq --filter "ancestor=localstack/localstack" | while read -r cid; do
    echo "Removendo container $cid..."
    docker rm -f "$cid" >/dev/null 2>&1
done

# Verificar se é modo hard
if [ "$1" == "--hard" ]; then
    echo "Modo HARD ativado — limpando volumes, imagens e redes associadas."

    # Remover volumes associados ao LocalStack
    docker volume ls --filter name=localstack -q | while read -r vid; do
        echo "Removendo volume $vid..."
        docker volume rm "$vid" >/dev/null 2>&1 || true
    done

    # Remover imagens antigas do LocalStack
    docker images "localstack/localstack" -q | while read -r iid; do
        echo "Removendo imagem $iid..."
        docker rmi -f "$iid" >/dev/null 2>&1 || true
    done

    # Remover redes com nome localstack
    docker network ls --filter name=localstack -q | while read -r nid; do
        echo "Removendo rede $nid..."
        docker network rm "$nid" >/dev/null 2>&1 || true
    done

    echo "Limpeza completa (modo hard) concluída."
fi

# Mostrar portas ocupadas
echo "Verificando portas travadas (4510–4566)..."
sudo lsof -i :4510-4566 2>/dev/null || echo "✅ Nenhum processo usando essas portas."

# Reiniciar LocalStack
echo "Iniciando LocalStack..."
localstack start -d

# Mostrar status
sleep 3
echo "Status dos serviços:"
localstack status services

echo "LocalStack reiniciado com sucesso!"
