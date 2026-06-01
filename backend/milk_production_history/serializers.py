from rest_framework import serializers
from milk_production_history.models import MilkProductionHistory


class MilkProductionHistorySerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        animal = attrs.get('animal')
        if animal and str(animal.sex).lower() == 'm':
            raise serializers.ValidationError({
                'animal': 'Ordenha de leite só pode ser registrada para fêmeas.'
            })
        return attrs

    class Meta:
        model = MilkProductionHistory
        fields = '__all__'
