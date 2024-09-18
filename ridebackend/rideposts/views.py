from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
import requests

from ridecars.models import CarPost
from .models import File
from .services import FileDirectUploadService, s3_generate_presigned_get, s3_generate_presigned_delete, s3_generate_presigned_put

class FileDirectUploadStartApi(APIView):
    permission_classes = [IsAuthenticated]
 
    class InputSerializer(serializers.Serializer):
        file_name = serializers.CharField()
        file_type = serializers.CharField()


    def post(self,request, *args, **kwargs):
        user = request.user
        car_post_id = request.data.get('car_post_id')
        car_post = CarPost.objects.get(id=car_post_id, user=user)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = FileDirectUploadService()
        presigned_data = service.start(**serializer.validated_data, user_id=user.id, post=car_post)

        return Response(data=presigned_data)
      
class FileDirectUploadFinishApi(APIView):
    class InputSerializer(serializers.Serializer):
        file_id = serializers.CharField()

    def post (self,request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_id = serializer.validated_data["file_id"]

        file = get_object_or_404(File, id=file_id)

        service = FileDirectUploadService()
        service.finish(file=file)

        return Response({"id": file.id})

#  def start_edit(self, *, file_id, file_name, file_type, user_id):
class EditImage(APIView):
    permission_classes = [IsAuthenticated]
    class InputSerializer(serializers.Serializer):
        file_name = serializers.CharField()
        file_type = serializers.CharField()
        file_id = serializers.CharField()
        file_key = serializers.CharField()
    
    def put(self, request):
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = FileDirectUploadService()
        presigned_data = service.start_edit(**serializer.validated_data, user_id=user.id)

        return Response(data=presigned_data)

class GetImageByCarPostId(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, car_post_id):
        car_post = CarPost.objects.get(pk=car_post_id, user=request.user)
        # first() method returns None in case there is no file that matches the post id ForeignKey 
        file = File.objects.filter(post=car_post).first()
        url = s3_generate_presigned_get(str(file.file))
        return Response({'url': url})
    

    
    

