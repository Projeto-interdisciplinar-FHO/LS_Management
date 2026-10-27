from rest_framework import serializers

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


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"


class BreedSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = Breed


class QuadrantSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = Quadrant


class CattleClassSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = CattleClass


class BullSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = Bull


class CowSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = Cow


class MovementTypeSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = MovementType


class AnimalMovementSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = AnimalMovement


class BirthOccurrenceSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = BirthOccurrence


class InseminationSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = Insemination


class BirthSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = Birth


class VaccineSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = Vaccine


class VaccinationGroupSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = VaccinationGroup


class VaccinationPlanSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = VaccinationPlan


class VaccinationSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = Vaccination


class VeterinaryOccurrenceSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = VeterinaryOccurrence


class AnimalHealthSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = AnimalHealth


class FoodSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = Food


class FeedingSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = Feeding


class FeedingPlanSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = FeedingPlan


class MilkingSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = Milking


class WeightHistorySerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = WeightHistory
