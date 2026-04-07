
from django.contrib import admin
from django.urls import path, include

from species.views import SpecieCreateListView, SpecieRetrieveUpdateDestroy
from quadrants.views import QuadrantCreateListView, QuadrantRetrieveUpdateDestroy
from purpose_types.views import PurposeTypeCreateListView, PurposeTypeRetrieveUpdateDestroy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('species/', SpecieCreateListView.as_view(), name="species-create-list"),
    path('species/<int:pk>', SpecieRetrieveUpdateDestroy.as_view(), name="species-detail-view"),
    path('quadrants/', QuadrantCreateListView.as_view(), name="quadrants-create-list"),
    path('quadrants/<int:pk>', QuadrantRetrieveUpdateDestroy.as_view(), name="quadrants-detail-view"),
    path('purpose_types/', PurposeTypeCreateListView.as_view(), name="purpose-types-create-list"),
    path('purpose_types/<int:pk>', PurposeTypeRetrieveUpdateDestroy.as_view(), name="purpose-types-detail-view"),
]
