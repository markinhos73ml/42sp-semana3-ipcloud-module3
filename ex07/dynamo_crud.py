import sys
import csv
import boto3
import base64
import uuid
from botocore.exceptions import ClientError

# Aumenta limite para campos grandes (Base64)
csv.field_size_limit(sys.maxsize)

# 🔹 Conexão com AWS real (Sandbox)
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1'
)

s3 = boto3.client(
    's3',
    region_name='us-east-1'
)

TABLE_NAME = 'Usuarios'
BUCKET_NAME = '42sp-marcosf2-bucket'  # ajuste para seu login

table = dynamodb.Table(TABLE_NAME)

# --- Função para decodificar e enviar imagem ao S3 ---
def upload_document_to_s3(base64_str: str) -> str:
    """Decodifica uma string Base64, salva no S3 e retorna a chave (nome) do objeto."""
    prefix = "data:image/jpeg;base64,"
    if base64_str.startswith(prefix):
        base64_str = base64_str[len(prefix):]

    image_bytes = base64.b64decode(base64_str)
    unique_name = f"{uuid.uuid4()}.jpg"

    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=unique_name,
            Body=image_bytes,
            ContentType='image/jpeg'
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied':
            print(f"Sem permissão para enviar '{unique_name}' para o bucket '{BUCKET_NAME}'.")
            print("Verifique sua role ou política de IAM.")
            return None
        else:
            raise e

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
            # Se houver coluna 'document', tenta enviar para S3
            if 'document' in row and row['document'].strip():
                doc_key = upload_document_to_s3(row['document'].strip())
                if doc_key:
                    item['document_key'] = doc_key
            table.put_item(Item=item)
    print("Dados carregados com sucesso!")

# --- Recuperar usuário ---
def retrieve(user_id: str):
    response = table.get_item(Key={'id': user_id})
    item = response.get('Item')
    if item:
        print(f"Usuário encontrado: {item}")
    else:
        print(f"Usuário {user_id} não encontrado.")

# --- Deletar usuário ---
def delete(user_id: str):
    table.delete_item(Key={'id': user_id})
    print(f"Usuário {user_id} removido.")

# --- Atualizar nome de usuário ---
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
