from django.db import models
from rideauth.models import User


# Create your models here.
class CarPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image_key = models.CharField(max_length=255, null=True, blank=True)
    image_id =  models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    car_name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    version = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=255)
    engine = models.CharField(max_length=255)
    fuel = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    transmission = models.CharField(max_length=255)
    gear_number = models.IntegerField()
    color = models.CharField(max_length=255)
    seat_number = models.IntegerField()
    door_number = models.IntegerField(null=True, blank=True)
    milleage = models.IntegerField()
    power = models.IntegerField()
    mpg = models.IntegerField(null=True, blank=True)
    description =  models.CharField(max_length=255, null=True, blank=True)
    emission_standard = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.IntegerField()
    price = models.IntegerField()



    