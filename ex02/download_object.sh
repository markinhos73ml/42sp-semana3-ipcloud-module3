#!/bin/bash

AWS_ENDPOINT_URL="http://localhost:4566"
BUCKET_NAME="42sp-marcosf2-bucket"
OBJECT_NAME="teste.txt"
DOWNLOAD_PATH="./downloaded_${OBJECT_NAME}"

echo "Baixando '${OBJECT_NAME}' do bucket '${BUCKET_NAME}'..."

aws --endpoint-url="${AWS_ENDPOINT_URL}" s3 cp "s3://${BUCKET_NAME}/${OBJECT_NAME}" "${DOWNLOAD_PATH}"

echo "Download concluído! Arquivo salvo como '${DOWNLOAD_PATH}'."
