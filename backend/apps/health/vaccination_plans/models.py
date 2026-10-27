from django.db import models
from apps.health.vaccines.models import Vaccine
from apps.health.vaccination_groups.models import VaccinationGroup


class VaccinationPlan(models.Model):
    vaccination_group = models.ForeignKey(VaccinationGroup, on_delete=models.PROTECT, related_name='vaccination_plans')
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name='vaccination_plans')
    periodicity = models.IntegerField()
    total_doses = models.IntegerField()
    vaccination_status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.vaccination_group.name} - {self.vaccine.name}"
