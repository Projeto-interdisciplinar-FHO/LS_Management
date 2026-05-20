from rest_framework import serializers
from vaccinations.models import Vaccination
from animals.serializers import AnimalSerializer
from vaccines.serializers import VaccineSerializer

class VaccinationSerializer(serializers.ModelSerializer):
    animal_name = serializers.CharField(source='animal.name', read_only=True)
    vaccine_name = serializers.CharField(source='vaccine.name', read_only=True)
    
    class Meta:
        model = Vaccination
        fields = "__all__"
    
    def to_representation(self, instance):
        """Adiciona is_overdue e days_until_next na resposta"""
        data = super().to_representation(instance)
        data['is_overdue'] = instance.is_overdue
        data['days_until_next'] = instance.days_until_next
        return data