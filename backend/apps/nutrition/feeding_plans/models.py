from django.db import models
from apps.herd.cattle.models import CattleClass
from apps.nutrition.foods.models import Food


class FeedingPlan(models.Model):
    animal_class = models.ForeignKey(CattleClass, on_delete=models.PROTECT, related_name='feeding_plans')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='feeding_plans')
    periodicity = models.IntegerField()

    def __str__(self):
        return f"{self.animal_class.name} - {self.food.name}"
