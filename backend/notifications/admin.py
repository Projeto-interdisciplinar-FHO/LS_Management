from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'notification_type', 'read', 'animal', 'created_at')
    list_filter = ('notification_type', 'read', 'created_at')
    search_fields = ('message', 'animal__name')
    readonly_fields = ('created_at', 'message', 'notification_type', 'animal')
    
    actions = ['mark_as_read', 'mark_as_unread', 'delete_old_notifications']
    
    def mark_as_read(self, request, queryset):
        count = queryset.update(read=True)
        self.message_user(request, f'{count} notificações marcadas como lidas.')
    mark_as_read.short_description = 'Marcar como lidas'
    
    def mark_as_unread(self, request, queryset):
        count = queryset.update(read=False)
        self.message_user(request, f'{count} notificações marcadas como não lidas.')
    mark_as_unread.short_description = 'Marcar como não lidas'
    
    def delete_old_notifications(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=30)
        count = Notification.objects.filter(created_at__lt=cutoff_date).delete()[0]
        self.message_user(request, f'{count} notificações antigas deletadas.')
    delete_old_notifications.short_description = 'Deletar notificações com mais de 30 dias'

    def has_add_permission(self, request):
        """Impede que notificações sejam criadas manualmente no admin"""
        return False
