from django.urls import include, path

urlpatterns = [
    path('vaccines/', include('apps.health.vaccines.urls')),
    path('vaccination_plans/', include('apps.health.vaccination_plans.urls')),
    path('vaccinations/', include('apps.health.vaccinations.urls')),
    path('animal_health/', include('apps.health.animal_health.urls')),
]
