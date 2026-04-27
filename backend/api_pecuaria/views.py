from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from animals.models import Animal
from animal_health.models import AnimalHealth
from vaccinations.models import Vaccination
from weight_history.models import WeightHistory
from .serializers import (
    AnimalSerializer,
    AnimalHealthSerializer,
    VaccinationSerializer,
    WeightHistorySerializer,
)


class AnimalCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer


class AnimalRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer


class AnimalHealthCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = AnimalHealth.objects.all()
    serializer_class = AnimalHealthSerializer


class AnimalHealthRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = AnimalHealth.objects.all()
    serializer_class = AnimalHealthSerializer


class VaccinationCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Vaccination.objects.all()
    serializer_class = VaccinationSerializer


class VaccinationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Vaccination.objects.all()
    serializer_class = VaccinationSerializer


class WeightHistoryCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = WeightHistory.objects.all()
    serializer_class = WeightHistorySerializer


class WeightHistoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = WeightHistory.objects.all()
    serializer_class = WeightHistorySerializer