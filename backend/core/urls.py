
from django.contrib import admin
from django.urls import path, include

from species.views import SpecieCreateListView, SpecieRetrieveUpdateDestroy
from quadrants.views import QuadrantCreateListView, QuadrantRetrieveUpdateDestroy
from purpose_types.views import PurposeTypeCreateListView, PurposeTypeRetrieveUpdateDestroy
from animals.views import AnimalCreateListView, AnimalRetrieveUpdateDestroy
from breeds.views import BreedCreateListView, BreedRetrieveUpdateDestroy
from weight_history.views import WeightHistoryCreateListView, WeightHistoryRetrieveUpdateDestroy
from milk_production_history.views import (
    MilkProductionHistoryCreateListView,
    MilkProductionHistoryRetrieveUpdateDestroy,
)
from vaccines.views import VaccineCreateListView, VaccineRetrieveUpdateDestroy
from vaccination_plans.views import VaccinationPlanCreateListView, VaccinationPlanRetrieveUpdateDestroy
from vaccinations.views import VaccinationCreateListView, VaccinationRetrieveUpdateDestroy
from foods.views import FoodCreateListView, FoodRetrieveUpdateDestroy
from feedings.views import FeedingCreateListView, FeedingRetrieveUpdateDestroy
from feeding_plans.views import FeedingPlanCreateListView, FeedingPlanRetrieveUpdateDestroy
from movement_types.views import MovementTypeCreateListView, MovementTypeRetrieveUpdateDestroy
from animal_movements.views import AnimalMovementCreateListView, AnimalMovementRetrieveUpdateDestroy
from animal_health.views import AnimalHealthCreateListView, AnimalHealthRetrieveUpdateDestroy
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from statistics_api.views import ApiStatsView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('species/', SpecieCreateListView.as_view(), name="species-create-list"),
    path('species/<int:pk>', SpecieRetrieveUpdateDestroy.as_view(), name="species-detail-view"),
    path('quadrants/', QuadrantCreateListView.as_view(), name="quadrants-create-list"),
    path('quadrants/<int:pk>', QuadrantRetrieveUpdateDestroy.as_view(), name="quadrants-detail-view"),
    path('purpose_types/', PurposeTypeCreateListView.as_view(), name="purpose-types-create-list"),
    path('purpose_types/<int:pk>', PurposeTypeRetrieveUpdateDestroy.as_view(), name="purpose-types-detail-view"),
    path('animals/', AnimalCreateListView.as_view(), name="animals-create-list"),
    path('animals/<int:pk>', AnimalRetrieveUpdateDestroy.as_view(), name="animals-detail-view"),
    path('breeds/', BreedCreateListView.as_view(), name="breeds-create-list"),
    path('breeds/<int:pk>', BreedRetrieveUpdateDestroy.as_view(), name="breeds-detail-view"),
    path('weight_history/', WeightHistoryCreateListView.as_view(), name="weight-history-create-list"),
    path('weight_history/<int:pk>', WeightHistoryRetrieveUpdateDestroy.as_view(), name="weight-history-detail-view"),
    path('milk_production_history/', MilkProductionHistoryCreateListView.as_view(), name="milk-production-history-create-list"),
    path('milk_production_history/<int:pk>', MilkProductionHistoryRetrieveUpdateDestroy.as_view(), name="milk-production-history-detail-view"),
    path('vaccines/', VaccineCreateListView.as_view(), name="vaccines-create-list"),
    path('vaccines/<int:pk>', VaccineRetrieveUpdateDestroy.as_view(), name="vaccines-detail-view"),
    path('vaccination_plans/', VaccinationPlanCreateListView.as_view(), name="vaccination-plans-create-list"),
    path('vaccination_plans/<int:pk>', VaccinationPlanRetrieveUpdateDestroy.as_view(), name="vaccination-plans-detail-view"),
    path('vaccinations/', VaccinationCreateListView.as_view(), name="vaccinations-create-list"),
    path('vaccinations/<int:pk>', VaccinationRetrieveUpdateDestroy.as_view(), name="vaccinations-detail-view"),
    path('foods/', FoodCreateListView.as_view(), name="foods-create-list"),
    path('foods/<int:pk>', FoodRetrieveUpdateDestroy.as_view(), name="foods-detail-view"),
    path('feedings/', FeedingCreateListView.as_view(), name="feedings-create-list"),
    path('feedings/<int:pk>', FeedingRetrieveUpdateDestroy.as_view(), name="feedings-detail-view"),
    path('feeding_plans/', FeedingPlanCreateListView.as_view(), name="feeding-plans-create-list"),
    path('feeding_plans/<int:pk>', FeedingPlanRetrieveUpdateDestroy.as_view(), name="feeding-plans-detail-view"),
    path('movement_types/', MovementTypeCreateListView.as_view(), name="movement-types-create-list"),
    path('movement_types/<int:pk>', MovementTypeRetrieveUpdateDestroy.as_view(), name="movement-types-detail-view"),
    path('animal_movements/', AnimalMovementCreateListView.as_view(), name="animal-movements-create-list"),
    path('animal_movements/<int:pk>', AnimalMovementRetrieveUpdateDestroy.as_view(), name="animal-movements-detail-view"),
    path('animal_health/', AnimalHealthCreateListView.as_view(), name="animal-health-create-list"),
    path('animal_health/<int:pk>', AnimalHealthRetrieveUpdateDestroy.as_view(), name="animal-health-detail-view"),

    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('authentication/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('authentication/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('authentication/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('statistics/', ApiStatsView.as_view(), name='stats-view'),
]
