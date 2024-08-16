from django.db import models
from django.conf import settings


def file_generate_upload_path(instance, filename):
    return f"files/{instance.file_name}"

class File(models.Model):
    file = models.FileField(
        upload_to=file_generate_upload_path,
        blank=True,
        null=True
    )

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
        
        
    