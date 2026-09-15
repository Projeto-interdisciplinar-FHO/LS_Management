from django.urls import include, path

urlpatterns = [
    path('weight_history/', include('apps.production.weight_history.urls')),
    path('milk_production_history/', include('apps.production.milk_production_history.urls')),
]
