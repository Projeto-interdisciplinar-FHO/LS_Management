from rest_framework.routers import DefaultRouter

from .views import (
    AnimalHealthViewSet, AnimalMovementViewSet, BirthOccurrenceViewSet,
    BirthViewSet, BreedViewSet, BullViewSet, CattleClassViewSet, CowViewSet,
    FeedingPlanViewSet, FeedingViewSet, FoodViewSet, InseminationViewSet,
    MilkingViewSet, MovementTypeViewSet, QuadrantViewSet,
    VaccinationGroupViewSet, VaccinationPlanViewSet, VaccinationViewSet,
    VaccineViewSet, VeterinaryOccurrenceViewSet, WeightHistoryViewSet,
)

router = DefaultRouter()
router.register("breeds", BreedViewSet)
router.register("quadrants", QuadrantViewSet)
router.register("classes", CattleClassViewSet)
router.register("bulls", BullViewSet)
router.register("cows", CowViewSet)
router.register("animals", CowViewSet, basename="animals")
router.register("movement_types", MovementTypeViewSet)
router.register("animal_movements", AnimalMovementViewSet)
router.register("birth_occurrences", BirthOccurrenceViewSet)
router.register("inseminations", InseminationViewSet)
router.register("births", BirthViewSet)
router.register("vaccines", VaccineViewSet)
router.register("vaccination_groups", VaccinationGroupViewSet)
router.register("vaccination_plans", VaccinationPlanViewSet)
router.register("vaccinations", VaccinationViewSet)
router.register("veterinary_occurrences", VeterinaryOccurrenceViewSet)
router.register("animal_health", AnimalHealthViewSet)
router.register("foods", FoodViewSet)
router.register("feedings", FeedingViewSet)
router.register("feeding_plans", FeedingPlanViewSet)
router.register("milking", MilkingViewSet)
router.register("milk_production_history", MilkingViewSet, basename="milk-production-history")
router.register("weight_history", WeightHistoryViewSet)

urlpatterns = router.urls
