from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
import requests

from .models import File
from .services import FileDirectUploadService, s3_generate_presigned_get, s3_generate_presigned_delete

class FileDirectUploadStartApi(APIView):
    permission_classes = [IsAuthenticated]
 
    class InputSerializer(serializers.Serializer):
        file_name = serializers.CharField()
        file_type = serializers.CharField()


    def post(self,request, *args, **kwargs):
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = FileDirectUploadService()
        presigned_data = service.start(**serializer.validated_data, user_id=user.id)

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
    
class GetImageByKey(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_key):
        url = s3_generate_presigned_get(file_key)
        return Response({'url': url})
    
class DeleteImageByKey(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, file_key):
        url = s3_generate_presigned_delete(file_key)
        requests.delete(url)

        return Response()
    

