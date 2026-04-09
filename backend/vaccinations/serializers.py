from rest_framework import serializers
from vaccinations.models import Vaccination

class VaccinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination
        fields = "__all__"