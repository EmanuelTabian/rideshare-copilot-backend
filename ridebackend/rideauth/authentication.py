import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from dotenv import load_dotenv
import os
load_dotenv()

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated")
        
        try:
            payload = jwt.decode(token, os.getenv('TOKEN_SECRET'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")

        user = User.objects.filter(id=payload['id']).first()
        
        if user is None:
            raise AuthenticationFailed("User not found")
        
        return (user, None)