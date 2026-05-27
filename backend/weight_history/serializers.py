from rest_framework import serializers
from weight_history.models import WeightHistory
from animals.models import Animal

class WeightHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightHistory
        fields = "__all__"
    
    def validate_animal(self, value):
        """Valida se o animal existe e está ativo"""
        if not value:
            raise serializers.ValidationError("Animal ID é obrigatório")
        
        try:
            animal = Animal.objects.get(id=value.id)
        except Animal.DoesNotExist:
            raise serializers.ValidationError(f"Animal com ID {value.id} não encontrado")
        
        # Verifica se está ativo (status='ativo' OU active=True)
        if animal.status != 'ativo' and not animal.active:
            raise serializers.ValidationError(f"Animal {animal.name} não está ativo. Status atual: {animal.status}")
        
        return value