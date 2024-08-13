from django.urls import path, include
from .views import RegisterView, LoginView, UserView, LogoutView, UpdateUserView,DeleteUserView


urlpatterns =  [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('user-update', UpdateUserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('user-delete', DeleteUserView.as_view())
]