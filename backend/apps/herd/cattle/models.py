from django.db import models

from apps.herd.breeds.models import Breed
from apps.herd.quadrants.models import Quadrant


class CattleClass(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "classes"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Bull(models.Model):
    name = models.CharField(max_length=100)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, related_name="bulls")
    register_number = models.IntegerField(unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "bulls"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Cow(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("sold", "Sold"),
        ("deceased", "Deceased"),
    ]

    name = models.CharField(max_length=100)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, related_name="cows")
    register_number = models.IntegerField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    score = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    reproductive_status = models.BooleanField(default=True)
    birth = models.ForeignKey(
        "reproduction.Birth",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="calves",
    )

    class Meta:
        db_table = "cows"
        ordering = ["name"]

    def __str__(self):
        return self.name
