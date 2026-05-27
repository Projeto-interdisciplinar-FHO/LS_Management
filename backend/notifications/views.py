from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import (
    NotificationSerializer,
    NotificationUnreadCountSerializer,
    NotificationBulkUpdateSerializer,
)

class NotificationListView(generics.ListAPIView):
    """
    Lista todas as notificações com paginação.
    Mais recentes primeiro.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    ordering = '-created_at'
    pagination_class = None  # Pode ser ajustado para paginação


class NotificationUnreadListView(generics.ListAPIView):
    """
    Lista apenas notificações não lidas.
    Útil para o dashboard do administrador.
    """
    queryset = Notification.objects.filter(read=False)
    serializer_class = NotificationSerializer
    ordering = '-created_at'
    pagination_class = None


class NotificationUnreadCountView(APIView):
    """
    Retorna apenas a contagem de notificações não lidas.
    Leve e rápido para polling contínuo do sininho.
    """
    def get(self, request):
        unread_count = Notification.objects.filter(read=False).count()
        return Response({
            'unread_count': unread_count
        })


class NotificationMarkAsReadView(generics.UpdateAPIView):
    """
    Marca uma notificação específica como lida.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.mark_as_read()
        return Response({
            'detail': 'Notificação marcada como lida',
            'notification': NotificationSerializer(notification).data
        })


class NotificationBulkMarkAsReadView(APIView):
    """
    Marca múltiplas notificações como lidas de uma vez.
    Útil quando o usuário clica em "marcar todas como lidas".
    """
    def post(self, request):
        serializer = NotificationBulkUpdateSerializer(data=request.data)
        if serializer.is_valid():
            notification_ids = serializer.validated_data['notification_ids']
            count = Notification.objects.filter(
                id__in=notification_ids
            ).update(read=True)
            return Response({
                'detail': f'{count} notificações marcadas como lidas'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationDeleteOldView(APIView):
    """
    Deleta notificações com mais de 30 dias (limpeza automática).
    Útil para executar via cron job ou signal.
    """
    def delete(self, request):
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=30)
        count, _ = Notification.objects.filter(created_at__lt=cutoff_date).delete()
        
        return Response({
            'detail': f'{count} notificações antigas deletadas'
        })


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalhes, atualização ou deleção de uma notificação específica.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
