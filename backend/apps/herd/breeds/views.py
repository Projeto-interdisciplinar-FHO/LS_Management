from rest_framework import generics
from apps.herd.breeds.models import Breed
from apps.herd.breeds.serializers import BreedSerializer


class BreedCreateListView(generics.ListCreateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class BreedRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
