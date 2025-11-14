#!/bin/bash

AWS_ENDPOINT_URL="http://localhost:4566"
BUCKET_NAME="42sp-marcosf2-bucket"
OBJECT_NAME="teste.txt"
LOCAL_FILE_PATH="./${OBJECT_NAME}"

echo "Enviando arquivo '${LOCAL_FILE_PATH}' para o bucket '${BUCKET_NAME}'..."

aws --endpoint-url="${AWS_ENDPOINT_URL}" s3 cp "${LOCAL_FILE_PATH}" "s3://${BUCKET_NAME}/${OBJECT_NAME}"

echo "Upload concluído!"
