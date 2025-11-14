#!/bin/bash
set -e

BUCKET_NAME="42sp-marcosf2-bucket"
AWS_ENDPOINT_URL="http://localhost:4566"

echo "Obtendo política do bucket..."
aws --endpoint-url=${AWS_ENDPOINT_URL} s3api get-bucket-policy --bucket "${BUCKET_NAME}" --query Policy --output text | jq .
