from rest_framework import generics
from weight_history.models import WeightHistory
from weight_history.serializers import WeightHistorySerializer

class WeightHistoryCreateListView(generics.ListCreateAPIView):
    queryset = WeightHistory.objects.all()
    serializer_class = WeightHistorySerializer

class WeightHistoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = WeightHistory.objects.all()
    serializer_class = WeightHistorySerializer