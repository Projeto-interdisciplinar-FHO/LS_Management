from django.urls import path

from apps.movements.movement_types.views import MovementTypeCreateListView, MovementTypeRetrieveUpdateDestroy

urlpatterns = [
    path('', MovementTypeCreateListView.as_view(), name="movement-types-create-list"),
    path('<int:pk>', MovementTypeRetrieveUpdateDestroy.as_view(), name="movement-types-detail-view"),
]
