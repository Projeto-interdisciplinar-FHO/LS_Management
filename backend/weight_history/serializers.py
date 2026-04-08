from rest_framework import serializers
from weight_history.models import WeightHistory

class WeightHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightHistory
        fields = "__all__"