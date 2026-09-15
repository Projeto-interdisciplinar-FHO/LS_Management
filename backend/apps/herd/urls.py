from django.urls import include, path

urlpatterns = [
    path('species/', include('apps.herd.species.urls')),
    path('quadrants/', include('apps.herd.quadrants.urls')),
    path('purpose_types/', include('apps.herd.purpose_types.urls')),
    path('animals/', include('apps.herd.animals.urls')),
    path('breeds/', include('apps.herd.breeds.urls')),
]
