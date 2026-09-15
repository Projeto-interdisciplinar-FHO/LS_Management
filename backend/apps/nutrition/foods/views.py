from rest_framework import generics
from apps.nutrition.foods.models import Food
from apps.nutrition.foods.serializers import FoodSerializer


class FoodCreateListView(generics.ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class FoodRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
