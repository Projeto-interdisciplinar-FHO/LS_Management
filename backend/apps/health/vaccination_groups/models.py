from django.db import models

from apps.herd.cattle.models import Cow


class VaccinationGroup(models.Model):
    name = models.CharField(max_length=50)
    animal = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name="vaccination_groups")

    class Meta:
        db_table = "vaccination_groups"
        ordering = ["name"]

    def __str__(self):
        return self.name
