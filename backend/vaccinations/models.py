from django.db import models
from animals.models import Animal
from vaccines.models import Vaccine

class Vaccination(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    dosage = models.DecimalField(max_digits=10, decimal_places=2)
    vaccination_date = models.DateField()
    periodicity = models.IntegerField()
    doses_taken = models.IntegerField()
    total_doses = models.IntegerField()
    vaccination_status = models.BooleanField()