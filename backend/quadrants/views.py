from rest_framework import generics
from quadrants.models import Quadrant
from quadrants.serializers import QuadrantSerializer

class QuadrantCreateListView(generics.ListCreateAPIView):
    queryset = Quadrant.objects.all()
    serializer_class = QuadrantSerializer

class QuadrantRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quadrant.objects.all()
    serializer_class = QuadrantSerializer