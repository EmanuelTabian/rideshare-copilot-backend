from rest_framework import serializers
from .models import CalculatorEntry
class CalculatorEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculatorEntry
        fields = ['id','pub_date','app_income', 'commission', 'expenses', 'earnings']

        def create(self, validated_data):
            instance = self.Meta.model(**validated_data)
            instance.save()
            return instance
        
        def patch(self, instance, validated_data):
            for attr, value in validated_data.items():
                if attr in ['app_income', 'commission', 'expenses', 'earnings']:
                    setattr(instance, attr, value)
            instance.save()
            return instance