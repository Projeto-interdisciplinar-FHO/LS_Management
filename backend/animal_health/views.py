from rest_framework import generics
from animal_health.models import AnimalHealth
from animal_health.serializers import AnimalHealthSerializer

class AnimalHealthCreateListView(generics.ListCreateAPIView):
    queryset = AnimalHealth.objects.all()
    serializer_class = AnimalHealthSerializer

class AnimalHealthRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnimalHealth.objects.all()
    serializer_class = AnimalHealthSerializer