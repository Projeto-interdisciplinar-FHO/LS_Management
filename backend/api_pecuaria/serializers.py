from rest_framework import serializers
from animals.models import Animal
from animal_health.models import AnimalHealth
from vaccinations.models import Vaccination
from weight_history.models import WeightHistory


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 'name', 'register_number', 'birth_date', 'sex', 'active']


class AnimalHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalHealth
        fields = ['id', 'animal', 'weight', 'temperature',
                  'sleep_quality', 'disease_prediction', 'consultation_date']


class VaccinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination
        fields = ['id', 'animal', 'vaccine', 'vaccination_date',
                  'doses_taken', 'total_doses', 'vaccination_status']


class WeightHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightHistory
        fields = '__all__'