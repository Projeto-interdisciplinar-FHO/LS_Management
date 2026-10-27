from django.db import models


class VaccineApplication(models.Model):
    cow = models.ForeignKey(
        "cattle.Cow",
        on_delete=models.CASCADE,
        related_name="vaccine_applications",
    )
    vaccine = models.ForeignKey(
        "vaccines.Vaccine",
        on_delete=models.PROTECT,
        related_name="applications",
    )
    application_date = models.DateField()
    dosage = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = "vaccine_applications"
        ordering = ["-application_date"]

    def __str__(self):
        return f"{self.cow} - {self.vaccine} ({self.application_date})"
