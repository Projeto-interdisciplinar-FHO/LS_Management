from django.db import models
from animals.models import Animal


class MilkProductionHistory(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='milk_production_history')
    milk_production = models.DecimalField(max_digits=10, decimal_places=2)
    production_date = models.DateField()

    def __str__(self):
        return f"{self.animal.name} - {self.production_date}"
