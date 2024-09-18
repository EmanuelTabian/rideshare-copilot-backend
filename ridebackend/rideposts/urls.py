from django.urls import path
from .views import FileDirectUploadStartApi, FileDirectUploadFinishApi,GetImageByCarPostId, EditImage

urlpatterns = [
    path('upload/direct/start', FileDirectUploadStartApi.as_view()),
    path('upload/direct/finish', FileDirectUploadFinishApi.as_view()),
    path('get-image-by-post-id/<path:car_post_id>', GetImageByCarPostId.as_view()),
    path('put-image', EditImage.as_view()),
]