#!/bin/bash
set -e

BUCKET_NAME="42sp-marcosf2-bucket"
POLICY_FILE="policy.json"
AWS_ENDPOINT_URL="http://localhost:4566"

echo "Removendo bloqueio de acesso público..."
aws --endpoint-url=${AWS_ENDPOINT_URL} s3api delete-public-access-block --bucket "${BUCKET_NAME}"

echo "Aplicando política pública de leitura..."
aws --endpoint-url=${AWS_ENDPOINT_URL} s3api put-bucket-policy \
    --bucket "${BUCKET_NAME}" \
    --policy file://"${POLICY_FILE}"

echo "Policy applied to bucket."
