from django.urls import path

from apps.health.vaccinations.views import (
    VaccinationCreateListView,
    VaccinationRetrieveUpdateDestroy,
    batch_vaccination,
    quadrant_animals_count,
    upcoming_vaccinations,
    vaccinations_by_animal,
)

urlpatterns = [
    path('', VaccinationCreateListView.as_view(), name="vaccinations-create-list"),
    path('<int:pk>', VaccinationRetrieveUpdateDestroy.as_view(), name="vaccinations-detail-view"),
    path('animal/<int:animal_id>/', vaccinations_by_animal, name="vaccinations-by-animal"),
    path('upcoming/', upcoming_vaccinations, name="vaccinations-upcoming"),
    path('batch/', batch_vaccination, name="vaccinations-batch"),
    path('quadrant/<int:quadrant_id>/animals-count/', quadrant_animals_count, name="quadrant-animals-count"),
]
