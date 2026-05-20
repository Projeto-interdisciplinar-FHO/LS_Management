from django.db import models
from animals.models import Animal

class AnimalHealth(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='health_records')
    medication_taken = models.IntegerField(default=0)
    veterinarian = models.CharField(max_length=100)
    consultation_date = models.DateField()
    consultation_reason = models.TextField()

    def __str__(self):
        return f"{self.animal.name} - {self.consultation_date}"