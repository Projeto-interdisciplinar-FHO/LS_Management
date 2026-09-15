from django.urls import path

from apps.herd.breeds.views import BreedCreateListView, BreedRetrieveUpdateDestroy

urlpatterns = [
    path('', BreedCreateListView.as_view(), name="breeds-create-list"),
    path('<int:pk>', BreedRetrieveUpdateDestroy.as_view(), name="breeds-detail-view"),
]
