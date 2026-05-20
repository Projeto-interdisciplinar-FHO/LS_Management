from django.db import models
from django.utils import timezone
from animals.models import Animal
from vaccines.models import Vaccine

class Vaccination(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    vaccination_plan = models.ForeignKey('vaccination_plans.VaccinationPlan', on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    dosage = models.DecimalField(max_digits=10, decimal_places=2)
    vaccination_date = models.DateField()
    next_vaccination_date = models.DateField(null=True, blank=True, help_text="Data da próxima dose recomendada")
    periodicity = models.IntegerField(null=True, blank=True, help_text="Periodicidade em dias")
    doses_taken = models.IntegerField(null=True, blank=True)
    total_doses = models.IntegerField(null=True, blank=True)
    vaccination_status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.animal.name} - {self.vaccine.name} ({self.vaccination_date})"
    
    @property
    def is_overdue(self):
        """Verifica se a próxima vacina está atrasada"""
        if not self.next_vaccination_date:
            return False
        return self.next_vaccination_date < timezone.now().date()
    
    @property
    def days_until_next(self):
        """Retorna quantidade de dias até a próxima vacinação"""
        if not self.next_vaccination_date:
            return None
        delta = (self.next_vaccination_date - timezone.now().date()).days
        return delta
