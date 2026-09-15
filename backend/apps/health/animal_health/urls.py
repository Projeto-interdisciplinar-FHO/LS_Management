from django.urls import path

from apps.health.animal_health.views import AnimalHealthCreateListView, AnimalHealthRetrieveUpdateDestroy

urlpatterns = [
    path('', AnimalHealthCreateListView.as_view(), name="animal-health-create-list"),
    path('<int:pk>', AnimalHealthRetrieveUpdateDestroy.as_view(), name="animal-health-detail-view"),
]
