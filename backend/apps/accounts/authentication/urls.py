from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.accounts.authentication.views import (
    CustomTokenObtainPairView,
    UsuarioDetailView,
    UsuarioListCreateView,
)

# Incluído na raiz (core/urls.py) porque atende dois prefixos: users/ e as rotas de token.
urlpatterns = [
    # Cadastro de usuarios (so Administrador). O 'users/register/' existe
    # com esse nome porque e o que o authService.js do front ja chamava.
    path('users/', UsuarioListCreateView.as_view(), name='usuarios-lista'),
    path('users/register/', UsuarioListCreateView.as_view(), name='usuarios-registro'),
    path('users/<int:pk>/', UsuarioDetailView.as_view(), name='usuarios-detalhe'),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token-obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('authentication/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('authentication/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('authentication/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
