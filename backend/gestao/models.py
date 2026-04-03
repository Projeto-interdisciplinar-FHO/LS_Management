from django.db import models
from django.utils import timezone

class Bovino(models.Model):
    Choices = [
        ('Ativo', 'Ativo'),
        ('Vendido', 'Vendido'),
    ]

    rfid_tag = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=100)

    raca = models.CharField(max_length=50, blank=True, null=True)

    status = models.CharField(
        max_length=20, 
        choices=Choices, 
        default='Ativo'
    )

    def __str__(self):
        return f"{self.nome} ({self.rfid_tag})"

class Historico(models.Model):
    TIPOS = [
        ('PESO', 'Peso (kg)'),
        ('VACINA', 'Vacina'),
        ('LEITE', 'Produção Leite (L)'),
        ('SONO', 'Sono (Horas)'),
        ('BPM', 'Batimentos (BPM)'),
    ]
    
    animal = models.ForeignKey(Bovino, on_delete=models.CASCADE, related_name='historicos')
    tipo = models.CharField(max_length=10, choices=TIPOS)
    valor = models.FloatField()
    sintomas = models.TextField(blank=True, null=True)
    data = models.DateTimeField(default=timezone.now)
    #data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']