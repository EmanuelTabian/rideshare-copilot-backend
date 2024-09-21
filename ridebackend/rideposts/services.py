import os
import pathlib
from uuid import uuid4

import boto3
import requests
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from dotenv import load_dotenv

from .models import File, file_generate_upload_path

load_dotenv()


def s3_generate_presigned_post(*, file_path, file_type):
    client = boto3.client(
        service_name="s3",
        aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    presigned_data = client.generate_presigned_post(settings.AWS_STORAGE_BUCKET_NAME, file_path, Fields={
        "acl":settings.AWS_DEFAULT_ACL,
        "Content-Type": file_type 
    }, Conditions=[
        {"acl":settings.AWS_DEFAULT_ACL},
        {"Content-Type": file_type}], 
        ExpiresIn=settings.AWS_QUERYSTRING_EXPIRE)
    return presigned_data

def s3_generate_presigned_get(file_key):
    client = boto3.client(
        service_name="s3",
        aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
     
    presigned_url = client.generate_presigned_url('get_object', Params={
         "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
         "Key": file_key
     },
     ExpiresIn=3600)
    return presigned_url

def s3_generate_presigned_put(file_key, file_type):
    client = boto3.client(
    service_name="s3",
    aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
    )
    print(file_type)
    presigned_url = client.generate_presigned_url('put_object', Params={
        "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
        "Key": file_key,
        "ContentType": file_type
    }, ExpiresIn=3600,
    HttpMethod="PUT")

    return presigned_url

def s3_generate_presigned_delete(file_key):
    client = boto3.client(
        service_name="s3",
        aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    presigned_url = client.generate_presigned_url(ClientMethod='delete_object', Params={
        # "Bucket": f"{os.getenv('AWS_STORAGE_BUCKET_NAME')}--{os.getenv('AWS_AZ_ID')}--x-s3.s3express-{os.getenv('AWS_AZ_ID')}.eu-west-2.amazonaws.com",
        "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
        "Key": file_key,
    }, ExpiresIn=3600,
    HttpMethod='DELETE')

    return presigned_url

def delete_image(file):
    url = s3_generate_presigned_delete(str(file.file))
    response = requests.delete(url)

    if response.status_code != 204:
        raise Exception(f"Failed to delete the image from S3: {response.status_code}")
    
    

def file_generate_name():
    return f"{uuid4().hex}"

class FileDirectUploadService:
    # Ensures that if something goes wrong with the methon, all changes are rolled back.
    @transaction.atomic
    def start(self, *, file_name, file_type, user_id, post):
        file = File(
            original_file_name = file_name,
            file_name=file_generate_name(),
            file_type=file_type,
            post=post,
            file=None
        )

        file.full_clean()
        file.save()
        upload_path = file_generate_upload_path(file, file.file_name, user_id)

        file.file = file.file.field.attr_class(file, file.file.field, upload_path)
        file.save()

        presigned_data = s3_generate_presigned_post(
            file_path=upload_path, file_type=file.file_type
        )
        return {"id": file.id, **presigned_data}
    
    @transaction.atomic
    def finish(self, *, file:File):
        file.upload_finished_at = timezone.now()
        file.full_clean()
        file.save()

        return file
    
    @transaction.atomic
    def start_edit(self, *, file, file_name ,file_type):
        file.original_file_name = file_name
        file.file_name = file_generate_name()
        file.file_type = file_type

        # Save
        file.full_clean()
        file.save()

        # Generate presigned url for data modification 
        presigned_url = s3_generate_presigned_put(file_key=str(file.file), file_type=str(file.file_type))
        return presigned_url

