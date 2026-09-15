"""Índice de rotas do projeto.

Cada módulo (apps/<modulo>/urls.py) define os prefixos dos seus apps, e cada
app (apps/<modulo>/<app>/urls.py) define as próprias rotas.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.herd.urls')),
    path('', include('apps.production.urls')),
    path('', include('apps.health.urls')),
    path('', include('apps.nutrition.urls')),
    path('', include('apps.movements.urls')),
    path('', include('apps.operations.urls')),
    path('', include('apps.accounts.urls')),
]
