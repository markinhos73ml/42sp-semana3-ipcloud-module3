import sys
import csv
import boto3

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

TABLE_NAME = "Usuarios"
table = dynamodb.Table(TABLE_NAME)

# Funções CRUD

def load_csv(file_path):
    """Carrega dados de um CSV para a tabela DynamoDB."""
    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                table.put_item(Item=row)
        print(f"Carregando dados de {file_path}")
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")

def retrieve_user(user_id):
    """Recupera um usuário pelo ID."""
    try:
        response = table.get_item(Key={"id": user_id})
        if "Item" in response:
            print(f"Usuário encontrado: {response['Item']}")
            return response["Item"]
        else:
            print(f"Usuário {user_id} não encontrado.")
            return None
    except Exception as e:
        print(f"Erro ao recuperar usuário: {e}")
        return None

def delete_user(user_id):
    """Deleta um usuário pelo ID, se existir."""
    try:
        user = retrieve_user(user_id)
        if user:
            table.delete_item(Key={"id": user_id})
            print(f"Usuário {user_id} removido.")
    except Exception as e:
        print(f"Erro ao deletar usuário: {e}")

def update_user(user_id, new_name):
    """Atualiza o nome de um usuário pelo ID, se existir."""
    try:
        user = retrieve_user(user_id)
        if user:
            table.update_item(
                Key={"id": user_id},
                UpdateExpression="SET #n = :val",
                ExpressionAttributeNames={"#n": "name"},
                ExpressionAttributeValues={":val": new_name}
            )
            print(f"Usuário {user_id} atualizado para nome = '{new_name}'")
    except Exception as e:
        print(f"Erro ao atualizar usuário: {e}")


def main():
    if len(sys.argv) < 3:
        print("Uso: python3 dynamo_crud.py <comando> <argumentos>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "load":
        file_path = sys.argv[2]
        load_csv(file_path)
    elif command == "retrieve":
        user_id = sys.argv[2]
        retrieve_user(user_id)
    elif command == "delete":
        user_id = sys.argv[2]
        delete_user(user_id)
    elif command == "update":
        if len(sys.argv) != 4:
            print("Uso: python3 dynamo_crud.py update <id> <novo_nome>")
            sys.exit(1)
        user_id = sys.argv[2]
        new_name = sys.argv[3]
        update_user(user_id, new_name)
    else:
        print(f"Comando desconhecido: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
