from django.urls import path

from apps.herd.purpose_types.views import PurposeTypeCreateListView, PurposeTypeRetrieveUpdateDestroy

urlpatterns = [
    path('', PurposeTypeCreateListView.as_view(), name="purpose-types-create-list"),
    path('<int:pk>', PurposeTypeRetrieveUpdateDestroy.as_view(), name="purpose-types-detail-view"),
]
