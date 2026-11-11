#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "❌ Erro: Você precisa fornecer uma mensagem para a migration."
    echo "Exemplo: ./makemigration.sh \"simulation snapshots\""
    exit 1
fi

MIGRATION_MESSAGE="$1"
CONTAINER_NAME="app"

echo "🔍 Localizando o container..."
CONTAINER_ID=$(docker compose ps -q $CONTAINER_NAME)

if [ -z "$CONTAINER_ID" ]; then
    echo "❌ Erro: O container do app não está rodando. Inicie com 'docker compose up -d'."
    exit 1
fi

echo "1️⃣ Gerando a migration..."
docker compose exec $CONTAINER_NAME uv run alembic revision --autogenerate -m "$MIGRATION_MESSAGE"

echo "2️⃣ Aplicando a migration no banco de dados..."
docker compose exec $CONTAINER_NAME uv run alembic upgrade head

echo "✨ Sucesso! O arquivo da migration foi gerado no seu projeto e aplicado no banco."