from django.db import models

from apps.herd.cattle.models import Cow


class VeterinaryOccurrence(models.Model):
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "veterinary_occurrences"
        ordering = ["description"]

    def __str__(self):
        return self.description


class AnimalHealth(models.Model):
    animal = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name="health_records")
    medication_taken = models.IntegerField(default=0)
    consultation_date = models.DateField()
    consultation_reason = models.TextField()
    occurrence = models.ForeignKey(
        VeterinaryOccurrence,
        on_delete=models.PROTECT,
        related_name="health_records",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "animal_health"
        ordering = ["-consultation_date"]