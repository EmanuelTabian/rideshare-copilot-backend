
from rest_framework import serializers

class InputSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    file_type = serializers.CharField()
    