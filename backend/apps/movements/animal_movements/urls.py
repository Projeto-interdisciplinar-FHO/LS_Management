from django.urls import path

from apps.movements.animal_movements.views import AnimalMovementCreateListView, AnimalMovementRetrieveUpdateDestroy

urlpatterns = [
    path('', AnimalMovementCreateListView.as_view(), name="animal-movements-create-list"),
    path('<int:pk>', AnimalMovementRetrieveUpdateDestroy.as_view(), name="animal-movements-detail-view"),
]
