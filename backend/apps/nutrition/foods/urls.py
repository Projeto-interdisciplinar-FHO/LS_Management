from django.urls import path

from apps.nutrition.foods.views import FoodCreateListView, FoodRetrieveUpdateDestroy

urlpatterns = [
    path('', FoodCreateListView.as_view(), name="foods-create-list"),
    path('<int:pk>', FoodRetrieveUpdateDestroy.as_view(), name="foods-detail-view"),
]
