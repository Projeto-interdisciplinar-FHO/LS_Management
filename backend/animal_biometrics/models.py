from django.db import models
from animals.models import Animal
from django.utils import timezone

class BiometricReading(models.Model):
    """
    Armazena leituras de sensores IoT (colares/brincos) dos animais.
    Dados provenientes da API externa que o Django consome e mastiga.
    """
    ALERT_LEVEL_CHOICES = [
        ('normal', 'Normal'),
        ('warning', 'Aviso'),
        ('critical', 'Crítico'),
    ]
    
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='biometric_readings')
    
    # Medições biométricas
    heart_rate = models.IntegerField(help_text="BPM - Batimentos por minuto")  # Ex: 72 BPM
    sleep_duration = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text="Horas de sono nas últimas 24h"
    )  # Ex: 6.50 horas
    body_temperature = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Temperatura corporal em Celsius"
    )  # Ex: 38.5°C
    
    # Sintomas detectados (campo de texto ou JSON)
    symptoms = models.CharField(
        max_length=500, 
        blank=True,
        help_text="Sintomas detectados. Ex: 'Agitação, Tosse, Respiração acelerada'"
    )
    
    # Metadata
    alert_level = models.CharField(
        max_length=20,
        choices=ALERT_LEVEL_CHOICES,
        default='normal'
    )
    reading_timestamp = models.DateTimeField(auto_now_add=True)  # Quando foi lida
    sensor_battery = models.IntegerField(
        null=True, 
        blank=True,
        help_text="Nível de bateria do sensor em %"
    )  # Ex: 85%
    
    class Meta:
        ordering = ['-reading_timestamp']
        indexes = [
            models.Index(fields=['-reading_timestamp']),
            models.Index(fields=['animal', '-reading_timestamp']),
        ]
    
    def __str__(self):
        return f"{self.animal.name} - {self.reading_timestamp.strftime('%d/%m/%Y %H:%M')}"
    
    def get_alert_level_emoji(self):
        """Retorna emoji baseado no nível de alerta"""
        emojis = {
            'normal': '✅',
            'warning': '⚠️',
            'critical': '🚨',
        }
        return emojis.get(self.alert_level, '❓')


class AnimalAlert(models.Model):
    """
    Alertas críticos gerados automaticamente pela análise de biometria.
    Sistema de alerta: se a vaca dormiu 0 horas E está com 120 BPM = Alerta Crítico.
    """
    SEVERITY_CHOICES = [
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta'),
        ('critical', 'Crítica'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('acknowledged', 'Reconhecido'),
        ('resolved', 'Resolvido'),
    ]
    
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='alerts')
    
    # Informação do alerta
    title = models.CharField(max_length=200, help_text="Ex: Suspeita de Febre Alta")
    description = models.TextField(help_text="Descrição detalhada do alerta")
    reason = models.CharField(
        max_length=500,
        help_text="Por que o alerta foi disparado. Ex: 'Frequência cardíaca 120 BPM + Sono 0 horas'"
    )
    
    # Severidade
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='medium'
    )
    
    # Dados que acionaram o alerta
    biometric_reading = models.ForeignKey(
        BiometricReading, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='alerts'
    )
    
    # Status do alerta
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['animal', 'status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.animal.name} - {self.title} ({self.get_severity_display()})"
    
    def get_severity_emoji(self):
        """Retorna emoji baseado na severidade"""
        emojis = {
            'low': '💭',
            'medium': '⚠️',
            'high': '🔴',
            'critical': '🚨',
        }
        return emojis.get(self.severity, '❓')
    
    def acknowledge(self):
        """Marca o alerta como reconhecido pelo operador"""
        self.status = 'acknowledged'
        self.acknowledged_at = timezone.now()
        self.save()
    
    def resolve(self):
        """Marca o alerta como resolvido"""
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        self.save()
