from django.urls import path

from apps.health.vaccination_plans.views import VaccinationPlanCreateListView, VaccinationPlanRetrieveUpdateDestroy

urlpatterns = [
    path('', VaccinationPlanCreateListView.as_view(), name="vaccination-plans-create-list"),
    path('<int:pk>', VaccinationPlanRetrieveUpdateDestroy.as_view(), name="vaccination-plans-detail-view"),
]
