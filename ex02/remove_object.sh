#!/bin/bash

AWS_ENDPOINT_URL="http://localhost:4566"
BUCKET_NAME="42sp-marcosf2-bucket"
OBJECT_NAME="teste.txt"

echo "Removendo '${OBJECT_NAME}' do bucket '${BUCKET_NAME}'..."

aws --endpoint-url="${AWS_ENDPOINT_URL}" s3 rm "s3://${BUCKET_NAME}/${OBJECT_NAME}"

echo "Objeto removido com sucesso!"
