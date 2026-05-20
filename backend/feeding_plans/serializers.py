from rest_framework import serializers
from feeding_plans.models import FeedingPlan


class FeedingPlanSerializer(serializers.ModelSerializer):
    alerta_nutricional_ia = serializers.SerializerMethodField()

    class Meta:
        model = FeedingPlan
        fields = '__all__'

    def get_alerta_nutricional_ia(self, obj):
        return getattr(obj, 'alerta_nutricional_ia', "Análise indisponível")