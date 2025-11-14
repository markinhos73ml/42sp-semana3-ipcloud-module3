import sys
import csv
import os
import boto3
import base64
import uuid

# Para lidar com campos grandes (imagens em base64)
import csv
import sys
csv.field_size_limit(sys.maxsize)

# Conexão com DynamoDB e S3 (LocalStack)
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

TABLE_NAME = 'Usuarios'
table = dynamodb.Table(TABLE_NAME)
BUCKET_NAME = '42sp-marcosf2-bucket'  # Ajuste para seu bucket

# --- Função para decodificar e enviar imagem para S3 ---
def upload_document_to_s3(base64_str: str) -> str:
    """Decodifica uma string Base64, salva no S3 e retorna a chave do objeto."""
    prefix = "data:image/jpeg;base64,"
    if base64_str.startswith(prefix):
        base64_str = base64_str[len(prefix):]

    image_bytes = base64.b64decode(base64_str)
    unique_name = f"{uuid.uuid4()}.jpg"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=unique_name,
        Body=image_bytes,
        ContentType='image/jpeg'
    )

    return unique_name

# --- Função para carregar CSV ---
def load(csv_file: str):
    print(f"Carregando dados de {csv_file}...")
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = {
                'id': row['id'],
                'name': row['name']
            }
            # Se houver coluna 'document' no CSV, envia para S3
            if 'document' in row and row['document'].strip():
                item['document_key'] = upload_document_to_s3(row['document'].strip())
            table.put_item(Item=item)
    print("Dados carregados com sucesso!")

# --- Função para recuperar usuário ---
def retrieve(user_id: str):
    response = table.get_item(Key={'id': user_id})
    item = response.get('Item')
    if item:
        print(f"Usuário encontrado: {item}")
    else:
        print(f"Usuário {user_id} não encontrado.")

# --- Função para deletar usuário ---
def delete(user_id: str):
    table.delete_item(Key={'id': user_id})
    print(f"Usuário {user_id} removido.")

# --- Função para atualizar usuário ---
def update(user_id: str, new_name: str):
    table.update_item(
        Key={'id': user_id},
        UpdateExpression="set #n = :name",
        ExpressionAttributeNames={'#n': 'name'},
        ExpressionAttributeValues={':name': new_name}
    )
    print(f"Usuário {user_id} atualizado para nome = '{new_name}'")

# --- Função principal ---
def main():
    if len(sys.argv) < 2:
        print("Uso: python3 dynamo_crud.py <comando> [args...]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == 'load':
        if len(sys.argv) != 3:
            print("Uso: python3 dynamo_crud.py load <arquivo.csv>")
            sys.exit(1)
        load(sys.argv[2])
    elif command == 'retrieve':
        if len(sys.argv) != 3:
            print("Uso: python3 dynamo_crud.py retrieve <user_id>")
            sys.exit(1)
        retrieve(sys.argv[2])
    elif command == 'delete':
        if len(sys.argv) != 3:
            print("Uso: python3 dynamo_crud.py delete <user_id>")
            sys.exit(1)
        delete(sys.argv[2])
    elif command == 'update':
        if len(sys.argv) != 4:
            print("Uso: python3 dynamo_crud.py update <user_id> <novo_nome>")
            sys.exit(1)
        update(sys.argv[2], sys.argv[3])
    else:
        print(f"Comando '{command}' não reconhecido.")

if __name__ == "__main__":
    main()
