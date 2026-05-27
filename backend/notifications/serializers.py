from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    animal_name = serializers.CharField(source='animal.name', read_only=True)
    notification_type_display = serializers.CharField(
        source='get_notification_type_display',
        read_only=True
    )

    class Meta:
        model = Notification
        fields = [
            'id',
            'message',
            'notification_type',
            'notification_type_display',
            'read',
            'created_at',
            'animal',
            'animal_name',
        ]
        read_only_fields = ['id', 'created_at', 'notification_type_display']

class NotificationUnreadCountSerializer(serializers.Serializer):
    unread_count = serializers.IntegerField()

class NotificationBulkUpdateSerializer(serializers.Serializer):
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="IDs das notificações a serem marcadas como lidas"
    )
