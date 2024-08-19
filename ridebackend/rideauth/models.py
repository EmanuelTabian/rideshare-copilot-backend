from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    # Set it back to none if user auth doen't work.
    username = models.CharField(max_length=50, null=True, blank=True)
   

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    