from rest_framework import generics
from animals.models import Animal
from animals.serializers import AnimalSerializer
from rest_framework.permissions import IsAuthenticated

class AnimalCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

class AnimalRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer