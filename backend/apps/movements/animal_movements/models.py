from django.db import models
from django.conf import settings
from apps.herd.quadrants.models import Quadrant
from apps.herd.cattle.models import Cow
from apps.movements.movement_types.models import MovementType


class AnimalMovement(models.Model):
    quadrant = models.ForeignKey(Quadrant, on_delete=models.CASCADE, related_name='animal_movements')
    movement_date = models.DateField()
    movement_reason = models.TextField()
    animal = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='movements')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='movements')
    movement_type = models.ForeignKey(MovementType, on_delete=models.CASCADE, related_name='movements')

    def __str__(self):
        return f"{self.animal.name} - {self.movement_date}"
