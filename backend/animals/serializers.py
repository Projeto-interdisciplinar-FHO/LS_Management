from rest_framework import serializers
from animals.models import Animal
from rest_framework.permissions import IsAuthenticated

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        permission_classes = (IsAuthenticated,)
        model = Animal
        fields = '__all__'