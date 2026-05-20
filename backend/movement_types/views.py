from rest_framework import generics
from movement_types.models import MovementType
from movement_types.serializers import MovementTypeSerializer


class MovementTypeCreateListView(generics.ListCreateAPIView):
    queryset = MovementType.objects.all()
    serializer_class = MovementTypeSerializer


class MovementTypeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovementType.objects.all()
    serializer_class = MovementTypeSerializer
