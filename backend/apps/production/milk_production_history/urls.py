from django.urls import path

from apps.production.milk_production_history.views import (
    MilkProductionHistoryByAnimalView,
    MilkProductionHistoryCreateListView,
    MilkProductionHistoryRetrieveUpdateDestroy,
)

urlpatterns = [
    path('', MilkProductionHistoryCreateListView.as_view(), name="milk-production-history-create-list"),
    path('<int:pk>', MilkProductionHistoryRetrieveUpdateDestroy.as_view(), name="milk-production-history-detail-view"),
    path('animal/<int:animal_id>/', MilkProductionHistoryByAnimalView.as_view(), name="milk-production-history-by-animal"),
]
