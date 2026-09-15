from rest_framework import serializers
from apps.nutrition.feeding_plans.models import FeedingPlan


class FeedingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedingPlan
        fields = '__all__'
