from rest_framework import serializers
from species.models import Specie


class SpecieSerializer(serializers.ModelSerializer):
    breeds_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Specie
        fields = ['id', 'name', 'breeds_count']
        read_only_fields = ['id', 'breeds_count']
    
    def get_breeds_count(self, obj):
        """Retorna a contagem de raças para esta espécie"""
        return obj.breeds.count()
