from rest_framework import serializers
from apps.health.vaccines.models import Vaccine

class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = "__all__"