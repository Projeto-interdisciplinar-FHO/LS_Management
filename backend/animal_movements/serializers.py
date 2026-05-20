from rest_framework import serializers
from animal_movements.models import AnimalMovement


class AnimalMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalMovement
        fields = '__all__'
