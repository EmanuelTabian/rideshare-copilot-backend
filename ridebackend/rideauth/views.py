from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, password_validation
from .serializers import UserSerializer
from .models import User
import jwt
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv
load_dotenv()
# Create your views here.

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []  

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        password_validation.validate_password(request.data['password'], password_validators=None)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = [] 

    def post (self,request):
        email = request.data['email']
        password = request.data['password']
        # user = User.objects.filter(email=email).first()
        user = authenticate(email=email, password=password)

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        
        payload = {
            'id': user.id,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=60),
            'iat': datetime.now(timezone.utc)
        }
        token = jwt.encode(payload, os.getenv('TOKEN_SECRET'), algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response
    
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)

        return Response(serializer.data)
    
class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self,request):
        user = request.user
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
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
    
