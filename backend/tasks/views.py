from rest_framework import viewsets
from tasks.models import Task
from tasks.serializers import TaskSerializer
from rest_framework.permissions import AllowAny

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        task = serializer.save()
        # Notifica admin
        try:
            from notifications.models import Notification
            Notification.create_notification(
                message=f"Operador criou tarefa: {task.title}",
                notification_type='task_created',
                animal=task.animal
            )
        except Exception:
            pass

    def perform_update(self, serializer):
        task = serializer.save()
        try:
            from notifications.models import Notification
            Notification.create_notification(
                message=f"Operador atualizou tarefa: {task.title}",
                notification_type='task_updated',
                animal=task.animal
            )
        except Exception:
            pass

    def perform_destroy(self, instance):
        title = instance.title
        animal = instance.animal
        instance.delete()
        try:
            from notifications.models import Notification
            Notification.create_notification(
                message=f"Operador deletou tarefa: {title}",
                notification_type='task_deleted',
                animal=animal
            )
        except Exception:
            pass
