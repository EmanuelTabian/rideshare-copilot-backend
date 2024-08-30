from django.urls import path
from .views import FileDirectUploadStartApi, FileDirectUploadFinishApi

urlpatterns = [
    path('upload/direct/start', FileDirectUploadStartApi.as_view()),
    path('upload/direct/finish', FileDirectUploadFinishApi.as_view()),
]