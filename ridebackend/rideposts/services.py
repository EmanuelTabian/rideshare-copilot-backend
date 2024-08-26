from django.db import transaction
from .models import File


class FileDirectUploadService:
    # Ensures that if something goes wrong with the methon, all changes are rolled back.
    @transaction.atomic
    def start(self, *, file_name, file_type):
        file = File(
            original_file_name = file_name,
            file_name=file_generate_name(file_name),
            file_type=file_type,
            file=None
        )

        file.full_clean()
        file.save()
        upload_path = file_generate_upload_path(file, file.name)

        file.file = file.file.field.attr_class(file, file.file.field, upload_path)
        file.save()

        presigned_data = s3_generate_presigned_post(
            file_path=upload_path, file_type = file.file_type
        )
        return {"id": file.id, **presigned_data}
