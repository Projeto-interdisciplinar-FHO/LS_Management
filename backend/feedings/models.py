from django.db import models
from animals.models import Animal
from foods.models import Food


class Feeding(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='feedings')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='feedings')
    feeding_time = models.DateTimeField()
    meal_weight = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.animal.name} - {self.food.name}"
