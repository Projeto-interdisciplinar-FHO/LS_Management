from django.db import models
from species.models import Specie


class Breed(models.Model):
    name = models.CharField(max_length=50)
    specie = models.ForeignKey(
        Specie,
        on_delete=models.CASCADE,
        related_name='breeds',
        null=True,
        blank=True,
        help_text="Espécie à qual esta raça pertence"
    )

    def __str__(self):
        return f"{self.name} ({self.specie.name if self.specie else 'N/A'})"
    
    class Meta:
        ordering = ['specie', 'name']
        verbose_name_plural = "Breeds"

