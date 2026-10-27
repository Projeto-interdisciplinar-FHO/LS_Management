"""Índice de rotas do projeto.

Cada módulo (apps/<modulo>/urls.py) define os prefixos dos seus apps, e cada
app (apps/<modulo>/<app>/urls.py) define as próprias rotas.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.api.urls')),
    path('', include('apps.accounts.urls')),
]
