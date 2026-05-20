from django.db import models
from animals.models import Animal
from vaccines.models import Vaccine


class VaccinationPlan(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='vaccination_plans')
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name='vaccination_plans')
    periodicity = models.IntegerField()
    total_doses = models.IntegerField()
    vaccination_status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.animal.name} - {self.vaccine.name}"
