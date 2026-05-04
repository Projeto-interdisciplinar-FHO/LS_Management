from rest_framework import serializers
from feedings.models import Feeding


class FeedingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeding
        fields = '__all__'
