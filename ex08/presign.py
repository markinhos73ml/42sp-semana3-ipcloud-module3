import sys
import boto3
from botocore.exceptions import ClientError

def generate_presigned_url(bucket_name: str, object_key: str, expiration: int = 600) -> str:
    """
    Gera uma URL temporária (presigned URL) para um objeto no S3.
    :param bucket_name: Nome do bucket
    :param object_key: Nome do objeto dentro do bucket
    :param expiration: Tempo de expiração em segundos (padrão: 600s = 10 minutos)
    :return: URL temporária
    """
    # Conecta ao S3 (LocalStack)
    s3_client = boto3.client(
        "s3",
        endpoint_url="http://localhost:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1"
    )

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration
        )
        return url
    except ClientError as e:
        print(f"Erro ao gerar presigned URL: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Uso: python3 presign.py <bucket_name> <object_key>")
        sys.exit(1)

    bucket_name = sys.argv[1]
    object_key = sys.argv[2]

    url = generate_presigned_url(bucket_name, object_key)
    print(url)

if __name__ == "__main__":
    main()
