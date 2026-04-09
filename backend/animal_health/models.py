from django.db import models
from animals.models import Animal

class AnimalHealth(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    sleep_quality = models.IntegerField()
    disease_prediction = models.IntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    consultation_date = models.DateField()
    temperature = models.IntegerField()