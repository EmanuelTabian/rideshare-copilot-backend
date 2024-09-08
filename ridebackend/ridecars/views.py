from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .serializers import CarPostSerializer
from .models import CarPost
from rideposts.models import File
class AddRidePost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request): 
        serializer = CarPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)

class GetAllRidePosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, page):
        car_posts = CarPost.objects.all()
        car_posts_length = len(car_posts)
        paginator = Paginator(car_posts, 10)
        car_posts_by_page = paginator.page(page).object_list
        serializer = CarPostSerializer(car_posts_by_page, many=True)
        return Response({'data': serializer.data, 'count': car_posts_length}) 

class GetRidePost(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, car_post_id):
        car_post = get_object_or_404(CarPost, pk=car_post_id)
        serializer = CarPostSerializer(car_post)
        return Response(serializer.data)


class GetUserCarPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
      user_car_posts = CarPost.objects.all().filter(user=request.user)
      serializer = CarPostSerializer(user_car_posts,many=True)
      return Response(serializer.data)

class UpdateRidePost(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, car_post_id):
        car_post = get_object_or_404(CarPost, pk=car_post_id)

        if car_post.user != request.user:
            return Response({"detail": "You do not have permission to edit this car post."})
        
        serializer = CarPostSerializer(car_post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class DeleteRidePost(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request):
        car_post_id = request.data.get('car_post_id')
        image_id = request.data.get('image_id')

        if car_post_id is None:
            return Response({'detail': "Missing required arguments: car_post_id or image_id"})


        car_post = get_object_or_404(CarPost, pk=car_post_id)
        if car_post.user != request.user:
            return Response({"detail": "You do not have permission to delete this car post."})

        car_post.delete()
        
        if image_id is not None:
             image_entry = get_object_or_404(File, pk=image_id)
             image_entry.delete()


        return Response()
