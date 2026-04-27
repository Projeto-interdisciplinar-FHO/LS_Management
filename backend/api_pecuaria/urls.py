from django.urls import path
from .views import (
    AnimalCreateListView,
    AnimalRetrieveUpdateDestroy,
    AnimalHealthCreateListView,
    AnimalHealthRetrieveUpdateDestroy,
    VaccinationCreateListView,
    VaccinationRetrieveUpdateDestroy,
    WeightHistoryCreateListView,
    WeightHistoryRetrieveUpdateDestroy,
)

urlpatterns = [
    # Animal
    path('animals/', AnimalCreateListView.as_view(), name='animal-list-create'),
    path('animals/<int:pk>/', AnimalRetrieveUpdateDestroy.as_view(), name='animal-detail'),

    # Saúde
    path('animal-health/', AnimalHealthCreateListView.as_view(), name='animal-health-list-create'),
    path('animal-health/<int:pk>/', AnimalHealthRetrieveUpdateDestroy.as_view(), name='animal-health-detail'),

    # Vacinação
    path('vaccinations/', VaccinationCreateListView.as_view(), name='vaccination-list-create'),
    path('vaccinations/<int:pk>/', VaccinationRetrieveUpdateDestroy.as_view(), name='vaccination-detail'),

    # Histórico de peso
    path('weight-history/', WeightHistoryCreateListView.as_view(), name='weight-history-list-create'),
    path('weight-history/<int:pk>/', WeightHistoryRetrieveUpdateDestroy.as_view(), name='weight-history-detail'),
]