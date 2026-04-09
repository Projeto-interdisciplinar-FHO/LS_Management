from rest_framework import serializers
from animal_health.models import AnimalHealth

class AnimalHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalHealth
        fields = "__all__"