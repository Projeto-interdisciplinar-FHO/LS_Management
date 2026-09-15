from django.urls import path

from apps.operations.notifications.views import (
    NotificationBulkMarkAsReadView,
    NotificationDetailView,
    NotificationListView,
    NotificationMarkAsReadView,
    NotificationUnreadCountView,
    NotificationUnreadListView,
)

# Notificações (Requisito 8.1)
urlpatterns = [
    path('', NotificationListView.as_view(), name="notifications-list"),
    path('unread/', NotificationUnreadListView.as_view(), name="notifications-unread-list"),
    path('unread-count/', NotificationUnreadCountView.as_view(), name="notifications-unread-count"),
    path('<int:pk>/', NotificationDetailView.as_view(), name="notifications-detail"),
    path('<int:pk>/mark-as-read/', NotificationMarkAsReadView.as_view(), name="notifications-mark-as-read"),
    path('bulk-mark-as-read/', NotificationBulkMarkAsReadView.as_view(), name="notifications-bulk-mark-as-read"),
]
