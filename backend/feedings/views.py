from rest_framework import generics
from feedings.models import Feeding
from feedings.serializers import FeedingSerializer


class FeedingCreateListView(generics.ListCreateAPIView):
    queryset = Feeding.objects.all()
    serializer_class = FeedingSerializer


class FeedingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feeding.objects.all()
    serializer_class = FeedingSerializer
