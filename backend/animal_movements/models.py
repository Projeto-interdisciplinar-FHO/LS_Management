from django.db import models
from django.contrib.auth.models import User
from quadrants.models import Quadrant
from animals.models import Animal
from movement_types.models import MovementType


class AnimalMovement(models.Model):
    quadrant = models.ForeignKey(Quadrant, on_delete=models.CASCADE, related_name='animal_movements')
    movement_date = models.DateField()
    movement_reason = models.TextField()
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='movements')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='movements')
    movement_type = models.ForeignKey(MovementType, on_delete=models.CASCADE, related_name='movements')

    def __str__(self):
        return f"{self.animal.name} - {self.movement_date}"
