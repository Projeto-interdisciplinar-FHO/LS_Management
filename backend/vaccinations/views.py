from rest_framework import generics
from vaccinations.models import Vaccination
from vaccinations.serializers import VaccinationSerializer

class VaccinationCreateListView(generics.ListCreateAPIView):
    queryset = Vaccination.objects.all()
    serializer_class = VaccinationSerializer

class VaccinationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vaccination.objects.all()
    serializer_class = VaccinationSerializer