import boto3

from midas_sales.config import settings

s3_client = boto3.client(
    "s3",
    region_name=settings.aws_region_name,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
)


def upload_in_bucket(file, directory, tenant_id):
    filename = f"{tenant_id}/{directory}/{file.filename}"
    s3_client.upload_fileobj(file.file, settings.aws_bucket_name, filename)
    return f"https://{settings.aws_bucket_name}.s3.amazonaws.com/{filename}"


def delete_in_bucket(url):
    filename = url.split("com/")[-1]
    s3_client.get_object(Bucket=settings.aws_bucket_name, Key=filename)
    return s3_client.delete_object(Bucket=settings.aws_bucket_name,
                                   Key=filename)
