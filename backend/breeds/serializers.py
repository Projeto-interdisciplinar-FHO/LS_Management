from rest_framework import serializers
from breeds.models import Breed


class BreedSerializer(serializers.ModelSerializer):
    specie_name = serializers.CharField(source='specie.name', read_only=True)
    
    class Meta:
        model = Breed
        fields = ['id', 'name', 'specie', 'specie_name']
        read_only_fields = ['id', 'specie_name']

