from django.urls import path
from .views import FileDirectUploadStartApi, FileDirectUploadFinishApi,GetImageByKey

urlpatterns = [
    path('upload/direct/start', FileDirectUploadStartApi.as_view()),
    path('upload/direct/finish', FileDirectUploadFinishApi.as_view()),
    path('get-image-by-file-key/<int:file_key>', GetImageByKey.as_view())
]