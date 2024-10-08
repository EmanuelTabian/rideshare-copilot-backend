from django.db import models

from rideauth.models import User


# Create your models here.
class CarPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    car_name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    version = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=255)
    engine = models.CharField(max_length=255)
    fuel = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    transmission = models.CharField(max_length=255)
    gear_number = models.CharField()
    color = models.CharField(max_length=255)
    seat_number = models.CharField()
    door_number = models.CharField(null=True, blank=True)
    milleage = models.CharField()
    power = models.CharField()
    mpg = models.CharField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    emission_standard = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    price = models.CharField()
