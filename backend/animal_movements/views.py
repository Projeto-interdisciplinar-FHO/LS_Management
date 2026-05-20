from rest_framework import generics
from animal_movements.models import AnimalMovement
from animal_movements.serializers import AnimalMovementSerializer


class AnimalMovementCreateListView(generics.ListCreateAPIView):
    queryset = AnimalMovement.objects.all()
    serializer_class = AnimalMovementSerializer


class AnimalMovementRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnimalMovement.objects.all()
    serializer_class = AnimalMovementSerializer
