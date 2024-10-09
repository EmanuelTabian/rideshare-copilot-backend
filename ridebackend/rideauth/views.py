import os
from datetime import datetime, timedelta, timezone

import jwt
from django.contrib.auth import authenticate, password_validation
from dotenv import load_dotenv
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import User
from .serializers import UserSerializer

load_dotenv()
# Create your views here.


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        password = request.data["password"]
        
        try:
            password_validation.validate_password(password, user=None, password_validators=None)
            serializer.is_valid(raise_exception=True)
            serializer.save()
      
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": e}, status=400)
            
            
       
          
        

        
       


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        # user = User.objects.filter(email=email).first()
        user = authenticate(email=email, password=password)

        if user is None:
            raise AuthenticationFailed("Incorrect email or password!")

        payload = {
            "id": user.id,
            # Temporary token expiration time fix, it will last for 24 hours so users don't get logged out as the app doesn't have a refresh token feature, for now.
            "exp": datetime.now(timezone.utc) + timedelta(hours=24),
            "iat": datetime.now(timezone.utc),
        }
        token = jwt.encode(payload, os.getenv("TOKEN_SECRET"), algorithm="HS256")

        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"jwt": token}
        return response


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)

        return Response(serializer.data)


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        if "password" in request.data:
            password_validation.validate_password(
                request.data["password"], password_validators=None
            )
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DeleteUserView(APIView):

    def delete(self, request):
        user = request.user
        user.delete()

        return Response()


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {"message": "success"}
        return response
