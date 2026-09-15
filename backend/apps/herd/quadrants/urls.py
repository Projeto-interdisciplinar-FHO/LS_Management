from django.urls import path

from apps.herd.quadrants.views import QuadrantCreateListView, QuadrantRetrieveUpdateDestroy

urlpatterns = [
    path('', QuadrantCreateListView.as_view(), name="quadrants-create-list"),
    path('<int:pk>', QuadrantRetrieveUpdateDestroy.as_view(), name="quadrants-detail-view"),
]
