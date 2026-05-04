from rest_framework import generics
from milk_production_history.models import MilkProductionHistory
from milk_production_history.serializers import MilkProductionHistorySerializer


class MilkProductionHistoryCreateListView(generics.ListCreateAPIView):
    queryset = MilkProductionHistory.objects.all()
    serializer_class = MilkProductionHistorySerializer


class MilkProductionHistoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = MilkProductionHistory.objects.all()
    serializer_class = MilkProductionHistorySerializer
