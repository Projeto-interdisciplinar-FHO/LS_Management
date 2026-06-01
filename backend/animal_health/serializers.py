from rest_framework import serializers
from animal_health.models import AnimalHealth

class AnimalHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalHealth
        fields = "__all__"
    animal_name = serializers.SerializerMethodField(read_only=True)
    animal_register = serializers.SerializerMethodField(read_only=True)

    def get_animal_name(self, obj):
        return obj.animal.name if obj.animal else None

    def get_animal_register(self, obj):
        return obj.animal.register_number if obj.animal else None