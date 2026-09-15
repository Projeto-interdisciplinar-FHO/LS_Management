from rest_framework import generics
from apps.health.vaccination_plans.models import VaccinationPlan
from apps.health.vaccination_plans.serializers import VaccinationPlanSerializer


class VaccinationPlanCreateListView(generics.ListCreateAPIView):
    queryset = VaccinationPlan.objects.all()
    serializer_class = VaccinationPlanSerializer


class VaccinationPlanRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = VaccinationPlan.objects.all()
    serializer_class = VaccinationPlanSerializer
