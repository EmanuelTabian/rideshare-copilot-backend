import os

from django.db import models
from dotenv import load_dotenv

from ridecars.models import CarPost

load_dotenv()


def file_generate_upload_path(instance, filename, user_id):
    return f"{os.getenv('AWS_STORAGE_BUCKET_NAME')}--{os.getenv('AWS_AZ_ID')}--x-s3/user-{user_id}/photos/{instance.file_name}"


class File(models.Model):
    post = models.ForeignKey(CarPost, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to=file_generate_upload_path, blank=True, null=True)

    original_file_name = models.TextField()

    file_name = models.CharField(max_length=255, unique=True)
    file_type = models.CharField(max_length=255)

    upload_finished_at = models.DateTimeField(blank=True, null=True)

    @property
    def is_valid(self):
        return bool(self.upload_finished_at)

    @property
    def url(self):
        return self.file.url
