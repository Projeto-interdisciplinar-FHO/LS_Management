from django.urls import path

from apps.herd.animals.views import AnimalListView, AnimalRetrieveUpdateDestroy

urlpatterns = [
    path('', AnimalListView.as_view(), name="animals-list"),
    path('<int:pk>/', AnimalRetrieveUpdateDestroy.as_view(), name="animals-detail-view"),
]
