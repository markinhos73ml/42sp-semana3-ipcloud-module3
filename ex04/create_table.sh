#!/bin/bash

CONFIG_FILE="table_config.json"

echo "Criando a tabela DynamoDB..."

aws --endpoint-url=http://localhost:4566 dynamodb create-table --cli-input-json file://$CONFIG_FILE

echo "Aguardando a tabela estar ativa..."
aws --endpoint-url=http://localhost:4566 dynamodb wait table-exists --table-name Usuarios

echo "Tabela criada com sucesso."