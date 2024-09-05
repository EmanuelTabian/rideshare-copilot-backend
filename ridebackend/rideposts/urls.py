from django.urls import path
from .views import FileDirectUploadStartApi, FileDirectUploadFinishApi,GetImageByKey, DeleteImageByKey, EditImageByKey

urlpatterns = [
    path('upload/direct/start', FileDirectUploadStartApi.as_view()),
    path('upload/direct/finish', FileDirectUploadFinishApi.as_view()),
    path('get-image-by-file-key/<path:file_key>', GetImageByKey.as_view()),
    path('delete-image-by-file-key/<path:file_key>', DeleteImageByKey.as_view()),
    path('put-image-by-file-key/<path:file_key>', EditImageByKey.as_view()),

]