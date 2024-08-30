from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CarPostSerializer

from rest_framework.permissions import IsAuthenticated
from .models import CarPost
class AddRidePost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request): 
        serializer = CarPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class GetAllRidePosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        car_posts = CarPost.objects.all()
        serializer = CarPostSerializer(car_posts, many=True)
        return Response(serializer.data) 

class GetRidePost(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, car_post_id):
        car_post = get_object_or_404(CarPost, pk=car_post_id)
        serializer = CarPostSerializer(car_post)
        return Response(serializer.data)
