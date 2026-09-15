from django.urls import path

from apps.nutrition.feedings.views import FeedingCreateListView, FeedingRetrieveUpdateDestroy

urlpatterns = [
    path('', FeedingCreateListView.as_view(), name="feedings-create-list"),
    path('<int:pk>', FeedingRetrieveUpdateDestroy.as_view(), name="feedings-detail-view"),
]
