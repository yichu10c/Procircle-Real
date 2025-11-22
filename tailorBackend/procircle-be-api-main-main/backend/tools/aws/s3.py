"""
AWS S3 Handler
"""
import os
import boto3
from botocore.exceptions import ClientError

from app.utils.exceptions import ApplicationException

AWS_S3_ENDPOINT = os.environ["AWS_S3_ENDPOINT"]
AWS_S3_BUCKET = os.environ["AWS_S3_BUCKET"]
AWS_S3_ASSET_DIR = os.environ["AWS_S3_ASSET_DIR"]
AWS_ACCESS_KEY_ID=os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY=os.environ["AWS_SECRET_ACCESS_KEY"]


s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

def generate_presigned_url(s3_key: str) -> str:
    """
    Generate a presigned URL S3 to upload a file
    """
    try:
        response = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": AWS_S3_BUCKET,
                "Key": s3_key,
                "ContentType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            },
            ExpiresIn=3600
        )
        return response
    except ClientError as e:
        raise ApplicationException(f"failed to generate presigned URL due to {e}")


def get_download_upload_presigned_url(key: str):
    """
    Get Upload and Download URL
    """
    s3key = f"{AWS_S3_ASSET_DIR}/{key}"
    download_url = f"{AWS_S3_ENDPOINT}/{s3key}"
    upload_url = generate_presigned_url(s3key)
    return download_url, upload_url


def upload_file(filepath: str, key: str):
    """
    Upload file to S3
    """
    try:
        s3key = f"{AWS_S3_ASSET_DIR}/{key}"
        s3_client.upload_file(filepath, AWS_S3_BUCKET, s3key)
        download_url = f"{AWS_S3_ENDPOINT}/{s3key}"
        return download_url
    except Exception as error:
        raise Exception(f"Failed when upload file to s3. {error=}", error)
