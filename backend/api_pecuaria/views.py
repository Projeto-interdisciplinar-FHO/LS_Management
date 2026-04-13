from rest_framework import generics
from gestao.models import Bovino, Historico
from .serializers import BovinoSerializer, HistoricoSerializer

class BovinoListCreateView(generics.ListCreateAPIView):
    queryset = Bovino.objects.all()
    serializer_class = BovinoSerializer

class DetalheBovinoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bovino.objects.all()
    serializer_class = BovinoSerializer
    lookup_field = 'rfid_tag' # Usamos rfid_tag em vez de ID

class RegistrarEventoView(generics.ListCreateAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer