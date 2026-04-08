from rest_framework import serializers
from quadrants.models import Quadrant

class QuadrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quadrant
        fields = '__all__'