from django.contrib import admin
from .models import CarPost
# Register your models here.

class CarsAdmin(admin.ModelAdmin):
    list_display = ('user','id',"car_name","model", "version", "year", "engine", "fuel", "body", "transmission", "gear_number", "color", "seat_number", "door_number", "milleage", "power", "mpg", "description", "emission_standard", "location", "contact", "price")
    list_display_links = ('user',"id")
    search_fields = ("user","app_income", "pub_date", "commission")
    list_per_page = 25

admin.site.register(CarPost,CarsAdmin)