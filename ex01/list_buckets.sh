#!/bin/bash

AWS_ENDPOINT_URL="http://localhost:4566"

echo "Listando buckets disponíveis:"
aws --endpoint-url="${AWS_ENDPOINT_URL}" s3api list-buckets \
    --query "Buckets[].Name" \
    --output table
