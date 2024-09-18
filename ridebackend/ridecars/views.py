from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .serializers import CarPostSerializer
from .models import CarPost
from rideposts.models import File
from rideposts.services import delete_image
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
        try:
            car_posts_page = paginator.page(page)
          
        except PageNotAnInteger:
            return Response({'error': 'Invalid page number. Page should be an integer!'})
        except EmptyPage:
            return Response({'error': "Page not found! The page number you're requesting is out of range!"})
        car_posts_by_page = car_posts_page.object_list
        serializer = CarPostSerializer(car_posts_by_page, many=True)
        
        pagination_details = {
            'current_page': car_posts_page.number,
            'total_pages': paginator.num_pages,
            'has_previous': car_posts_page.has_previous(),
            'has_next': car_posts_page.has_next(),
            'previous_page_number': car_posts_page.previous_page_number() if car_posts_page.has_previous() else None,
            'next_page_number': car_posts_page.next_page_number() if car_posts_page.has_next() else None
        }
     
        return Response({'data': serializer.data, 'count': car_posts_length, 'pagination': pagination_details})
    
class GetRidePost(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, car_post_id):
        car_post = get_object_or_404(CarPost, pk=car_post_id)
        serializer = CarPostSerializer(car_post)
        return Response(serializer.data)


class GetUserCarPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, page):
      user_car_posts = CarPost.objects.all().filter(user=request.user)
      car_posts_length = len(user_car_posts)
      paginator = Paginator(user_car_posts, 10)
      try:
         car_posts_page = paginator.page(page)
      except PageNotAnInteger:
            return Response({'error': 'Invalid page number. Page should be an integer!'})
      except EmptyPage:
            return Response({'error': "Page not found! The page number you're requesting is out of range!"})
      car_posts_by_page = car_posts_page.object_list
      serializer = CarPostSerializer(car_posts_by_page, many=True)
        
      pagination_details = {
            'current_page': car_posts_page.number,
            'total_pages': paginator.num_pages,
            'has_previous': car_posts_page.has_previous(),
            'has_next': car_posts_page.has_next(),
            'previous_page_number': car_posts_page.previous_page_number() if car_posts_page.has_previous() else None,
            'next_page_number': car_posts_page.next_page_number() if car_posts_page.has_next() else None
        }
     
      return Response({'data': serializer.data, 'count': car_posts_length, 'pagination': pagination_details})

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
        # Get the car post that will get deleted based on the car post id that will be received
        car_post_id = request.data.get('car_post_id')
        print(car_post_id)
        if car_post_id is None:
            return Response({'detail': "Missing required argument: car_post_id"})


        car_post = get_object_or_404(CarPost, pk=car_post_id)
        # Check for a file entry associated with the post, first() will return None if there is no file
        file = File.objects.filter(post=car_post).first()
       
        # Conditionally delete the image from the S3 Bucket
        if file:
            # Use the image deletion service to generate the presigned url and request deletion
            delete_image(file)
           
          

        if car_post.user != request.user:
            return Response({"detail": "You do not have permission to delete this car post."})

        car_post.delete()
        
        return Response()
