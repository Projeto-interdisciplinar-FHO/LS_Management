from django.db import models

from apps.herd.cattle.models import Bull, Cow


class BirthOccurrence(models.Model):
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "birth_occurrences"
        ordering = ["description"]

    def __str__(self):
        return self.description


class Insemination(models.Model):
    mother = models.ForeignKey(Cow, on_delete=models.PROTECT, related_name="inseminations")
    father = models.ForeignKey(Bull, on_delete=models.PROTECT, related_name="inseminations")
    date = models.DateField()

    class Meta:
        db_table = "inseminations"
        ordering = ["-date"]


class Birth(models.Model):
    insemination = models.ForeignKey(
        Insemination,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="births",
    )
    occurrence = models.ForeignKey(
        BirthOccurrence,
        on_delete=models.PROTECT,
        related_name="births",
    )
    date = models.DateField()
    weight = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = "births"
        ordering = ["-date"]
