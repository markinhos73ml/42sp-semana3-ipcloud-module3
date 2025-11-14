#!/bin/bash

# Configurações
AWS_ENDPOINT_URL="http://localhost:4566"
BUCKET_NAME="42sp-marcosf2-bucket"

echo "Criando bucket: ${BUCKET_NAME}..."

# Cria o bucket
aws --endpoint-url="${AWS_ENDPOINT_URL}" s3api create-bucket \
    --bucket "${BUCKET_NAME}" \
    --region us-east-1

# Aguarda até o bucket existir
echo "Aguardando criação do bucket..."
aws --endpoint-url="${AWS_ENDPOINT_URL}" s3api wait bucket-exists \
    --bucket "${BUCKET_NAME}"

echo "Bucket '${BUCKET_NAME}' criado com sucesso!"
