from rest_framework import generics
from vaccines.models import Vaccine
from vaccines.serializers import VaccineSerializer

class VaccineCreateListView(generics.ListCreateAPIView):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer

class VaccineRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer