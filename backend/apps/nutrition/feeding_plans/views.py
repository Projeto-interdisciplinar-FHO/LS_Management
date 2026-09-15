from rest_framework import generics
from apps.nutrition.feeding_plans.models import FeedingPlan
from apps.nutrition.feeding_plans.serializers import FeedingPlanSerializer


class FeedingPlanCreateListView(generics.ListCreateAPIView):
    queryset = FeedingPlan.objects.all()
    serializer_class = FeedingPlanSerializer


class FeedingPlanRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeedingPlan.objects.all()
    serializer_class = FeedingPlanSerializer
