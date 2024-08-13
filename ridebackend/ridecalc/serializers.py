from rest_framework import serializers
from .models import CalculatorEntry
class CalculatorEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculatorEntry
        fields = ['user','pub_date', 'app_income', 'commission', 'expenses', 'earnings']

        def create(self, validated_data):
            instance = self.Meta.model(**validated_data)
            instance.save()
            return instance