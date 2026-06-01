from rest_framework import generics
from animal_health.models import AnimalHealth
from animal_health.serializers import AnimalHealthSerializer

class AnimalHealthCreateListView(generics.ListCreateAPIView):
    queryset = AnimalHealth.objects.all()
    serializer_class = AnimalHealthSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        animal_id = self.request.query_params.get('animal_id')
        if animal_id:
            queryset = queryset.filter(animal_id=animal_id)
        return queryset

class AnimalHealthRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnimalHealth.objects.all()
    serializer_class = AnimalHealthSerializer