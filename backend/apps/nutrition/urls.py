from django.urls import include, path

urlpatterns = [
    path('foods/', include('apps.nutrition.foods.urls')),
    path('feedings/', include('apps.nutrition.feedings.urls')),
    path('feeding_plans/', include('apps.nutrition.feeding_plans.urls')),
]
