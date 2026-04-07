from django.db import models

class Quadrant(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    area = models.IntegerField()
    max_animals = models.IntegerField()

    def __str__(self):
        return self.name