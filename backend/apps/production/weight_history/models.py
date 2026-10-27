from django.db import models
from apps.herd.cattle.models import Cow

class WeightHistory(models.Model):
    animal = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name="weight_history")
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    weighing_date = models.DateField()
