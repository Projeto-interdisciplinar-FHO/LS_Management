from django.urls import path

from apps.herd.species.views import SpecieCreateListView, SpecieRetrieveUpdateDestroy

urlpatterns = [
    path('', SpecieCreateListView.as_view(), name="species-create-list"),
    path('<int:pk>', SpecieRetrieveUpdateDestroy.as_view(), name="species-detail-view"),
]
