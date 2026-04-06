
from django.contrib import admin
from django.urls import path, include

from species.views import SpecieCreateListView, SpecieRetriveUpdateDestroy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('species/', SpecieCreateListView.as_view(), name="species-create-list"),
    path('species/<int:pk>', SpecieRetriveUpdateDestroy.as_view(), name="species-detail-view"),
]
