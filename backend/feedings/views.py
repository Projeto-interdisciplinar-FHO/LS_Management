from rest_framework import generics
from feedings.models import Feeding
from feedings.serializers import FeedingSerializer


class FeedingCreateListView(generics.ListCreateAPIView):
    queryset = Feeding.objects.all().select_related('animal', 'food')
    serializer_class = FeedingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        animal_id = self.request.query_params.get('animal_id')
        if animal_id:
            queryset = queryset.filter(animal_id=animal_id)
        return queryset


class FeedingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feeding.objects.all()
    serializer_class = FeedingSerializer
