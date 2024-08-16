from django.shortcuts import render

from django.shortcuts import get_object_or_404

from serializers import InputSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import File


class FileDirectUploadStartApi(APIView):
    def post(self,request):
        serializer = InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
      

