from rest_framework import serializers
from apps.herd.quadrants.models import Quadrant

class QuadrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quadrant
        fields = '__all__'