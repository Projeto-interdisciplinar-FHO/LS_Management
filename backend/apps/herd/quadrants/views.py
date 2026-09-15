from rest_framework import generics
from apps.herd.quadrants.models import Quadrant
from apps.herd.quadrants.serializers import QuadrantSerializer

class QuadrantCreateListView(generics.ListCreateAPIView):
    queryset = Quadrant.objects.all()
    serializer_class = QuadrantSerializer

class QuadrantRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quadrant.objects.all()
    serializer_class = QuadrantSerializer