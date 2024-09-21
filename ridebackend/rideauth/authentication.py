import os

import jwt
from dotenv import load_dotenv
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import User

load_dotenv()


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            print("asdddd")
            raise AuthenticationFailed("Unauthenticated")
        
        try:
            payload = jwt.decode(token, os.getenv('TOKEN_SECRET'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")

        user = User.objects.filter(id=payload['id']).first()
        
        if user is None:
            raise AuthenticationFailed("User not found")
        
        return (user, None)