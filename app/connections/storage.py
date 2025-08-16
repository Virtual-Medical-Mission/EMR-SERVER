import os
import boto3
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv(dotenv_path='.env')

STORAGE_BUCKET_URL = os.getenv("STORAGE_BUCKET_URL")
STORAGE_USERNAME = os.getenv("STORAGE_USERNAME")
STORAGE_PASSWORD = os.getenv("STORAGE_PASSWORD")

if not all([STORAGE_BUCKET_URL, STORAGE_USERNAME, STORAGE_PASSWORD]):
    raise ValueError("One or more storage environment variables are not set. Check your .env file.")

parsed = urlparse(f"https://{STORAGE_BUCKET_URL}")
parts = parsed.netloc.split('.')
bucket_name = parts[0]
region = parts[2] if len(parts) > 2 else None

s3_client = boto3.client(
    "s3",
    aws_access_key_id=STORAGE_USERNAME,
    aws_secret_access_key=STORAGE_PASSWORD,
    region_name=region
)

def check_bucket_access():
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except Exception:
        return False