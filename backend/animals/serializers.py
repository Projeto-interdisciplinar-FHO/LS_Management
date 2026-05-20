from rest_framework import serializers
from animals.models import Animal
from species.models import Specie
from breeds.models import Breed
from quadrants.models import Quadrant
from purpose_types.models import PurposeType

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'
    
    def validate_specie(self, value):
        """Valida se a espécie existe"""
        if not Specie.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(f"Espécie com ID {value.id} não existe.")
        return value
    
    def validate_quadrant(self, value):
        """Valida se o quadrante existe"""
        if not Quadrant.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(f"Quadrante com ID {value.id} não existe.")
        return value
    
    def validate_purpose(self, value):
        """Valida se o tipo de propósito existe"""
        if not PurposeType.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(f"Tipo de propósito com ID {value.id} não existe.")
        return value
    
    def validate_breed(self, value):
        """Valida se a raça existe (opcional)"""
        if value and not Breed.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(f"Raça com ID {value.id} não existe.")
        return value
    
    def validate_sex(self, value):
        """Valida se o sexo é válido (m ou f)"""
        if value.lower() not in ['m', 'f']:
            raise serializers.ValidationError("Sexo deve ser 'm' (Macho) ou 'f' (Fêmea).")
        return value.lower()
    
    def validate_weight(self, value):
        """Valida se o peso é positivo"""
        if value <= 0:
            raise serializers.ValidationError("Peso deve ser maior que zero.")
        return value