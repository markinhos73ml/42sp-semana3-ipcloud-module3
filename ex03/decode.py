import sys
import os
import base64
import boto3

def decode_image(base64_str: str) -> bytes:
    """Decodifica uma string Base64 em bytes."""
    return base64.b64decode(base64_str)

def main():
    # Verifica os argumentos
    if len(sys.argv) != 3:
        print("Uso: python3 decode.py <bucket_name> <arquivo_base64.txt>")
        sys.exit(1)

    bucket_name = sys.argv[1]
    input_file = sys.argv[2]

    # Verifica se o arquivo existe na pasta atual
    if not os.path.exists(input_file):
        print(f"Erro: arquivo '{input_file}' não encontrado.")
        sys.exit(1)

    # Lê o conteúdo do arquivo
    with open(input_file, "r") as f:
        base64_data = f.read().strip()

    # Remove prefixo, se existir
    prefix = "data:image/jpeg;base64,"
    if base64_data.startswith(prefix):
        base64_data = base64_data[len(prefix):]

    # Decodifica a imagem
    image_bytes = decode_image(base64_data)

    # Define o nome do arquivo de saída (.jpg)
    image_name = os.path.splitext(os.path.basename(input_file))[0] + ".jpg"

    # Conecta ao S3 (LocalStack)
    s3 = boto3.client(
        "s3",
        endpoint_url="http://localhost:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )

    try:
        # Faz upload direto para o bucket
        s3.put_object(Bucket=bucket_name, Key=image_name, Body=image_bytes, ContentType="image/jpeg")
        print(f"'{image_name}' saved on bucket '{bucket_name}'!")
    except Exception as e:
        print(f"Erro ao salvar no S3: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
