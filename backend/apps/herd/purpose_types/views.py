from rest_framework import generics
from apps.herd.purpose_types.models import PurposeType
from apps.herd.purpose_types.serializers import PurposeTypeSerializer

class PurposeTypeCreateListView(generics.ListCreateAPIView):
    queryset = PurposeType.objects.all()
    serializer_class = PurposeTypeSerializer

class PurposeTypeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurposeType.objects.all()
    serializer_class = PurposeTypeSerializer