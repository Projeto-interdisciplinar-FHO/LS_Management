from rest_framework import generics
from breeds.models import Breed
from breeds.serializers import BreedSerializer


class BreedCreateListView(generics.ListCreateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class BreedRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
