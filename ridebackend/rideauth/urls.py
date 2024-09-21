from django.urls import path

from .views import (
    DeleteUserView,
    LoginView,
    LogoutView,
    RegisterView,
    UpdateUserView,
    UserView,
)

urlpatterns = [
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("user", UserView.as_view()),
    path("user-update", UpdateUserView.as_view()),
    path("logout", LogoutView.as_view()),
    path("user-delete", DeleteUserView.as_view()),
]
