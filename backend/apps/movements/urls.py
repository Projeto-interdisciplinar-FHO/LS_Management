from django.urls import include, path

urlpatterns = [
    path('movement_types/', include('apps.movements.movement_types.urls')),
    path('animal_movements/', include('apps.movements.animal_movements.urls')),
]
