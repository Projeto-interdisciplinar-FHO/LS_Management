from django.db import models
from species.models import Specie
from quadrants.models import Quadrant
from purpose_types.models import PurposeType

class Animal(models.Model):
    name = models.CharField(max_length=45)
    birth_date = models.DateField()
    register_number = models.IntegerField()
    weight = models.DecimalField(max_digits=8, decimal_places=2)
    active = models.BooleanField()
    sex = models.CharField(max_length=1)
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE)
    quadrant = models.ForeignKey(Quadrant, on_delete=models.CASCADE)
    purpose = models.ForeignKey(PurposeType, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name