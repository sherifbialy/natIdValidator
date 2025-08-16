from rest_framework import serializers
from .models import APIKey, NationalID

class NationalIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationalID
        fields = "__all__"


class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = "__all__"
        read_only_fields = ("key", "usage_count", "last_reset", "created_at")
