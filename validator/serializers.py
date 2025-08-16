from rest_framework import serializers
from .models import NationalID

class NationalIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationalID
        fields = "__all__"
