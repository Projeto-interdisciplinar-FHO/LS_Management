from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.authentication.serializers import CustomTokenObtainPairSerializer, UsuarioSerializer
from core.permissions import EhAdministrador


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View customizada que retorna o campo is_superuser junto com os tokens.
    """
    serializer_class = CustomTokenObtainPairSerializer


class UsuarioListCreateView(generics.ListCreateAPIView):
    """Lista e cadastra usuarios. So o Administrador.

    Nao existia rota nenhuma de usuario: o `authService.js` do front chamava
    `users/register/` com um comentario dizendo "ajuste a URL conforme seu
    Django" — a rota nunca foi criada. Na pratica, so dava para criar gente
    pelo `manage.py createsuperuser`, no terminal do servidor.
    """

    queryset = User.objects.all().order_by("username")
    serializer_class = UsuarioSerializer
    permission_classes = [EhAdministrador]


class UsuarioDetailView(generics.RetrieveUpdateAPIView):
    """Consulta e edita um usuario. Sem exclusao, de proposito.

    Usuario apagado leva junto o historico de quem lancou cada pesagem e cada
    vacinacao. Para tirar alguem de circulacao existe `is_active=false`, que
    bloqueia o login e preserva o rastro.
    """

    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [EhAdministrador]
