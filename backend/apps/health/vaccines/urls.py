from django.urls import path

from apps.health.vaccines.views import VaccineCreateListView, VaccineRetrieveUpdateDestroy

urlpatterns = [
    path('', VaccineCreateListView.as_view(), name="vaccines-create-list"),
    path('<int:pk>', VaccineRetrieveUpdateDestroy.as_view(), name="vaccines-detail-view"),
]
