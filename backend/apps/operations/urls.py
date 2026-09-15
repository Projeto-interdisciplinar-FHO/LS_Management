from django.urls import include, path

urlpatterns = [
    path('tasks/', include('apps.operations.tasks.urls')),
    path('notifications/', include('apps.operations.notifications.urls')),
]
