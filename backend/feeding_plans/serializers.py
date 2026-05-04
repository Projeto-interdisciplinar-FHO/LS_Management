from rest_framework import serializers
from feeding_plans.models import FeedingPlan


class FeedingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedingPlan
        fields = '__all__'
