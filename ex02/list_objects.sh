#!/bin/bash

AWS_ENDPOINT_URL="http://localhost:4566"
BUCKET_NAME="42sp-marcosf2-bucket"

echo "Objetos dentro do bucket '${BUCKET_NAME}':"
aws --endpoint-url="${AWS_ENDPOINT_URL}" s3 ls "s3://${BUCKET_NAME}/"
