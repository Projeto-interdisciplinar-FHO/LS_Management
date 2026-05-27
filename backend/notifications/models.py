from django.db import models
from django.utils import timezone

class Notification(models.Model):
    """
    Modelo para notificações do administrador.
    Registra todas as ações importantes realizadas pelos operadores.
    """
    
    NOTIFICATION_TYPES = [
        ('weight', 'Pesagem Registrada'),
        ('vaccination', 'Vacinação Aplicada'),
        ('feeding', 'Alimentação Registrada'),
        ('health', 'Problema de Saúde Identificado'),
        ('movement', 'Movimento de Animal'),
        ('milk', 'Ordenha Registrada'),
        ('batch_vaccination', 'Vacinação em Lote'),
        ('animal_created', 'Animal Cadastrado'),
    ]

    message = models.TextField(
        help_text="Mensagem da notificação para o administrador"
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='weight',
        help_text="Tipo de notificação"
    )
    read = models.BooleanField(
        default=False,
        help_text="Indica se a notificação foi lida"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e hora de criação"
    )
    
    # Relacionamentos opcionais para rastreabilidade
    animal = models.ForeignKey(
        'animals.Animal',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications',
        help_text="Animal relacionado à notificação"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['read', '-created_at']),
        ]

    def __str__(self):
        return f"[{self.get_notification_type_display()}] {self.message[:50]}"

    def mark_as_read(self):
        """Marca a notificação como lida"""
        if not self.read:
            self.read = True
            self.save(update_fields=['read'])

    @classmethod
    def create_notification(cls, message, notification_type='weight', animal=None):
        """
        Método auxiliar para criar notificações de forma consistente
        
        Args:
            message (str): Mensagem da notificação
            notification_type (str): Tipo de notificação
            animal (Animal): Animal relacionado (opcional)
        
        Returns:
            Notification: Notificação criada
        """
        return cls.objects.create(
            message=message,
            notification_type=notification_type,
            animal=animal,
            read=False
        )

    @classmethod
    def get_unread_count(cls):
        """Retorna a contagem de notificações não lidas"""
        return cls.objects.filter(read=False).count()

    @classmethod
    def get_unread_notifications(cls, limit=10):
        """Retorna as notificações não lidas mais recentes"""
        return cls.objects.filter(read=False)[:limit]
