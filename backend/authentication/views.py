from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View customizada que retorna o campo is_superuser junto com os tokens.
    """
    serializer_class = CustomTokenObtainPairSerializer
