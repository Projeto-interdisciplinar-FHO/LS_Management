from rest_framework import viewsets
from apps.operations.tasks.models import Task
from apps.operations.tasks.serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        task = serializer.save()
        # Notifica admin
        try:
            from apps.operations.notifications.models import Notification
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
            from apps.operations.notifications.models import Notification
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
            from apps.operations.notifications.models import Notification
            Notification.create_notification(
                message=f"Operador deletou tarefa: {title}",
                notification_type='task_deleted',
                animal=animal
            )
        except Exception:
            pass
