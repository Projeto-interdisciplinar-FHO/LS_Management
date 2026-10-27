from django.utils import timezone
from rest_framework import viewsets

from apps.health.animal_health.models import AnimalHealth, VeterinaryOccurrence
from apps.health.vaccination_groups.models import VaccinationGroup
from apps.health.vaccination_plans.models import VaccinationPlan
from apps.health.vaccinations.models import Vaccination
from apps.health.vaccines.models import Vaccine
from apps.herd.breeds.models import Breed
from apps.herd.cattle.models import Bull, CattleClass, Cow
from apps.herd.quadrants.models import Quadrant
from apps.movements.animal_movements.models import AnimalMovement
from apps.movements.movement_types.models import MovementType
from apps.nutrition.feeding_plans.models import FeedingPlan
from apps.nutrition.feedings.models import Feeding
from apps.nutrition.foods.models import Food
from apps.production.milk_production_history.models import Milking
from apps.production.weight_history.models import WeightHistory
from apps.reproduction.models import Birth, BirthOccurrence, Insemination

from .serializers import (
    AnimalHealthSerializer, AnimalMovementSerializer, BirthOccurrenceSerializer,
    BirthSerializer, BreedSerializer, BullSerializer, CattleClassSerializer,
    CowSerializer, FeedingPlanSerializer, FeedingSerializer, FoodSerializer,
    InseminationSerializer, MilkingSerializer, MovementTypeSerializer,
    QuadrantSerializer, VaccinationGroupSerializer, VaccinationPlanSerializer,
    VaccinationSerializer, VaccineSerializer, VeterinaryOccurrenceSerializer,
    WeightHistorySerializer,
)


class QuerysetViewSet(viewsets.ModelViewSet):
    filter_field = "animal_id"

    def get_queryset(self):
        queryset = self.queryset
        value = self.request.query_params.get(self.filter_field)
        if value and self.filter_field in {field.name for field in queryset.model._meta.fields}:
            queryset = queryset.filter(**{self.filter_field: value})
        return queryset


class BreedViewSet(QuerysetViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class QuadrantViewSet(QuerysetViewSet):
    queryset = Quadrant.objects.all()
    serializer_class = QuadrantSerializer


class CattleClassViewSet(QuerysetViewSet):
    queryset = CattleClass.objects.all()
    serializer_class = CattleClassSerializer


class BullViewSet(QuerysetViewSet):
    queryset = Bull.objects.all()
    serializer_class = BullSerializer


class CowViewSet(QuerysetViewSet):
    queryset = Cow.objects.all()
    serializer_class = CowSerializer


class MovementTypeViewSet(QuerysetViewSet):
    queryset = MovementType.objects.all()
    serializer_class = MovementTypeSerializer


class AnimalMovementViewSet(QuerysetViewSet):
    queryset = AnimalMovement.objects.select_related("animal", "quadrant", "movement_type")
    serializer_class = AnimalMovementSerializer


class BirthOccurrenceViewSet(QuerysetViewSet):
    queryset = BirthOccurrence.objects.all()
    serializer_class = BirthOccurrenceSerializer


class InseminationViewSet(QuerysetViewSet):
    queryset = Insemination.objects.select_related("mother", "father")
    serializer_class = InseminationSerializer


class BirthViewSet(QuerysetViewSet):
    queryset = Birth.objects.select_related("occurrence", "insemination")
    serializer_class = BirthSerializer


class VaccineViewSet(QuerysetViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer


class VaccinationGroupViewSet(QuerysetViewSet):
    queryset = VaccinationGroup.objects.select_related("animal")
    serializer_class = VaccinationGroupSerializer


class VaccinationPlanViewSet(QuerysetViewSet):
    queryset = VaccinationPlan.objects.select_related("vaccine", "vaccination_group")
    serializer_class = VaccinationPlanSerializer


class VaccinationViewSet(QuerysetViewSet):
    queryset = Vaccination.objects.select_related("animal", "vaccine")
    serializer_class = VaccinationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get("upcoming") == "true":
            queryset = queryset.filter(next_vaccination_date__gte=timezone.localdate())
        return queryset


class VeterinaryOccurrenceViewSet(QuerysetViewSet):
    queryset = VeterinaryOccurrence.objects.all()
    serializer_class = VeterinaryOccurrenceSerializer


class AnimalHealthViewSet(QuerysetViewSet):
    queryset = AnimalHealth.objects.select_related("animal", "occurrence")
    serializer_class = AnimalHealthSerializer


class FoodViewSet(QuerysetViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class FeedingViewSet(QuerysetViewSet):
    queryset = Feeding.objects.select_related("animal", "food")
    serializer_class = FeedingSerializer


class FeedingPlanViewSet(QuerysetViewSet):
    queryset = FeedingPlan.objects.select_related("animal_class", "food")
    serializer_class = FeedingPlanSerializer


class MilkingViewSet(QuerysetViewSet):
    queryset = Milking.objects.select_related("animal")
    serializer_class = MilkingSerializer


class WeightHistoryViewSet(QuerysetViewSet):
    queryset = WeightHistory.objects.select_related("animal")
    serializer_class = WeightHistorySerializer
