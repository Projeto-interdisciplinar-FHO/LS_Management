from rest_framework import serializers
from movement_types.models import MovementType


class MovementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementType
        fields = '__all__'
