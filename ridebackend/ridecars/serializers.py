from rest_framework import serializers
from .models import CarPost

class CarPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarPost
        fields = ['user_id' ,'id','created_at','car_name','model', 'version', 'year', 'engine', 'fuel', 'body', 'transmission', "gear_number", 'color', 'seat_number', 'door_number', 'milleage', 'power', 'mpg','description', 'emission_standard', 'location', 'phone_number', 'price']

        def create(self, validated_data):
            instance = self.Meta.model(**validated_data)
            instance.save()
            return instance
        
        def patch(self, instance, validated_data):
            for attr, value in validated_data.items():
                if attr in ['car_name','model', 'version', 'year', 'engine', 'fuel', 'body', 'transmission', "gear_number", 'color', 'seat_number', 'door_number', 'milleage', 'power', 'mpg','description', 'emission_standard', 'location', 'phone_number', 'price']:
                    setattr(instance, attr, value)
            instance.save()
            return instance
