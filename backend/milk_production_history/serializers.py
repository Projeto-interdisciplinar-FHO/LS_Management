from rest_framework import serializers
from milk_production_history.models import MilkProductionHistory


class MilkProductionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MilkProductionHistory
        fields = '__all__'
