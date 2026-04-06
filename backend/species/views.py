from rest_framework import generics
from species.models import Specie
from species.serializes import SpecieSerializer

class SpecieCreateListView(generics.ListCreateAPIView):
    queryset = Specie.objects.all()
    serializer_class = SpecieSerializer

class SpecieRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specie.objects.all()
    serializer_class = SpecieSerializer