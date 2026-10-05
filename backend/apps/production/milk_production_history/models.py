from django.db import models

from apps.herd.cattle.models import Cow


class Milking(models.Model):
    animal = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name="milkings")
    milk_production = models.DecimalField(max_digits=10, decimal_places=2)
    production_date = models.DateField()
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "milkings"
        ordering = ["-production_date"]
