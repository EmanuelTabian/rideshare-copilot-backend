from django.db import transaction
from .models import File, file_generate_upload_path
from django.utils import timezone
from django.conf import settings
import pathlib
from uuid import uuid4
import boto3
import os
from dotenv import load_dotenv
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

def s3_generate_presigned_delete(file_key):
    client =  boto3.client(
          service_name="s3",
        aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    presigned_url = client.generate_presigned_url(ClientMethod='delete_object', Params={
        "Bucket": f"{os.getenv('AWS_STORAGE_BUCKET_NAME')}--{os.getenv('AWS_AZ_ID')}--x-s3.s3express-{os.getenv('AWS_AZ_ID')}.eu-west-2.amazonaws.com",
        "Key": file_key,
    }, ExpiresIn=3600)

    return presigned_url

def file_generate_name(original_file_name):
    mime_type = pathlib.Path(original_file_name).suffix
    return f"{uuid4().hex}{mime_type}"

class FileDirectUploadService:
    # Ensures that if something goes wrong with the methon, all changes are rolled back.
    @transaction.atomic
    def start(self, *, file_name, file_type, user_id):
        file = File(
            original_file_name = file_name,
            file_name=file_generate_name(file_name),
            file_type=file_type,
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
