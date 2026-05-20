from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializador customizado que adiciona o campo is_superuser à resposta do token.
    """
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Adiciona o campo is_superuser ao token
        token['is_superuser'] = user.is_superuser
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Adiciona is_superuser à resposta
        data['is_superuser'] = self.user.is_superuser
        
        return data
