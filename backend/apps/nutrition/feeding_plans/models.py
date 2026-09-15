from django.db import models
from apps.herd.animals.models import Animal
from apps.nutrition.foods.models import Food


class FeedingPlan(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='feeding_plans')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='feeding_plans')
    periodicity = models.IntegerField()

    def __str__(self):
        return f"{self.animal.name} - {self.food.name}"
