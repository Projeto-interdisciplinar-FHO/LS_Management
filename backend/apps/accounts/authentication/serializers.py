from django.contrib.auth.models import Group, User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.permissions import ADMINISTRADOR, OPERADOR, papel_de


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Devolve, junto dos tokens, quem é o usuário e o que ele é.

    O `papel` vai também DENTRO do token (assinado), e não só no corpo da
    resposta: o corpo o navegador pode reescrever, o token não. Quem decide
    permissão de verdade é o backend lendo o usuário — o campo aqui serve
    para a tela saber o que desenhar, não para autorizar.

    `is_superuser` continua na resposta porque a tela de login atual o
    consome; tirar agora quebraria o front sem necessidade.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["is_superuser"] = user.is_superuser
        token["papel"] = papel_de(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["is_superuser"] = self.user.is_superuser
        data["papel"] = papel_de(self.user)
        data["username"] = self.user.username
        data["nome"] = self.user.get_full_name() or self.user.username
        return data


class UsuarioSerializer(serializers.ModelSerializer):
    """Cadastro e listagem de usuarios, com o papel junto.

    O papel entra e sai como uma palavra ("Administrador"/"Operador") em vez
    de um id de grupo: quem preenche a tela pensa em cargo, nao em chave
    estrangeira, e assim o front nao precisa carregar a lista de grupos so
    para montar um <select> de duas opcoes.
    """

    papel = serializers.ChoiceField(
        choices=[ADMINISTRADOR, OPERADOR], default=OPERADOR
    )
    # write_only: senha entra no cadastro e NUNCA volta numa listagem.
    password = serializers.CharField(
        write_only=True, required=False, validators=[validate_password],
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = [
            "id", "username", "first_name", "last_name", "email",
            "is_active", "papel", "password", "date_joined",
        ]
        read_only_fields = ["id", "date_joined"]

    def to_representation(self, instancia):
        dados = super().to_representation(instancia)
        # Le do banco em vez do valor enviado: se alguem mexer no grupo pelo
        # admin do Django, a listagem mostra a verdade.
        dados["papel"] = papel_de(instancia)
        return dados

    def validate_username(self, valor):
        qs = User.objects.filter(username__iexact=valor)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Ja existe um usuario com este login.")
        return valor

    def _aplicar_papel(self, usuario, papel):
        grupo, _ = Group.objects.get_or_create(name=papel)
        usuario.groups.set([grupo])
        # is_staff da acesso ao /admin do Django; is_superuser NAO e usado
        # para definir papel — quem define e o grupo. Manter os dois em sincronia
        # evita o defeito antigo, em que um "Operador" superusuario entrava
        # como administrador.
        usuario.is_staff = papel == ADMINISTRADOR
        usuario.save(update_fields=["is_staff"])

    def create(self, dados):
        papel = dados.pop("papel", OPERADOR)
        senha = dados.pop("password", None)
        if not senha:
            raise serializers.ValidationError({"password": "Informe uma senha."})
        usuario = User(**dados)
        usuario.set_password(senha)      # nunca gravar senha em texto
        usuario.save()
        self._aplicar_papel(usuario, papel)
        return usuario

    def update(self, usuario, dados):
        papel = dados.pop("papel", None)
        senha = dados.pop("password", None)
        for campo, valor in dados.items():
            setattr(usuario, campo, valor)
        if senha:
            usuario.set_password(senha)
        usuario.save()
        if papel:
            self._aplicar_papel(usuario, papel)
        return usuario
