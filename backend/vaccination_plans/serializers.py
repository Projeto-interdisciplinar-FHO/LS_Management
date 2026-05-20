from rest_framework import serializers
from vaccination_plans.models import VaccinationPlan


class VaccinationPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccinationPlan
        fields = '__all__'
