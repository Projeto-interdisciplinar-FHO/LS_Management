from rest_framework import generics
from animals.models import Animal
from animals.serializers import AnimalSerializer

class AnimalCreateListView(generics.ListCreateAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

class AnimalRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer