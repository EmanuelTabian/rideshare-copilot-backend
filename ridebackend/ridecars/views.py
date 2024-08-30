from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CarPostSerializer

from rest_framework.permissions import IsAuthenticated
class AddRidePost(APIView):
    permissions = [IsAuthenticated]

    def post(self,request): 
        serializer = CarPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
