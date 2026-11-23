from django.urls import path

from apps.production.weight_history.views import (
    WeightHistoryByAnimalView,
    WeightHistoryCreateListView,
    WeightHistoryRetrieveUpdateDestroy,
)

urlpatterns = [
    path('', WeightHistoryCreateListView.as_view(), name="weight-history-create-list"),
    path('<int:pk>', WeightHistoryRetrieveUpdateDestroy.as_view(), name="weight-history-detail-view"),
    path('animal/<int:animal_id>/', WeightHistoryByAnimalView.as_view(), name="weight-history-by-animal"),
]
