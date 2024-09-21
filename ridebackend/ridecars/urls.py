from django.urls import path

from .views import (AddRidePost, DeleteRidePost, GetAllRidePosts, GetRidePost,
                    GetUserCarPosts, UpdateRidePost)

urlpatterns = [
    path('add-carpost', AddRidePost.as_view()),
    path('get-carposts/<path:page>', GetAllRidePosts.as_view()),
    path('get-carpost/<int:car_post_id>', GetRidePost.as_view()),
    path('get-user-carposts/<path:page>', GetUserCarPosts.as_view()),
    path('update-ridepost/<int:car_post_id>', UpdateRidePost.as_view()),
    path('delete-ridepost', DeleteRidePost.as_view()),
]

