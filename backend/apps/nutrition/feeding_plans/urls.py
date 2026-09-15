from django.urls import path

from apps.nutrition.feeding_plans.views import FeedingPlanCreateListView, FeedingPlanRetrieveUpdateDestroy

urlpatterns = [
    path('', FeedingPlanCreateListView.as_view(), name="feeding-plans-create-list"),
    path('<int:pk>', FeedingPlanRetrieveUpdateDestroy.as_view(), name="feeding-plans-detail-view"),
]
